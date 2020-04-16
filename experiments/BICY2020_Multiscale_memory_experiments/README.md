To run this set of experiments from run the project root directory run the following commands:

  sh ./experiments/BICY2020_Multiscale_memory_experiments/run_all.sh

Wait about 20 minutes until the experiment has been executed.
You can check this with the following command:

  watch squeue -u USER_NAME

Post process all configurations individually:

  sh ./experiments/BICY2020_Multiscale_memory_experiments/run_all.sh
  
  
Wait once again until done processing:

  watch squeue -u USER_NAME
  
  
Merge all configurations:

  sh ./experiments/BICY2020_Multiscale_memory_experiments/run_all.sh
  
  
Plot 
