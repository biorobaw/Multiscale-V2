#in git root folder execute the following commands:

# AUXILIARY FUNCTION
map() { eval "echo \${$1[$2]}"; }
config() {
	python scripts/utils/rat_to_config.py	$1 $2
}

# FOLDERS
EXPERIMENT_FOLDER="experiments/BICY2020_modified"
CONFIGS_FOLDER=$EXPERIMENT_FOLDER/config_files
LOG_FOLDER=$EXPERIMENT_FOLDER/logs

# SCRIPTS
SCRIPT_1_RUN_ALL="scripts/circe_cluster/run_all_batches.sh"
SCRIPT_2_CHECK="scripts/log_processing/pythonUtils/MissingFiles.py"
SCRIPT_3_PROCESS_CONFIG="scripts/circe_cluster/configuration_process_results.sh"
SCRIPT_3_PLOT_PATHS=$EXPERIMENT_FOLDER/post_processing/plot_paths.py
SCRIPT_4_MERGE="scripts/log_processing/mergeConfigs.py"
SCRIPT_5_PLOT_EXPERIMENT=$EXPERIMENT_FOLDER/post_processing/plot_experiments.py


# EXPERIMENTS
RUN=()
#RUN+=(E1)
#RUN+=(E2)
#RUN+=(E3)
#RUN+=(E4)
#RUN+=(E5)
#RUN+=(E6)
#RUN+=(E7)
#RUN+=(E8)
# RUN+=(E9)
# RUN+=(E10)
RUN+=(E11)

# Each experiment requires parameters: 
#	NAME : name of the experiment
#	BATCH_SIZE : the number of rats executed together by each slurm process
#	SAMPLE_RATE : states every how many episodes should we log results
#!/bin/sh
# OPTIONAL parameters:
#	MIN_RAT, MAX_RAT to be executed
#	MIN_CONFIG, MAX_CONFIG to be processed
# 

declare -A E1=( ["NAME"]=experiment1-traces 	       ["BATCH_SIZE"]=10 ["SAMPLE_RATE"]=5  )
declare -A E2=( ["NAME"]=experiment2-singleMin 	       ["BATCH_SIZE"]=10 ["SAMPLE_RATE"]=5  )
declare -A E3=( ["NAME"]=experiment3-singleSame        ["BATCH_SIZE"]=4  ["SAMPLE_RATE"]=1  )
declare -A E4=( ["NAME"]=experiment4-extraAtFeeder     ["BATCH_SIZE"]=10 ["SAMPLE_RATE"]=5  )
declare -A E5=( ["NAME"]=experiment5-density 	       ["BATCH_SIZE"]=8  ["SAMPLE_RATE"]=10 )
#E5[MIN_RAT]=7527
#E5[MAX_RAT]=7527
declare -A E6=( ["NAME"]=experiment6-extraAtGap 	   ["BATCH_SIZE"]=10 ["SAMPLE_RATE"]=5  )
declare -A E7=( ["NAME"]=experiment7-nonUniform 	   ["BATCH_SIZE"]=10 ["SAMPLE_RATE"]=5  )
#E7[MIN_RAT]=9100
#E7[MAX_RAT]=9999
#E7[MIN_CONFIG]=0
#E7[MAX_CONFIG]=99
declare -A E8=( ["NAME"]=experiment8-obstacles	     	["BATCH_SIZE"]=10 ["SAMPLE_RATE"]=5  )
#E8[MIN_RAT]=2400
#E8[MAX_RAT]=2499
declare -A E9=( ["NAME"]=experiment9-biology1           ["BATCH_SIZE"]=100 ["SAMPLE_RATE"]=5  )
declare -A E10=( ["NAME"]=experiment10-choosingMetrics  ["BATCH_SIZE"]=100 ["SAMPLE_RATE"]=1  )
# E9[MIN_RAT]=8
# E10[MAX_RAT]=29
#E9[MIN_CONFIG]=0
# E9[MAX_CONFIG]=0
declare -A E11=( ["NAME"]=experiment11-article2  ["BATCH_SIZE"]=10 ["SAMPLE_RATE"]=5  )
# E11[MAX_RAT]=355

for E in ${RUN[*]}; do
	eval "$E[LOG_FOLDER]=\$LOG_FOLDER/\$(map $E NAME)"
	eval "$E[CONFIG_FILE]=\$CONFIGS_FOLDER/\$(map $E NAME).csv"

done
