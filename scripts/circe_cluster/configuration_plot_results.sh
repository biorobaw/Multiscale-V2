#!/bin/bash

#SBATCH --time=0:10:00
#SBATCH --cpus-per-task 2 
#SBATCH --mem=2000M
#SBATCH -p mri2016
#SBATCH -o ./slurm/output.%A.%a.out # STDOUT

baseDir=$1
configId=c$SLURM_ARRAY_TASK_ID

echo "configId " $configId

python plotConfig.py $baseDir $configId

