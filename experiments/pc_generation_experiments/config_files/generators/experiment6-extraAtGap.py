from baseGenerator import *

# EXPERIMENT SETUP FIELDS  
outputFile     = '../experiment6-extraAtGap.csv'     # relative to this folder
experiment     = 'experiments/setups/experiment_1.xml'  # relative to git root folder
group          = 'g1'
ratsPerConfig  = 100                                     # reduced from 100 to 25
rat_ids = [i for i in range(ratsPerConfig)]


# MAZE RELATED FIELDS
mazeWidth   = 2.2
mazeHeight  = 3
mazes       = ['M1.xml']
mazesPath   = 'experiments/mazes' # relative to git root folder
episodesPerStartingLocation = 10000


# PC RELATED FIELDS
# layers from previous experiments
single_layers = pd.DataFrame(columns=['pcSizes', 'minX', 'maxX', 'numX', 'minY', 'maxY', 'numY'])
single_layers.loc[ 0] = (0.04, -1.084390243902439 , 1.084390243902439 , 40, -1.485	           , 1.485	           , 55)
single_layers.loc[ 1] = (0.08, -1.0676190476190477, 1.0676190476190477, 20, -1.4710344827586208, 1.4710344827586208, 28)
single_layers.loc[ 2] = (0.12, -1.0573333333333335, 1.0573333333333335, 14, -1.4657142857142857, 1.4657142857142857, 20)
single_layers.loc[ 3] = (0.16, -1.05              , 1.05              , 11, -1.4525	           , 1.4525	           , 15)
single_layers.loc[ 4] = (0.2 , -1.04              , 1.04              , 9 , -1.457142857142857 , 1.457142857142857 , 13)
single_layers.loc[ 5] = (0.24, -1.0050000000000001, 1.0050000000000001, 7 , -1.4236363636363636, 1.4236363636363636, 10)
single_layers.loc[ 6] = (0.28, -0.9857142857142858, 0.9857142857142858, 6 , -1.424	           , 1.424	           , 9 )
single_layers.loc[ 7] = (0.32, -1.0142857142857145, 1.0142857142857145, 6 , -1.456	           , 1.456	           , 9 )
single_layers.loc[ 8] = (0.36, -0.9733333333333334, 0.9733333333333334, 5 , -1.395	           , 1.395	           , 7 )
single_layers.loc[ 9] = (0.4 , -1.0               , 1.0               , 5 , -1.4249999999999998, 1.4249999999999998, 7 )
single_layers.loc[10] = (0.44, -0.924             , 0.924             , 4 , -1.3857142857142857, 1.3857142857142857, 6 )
single_layers.loc[11] = (0.48, -0.9480000000000001, 0.9480000000000001, 4 , -1.4142857142857141, 1.4142857142857141, 6 )
single_layers.loc[12] = (0.52, -0.972000000000000 , 0.9720000000000001, 4 , -1.4428571428571428, 1.4428571428571428, 6 )
single_layers.loc[13] = (0.56, -0.9960000000000001, 0.9960000000000001, 4 , -1.4714285714285715, 1.4714285714285715, 6 )

# new layer to add - 3 by 3 grid
r  = 0.16
nx = 3                        # grid size (columns)
ny = 3                        # grid size (rows)
dx = 2*1.05 / 10              # original dx of layer 0.16
dy = 2*1.4386666666666665/13  # original dy of layer 0.16
mx = 0.1 - dx*(nx-1)/2.0      # min x
Mx = 0.1 + dx*(nx-1)/2.0      # max x
my = 1.2 - dy*(ny-1)/2.0      # min y
My = 1.2 + dy*(ny-1)/2.0      # max y
single_layers.loc[14] = (r, mx, Mx, nx, my, My, ny)

# new layer to add - 4 by 4 grid around gap
r  = 0.16
nx = 4                        # grid size (columns)
ny = 4                        # grid size (rows)
dx = 2*1.05 / 10              # original dx of layer 0.16
dy = 2*1.4386666666666665/13  # original dy of layer 0.16
mx = 0.5 + 0.15/2 - dx*(nx-1)/2.0      # min x
Mx = 0.5 + 0.15/2 + dx*(nx-1)/2.0      # max x
my = 0 - dy*(ny-1)/2.0      # min y
My = 0 + dy*(ny-1)/2.0      # max y
single_layers.loc[15] = (r, mx, Mx, nx, my, My, ny)

# add traces to the single layers and the convert columns to strings:
# single_layers['traces'] = 0.7
final_columns = ['pcSizes', 'minX', 'maxX', 'numX', 'minY', 'maxY', 'numY']
single_layers.numX = single_layers.numX.astype(int)  # must set to int before string
single_layers.numY = single_layers.numY.astype(int)  # myst set to int before string
for c in final_columns:
    single_layers[c] = single_layers[c].astype(str)

# choose layer combinations to be used
combinations = [[i] for i in range(3, 14)]
for i in range(1, len(combinations)):
    combinations[i] += [14, 15]

# prepare combinations
combined_layers = pd.concat([single_layers.loc[c].agg(','.join).to_frame().transpose() for c in combinations], ignore_index=True)
combined_layers['key'] = 0  # the constant key is required to perform following cartesian product


traces = [','.join([str(i/10) for j in range(3)]) for i in range(10)]

# GENERATE DATA FRAMES
experiment_DF = dataFrame('experiment', experiment)
group_DF      = dataFrame('group',      group)
ratIds_DF     = dataFrame('run_id',     rat_ids)
mazes_DF      = generateMazeDF(mazesPath, mazes)
pcs_DF        = combined_layers
traces_DF     = dataFrame('traces', traces)



##############################################################
#generate table
                             
#Combine tables
noRats = reduce(allXall , [experiment_DF, group_DF, mazes_DF, pcs_DF, traces_DF] )
noRats = createConfigColumn(noRats)
noRats['numEpisodes'] = noRats['numStartingPositions']*episodesPerStartingLocation

withRats = allXall(noRats, ratIds_DF);
saveResult(withRats, outputFile)
saveResult(noRats, '../norats6.csv')



            







