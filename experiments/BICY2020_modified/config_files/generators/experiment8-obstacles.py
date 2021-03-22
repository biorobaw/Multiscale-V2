from baseGenerator import *

# EXPERIMENT SETUP FIELDS  
outputFile     = '../experiment8-obstacles.csv'     # relative to this folder
experiment     = 'experiments/setups/experiment_1.xml'  # relative to git root folder
group          = 'g1'
ratsPerConfig  = 100                                     # reduced from 100 to 25
rat_ids = [i for i in range(ratsPerConfig)]


# MAZE RELATED FIELDS
mazeWidth   = 2.2
mazeHeight  = 3
mazes       = [f'M{i}{j:02d}.xml' for i in range(1,7) for j in range(0,10)]
mazesPath   = 'experiments/mazes/obstacles' # relative to git root folder
episodesPerStartingLocation = 10000
num_obstacles = {f'{mazesPath}/M{i}{j:02d}.xml' : i*10 for i in range(1,7) for j in range(0,10)}
mazes_DF      = generateMazeDF(mazesPath, mazes)
print(mazes_DF)

# PC RELATED FIELDS
pc_path  = 'experiments/pc_layers/'

# GENERATE DATA FRAMES
experiment_DF = dataFrame('experiment', experiment)
group_DF      = dataFrame('group',      group)
ratIds_DF     = dataFrame('run_id',     rat_ids)
pc_layers_DF  = dataFrame('pc_files', [pc_path + f for f in ['u08.csv']])
traces_DF     = dataFrame('traces', [ 0.8 ])



##############################################################
#generate table
                             
#Combine tables
noRats = reduce(allXall , [experiment_DF, group_DF, mazes_DF, pc_layers_DF, traces_DF] )
noRats = createConfigColumn(noRats)
noRats['numEpisodes'] = noRats['numStartingPositions']*episodesPerStartingLocation
noRats['numObstacles'] = noRats['mazeFile'].map(num_obstacles)

withRats = allXall(noRats, ratIds_DF);
saveResult(withRats, outputFile)
saveResult(noRats, '../norats8.csv')



            







