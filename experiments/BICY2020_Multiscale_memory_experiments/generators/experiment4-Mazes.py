from baseGenerator import *

# EXPERIMENT SETUP FIELDS  
outputFile     = '../experiment4-Mazes.csv'           # relative to this folder
experiment     = 'experiments/setups/experiment_1.xml' # relative to git root folder
group          = 'Control'
ratsPerConfig  = 100
rat_ids = [i for i in range(ratsPerConfig)]


# MAZE RELATED FIELDS
mazeWidth   = 2.2
mazeHeight  = 3
mazes       = ['M{}.xml'.format(i) for i in range(2,8)]
mazesPath   = 'experiments/mazes' # relative to git root folder
episodesPerStartingLocation = 250

    
# PC RELATED FIELDS
pcRadii     = [0.04*i for i in range(1,9)]
numPCx      = calculate_min_coverage_PCx(mazeWidth, pcRadii)
traces      = 0.7



# GENERATE DATA FRAMES
experiment_DF = dataFrame('experiment',experiment)
group_DF      = dataFrame('group',group)
ratIds_DF     = dataFrame('run_id',rat_ids)
mazes_DF      = generateMazeDF(mazesPath, mazes)
pcs_DF        = generatePC_DF_OLD(mazeWidth, mazeHeight, numPCx , pcRadii)
traces_DF     = dataFrame('traces',traces)            



##############################################################
#generate table
                             
#Combine tables
noRats = reduce(allXall , [experiment_DF, group_DF, mazes_DF, pcs_DF, traces_DF] )
noRats = createConfigColumn(noRats)
noRats['numEpisodes'] = noRats['numStartingPositions']*episodesPerStartingLocation

withRats = allXall(noRats,ratIds_DF);
saveResult(withRats,outputFile)
saveResult(noRats,'../norats4.csv')



            







