#!/bin/bash
#SBATCH --nodes=1 
#SBATCH --ntasks=1 
#SBATCH --cpus-per-task=4 
#SBATCH --mem=10000M
#SBATCH --time=5:0:0 
#SBATCH --job-name=exercise_1.3
#SBATCH --error=slurm/slurm_%j.err
#SBATCH --output=slurm/slurm_%j.out
#SBATCH --mail-type=all

module restore pbhm-mods
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/work/TALC/enci619.05_2024w/local/lib64"

offset=$SLURM_ARRAY_TASK_ID
echo $offset

baseYear=1987
offset=${offset:1}
startYear=$(($offset + $baseYear))
echo $startYear

python3 /Users/hasithaj/PycharmProjects/FROSTBYTE/scripts/plot.py $startYear




