#include "benchmarks/benchmark_hybrid_pgm_lipp_v2.h"

#include "benchmark.h"
#include "competitors/hybrid_pgm_lipp.h"

// flush_threshold = 10% of 2,000,000 total ops = 200,000.
// count_all_ops = true: every Insert + EqualityLookup + RangeQuery counts
// toward the threshold, not just inserts.
void benchmark_64_hybrid_pgm_lipp_v2(tli::Benchmark<uint64_t>& benchmark) {
  benchmark.template Run<HybridPGMLIPP<uint64_t, 64,  200000, true>>();
  benchmark.template Run<HybridPGMLIPP<uint64_t, 128, 200000, true>>();
  benchmark.template Run<HybridPGMLIPP<uint64_t, 256, 200000, true>>();
}
