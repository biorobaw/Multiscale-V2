from baseGenerator import *

# EXPERIMENT SETUP FIELDS  
outputFileNoRats = '../norats9.csv'
outputFile     = '../experiment9-biology1.csv'     # relative to this folder
experiment     = 'experiments/setups/experiment_1.xml'  # relative to git root folder
group          = 'g1'
ratsPerConfig  = 20                                     # reduced from 100 to 25
rat_ids = [i for i in range(ratsPerConfig)]


# MAZE RELATED FIELDS
mazesPath   = 'experiments/mazes/biology' # relative to git root folder
mazeWidth   = 2.2
mazeHeight  = 3
num_obstacles  = [0, 6, 11, 23] 
configs_per_num_obstalces = 1
episodesPerStartingLocation = 4000

mazes       = [f'M1{i:02d}{j:02d}.xml' for i in num_obstacles for j in range(0,configs_per_num_obstalces)]
map_num_obstacles = {f'{mazesPath}/{m}' : int(m[2:4]) for m in mazes}
mazes_DF      = generateMazeDF(mazesPath, mazes)
print(mazes_DF)

# PC RELATED FIELDS
pc_path  = 'experiments/pc_layers/uniform_densities/'

# GENERATE DATA FRAMES
experiment_DF = dataFrame('experiment', experiment)
group_DF      = dataFrame('group',      group)
ratIds_DF     = dataFrame('run_id',     rat_ids)
pc_layers_DF  = dataFrame('pc_files', [pc_path + f for f in ['u56_10.csv']])
traces_DF     = dataFrame('traces', [ 0.4 ])



##############################################################
#generate table
                             
#Combine tables
noRats = reduce(allXall , [experiment_DF, group_DF, mazes_DF, pc_layers_DF, traces_DF] )
noRats = createConfigColumn(noRats)
noRats['numEpisodes'] = noRats['numStartingPositions']*episodesPerStartingLocation
noRats['numObstacles'] = noRats['mazeFile'].map(map_num_obstacles)
noRats['num_cells'] = noRats['pc_files'].map(count_cells)

withRats = allXall(noRats, ratIds_DF);
saveResult(withRats, outputFile)
saveResult(noRats, outputFileNoRats)



            







