#!/bin/bash

#SBATCH --time=1:00:00
#SBATCH --cpus-per-task 2
#SBATCH --mem=2000M
##SBATCH -p mri2016

plot_file=$1
baseDir=$2
[ -z $SLURM_ARRAY_TASK_ID ] && SLURM_ARRAY_TASK_ID=$3
TASK_ID=$SLURM_ARRAY_TASK_ID

echo "TASK_ID " $TASK_ID

module add apps/python/3.7.3
PYTHONUSERBASE=/home/p/pablos/work/pythonlibs


config_range=`python ./scripts/utils/map_core_to_configs.py $baseDir $TASK_ID`
range=(${config_range//-/ })
echo "CONFIG_RANGE: " $config_range  


for i in $(seq ${range[0]} ${range[1]}); do 

    echo "python $plot_file $baseDir c$i"
    python $plot_file $baseDir c$i

    if [ $? -eq 0 ]; then
        echo "SUCCESS $baseDir $configId" 
    else
        echo "FAIL $baseDir $configId"
    fi

done






