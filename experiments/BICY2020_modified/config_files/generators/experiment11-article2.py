from baseGenerator import *
import git
from os import listdir
from os.path import isfile, join

# EXPERIMENT SETUP FIELDS  ##################################################

outputFileNoRats = '../norats11.csv'
outputFile     = '../experiment11-article2.csv'     # relative to this folder
experiment     = 'experiments/setups/experiment_1.xml'  # relative to git root folder

# constants for all configs ################################################

mazeWidth   = 2.2
mazeHeight  = 3
episodesPerStartingLocation = 10000
group          = 'g1'

experiment_DF = dataFrame('experiment', experiment)
group_DF      = dataFrame('group',      group)
traces_DF     = dataFrame('traces',     [ 0, 0.7 ])

dir_git_root = git.Repo('.', search_parent_directories=True).git.rev_parse("--show-toplevel")
dir_mazes = 'experiments/mazes/'
dir_obstacle_mazes = dir_mazes + 'obstacles/'

dir_layers  = 'experiments/pc_layers/'
dir_layers_uniform = dir_layers +'uniform/'
dir_layers_locally_uniform = dir_layers + 'locally_uniform/'
dir_layers_non_uniform = dir_layers + 'non_uniform/'
dir_layers_multi_layer = dir_layers + 'multi_layer/'


def load_layers(folder):
    full_path = join(dir_git_root, folder)
    layers = [f for f in listdir(full_path) if isfile(join(full_path, f)) and f[-4:]=='.csv']
    return dataFrame('pc_files', [folder + f for f in layers])

layers_uniform_DF          = load_layers(dir_layers_uniform)
layers_locally_uniform_DF  = load_layers(dir_layers_locally_uniform)
layers_non_uniform_DF      = load_layers(dir_layers_non_uniform)
layers_multi_layer_DF      = load_layers(dir_layers_multi_layer)

# print( layers_uniform_DF )
# print( layers_locally_uniform_DF )
# print( layers_non_uniform_DF )
# print( layers_multi_layer_DF)


mazes_basic_DF = generateMazeDF(dir_mazes, [ f'M{m}.xml' for m in [0, 1, 8]])
mazes_obstacles_DF = generateMazeDF(dir_obstacle_mazes, [ f'M{10*o}{id}.xml' for  o in range(1,7) for id in range(10) ])

# map_num_obstacles = {f'{mazesPath}/{m}' : int(m[2:4]) for m in mazes}

init_configs = 0


# density experiment mazes 0,1,8: ###########################################


ratsPerConfig = 100
no_rats_density_m0_8 = reduce(allXall , [experiment_DF, group_DF, mazes_basic_DF, layers_uniform_DF, traces_DF] )
no_rats_density_m0_8 = createConfigColumn(no_rats_density_m0_8, init_configs)
no_rats_density_m0_8['numEpisodes'] = no_rats_density_m0_8['numStartingPositions']*episodesPerStartingLocation
all_runs_m0_8 = allXall(no_rats_density_m0_8, dataFrame('run_id', [i for i in range(ratsPerConfig)]));



# density experiment mazes M100-M609 ########################################

ratsPerConfig = 10
init_configs += len(no_rats_density_m0_8)
no_rats_density_m100_609 = reduce(allXall , [experiment_DF, group_DF, mazes_obstacles_DF, layers_uniform_DF, traces_DF] )
no_rats_density_m100_609 = createConfigColumn(no_rats_density_m100_609, init_configs)
no_rats_density_m100_609['numEpisodes'] = no_rats_density_m100_609['numStartingPositions']*episodesPerStartingLocation
all_runs_m100_609 = allXall(no_rats_density_m100_609, dataFrame('run_id', [i for i in range(ratsPerConfig)]));

# locally uniform experiments ###############################################

ratsPerConfig=100
init_configs += len(no_rats_density_m100_609)
no_rats_locally_uniform = reduce(allXall , [experiment_DF, group_DF, mazes_basic_DF, layers_locally_uniform_DF, traces_DF] )

# remove bad rows (where maze is M8 or maze is M0 and layers is lu1):
no_rats_locally_uniform = no_rats_locally_uniform.query('not mazeFile.str.contains("M8.xml")')
no_rats_locally_uniform = no_rats_locally_uniform.query('not mazeFile.str.contains("M0.xml") or not pc_files.str.contains("lu1")')
no_rats_locally_uniform = no_rats_locally_uniform.copy().reset_index(drop=True)

no_rats_locally_uniform = createConfigColumn(no_rats_locally_uniform, init_configs)
no_rats_locally_uniform['numEpisodes'] = no_rats_locally_uniform['numStartingPositions']*episodesPerStartingLocation
all_runs_locally_uniform = allXall(no_rats_locally_uniform, dataFrame('run_id', [i for i in range(ratsPerConfig)]));


# non uniform experiments 333333###############################################

ratsPerConfig=100
init_configs += len(no_rats_locally_uniform)
mazes_pcs_DF = oneXone(mazes_basic_DF, layers_non_uniform_DF)

no_rats_non_uniform = reduce(allXall , [experiment_DF, group_DF, mazes_pcs_DF, traces_DF] )
no_rats_non_uniform = createConfigColumn(no_rats_non_uniform, init_configs)
no_rats_non_uniform['numEpisodes'] = no_rats_non_uniform['numStartingPositions']*episodesPerStartingLocation
all_runs_non_uniform = allXall(no_rats_non_uniform, dataFrame('run_id', [i for i in range(ratsPerConfig)]));


# multi layer experiments (contribution) #####################################

ratsPerConfig = 100
init_configs += len(no_rats_non_uniform)
no_rats_multi_layer = reduce(allXall , [experiment_DF, group_DF, mazes_obstacles_DF, layers_multi_layer_DF, traces_DF] )
no_rats_multi_layer = createConfigColumn(no_rats_multi_layer, init_configs)
no_rats_multi_layer['numEpisodes'] = no_rats_multi_layer['numStartingPositions']*episodesPerStartingLocation
all_runs_multi_layer = allXall(no_rats_multi_layer, dataFrame('run_id', [i for i in range(ratsPerConfig)]));







##############################################################

no_rats   = pd.concat([no_rats_density_m0_8, no_rats_density_m100_609, 
                       no_rats_locally_uniform, no_rats_non_uniform, no_rats_multi_layer], ignore_index=True)
with_rats = pd.concat([all_runs_m0_8, all_runs_m100_609, all_runs_locally_uniform,
                       all_runs_non_uniform, all_runs_multi_layer], ignore_index=True)

saveResult(with_rats, outputFile)
saveResult(no_rats, outputFileNoRats)



            







