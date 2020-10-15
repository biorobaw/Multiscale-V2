#in git root folder execute the following commands:

source "experiments/BICY2020_modified/run_set_variables.sh"

PLOT_EXPERIMENT=$EXPERIMENT_FOLDER/post_processing/plot_experiments.py



#SBATCH --time=0:10:00
#SBATCH --cpus-per-task 2 
#SBATCH --mem=2000M

BATCH_SCRIPT="module add apps/python/3.7.3; python $PLOT_EXPERIMENT $LOG_FOLDER/ENAME/ c\$SLURM_ARRAY_TASK_ID"

[ -z "$DO_EXPERIMENT_1" ] || sbatch -a 0-279 --mem=1000 --time=0:20:00 --cpus-per-task=2 "${BATCH_SCRIPT/ENAME/experiment1-traces}"
[ -z "$DO_EXPERIMENT_2" ] || sbatch -a 0-27  --mem=1000 --time=0:20:00 --cpus-per-task=2 "${BATCH_SCRIPT/ENAME/experiment2-singleMin}"
[ -z "$DO_EXPERIMENT_3" ] || sbatch -a 0-27  --mem=1000 --time=0:20:00 --cpus-per-task=2 "${BATCH_SCRIPT/ENAME/experiment3-singleSame}"
[ -z "$DO_EXPERIMENT_4" ] || sbatch -a 0-219 --mem=1000 --time=0:20:00 --cpus-per-task=2 "${BATCH_SCRIPT/ENAME/experiment4-extraAtFeeder}"
[ -z "$DO_EXPERIMENT_5" ] || sbatch -a 0-159 --mem=1000 --time=0:20:00 --cpus-per-task=2 "${BATCH_SCRIPT/ENAME/experiment5-density}"
[ -z "$DO_EXPERIMENT_6" ] || sbatch -a 0-109 --mem=1000 --time=0:20:00 --cpus-per-task=2 "${BATCH_SCRIPT/ENAME/experiment6-extraAtGap}"
# python $PLOT_EXPERIMENT ${LOG_FOLDER}experiment4-mazes/
# python $PLOT_EXPERIMENT ${LOG_FOLDER}experiment5-single/
# python $PLOT_EXPERIMENT ${LOG_FOLDER}experiment5-twoScales/