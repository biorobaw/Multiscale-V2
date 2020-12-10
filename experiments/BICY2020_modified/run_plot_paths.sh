#in git root folder execute the following commands:

source "experiments/BICY2020_modified/run_set_variables.sh"

PLOT_EXPERIMENT=$EXPERIMENT_FOLDER/post_processing/plot_paths.py

BATCH_SCRIPT="module add apps/python/3.7.3; python $PLOT_EXPERIMENT ENAME/ c\$SLURM_ARRAY_TASK_ID"

[ -z "$DO_EXPERIMENT_1" ] || sbatch -a 0-279 --mem=500M --time=0:15:00 --cpus-per-task=2 --wrap="${BATCH_SCRIPT/ENAME/$LOG_E1}"
[ -z "$DO_EXPERIMENT_2" ] || sbatch -a 0-27  --mem=500M --time=0:15:00 --cpus-per-task=2 --wrap="${BATCH_SCRIPT/ENAME/$LOG_E2}"
[ -z "$DO_EXPERIMENT_3" ] || sbatch -a 0-27  --mem=500M --time=0:15:00 --cpus-per-task=2 --wrap="${BATCH_SCRIPT/ENAME/$LOG_E3}"
[ -z "$DO_EXPERIMENT_4" ] || sbatch -a 0-219 --mem=500M --time=0:15:00 --cpus-per-task=2 --wrap="${BATCH_SCRIPT/ENAME/$LOG_E4}"
[ -z "$DO_EXPERIMENT_5" ] || sbatch -a 0-159 --mem=500M --time=0:15:00 --cpus-per-task=2 --wrap="${BATCH_SCRIPT/ENAME/$LOG_E5}"
[ -z "$DO_EXPERIMENT_6" ] || sbatch -a 0-109 --mem=500M --time=0:15:00 --cpus-per-task=2 --wrap="${BATCH_SCRIPT/ENAME/$LOG_E6}"
[ -z "$DO_EXPERIMENT_7" ] || sbatch -a 0-9  --mem=500M --time=0:15:00 --cpus-per-task=2 --wrap="${BATCH_SCRIPT/ENAME/$LOG_E7}"
