#!/bin/sh
#cd to folder
echo `pwd`
cd $1

#list of experiment folder
EXPERIMENTS=(
  # "experiment1-traces"
  "experiment2-singleMin"
  # "experiment3-singleSame"
  # "experiment4-mazes"
  # "experiment5-single"
  # "experiment5-twoScales"
)

#create list of files to be compressed
FILES=""
for E in ${EXPERIMENTS[@]}; do
  [ -d "logs/$E/articlePlots/" ] && FILES="$FILES logs/$E/articlePlots/"
  FILES="$FILES logs/$E/experiments"
  FILES="$FILES logs/$E/mazes"
  FILES="$FILES logs/$E/cmdHistory.txt"
  FILES="$FILES logs/$E/configs.csv"
  FILES="$FILES logs/$E/runtimes.pickle"
  FILES="$FILES logs/$E/summaries.pickle"
  FILES="$FILES logs/$E/summaries_normalized.pickle"
done

tar -zcvf results.tar.gz $FILES


#cd to original folder
cd -


