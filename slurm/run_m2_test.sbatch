#!/bin/bash
#SBATCH --job-name=cos568-m2-test
#SBATCH --output=logs/m2_test-%j.out
#SBATCH --error=logs/m2_test-%j.err
#SBATCH --time=00:30:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=32G
#SBATCH --gres=gpu:1
#SBATCH --constraint=gpu80

module load anaconda3/2025.6
module load boost/1.85.0
conda activate prj_cos568

cd /scratch/gpfs/KOROLOVA/bt4811/cos_568_prj/COS568-LI-SP26
mkdir -p logs results

# Reuse the shared build/ dir (keeps CMakeCache with Boost paths intact).
# Delete all .o files first so -march=native recompiles on this node's CPU,
# avoiding "Illegal instruction" from stale login-node objects.
BUILD_DIR=build
BENCHMARK=${BUILD_DIR}/benchmark

echo "=== Rebuilding on compute node (CPU: $(uname -p), host: $(hostname), job: $SLURM_JOB_ID) ==="
mkdir -p $BUILD_DIR && cd $BUILD_DIR
cmake .. -DCMAKE_BUILD_TYPE=Release
find . -name "*.o" -delete
make -j$(nproc)
cd ..

function set_header() {
    local FILE=$1
    local HDR="index_name,build_time_ns1,build_time_ns2,build_time_ns3,index_size_bytes,mixed_throughput_mops1,mixed_throughput_mops2,mixed_throughput_mops3,search_method,value"
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

    echo "  Running: $DESC ($INDEX on $DATA)"
    $BENCHMARK ./data/$DATA "$OPS_FILE" --through --csv --only $INDEX -r 3 || \
        echo "  WARNING: benchmark exited with error for $INDEX / $DATA / $DESC"

    if [ -f "$RESULT_FILE" ]; then
        set_header "$RESULT_FILE"
    fi
}

echo "=== Running LIPP on fb dataset — 2 mixed workloads ==="
DATA=fb_100M_public_uint64

run_workload $DATA LIPP "ops_2M_0.000000rq_0.500000nl_0.100000i_0m_mix" "Mixed (10% insert)"
run_workload $DATA LIPP "ops_2M_0.000000rq_0.500000nl_0.900000i_0m_mix" "Mixed (90% insert)"

echo "=== Test complete ==="
