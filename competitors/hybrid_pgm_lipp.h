#ifndef TLI_HYBRID_PGM_LIPP_H
#define TLI_HYBRID_PGM_LIPP_H

#include <algorithm>
#include <cstdlib>
#include <iostream>
#include <limits>
#include <unordered_map>
#include <vector>

#include "../util.h"
#include "base.h"
#include "pgm_index_dynamic.hpp"
#include "./lipp/src/core/lipp.h"
#include "../searches/branching_binary_search.h"

// flush_threshold: trigger a flush after this many operations.
// count_all_ops: when false (default), only Insert calls count toward the
//   threshold (original behavior). When true, every Insert + EqualityLookup
//   + RangeQuery call counts, so the flush period is relative to total ops.
template <class KeyType, size_t pgm_error, size_t flush_threshold = 100000,
          bool count_all_ops = false>
class HybridPGMLIPP : public Base<KeyType> {
 public:
  HybridPGMLIPP(const std::vector<int>& params) : pgm_count_(0), op_count_(0), peak_pgm_size_(0) {}

  uint64_t Build(const std::vector<KeyValue<KeyType>>& data, size_t num_threads) {
    // Reset both structures so Build() is safe to call on a reused object.
    pgm_ = decltype(pgm_)();
    pgm_count_ = 0;
    op_count_ = 0;
    peak_pgm_size_ = 0;

    std::vector<std::pair<KeyType, uint64_t>> loading_data;
    loading_data.reserve(data.size());
    for (const auto& itm : data) {
      loading_data.push_back(std::make_pair(itm.key, itm.value));
    }

    uint64_t build_time = util::timing([&] {
      // bulk_load() calls destroy_tree(root) internally, so lipp_ is fully reset.
      lipp_.bulk_load(loading_data.data(), loading_data.size());
    });

    return build_time;
  }

  size_t EqualityLookup(const KeyType& lookup_key, uint32_t thread_id) const {
    if constexpr (count_all_ops) { op_count_++; }

    // Check the PGM write buffer first for keys inserted since the last flush.
    if (pgm_count_ > 0) {
      auto it = pgm_.find(lookup_key);
      if (it != pgm_.end()) {
        return it->value();
      }
    }

    uint64_t value;
    if (!lipp_.find(lookup_key, value)) {
      return util::NOT_FOUND;
    }
    return value;
  }

  uint64_t RangeQuery(const KeyType& lower_key, const KeyType& upper_key, uint32_t thread_id) const {
    if constexpr (count_all_ops) { op_count_++; }

    uint64_t result = 0;

    // Sum LIPP entries in [lower_key, upper_key].
    auto lipp_it = lipp_.lower_bound(lower_key);
    while (lipp_it != lipp_.end() && lipp_it->comp.data.key <= upper_key) {
      result += lipp_it->comp.data.value;
      ++lipp_it;
    }

    // Sum PGM write-buffer entries in range (keys inserted since last flush).
    // These are disjoint from LIPP under the unique-key insert assumption.
    if (pgm_count_ > 0) {
      auto pgm_it = pgm_.lower_bound(lower_key);
      while (pgm_it != pgm_.end() && pgm_it->key() <= upper_key) {
        result += pgm_it->value();
        ++pgm_it;
      }
    }

    return result;
  }

  void Insert(const KeyValue<KeyType>& data, uint32_t thread_id) {
    pgm_.insert(data.key, data.value);
    pgm_count_++;
    op_count_++;

    // Flush when the relevant counter crosses the threshold.
    // count_all_ops=true: op_count_ tracks all ops (set from lookups too).
    // count_all_ops=false: only insert ops counted, same as original pgm_count_.
    const size_t trigger = count_all_ops ? op_count_ : pgm_count_;
    if (trigger >= flush_threshold) {
      FlushPGMToLIPP();
    }
  }

  std::string name() const {
    return count_all_ops ? "HybridPGMLIPPv2" : "HybridPGMLIPP";
  }

  std::size_t size() const {
    // lipp_.index_size() is O(N) so we only call it once here (at report time).
    // peak_pgm_size_ holds the max PGM buffer size seen just before any flush,
    // giving the true peak footprint without re-traversing LIPP during the run.
    return lipp_.index_size() + peak_pgm_size_;
  }

  bool applicable(bool unique, bool range_query, bool insert, bool multithread, const std::string& ops_filename) const {
    return unique && !multithread;
  }

  std::vector<std::string> variants() const {
    std::vector<std::string> vec;
    vec.push_back(std::to_string(pgm_error));
    vec.push_back(std::to_string(flush_threshold));
    vec.push_back(count_all_ops ? "all_ops" : "insert_ops");
    return vec;
  }

 private:
  void FlushPGMToLIPP() {
    // Capture PGM buffer size before flush (cheap, no tree traversal).
    size_t pgm_sz = pgm_.size_in_bytes();
    if (pgm_sz > peak_pgm_size_) peak_pgm_size_ = pgm_sz;

    // Collect PGM items (DynamicPGMIndex iterates in sorted key order).
    std::vector<std::pair<KeyType, uint64_t>> pgm_items;
    pgm_items.reserve(pgm_count_);
    for (auto it = pgm_.begin(); it != pgm_.end(); ++it) {
      pgm_items.emplace_back(it->key(), it->value());
    }

    // Check whether any PGM key already exists in LIPP (e.g. an update).
    bool has_conflicts = false;
    for (const auto& [key, value] : pgm_items) {
      uint64_t tmp;
      if (lipp_.find(key, tmp)) {
        has_conflicts = true;
        break;
      }
    }

    if (!has_conflicts) {
      // Fast path: all PGM keys are new — insert directly into LIPP.
      for (const auto& [key, value] : pgm_items) {
        lipp_.insert(key, value);
      }
    } else {
      // Slow path: LIPP has no update(), so rebuild with PGM values winning on conflict.
      std::unordered_map<KeyType, uint64_t> pgm_map(pgm_items.begin(), pgm_items.end());

      std::vector<std::pair<KeyType, uint64_t>> merged;
      // Iterate all existing LIPP entries; override value if PGM has a newer one.
      auto lipp_it = lipp_.lower_bound(std::numeric_limits<KeyType>::min());
      while (lipp_it != lipp_.end()) {
        KeyType k = lipp_it->comp.data.key;
        uint64_t v = lipp_it->comp.data.value;
        auto pgm_it = pgm_map.find(k);
        if (pgm_it != pgm_map.end()) {
          v = pgm_it->second;
          pgm_map.erase(pgm_it);
        }
        merged.emplace_back(k, v);
        ++lipp_it;
      }
      // Append PGM keys that were not in LIPP at all.
      for (const auto& [key, value] : pgm_map) {
        merged.emplace_back(key, value);
      }

      std::sort(merged.begin(), merged.end());
      // bulk_load() calls destroy_tree(root) internally, so it fully resets lipp_.
      // LIPP has a deleted assignment operator so we cannot reassign; not needed.
      lipp_.bulk_load(merged.data(), merged.size());
    }

    // Reset DPGM to empty. Default-construct to avoid UB from log2(0).
    pgm_ = decltype(pgm_)();
    pgm_count_ = 0;
    op_count_ = 0;
  }

  // pgm_ const methods are called from EqualityLookup (const), so not mutable.
  DynamicPGMIndex<KeyType, uint64_t, BranchingBinarySearch<0>,
                  PGMIndex<KeyType, BranchingBinarySearch<0>, pgm_error, 16>> pgm_;
  LIPP<KeyType, uint64_t> lipp_;
  size_t pgm_count_;
  // op_count_ is mutable so EqualityLookup/RangeQuery (const) can increment it.
  mutable size_t op_count_;
  size_t peak_pgm_size_;
};

#endif
