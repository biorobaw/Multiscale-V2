#!/bin/bash

#SBATCH --time=1:00:00
#SBATCH --cpus-per-task 2
#SBATCH --qos=preempt
#SBATCH --mem=2000M
#SBATCH -p mri2016

baseDir=$1
configId=c$SLURM_ARRAY_TASK_ID

echo "configId " $configId

module rm apps/python/3.7.0
module add apps/python/3.7.3

PYTHONUSERBASE=/home/p/pablos/work/pythonlibs
# module list
# echo ""
# ls /usr/lib64/ | grep libffi
# echo $LD_LIBRARY_PATH
# which python
# echo $PATH
# echo $PYTHONPATH
# echo $PYTHONSTARTUP
# echo $PYTHONCASEOK
# echo $PYTHONHOME

python ./scripts/log_processing/processConfig2.py $baseDir $configId


if [ $? -eq 0 ]; then
    echo SUCCESS
else
    echo "FAIL $baseDir $configId"
fi
