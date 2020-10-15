#in git root folder execute the following commands:

source "experiments/BICY2020_modified/run_set_variables.sh"

PLOT_EXPERIMENT=$EXPERIMENT_FOLDER/post_processing/plot_paths.py

BATCH_SCRIPT="module add apps/python/3.7.3; python $PLOT_EXPERIMENT $LOG_FOLDER/ENAME/ c\$SLURM_ARRAY_TASK_ID"

[ -z "$DO_EXPERIMENT_1" ] || sbatch -a 0-279 --mem=500M --time=0:15:00 --cpus-per-task=2 "${BATCH_SCRIPT/ENAME/experiment1-traces}"
[ -z "$DO_EXPERIMENT_2" ] || sbatch -a 0-27  --mem=500M --time=0:15:00 --cpus-per-task=2 "${BATCH_SCRIPT/ENAME/experiment2-singleMin}"
[ -z "$DO_EXPERIMENT_3" ] || sbatch -a 0-27  --mem=500M --time=0:15:00 --cpus-per-task=2 "${BATCH_SCRIPT/ENAME/experiment3-singleSame}"
[ -z "$DO_EXPERIMENT_4" ] || sbatch -a 0-219 --mem=500M --time=0:15:00 --cpus-per-task=2 "${BATCH_SCRIPT/ENAME/experiment4-extraAtFeeder}"
[ -z "$DO_EXPERIMENT_5" ] || sbatch -a 0-159 --mem=500M --time=0:15:00 --cpus-per-task=2 "${BATCH_SCRIPT/ENAME/experiment5-density}"
[ -z "$DO_EXPERIMENT_6" ] || sbatch -a 0-109 --mem=500M --time=0:15:00 --cpus-per-task=2 "${BATCH_SCRIPT/ENAME/experiment6-extraAtGap}"
