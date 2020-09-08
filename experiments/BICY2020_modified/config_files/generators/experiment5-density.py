from baseGenerator import *

# EXPERIMENT SETUP FIELDS  
outputFile     = '../experiment5-density.csv'     # relative to this folder
experiment     = 'experiments/setups/experiment_1.xml'  # relative to git root folder
group          = 'g1'
ratsPerConfig  = 50                                     # reduced from 100 to 25
rat_ids = [i for i in range(ratsPerConfig)]


# MAZE RELATED FIELDS
mazeWidth   = 2.2
mazeHeight  = 3
mazes       = ['M0.xml', 'M1.xml']
mazesPath   = 'experiments/mazes'  # relative to git root folder
episodesPerStartingLocation = 10000


# PC RELATED FIELDS
# layers from previous experiments
# single_layers = pd.DataFrame(columns=['pcSizes', 'minX', 'maxX', 'numX', 'minY', 'maxY', 'numY'])
# single_layers.loc[ 0] = (0.04, -1.084390243902439 , 1.084390243902439 , 40, -1.485	           , 1.485	           , 55)
# single_layers.loc[ 1] = (0.08, -1.0676190476190477, 1.0676190476190477, 20, -1.4710344827586208, 1.4710344827586208, 28)
# single_layers.loc[ 2] = (0.12, -1.0573333333333335, 1.0573333333333335, 14, -1.4657142857142857, 1.4657142857142857, 20)
# single_layers.loc[ 3] = (0.16, -1.05              , 1.05              , 11, -1.4525	           , 1.4525	           , 15)
# single_layers.loc[ 4] = (0.2 , -1.04              , 1.04              , 9 , -1.457142857142857 , 1.457142857142857 , 13)
# single_layers.loc[ 5] = (0.24, -1.0050000000000001, 1.0050000000000001, 7 , -1.4236363636363636, 1.4236363636363636, 10)
# single_layers.loc[ 6] = (0.28, -0.9857142857142858, 0.9857142857142858, 6 , -1.424	           , 1.424	           , 9 )
# single_layers.loc[ 7] = (0.32, -1.0142857142857145, 1.0142857142857145, 6 , -1.456	           , 1.456	           , 9 )
# single_layers.loc[ 8] = (0.36, -0.9733333333333334, 0.9733333333333334, 5 , -1.395	           , 1.395	           , 7 )
# single_layers.loc[ 9] = (0.4 , -1.0               , 1.0               , 5 , -1.4249999999999998, 1.4249999999999998, 7 )
# single_layers.loc[10] = (0.44, -0.924             , 0.924             , 4 , -1.3857142857142857, 1.3857142857142857, 6 )
# single_layers.loc[11] = (0.48, -0.9480000000000001, 0.9480000000000001, 4 , -1.4142857142857141, 1.4142857142857141, 6 )
# single_layers.loc[12] = (0.52, -0.972000000000000 , 0.9720000000000001, 4 , -1.4428571428571428, 1.4428571428571428, 6 )
# single_layers.loc[13] = (0.56, -0.9960000000000001, 0.9960000000000001, 4 , -1.4714285714285715, 1.4714285714285715, 6 )

maxx = 1.05
maxy = 1.45
r    = .44

minNx  = 5
stepNx = 5
maxNx  = 40
nx = np.arange(minNx, maxNx+stepNx, stepNx, dtype=np.int)
ny = np.ceil(nx*mazeHeight/mazeWidth).astype(int)


traces = 0.1*np.arange(0, 10)


# GENERATE DATA FRAMES
experiment_DF = dataFrame('experiment', experiment)
group_DF      = dataFrame('group',      group)
ratIds_DF     = dataFrame('run_id',     rat_ids)
mazes_DF      = generateMazeDF(mazesPath, mazes)

pc_r          = dataFrame('pcSizes', r)
pc_minx       = dataFrame('minX', -maxx)
pc_maxx       = dataFrame('maxX',  maxx)
pc_numx       = dataFrame('numX',    nx)
pc_miny       = dataFrame('minY', -maxy)
pc_maxy       = dataFrame('maxY',  maxy)
pc_numy       = dataFrame('numY',    ny)
pc_traces     = dataFrame('traces', traces)

pc_x  = reduce(allXall, [pc_minx, pc_maxx, pc_numx])
pc_y  = reduce(allXall, [pc_miny, pc_maxy, pc_numy])
pc_xy = oneXone(pc_x, pc_y)



##############################################################
#generate table
                             
#Combine tables
noRats = reduce(allXall , [experiment_DF, group_DF, mazes_DF,
                           pc_r, pc_xy, pc_traces])
noRats = createConfigColumn(noRats)
noRats['numEpisodes'] = noRats['numStartingPositions']*episodesPerStartingLocation

withRats = allXall(noRats, ratIds_DF);
saveResult(withRats, outputFile)
saveResult(noRats, '../norats5.csv')



            







