#!/bin/bash
#SBATCH --job-name=cos568-m1
#SBATCH --output=logs/m1-%j.out
#SBATCH --error=logs/m1-%j.err
#SBATCH --time=02:00:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=32G
#SBATCH --constraint=intel

module load anaconda3/2025.6
module load boost/1.85.0  
conda activate prj_cos568

mkdir -p logs
chmod +x scripts/*.sh

./scripts/run_all.sh
python scripts/analysis.py
