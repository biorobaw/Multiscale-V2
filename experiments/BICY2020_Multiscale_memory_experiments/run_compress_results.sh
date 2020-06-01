#cd to folder
echo `pwd`
cd $1

#list of experiment folder
EXPERIMENTS=(
  "experiment1-traces"
  "experiment2-singleMin"
  "experiment3-singleSame"
  "experiment4-mazes"
  "experiment5-single"
  "experiment5-twoScales"
)

#create list of files to be compressed
FILES=""
for E in ${EXPERIMENTS[@]}; do
  [ -d "$E/articlePlots/" ] && FILES="$FILES $E/articlePlots/"
  FILES="$FILES $E/experiments"
  FILES="$FILES $E/mazes"
  FILES="$FILES $E/cmdHistory.txt"
  FILES="$FILES $E/configs.csv"
  FILES="$FILES $E/runtimes.pickle"
  FILES="$FILES $E/summaries.pickle"
  FILES="$FILES $E/summaries_normalized.pickle"
done

tar -zcvf results.tar.gz $FILES


#cd to original folder
cd -


