#!/bin/bash

configFile=$1
baseLogFolder=$2
batchSize=$3


#note: base is used since sbatch -a cannot produce any integer
#      thus the range to be executed is (base+fromIndiv) to (base+toIndiv) 
#mvn package

#add python module to circe
module add apps/python/3.7.0

#create log folder structure:
python scripts/circe_cluster/python/logFolderGenerator.py ${baseLogFolder} ${configFile}


#store command executed along with commit version and time
cmdHistory=${baseLogFolder}/cmdHistory.txt
date >> ${cmdHistory}
git log --pretty=format:'%h' -n 1 >> ${cmdHistory} && echo " ${configFile}" >>${cmdHistory}

#get number of lines in configFile:
numLines=`wc -l ${configFile} | cut -f1 -d' '`

#range of individuals
fromIndiv=0
toIndiv=`expr ${numLines} - 2`
maxBatch=`expr $toIndiv / $batchSize`


echo "executing indivs: $fromIndiv to $toIndiv in ($maxBatch + 1) batches of $batchSize"



#execute each line
#outputFilePattern="${baseLogFolder}/slurmOut/slurm-%A_%a.out"
idMessage=`sbatch -a 0-$maxBatch ./scripts/circe_cluster/one_batch.sh $configFile $baseLogFolder $batchSize`
ratsId=`echo $idMessage | cut -d " " -f 4`
echo $ratsId
#sbatch --qos=preempt -p mri2016 --dependency=afterok:$ratsId scripts/postProcess.sh $logPath
