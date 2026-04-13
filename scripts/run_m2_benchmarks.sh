#!/bin/bash

echo "=== Full benchmark: all indexes on all datasets, all 4 workloads ==="

BENCHMARK=build/benchmark
if [ ! -f $BENCHMARK ]; then
    echo "benchmark binary does not exist — run build first"
    exit 1
fi

mkdir -p ./results

# Write or refresh the header for a given results CSV file.
function set_header() {
    local FILE=$1
    if [[ $FILE == *0.000000i* ]]; then
        local HDR="index_name,build_time_ns1,build_time_ns2,build_time_ns3,index_size_bytes,lookup_throughput_mops1,lookup_throughput_mops2,lookup_throughput_mops3,search_method,value"
    elif [[ $FILE == *mix* ]]; then
        local HDR="index_name,build_time_ns1,build_time_ns2,build_time_ns3,index_size_bytes,mixed_throughput_mops1,mixed_throughput_mops2,mixed_throughput_mops3,search_method,value"
    else
        local HDR="index_name,build_time_ns1,build_time_ns2,build_time_ns3,index_size_bytes,insert_throughput_mops1,lookup_throughput_mops1,insert_throughput_mops2,lookup_throughput_mops2,insert_throughput_mops3,lookup_throughput_mops3,search_method,value"
    fi
    if head -n 1 "$FILE" 2>/dev/null | grep -q "index_name"; then
        sed -i '1d' "$FILE"
    fi
    sed -i "1s|^|${HDR}\n|" "$FILE"
}

function run_workload() {
    local DATA=$1
    local INDEX=$2
    local OPS_SUFFIX=$3
    local DESC=$4
    local OPS_FILE="./data/${DATA}_${OPS_SUFFIX}"
    local RESULT_FILE="./results/${DATA}_${OPS_SUFFIX}_results_table.csv"

    if [ ! -f "$OPS_FILE" ]; then
        echo "  SKIP — workload file not found: $OPS_FILE"
        return
    fi

    echo "  $DESC ($INDEX on $DATA)"
    $BENCHMARK ./data/$DATA "$OPS_FILE" --through --csv --only $INDEX -r 3 || \
        echo "  WARNING: benchmark exited with error for $INDEX / $DATA / $DESC"

    # Write header immediately so CSV is usable even if later runs crash.
    if [ -f "$RESULT_FILE" ]; then
        set_header "$RESULT_FILE"
    fi
}

for DATA in fb_100M_public_uint64 books_100M_public_uint64 osmc_100M_public_uint64; do
    for INDEX in LIPP BTree DynamicPGM HybridPGMLIPP; do
        echo "=== $INDEX on $DATA ==="
        run_workload $DATA $INDEX "ops_2M_0.000000rq_0.500000nl_0.000000i"     "1) Lookup-only"
        run_workload $DATA $INDEX "ops_2M_0.000000rq_0.500000nl_0.500000i_0m"  "2) Insert+Lookup (50%)"
        run_workload $DATA $INDEX "ops_2M_0.000000rq_0.500000nl_0.100000i_0m_mix" "3) Mixed (10% insert)"
        run_workload $DATA $INDEX "ops_2M_0.000000rq_0.500000nl_0.900000i_0m_mix" "4) Mixed (90% insert)"
    done
done

echo "=== All benchmarking complete ==="
