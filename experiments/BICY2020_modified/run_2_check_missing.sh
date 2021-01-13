#in git root folder execute the following commands:

source "experiments/BICY2020_modified/run_set_variables.sh"

CHECK_FILE="r#ID-steps.bin"

for E in ${RUN[*]}; do
	echo "sh python $SCRIPT_2_CHECK $(map $E LOG_FOLDER) $CHECK_FILE $(map $E RATS)"
	python $SCRIPT_2_CHECK $(map $E LOG_FOLDER) $CHECK_FILE $(map $E RATS)
done