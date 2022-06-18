from baseGenerator import *
import git
from os import listdir
from os.path import isfile, join
import numpy as np

# EXPERIMENT SETUP FIELDS  ##################################################

outputFileNoRats = '../norats1.csv'
outputFile     = '../experiment1-pcGenerationThreshold.csv'     # relative to this folder

# DESCRIPTION:

# Generate place cells for an empty maze using different scales and pc generation thresholds
# use 10 rats for each configuration.


# OUTPUT COLUMNS:

outputColumns = [
    "config",
    "experiment",
    "group" ,
    "mazeFile",
    "numEpisodes",
    "numStartingPositions",
    "pc_files",
    "independent_pcs",
    "pc_modulation_method",
    "pc_generation_radii",
    "pc_generation_method",
    "pc_generation_threshold",
    "pc_generation_active_layers_only",
    "save_pcs",
    "traces",
    "run_id",
]

# ALL DIRECTORIES (do not erase to allow copy pasting for new generator files)
dir_git_root = git.Repo('.', search_parent_directories=True).git.rev_parse("--show-toplevel")
dir_setups = 'experiments/setups/'
dir_mazes = 'experiments/mazes/'
dir_obstacle_mazes = dir_mazes + 'obstacles/'

dir_layers  = 'experiments/pc_layers/'
dir_layers_uniform = dir_layers +'uniform/'
dir_layers_locally_uniform = dir_layers + 'locally_uniform/'
dir_layers_non_uniform = dir_layers + 'non_uniform/'
dir_layers_multi_layer = dir_layers + 'multi_layer/'


# USEFUL FUNCTIONS:
def load_layers(folder):
    full_path = join(dir_git_root, folder)
    layers = [f for f in listdir(full_path) if isfile(join(full_path, f)) and f[-4:]=='.csv']
    return dataFrame('pc_files', [folder + f for f in layers])



# GENERATE DATAFRAMES 
episodesPerStartingLocation = 10
ratsPerConfig = 10
aux_r10 = np.arange(1,10)

experiment_DF           = dataFrame('experiment', dir_setups + 'experiment_1.xml')  # relative to git root folder
group_DF                = dataFrame('group', 'g1')
maze_DF                 = generateMazeDF(dir_mazes, ['M0.xml']) # also computes num starting positions for each maze
maze_DF['numEpisodes']  = maze_DF['numStartingPositions']*episodesPerStartingLocation
pc_files_DF             = dataFrame('pc_files', dir_layers + 'empty.csv')
independent_pcs_DF      = dataFrame('independent_pcs', 'false')
pc_modulation_method_DF = dataFrame('pc_modulation_method', 'none')
pc_generation_method_DF = dataFrame('pc_generation_method', 'layer') # create one for each layer that is below the given threshold
pc_generation_raddi_DF  = dataFrame('pc_generation_radii', [0.08, 0.24, 0.40, 0.56])
pc_generation_thresholds_DF         = dataFrame('pc_generation_threshold', list(aux_r10*0.001) + list(aux_r10*0.01) + list(aux_r10*0.1) )
pc_generation_active_layers_only_DF = dataFrame('pc_generation_active_layers_only', 'false')
save_pcs_DF                         = dataFrame('save_pcs', 'true')
traces_DF_DF                        = dataFrame('traces', '0')


# GENERATE FINAL DFs:
reduce_DFs = [
    experiment_DF,
    group_DF,
    maze_DF,
    pc_files_DF,
    independent_pcs_DF,
    pc_modulation_method_DF,
    pc_generation_method_DF,
    pc_generation_raddi_DF,
    pc_generation_thresholds_DF,
    pc_generation_active_layers_only_DF,
    save_pcs_DF,
    traces_DF_DF,
]
no_rats_DF = reduce(allXall , reduce_DFs )
no_rats_DF = createConfigColumn(no_rats_DF)
rats_DF = allXall(no_rats_DF, dataFrame('run_id', list(range(ratsPerConfig))))


saveResult(rats_DF, outputFile)
saveResult(no_rats_DF, outputFileNoRats)



            







