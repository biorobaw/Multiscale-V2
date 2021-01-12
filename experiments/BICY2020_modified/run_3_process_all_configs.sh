# This script starts slurm path plotting scripts and configuration processing scripts 

source "experiments/BICY2020_modified/run_set_variables.sh"

# slurm script for path plotting:
BATCH_SCRIPT="module add apps/python/3.7.3; python $SCRIPT_3_PLOT_PATHS ENAME/ c\$SLURM_ARRAY_TASK_ID"

[ -z "$DO_EXPERIMENT_1" ] || sbatch -a 0-279 --mem=500M --time=0:15:00 --cpus-per-task=2 --wrap="${BATCH_SCRIPT/ENAME/$LOG_FOLDER_E1}"
[ -z "$DO_EXPERIMENT_2" ] || sbatch -a 0-27  --mem=500M --time=0:15:00 --cpus-per-task=2 --wrap="${BATCH_SCRIPT/ENAME/$LOG_FOLDER_E2}"
[ -z "$DO_EXPERIMENT_3" ] || sbatch -a 0-27  --mem=500M --time=0:15:00 --cpus-per-task=2 --wrap="${BATCH_SCRIPT/ENAME/$LOG_FOLDER_E3}"
[ -z "$DO_EXPERIMENT_4" ] || sbatch -a 0-219 --mem=500M --time=0:15:00 --cpus-per-task=2 --wrap="${BATCH_SCRIPT/ENAME/$LOG_FOLDER_E4}"
[ -z "$DO_EXPERIMENT_5" ] || sbatch -a 0-159 --mem=500M --time=0:15:00 --cpus-per-task=2 --wrap="${BATCH_SCRIPT/ENAME/$LOG_FOLDER_E5}"
[ -z "$DO_EXPERIMENT_6" ] || sbatch -a 0-109 --mem=500M --time=0:15:00 --cpus-per-task=2 --wrap="${BATCH_SCRIPT/ENAME/$LOG_FOLDER_E6}"
[ -z "$DO_EXPERIMENT_7" ] || sbatch -a 0-99  --mem=500M --time=0:15:00 --cpus-per-task=2 --wrap="${BATCH_SCRIPT/ENAME/$LOG_FOLDER_E7}"


[ -z "$DO_EXPERIMENT_1" ] || sbatch -a 0-279  $SCRIPT_3_PROCESS_CONFIG $LOG_FOLDER_E1/ 5
[ -z "$DO_EXPERIMENT_2" ] || sbatch -a 0-27   $SCRIPT_3_PROCESS_CONFIG $LOG_FOLDER_E2/ 5
[ -z "$DO_EXPERIMENT_3" ] || sbatch -a 0-27   $SCRIPT_3_PROCESS_CONFIG $LOG_FOLDER_E3/
[ -z "$DO_EXPERIMENT_4" ] || sbatch -a 0-219  $SCRIPT_3_PROCESS_CONFIG $LOG_FOLDER_E4/ 5
[ -z "$DO_EXPERIMENT_5" ] || sbatch -a 0-159  $SCRIPT_3_PROCESS_CONFIG $LOG_FOLDER_E5/ 10
[ -z "$DO_EXPERIMENT_6" ] || sbatch -a 0-109  $SCRIPT_3_PROCESS_CONFIG $LOG_FOLDER_E6/ 5
[ -z "$DO_EXPERIMENT_7" ] || sbatch -a 0-99   $SCRIPT_3_PROCESS_CONFIG $LOG_FOLDER_E7/ 5
# sbatch -a 0-47 $PROCESS_CONFIG ${LOG_FOLDER}experiment4-mazes/
# sbatch -a 0-27 $PROCESS_CONFIG ${LOG_FOLDER}experiment5-single/
# sbatch -a 0-181 $PROCESS_CONFIG ${LOG_FOLDER}experiment5-twoScales/