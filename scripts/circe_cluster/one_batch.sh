#!/bin/bash

#SBATCH --time=0:15:00
#SBATCH --cpus-per-task 2 
#SBATCH --qos=preempt
#SBATCH --mem=2000M
#SBATCH -p mri2016
##SBATCH -o ./slurm/output.%A.%a.out # STDOUT

echo 'in script'
configFile=$1
baseLogFolder=$2


if [ -z "$SLURM_ARRAY_TASK_ID" ]; then
  ratid=$4
  #needs to be reimplemented
else
  batchSize=$3
  batchID=$SLURM_ARRAY_TASK_ID
  baseID=`expr $batchSize \* $batchID`
  maxID=`expr $batchSize - 1`
fi

#module add apps/jre/1.8.0_121.x86 
#module unload apps/jre/1.7.0_80.x64

java -version

FAILED_IDS=""
for i in $(seq 0 $maxID)
do
  configId=`expr $baseID + $i`
  echo "---java -cp target/Multiscale-F2019-1.0.0-SNAPSHOT-jar-with-dependencies.jar -Xmx1500m com.github.biorobaw.scs.Main $configFile $configId $baseLogFolder"
  java -cp target/Multiscale-F2019-1.0.0-SNAPSHOT-jar-with-dependencies.jar -Xmx1500m com.github.biorobaw.scs.Main $configFile $configId $baseLogFolder
  
  
  if [ $? -eq 0 ]; then
      echo SUCCESS
  else
      echo FAIL
      FAILED_IDS="$configId, $FAILED_IDS"
  fi
  
done

if [ -z $FAILED_IDS ]; then
  echo "FAILED IDS: $FAILED_IDS"
fi





