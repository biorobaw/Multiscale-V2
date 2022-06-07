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
mazes       = ['M0.xml','M1.xml','M8.xml']
mazesPath   = 'experiments/mazes' # relative to git root folder
episodesPerStartingLocation = 10000
mazes_DF      = generateMazeDF(mazesPath, mazes)

# PC RELATED FIELDS
pc_path  = 'experiments/pc_layers/'
maze_layers = pd.DataFrame(columns=['maze_id','pc_files'],
                           data=[[0,pc_path + 'u04.csv'],
                                 [0,pc_path + 'non_uniform_0.csv'],
                                 [1,pc_path + 'u08.csv'],
                                 [1,pc_path + 'u12.csv'],
                                 [1,pc_path + 'non_uniform_1.csv'],
                                 [2,pc_path + 'u04.csv'],
                                 [2,pc_path + 'u08.csv'],
                                 [2,pc_path + 'u12.csv'],
                                 [2,pc_path + 'u16.csv'],
                                 [2,pc_path + 'non_uniform_8.csv']
                                ]
                           )
mazes_pcs_DF = mazes_DF.loc[maze_layers.maze_id].reset_index(drop=True)
mazes_pcs_DF['pc_files'] = maze_layers.pc_files


# GENERATE DATA FRAMES
experiment_DF = dataFrame('experiment', experiment)
group_DF      = dataFrame('group',      group)
ratIds_DF     = dataFrame('run_id',     rat_ids)
traces_DF     = dataFrame('traces', [0.1*i for i in range(10)])



##############################################################
#generate table
                             
#Combine tables
noRats = reduce(allXall , [experiment_DF, group_DF, mazes_pcs_DF, traces_DF] )
noRats = createConfigColumn(noRats)
noRats['numEpisodes'] = noRats['numStartingPositions']*episodesPerStartingLocation

withRats = allXall(noRats, ratIds_DF);
saveResult(withRats, outputFile)
saveResult(noRats, '../norats7.csv')



            







