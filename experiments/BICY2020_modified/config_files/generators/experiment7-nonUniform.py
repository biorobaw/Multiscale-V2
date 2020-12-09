from baseGenerator import *

# EXPERIMENT SETUP FIELDS  
outputFile     = '../experiment7-nonUniform.csv'     # relative to this folder
experiment     = 'experiments/setups/experiment_1.xml'  # relative to git root folder
group          = 'g1'
ratsPerConfig  = 100                                     # reduced from 100 to 25
rat_ids = [i for i in range(ratsPerConfig)]


# MAZE RELATED FIELDS
mazeWidth   = 2.2
mazeHeight  = 3
mazes       = ['M0.xml', 'M1.xml']
mazesPath   = 'experiments/mazes' # relative to git root folder
episodesPerStartingLocation = 10000


# PC RELATED FIELDS
pc_path  = 'experiments/pc_layers/'
pc_files = [ pc_path + file for file in ['pcs_maze0.csv', 'pcs_maze1.csv']]
traces   = [0.1*i for i in range(10)]

# GENERATE DATA FRAMES
experiment_DF = dataFrame('experiment', experiment)
group_DF      = dataFrame('group',      group)
ratIds_DF     = dataFrame('run_id',     rat_ids)
mazes_DF      = generateMazeDF(mazesPath, mazes)
pcs_DF        = dataFrame('pc_files', pc_files)
traces_DF     = dataFrame('traces', traces)



##############################################################
#generate table
                             
#Combine tables
noRats = reduce(allXall , [experiment_DF, group_DF, oneXone(mazes_DF, pcs_DF), traces_DF] )
noRats = createConfigColumn(noRats)
noRats['numEpisodes'] = noRats['numStartingPositions']*episodesPerStartingLocation

withRats = allXall(noRats, ratIds_DF);
saveResult(withRats, outputFile)
saveResult(noRats, '../norats7.csv')



            







