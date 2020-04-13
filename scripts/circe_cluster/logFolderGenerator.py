import pandas as pd
import os
import sys

#get console input
baseFolder = sys.argv[1]
file = sys.argv[2]

#load the configs and get the names of the configs
configs =pd.read_csv(file,sep='\t')
configFolders = pd.unique(configs['config'])
mazes = pd.unique(configs['mazeFile'])
experiments = pd.unique(configs['experiment'])

#create function for creating folder paths:
def makedirs(dir):
  try:  
      os.makedirs(dir)
  except OSError:  
      return False
  else:  
      return True

#create base folder and the rest of the logfolders
makedirs(baseFolder)
for folder in  configFolders:
  makedirs(baseFolder +"/" + folder)

#create mazes and experiments folder
makedirs(baseFolder+"/experiments")
makedirs(baseFolder+"/mazes")
makedirs(baseFolder+"/slurmOut")

#copy config file, mazes and experiments to base folder
import shutil
shutil.copy2(file,baseFolder + '/configs.csv')
for m in mazes:
    shutil.copy2(m,baseFolder+"/mazes/"+os.path.basename(m))
for e in experiments:
    shutil.copy2(e,baseFolder+"/experiments/"+os.path.basename(e))
#copy maze metrics
shutil.copy2('experiments/mazes/mazeMetrics.csv',baseFolder+'/mazes/mazeMetrics.csv')
