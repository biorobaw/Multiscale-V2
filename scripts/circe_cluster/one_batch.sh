#!/bin/bash

#SBATCH --time=4:00:00
#SBATCH --cpus-per-task 2 
#SBATCH --mem=1000M
#SBATCH -p mri2016

echo 'in script'
configFile=$1
baseLogFolder=$2

CMD_ARGS="-cp target/Multiscale-F2019-1.0.0-SNAPSHOT-jar-with-dependencies.jar -Xmx1500m com.github.biorobaw.scs.Main"

module add apps/jdk/11.0.5


FAILED_IDS=""
if [ -z "$SLURM_ARRAY_TASK_ID" ]; then
  IDS=$3
  IFS=,
  
  for configId in $IDS;
  do
    IFS=$' \t\n'
    echo "---java $CMD_ARGS $configFile $configId $baseLogFolder"
    java $CMD_ARGS $configFile $configId $baseLogFolder
  
    if [ $? -eq 0 ]; then
        echo SUCCESS
    else
        FAILED_IDS="$configId, $FAILED_IDS"
    fi
  done
  

else
  batchSize=$3
  batchID=$SLURM_ARRAY_TASK_ID
  baseID=`expr $batchSize \* $batchID`
  maxID=`expr $batchSize - 1`
  
  
  for i in $(seq 0 $maxID)
  do
    configId=`expr $baseID + $i`
    
    echo "---java $CMD_ARGS $configFile $configId $baseLogFolder"
    java $CMD_ARGS $configFile $configId $baseLogFolder
    
    
    if [ $? -eq 0 ]; then
        echo SUCCESS
    else
        FAILED_IDS="$configId, $FAILED_IDS"
    fi
    
  done

fi


if [ -z $FAILED_IDS ]; then
  echo "FAILED IDS: $FAILED_IDS"
fi









