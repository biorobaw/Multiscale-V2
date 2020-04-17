from baseGenerator import *

# EXPERIMENT SETUP FIELDS  
outputFile     = '../experiment5-TwoScales.csv'           # relative to this folder
experiment     = 'experiments/setups/experiment_1.xml' # relative to git root folder
group          = 'g1'
ratsPerConfig  = 100
rat_ids = [i for i in range(ratsPerConfig)]


# MAZE RELATED FIELDS
mazeWidth   = 2.2
mazeHeight  = 3
mazes       = ['M0.xml','M1.xml']
mazesPath   = 'experiments/mazes' # relative to git root folder
episodesPerStartingLocation = 100

    
# PC RELATED FIELDS
layerRadius = [0.04*i for i in range(1,15)]
layerNumX   = calculate_min_coverage_PCx(mazeWidth, layerRadius)
traces      = '0,0'  

singleSets = (layerRadius,) + generatePC_layers_OLD(mazeWidth, mazeHeight, layerNumX, layerRadius)
setTitles  = ['pcSizes', 'minX', 'maxX', 'numX', 'minY', 'maxY', 'numY']
combinedSets = [ [ '{},{}'.format(s[i],s[j])  for i in range(0,13) for j in range(i+1,14)] 
                  for s in singleSets ]


# GENERATE DATA FRAMES
experiment_DF = dataFrame('experiment',experiment)
group_DF      = dataFrame('group',group)
ratIds_DF     = dataFrame('run_id',rat_ids)
mazes_DF      = generateMazeDF(mazesPath, mazes)
traces_DF     = dataFrame('traces',traces)            
pcs_DF        = reduce(oneXone, [dataFrame(t,s) for t,s in zip(setTitles, combinedSets)])



##############################################################
#generate table
                             
#Combine tables
noRats = reduce(allXall , [experiment_DF, group_DF, mazes_DF, pcs_DF, traces_DF] )
noRats = createConfigColumn(noRats)
noRats['numEpisodes'] = noRats['numStartingPositions']*episodesPerStartingLocation

withRats = allXall(noRats,ratIds_DF);
saveResult(withRats,outputFile)
saveResult(noRats,'../norats5.csv')



            







