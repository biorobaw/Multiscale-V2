#!/bin/bash

configFile=$1
baseLogFolder=$2
batchSize=$3

min_indiv=$4 # optional parameter, if non given min indiv will be 0 (min rat in config file)
max_indiv=$5 # optional paraneter, if non given max indiv will be the last rat in the config file
do_missing=$6

#note: base is used since sbatch -a cannot produce any integer
#      thus the range to be executed is (base+fromIndiv) to (base+toIndiv) 
#mvn package

#add python module to circe
module add apps/python/3.7.3

#create log folder structure:
python scripts/circe_cluster/logFolderGenerator.py ${baseLogFolder} ${configFile}


#store command executed along with commit version and time
cmdHistory=${baseLogFolder}/cmdHistory.txt
date >> ${cmdHistory}
git log --pretty=format:'%h' -n 1 >> ${cmdHistory} && echo " ${configFile}" >>${cmdHistory}

#min individuals
fromIndiv=`[ -z "$min_indiv" ] && echo 0 || echo $min_indiv`
minBatch=`expr $fromIndiv / $batchSize`

# max individual
# first get number of lines in configFile:
numLines=`wc -l ${configFile} | cut -f1 -d' '`
maxRatInFile=`expr ${numLines} - 2`

toIndiv=`[ -z "$max_indiv" ] && echo $maxRatInFile || echo $max_indiv`
maxBatch=`expr $toIndiv / $batchSize`


echo "executing indivs: $fromIndiv to $toIndiv in ($maxBatch + 1) batches of $batchSize"



#execute each line
#outputFilePattern="${baseLogFolder}/slurmOut/slurm-%A_%a.out"
echo "sbatch -a $minBatch-$maxBatch ./scripts/circe_cluster/one_batch.sh $configFile $baseLogFolder $batchSize $fromIndiv $toIndiv $do_missing"
idMessage=`sbatch -a $minBatch-$maxBatch ./scripts/circe_cluster/one_batch.sh $configFile $baseLogFolder $batchSize $fromIndiv $toIndiv $do_missing`
ratsId=`echo $idMessage | cut -d " " -f 4`
echo $ratsId
#sbatch --qos=preempt -p mri2016 --dependency=afterok:$ratsId scripts/postProcess.sh $logPath
