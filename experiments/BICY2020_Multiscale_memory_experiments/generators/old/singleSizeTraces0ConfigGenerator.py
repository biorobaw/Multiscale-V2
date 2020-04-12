import numpy as np
import pandas as pd
import os
import xml.etree.ElementTree as ET
import math

def dataFrame(colname,values):
  return pd.DataFrame({colname:values,'key':0})
  
def oneXone(df1,df2):
  return pd.concat([df1,df2[df2.columns.difference(df1.columns)]],axis=1)

def allXall(df1,df2):
  return df1.merge(df2,on='key')
  
def createConfigColumn(df):
  df['config']= 'c' + df.index.map(str)
   
  
def saveResult(df,fileName):
  df.drop(['key'],axis=1).to_csv(fileName,sep='\t',index=False)
  
numRatsPerConfig = 100
episodesPerStartingLocation = 100
runLevel = 1

outputFile = 'singleSizeTraces0ConfigSet.csv'

runLevel = dataFrame('runLevel',[runLevel])
experiment = dataFrame('experiment',[ './multiscalemodel/src/edu/usf/ratsim/model/pablo/multiscale_memory/experiments/experiment.xml'])
group = dataFrame('group',['Control'])

ratIds = dataFrame('subName',range(numRatsPerConfig))

mazePaths = ['multiscalemodel/src/edu/usf/ratsim/model/pablo/multiscale_memory/mazes/M0.xml',
            'multiscalemodel/src/edu/usf/ratsim/model/pablo/multiscale_memory/mazes/M1.xml'
            ]
mazes = dataFrame('mazeFile',mazePaths)
            
fullMazePaths = [os.environ['SCS_FOLDER']+'/' + f for f in mazePaths]      
numLocations = [len(ET.parse(f).getroot().iter('startPositions').__next__().findall('pos')) for f in fullMazePaths    ]
numLocations = dataFrame('numStartingPositions',numLocations)

pcSizes = dataFrame('pcSizes',[0.04*i for i in range(1,15)])
                              
#we got 27.5 from doing d_between_cells*sqrt(2) < 2r
#d_between_cells = (maze_width + 2r)/(n+1)
numPCx = dataFrame('numPCx',[math.ceil((1+27.5/i)*math.sqrt(2)-1) for i in range(1,15)])

##############################################################
#generate table
                             
#combine mazes and numLocations one2one
partial = oneXone(mazes,numLocations)

#calculate num of episodes for each maze: locations*episodes per location
partial['numEpisodes'] = partial['numStartingPositions']*episodesPerStartingLocation


partial = allXall(group,partial)
partial = allXall(experiment,partial)
partial = allXall(runLevel,partial)

pcTable = oneXone(pcSizes,numPCx)
pcTable['traces']=0
partial = allXall(partial,pcTable)

createConfigColumn(partial)


final = allXall(partial,ratIds);

saveResult(final,outputFile)




            







