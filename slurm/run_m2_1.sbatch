#!/bin/bash
#SBATCH --job-name=cos568-m2-1-fb
#SBATCH --output=logs/m2_1-%j.out
#SBATCH --error=logs/m2_1-%j.err
#SBATCH --time=01:00:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=32G
#SBATCH --gres=gpu:1
#SBATCH --constraint=gpu80

module load anaconda3/2025.6
module load boost/1.85.0
conda activate prj_cos568

mkdir -p logs

cd /scratch/gpfs/KOROLOVA/bt4811/cos_568_prj/COS568-LI-SP26

echo "=== Step 1: Rebuild benchmark binary (host: $(hostname), job: $SLURM_JOB_ID) ==="
# Reuse the shared build/ dir (keeps CMakeCache with Boost paths intact).
# Delete all .o files first so -march=native recompiles on this node's CPU,
# avoiding "Illegal instruction" from stale login-node objects.
BUILD_DIR=build
mkdir -p $BUILD_DIR && cd $BUILD_DIR
cmake .. -DCMAKE_BUILD_TYPE=Release
find . -name "*.o" -delete
make -j$(nproc)
cd ..

BENCHMARK=${BUILD_DIR}/benchmark
mkdir -p ./results

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

    if [ -f "$RESULT_FILE" ]; then
        set_header "$RESULT_FILE"
    fi
}

# HybridPGMLIPPv2: flush every 10% of total ops (200,000 out of 2M),
# counting all operation types (inserts + lookups) toward the threshold.
echo "=== Step 2: Run indexes on fb dataset (2 mixed workloads, no BTree) ==="
DATA=fb_100M_public_uint64
for INDEX in LIPP DynamicPGM HybridPGMLIPPv2; do
    echo "=== $INDEX on $DATA ==="
    run_workload $DATA $INDEX "ops_2M_0.000000rq_0.500000nl_0.100000i_0m_mix" "3) Mixed (10% insert)"
    run_workload $DATA $INDEX "ops_2M_0.000000rq_0.500000nl_0.900000i_0m_mix" "4) Mixed (90% insert)"
done

echo "=== Step 3: Generate plots ==="
python3 scripts/analysis_m2_1.py

echo "=== m2_1 benchmark + analysis complete ==="
