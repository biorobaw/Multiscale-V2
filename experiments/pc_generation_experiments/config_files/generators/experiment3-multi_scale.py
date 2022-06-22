from baseGenerator import *
import git
from os import listdir
from os.path import isfile, join
import numpy as np

# EXPERIMENT SETUP FIELDS  ##################################################

outputFileNoRats = '../norats3.csv'
outputFile     = '../experiment3-multiscale.csv'     # relative to this folder

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
    "mix_name",
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
dir_generative_mazes = dir_mazes + 'generative_experiments/'

dir_layers  = 'experiments/pc_layers/'
dir_layers_uniform = dir_layers +'uniform/'
dir_layers_locally_uniform = dir_layers + 'locally_uniform/'
dir_layers_non_uniform = dir_layers + 'non_uniform/'
dir_layers_multi_layer = dir_layers + 'multi_layer/'
empty_maze = dir_layers + 'empty.csv'


# USEFUL FUNCTIONS:
def load_layers(folder):
    full_path = join(dir_git_root, folder)
    layers = [f for f in listdir(full_path) if isfile(join(full_path, f)) and f[-4:]=='.csv']
    return dataFrame('pc_files', [folder + f for f in layers])



# GENERATE DATAFRAMES 
episodesPerStartingLocation = 3000
ratsPerConfig = 20
aux_r10 = np.arange(1,10)

experiment_DF           = dataFrame('experiment', dir_setups + 'experiment_1.xml')  # relative to git root folder
group_DF                = dataFrame('group', 'g1')
maze_DF                 = generateMazeDF(dir_generative_mazes, ['M0.xml','M1.xml','M2.xml','M3.xml','M4.xml']) # also computes num starting positions for each maze
maze_DF['numEpisodes']  = maze_DF['numStartingPositions']*episodesPerStartingLocation
pc_files_DF             = dataFrame('pc_files', ",".join([empty_maze]*4))
independent_pcs_DF      = dataFrame('independent_pcs', 'false')
pc_modulation_method_DF = dataFrame('pc_modulation_method', 'none')
pc_generation_method_DF = dataFrame('pc_generation_method', 'layer') # create one for each layer that is below the given threshold
pc_generation_raddi_thresholds_DF   = pd.DataFrame(columns = ['key', 'pc_generation_radii', 'pc_generation_threshold', 'mix_name' ], # assume bests are 0.004, 0.3, 0.4, 0.6
    data = [
        [0,     '0.08,024,0.4,0.56',    '0.001,0.001,0.001,0.001', 'max0'],
        [0,     '0.08,024,0.4,0.56',    '0.004,0.1,0.1,0.1', 'max1'],
        [0,     '0.08,024,0.4,0.56',    '0.004,0.2,0.2,0.2', 'max2'],
        [0,     '0.08,024,0.4,0.56',    '0.004,0.3,0.3,0.3', 'max3'],
        [0,     '0.08,024,0.4,0.56',    '0.004,0.3,0.4,0.4', 'max4'],
        [0,     '0.08,024,0.4,0.56',    '0.004,0.3,0.4,0.5', 'max5'],
        [0,     '0.08,024,0.4,0.56',    '0.004,0.3,0.4,0.6', 'max6'],
    ]
)
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
    pc_generation_raddi_thresholds_DF,
    pc_generation_active_layers_only_DF,
    save_pcs_DF,
    traces_DF_DF,
]
no_rats_DF = reduce(allXall , reduce_DFs )
no_rats_DF = createConfigColumn(no_rats_DF)
rats_DF = allXall(no_rats_DF, dataFrame('run_id', list(range(ratsPerConfig))))[['key'] + outputColumns]



saveResult(rats_DF, outputFile)
saveResult(no_rats_DF, outputFileNoRats)



            






