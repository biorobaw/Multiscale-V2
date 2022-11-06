# Multiscale-F2019

This project expands our previous Multiscale model (found in repository scs, branch v2.1, under multiscale->src->edu->usf->ratsim->model->pablo->multiscale_memory).  
Any questions can be directed at pablos@usf.edu

# Requirements

- [Java](https://www.java.com/en/)   (for running the simulations)      >= 15
- [Maven](https://maven.apache.org/)  (for compiling the code)           >= 3.8.1
- [Python](https://www.python.org/) (for plotting and post-processing) >= 3.7.3
- [Jupyter Notebook](https://jupyter.org/) (plotting)               >= 6.4.4
- [Slurm](https://slurm.schedmd.com/documentation.html) (for running parallel simulations)  >= 21.08.8-2
- [Intellij](https://www.jetbrains.com/idea/) (optional Jave IDE) 2021

**Notes** 
- The software has been tested with the versions specified above. 
- Versions do not necessarily reflect actual requirements.
- The software is configured to work with Intellij out of the box (hopefully :)), but other IDEs are possible.
- Experiments were designed to be run with Slurm on [CIRCE](https://wiki.rc.usf.edu/index.php/CIRCE)  (USF's computer cluster). 
- Running full experiments without access to CIRCE or Slurm cluster will require adapting the run scripts (see [Run instructions](#run-instructions)).

# Installation

Previous to the following code make sure to install all requirements.

``` 
mkdir scs_home          # create a folder for the project
cd scs_home             # move to the folder
git clone               # clone the project into the folder
cd Multiscale-V2        # move into the cloned folder
python init_config.py   # download scs to scs_home/scs and configurates git
```

# Project Structure

The following summarizes the folder structure after running the installation instructions.

```
scs_home
└─ scs                                    # scs library
|                                         # 
└─ Multiscale-V2                          # Multiscale project 
   └─ docs                                # Deprecated documentation - TODO: update
   └─ scripts                             # Contains python and bash scripts utilities
   └─ src                                 # Contains the java code for simulating rats
   └─ experiments                         # Folder to define experiments and store results
   |  └─ mazes                            # Files describing the mazes
   |  └─ pc_layers                        # Files describing the place cell layers
   |  └─ setups                           # Files describing experiments with simulated rats
   |  └─ BICY2020_modified                # Latest experiments with multiscale model
   |     └─ config_files                  # Contains files describing tables of parameters
   |     |  └─ generatos                  # scripts to generate parameter tables
   |     |  |  experiment11-article2.csv  # Parameter table of the latest experiments     
   |     |                                #
   |     └─ post_processing               # contains scripts for post processing data   
   |     └─ [logs]                        # Automatically created after running an experiment
   |     |                                # Contains the results of the experiment
   |     |
   |     | ( Following bash scripts execute full experiments on CIRCE - see requirements)
   |     | ( update to run with your own system )
   |     |  run_set_variables.sh          # Defines which experiments and rats 
   |     |                                # to run and what scripts to use.
   |     |                                # This file is used by following scripts
   |     |  run_1_all.sh                  # Runs experiments defined by run_set_variables.sh
   |     |  run_2_check_missing.sh        # Checks for errors after running run_1_all.sh
   |     |  run_3_process_all_configs.sh  # Post processes data
   |     |  run_4_merge_configs.sh        # Merges results into a single database
   |     |  run_5_plot_all_experiments.sh # plots results of all experiments (deprecated)
   |     |  run_6_compress_results.sh     # Compress results for downloading (deprecated)
   |
   |  articl2.ipynb                       # Jupyter notebook for plotting data
   |                                      # Must run experiments before executing this file
   |  init_config.py                      # Configuration script run after cloning project
   |  pkgs.txt                            # List of python packages used
   |  pom.xml                             # Maven pom file
   |  Multiscale-F2019.iml                # Intellij project
```


# General concepts

### Model
Refers to the spatial cognition model developed in this project.

### Setup files

Setup files are XML files found in the [setups folder](experiments->setup). 
They describe setups for performing robot experiments using the framework `SCS`.
Among other things, setup files describe:
- Which GUI to use (if any)
- Which simulator to use
- Initial simulation speed and state (e.g.: pause)
- Which spatial cognition models to use and their parameters
- Mazes to be used
- Tasks to be performed at different stages of the simulation such as:
    +  Placing the robot at the start of an episode
    +  Giving rewards for reaching a goal
    +  Logging information

### Configuration

A configuration refers to a specific combination of model parameters.  
Configurations assign a value to each model parameter.  
An experiment compares the model by simulating multiple individuals for each configuration.

### Configuration files

Configuration files are CSV files found in the `config_files` folders.  
Each file contains a table of parameters describing all individuals to be simulated in an experiment.  
Each row defines the parameters of a single individual.  
The latest configuration file is [experiment11-article2.csv](experiments/BICY2020_modified/config_files/experiment11-article2.csv)

# Run instructions

## Running a single rat using Intellij

1. Open folder Multiscale-V2 using Intellij  
2. Reload each Maven project:  
    1. In the list of projects, secondary click on `SCS`  
    2. Choose option `Maven->Reload Project` from the dropdown list  
    3. If prompted, choose trust project  
    4. Repeat steps 2.1 - 2.3 for project `Multiscale-V2`
3. Run default run configuration either from Intellij's toolbars or press `shift+F10`

Notes:
- Intellij will automatically compile the project using maven and run a predefined simulation.
- By default, the GUI is turned off, see [Turning GUI on](#turning-gui-on).
- Upon successful execution, you will see the message:  
`"[+] Finished experiment"`  
followed by the time taken to perform the simulation.
- To change the individual being simulated you must update the list of arguments defined in Intellij's run configuration.  
See [Running a single rat using maven](#running-a-single-rat-using-maven) for details about the arguments.

## Running a single rat using maven

Run the following code from folder `scs_home`:
```
cd scs                  # move to scs folder
mvn install             # install scs to your local maven library
cd ../Multiscale-V2     # move to Multiscale-V2 project
mvn package             # use maven to generate jar file
java -cp target/Multiscale-F2019-1.0.0-SNAPSHOT-jar-with-dependencies.jar com.github.biorobaw.scs.Main <CONFIG_FILE> <ROW> yes
```
In the code above:
- **`<CONFIG_FILE>`** should be replaced by the path to a configuration file (see [Configuration Files](#configuration-files)) 
- **`<ROW>`** should be replaced by an integer corresponding to the individual to be simulated from the configuration file.  
The first individual is 0.
- Full example: `java -cp target/Multiscale-F2019-1.0.0-SNAPSHOT-jar-with-dependencies.jar com.github.biorobaw.scs.Main experiments\BICY2020_modified\config_files\experiment1-traces.csv 0 experiments\BICY2020_modified\logs\test yes`
- The last argument set to either 'yes' or 'no', indicates whether to create the logging folder structure or not.  
When running a single rat we suggest setting it to 'yes'.  
Scripts for running parallel simulations create the folder structure before simulations and set the argument to 'no' (see [Running a full experiment](#running-a-full-experiment)).


## Turning GUI on

To turn the GUI on, replace `DisplayNone` by `DisplayJavaFX` in the `display` element on the [xml setup file](experiments/setups/experiment_1.xml) (line 14).

## Running a full experiment

To run a full experiment, all individuals in a configuration file have to be successfully executed.  
To run simulations in parallel, we provide bash scripts that submit [Slurm](https://slurm.schedmd.com/documentation.html) batch jobs (see [Project Structure](#project-structure)).  
The scripts are meant to be executed in [CIRCE](https://wiki.rc.usf.edu/index.php/CIRCE) (USF's cluster of computers) and may require adapting if running in another system.  
Bash scripts should be run sequentially after completing each batch job.  

To run an experiment execute the following code from the home folder:

```
# move to Multiscale folder
cd Multiscale-V2

# submit slurm job to run all rats in all experiments
# defined in run_set_variables.sh
# the script will also init the log folder
# and move any necessary files
sh experiments/BICY2020_modified/run_1_all.sh                                 

# wait until slurms jobs are done before executing next command
# check whether any simulations failed
# failures are typically caused by running out of time in the server
# which result in the remaining processes being cancelled
# the following script checks for missing and resubmits rats if necessary
sh experiments/BICY2020_modified/run_2_check_missing.sh        

# if no rats are missing:
# submit slurm job to generate database for each configuration
sh experiments/BICY2020_modified/run_3_process_all_configs.sh

# merge all results into a single database
sh experiments/BICY2020_modified/run_4_merge_configs.sh

# Open jupyter notebook for plotting
jupyter-notebook.exe .\articl2.ipynb
```

As a result of the process, a log folder will be generated in the experiment folder (see [Project Structure](#Project project-structure)).  
The log folder should contain the results of the experiment with a sqlite database named `experiment_results.sqlite`.


# TODO

* Modify the pom file so SCS is imported from GitHub rather than the local repository
