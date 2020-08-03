EXECUTION INSTRUCTIONS

	To execute the experiments, run the following files in USF's cluster "CIRCE":

	1.  run_all.sh  				(after running the command, wait until the job is completed, you can check this with: watch squeue -u USERNAME)
	2.  run_check_missing.sh  		(if there are missing ids, rerun those specific rats, repeat this step until no missing ids)
	3.  run_process_all_configs.sh  (wait for job to be completed, to check completion use command watch squeue -u USERNAME)
	4.  run_process_experiments.sh 	(this will merge generated databases)
	5.  run_plot_all_experiments.sh (this will plot the experiments)
	6.	run_compress_results.sh		(execute to compress results and store them when done with the experiment)


LIST OF EXPERIMENTS:

	NOTE: All experiments use 100 rats per config unless otherwise stated

	1) Traces
		Question: What is the best eligibility trace for each scale?
		For each pc radius (from 4cm to 56cm in steps of 4)
		For each eligibility trace from 0 to 0.9 in steps of 0.1
		
		Each pc layer uses the minimum number of cells per layer
		Tested on maze M1
		
	2) SingleMin
		Question: What scale will perform best if using the minimum number of cells required to cover the maze?
		For each pc radius (from 4cm to 56cm in steps of 4)
		
		Eligibility trace fixed based on 1
		Each pc layer uses the minimum number of cells per layer
		Tested on mazes M0 - M1
		
	3) SingleSame
		Question: What scale will perform best if all scales use the same number of cells?
		For each pc radius (from 4cm to 56cm in steps of 4)
	
		Eligibility trace fixed based on 1
		Each pc layer uses the minimum number of cells per layer
		Tested on mazes M0 - M1
	
