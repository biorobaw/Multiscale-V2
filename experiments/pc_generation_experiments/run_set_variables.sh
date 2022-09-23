#in git root folder execute the following commands:

# AUXILIARY FUNCTION
map() { eval "echo \${$1[$2]}"; }
config() {
	python scripts/utils/rat_to_config.py	$1 $2
}

# FOLDERS
EXPERIMENT_FOLDER="experiments/pc_generation_experiments"
CONFIGS_FOLDER=$EXPERIMENT_FOLDER/config_files
LOG_FOLDER=$EXPERIMENT_FOLDER/logs

# SCRIPTS
SCRIPT_1_RUN_ALL="scripts/circe_cluster/run_all_batches.sh"
SCRIPT_2_CHECK="scripts/log_processing/pythonUtils/MissingFiles.py"
SCRIPT_3_PROCESS_CONFIG="scripts/circe_cluster/configuration_process_results.sh"
SCRIPT_3_PLOT_PATHS_SLURM="scripts/circe_cluster/plot_paths.sh"
SCRIPT_3_PLOT_PATHS=$EXPERIMENT_FOLDER/post_processing/plot_paths.py
SCRIPT_4_MERGE="scripts/log_processing/mergeConfigs.py"
SCRIPT_5_PLOT_EXPERIMENT=$EXPERIMENT_FOLDER/post_processing/plot_experiments.py


# EXPERIMENTS
RUN=()
RUN+=(E4)

# Each experiment requires parameters: 
#	NAME : name of the experiment
#	BATCH_SIZE : the number of rats executed together by each slurm process
#	SAMPLE_RATE : states every how many episodes should we log results
#!/bin/sh
# OPTIONAL parameters:
#	MIN_RAT, MAX_RAT to be executed
#	MIN_CONFIG, MAX_CONFIG to be processed
# 

declare -A E1=( ["NAME"]=experiment1-pcGenerationThreshold  ["BATCH_SIZE"]=10 ["SAMPLE_RATE"]=1  )
declare -A E2=( ["NAME"]=experiment2-optimalThreshold  ["BATCH_SIZE"]=10 ["SAMPLE_RATE"]=5  )
declare -A E3=( ["NAME"]=experiment3-multiscale  ["BATCH_SIZE"]=10 ["SAMPLE_RATE"]=5  )
declare -A E4=( ["NAME"]=experiment3-closestWallMultiscale  ["BATCH_SIZE"]=10 ["SAMPLE_RATE"]=5  )

# E12[MIN_RAT]=60028
# E12[MAX_RAT]=60028
# E12[MIN_CONFIG]=600
# E12[MAX_CONFIG]=600

for E in ${RUN[*]}; do
	eval "$E[LOG_FOLDER]=\$LOG_FOLDER/\$(map $E NAME)"
	eval "$E[CONFIG_FILE]=\$CONFIGS_FOLDER/\$(map $E NAME).csv"

done
