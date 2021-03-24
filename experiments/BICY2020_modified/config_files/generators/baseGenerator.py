import numpy as np
import pandas as pd
import os
import xml.etree.ElementTree as ET
import math
from functools import reduce
import git

def get_git_root():
  git_repo = git.Repo('.', search_parent_directories=True)
  git_root = git_repo.git.rev_parse("--show-toplevel")
  return git_root

def dataFrame(colname,values):
  if isinstance(values, list) or isinstance(values, np.ndarray):
    # print(values)
    return pd.DataFrame({'key': 0, colname: values})
  else:
    return pd.DataFrame({'key': 0, colname: [values]})
  
def oneXone(df1,df2):
  return pd.concat([df1,df2.drop('key', axis=1)],axis=1)

def allXall(df1,df2):
  return df1.merge(df2,on='key',sort=False)
  
def createConfigColumn(df):
  configs = [ 'c{}'.format(i) for i in range(len(df.index))]
  return oneXone(dataFrame('config',configs), df)   
  
def saveResult(df,fileName):
  df.drop(['key'],axis=1) \
    .to_csv(fileName,sep='\t',index=False)
  
def numStartLocations(mazeFile):
  pos = ET.parse(mazeFile).getroot() \
          .iter('startPositions').__next__() \
          .findall('pos')
  return len(pos)
  
def generateMazeDF(mazePath,mazes):
  fullMazePaths = [ mazePath +'/'+ m for m in mazes ]
  mazeDF = dataFrame('mazeFile',fullMazePaths)
  
  git_root = get_git_root()
  numLocations = [ numStartLocations(git_root + '/' + f) for f in fullMazePaths ]
  numLocationsDF = dataFrame('numStartingPositions',numLocations)
  
  return oneXone(mazeDF,numLocationsDF)

def calculate_min_coverage_PCx(mazeWidth,radii):
  # OBS (1) uniform PC distribution:  |-O-O-O-...-O-| 
  # OBS (2) if d = oriented distance between 2 PC borders we have: n2r + (n+1)d = w
  # THUS (3):  d = (w-n2r)/(n+1) = (w+2r)/(n+1)-2r
  # OBS (4) if D = distance between 2 PC centers :  D = 2r + d
  # FROM (3) and (4) : D = (w+2r)/(n+1)
  # Minimum coverage restriction for grid: D*sqrt(2) < 2r
  # THUS : (w/(2r)+1)*sqrt(2)-1 < n
  # THUS n_min = ceil((w/(2r)+1)*sqrt(2)-1)

  return [math.ceil((1+mazeWidth/(2*r))*math.sqrt(2)-1) for r in radii]

def generatePC_DF_OLD_MIN_COVERAGE(mazeWidth, mazeHeight, radii):
  numPCx = calculate_min_coverage_PCx(mazeWidth, radii)
  return generatePC_DF_OLD(mazeWidth, mazeHeight, numPCx, radii)

def generatePC_layers_OLD(mazeWidth, mazeHeight, numPCx, radii):
  w = mazeWidth
  h = mazeHeight
  
  proportion = h / w
  numPCy = [math.ceil(nx*proportion) for nx in numPCx]
  
  
  # see function calculate_min_coverage_PCx for description of symbols
  maxX = [ w/2 + r - (w + 2*r)/(nx+1) for r, nx in zip(radii,numPCx)]
  maxY = [ h/2 + r - (h + 2*r)/(ny+1) for r, ny in zip(radii,numPCy)]
  minX = [-M for M in maxX]
  minY = [-M for M in maxY]

  return minX, maxX, numPCx, minY, maxY, numPCy
  
def generatePC_DF_OLD(mazeWidth, mazeHeight, numPCx, radii):
  sets = (radii,) + generatePC_layers_OLD(mazeWidth, mazeHeight, numPCx, radii)
  titles  = ['pcSizes', 'minX', 'maxX', 'numX', 'minY', 'maxY', 'numY']
  return reduce(oneXone, [dataFrame(t,s) for t,s in zip(titles, sets)])
  
  
  
def count_cells(file):
    root = get_git_root()
    full_path = os.path.join(root, file)
    return len(open(full_path).readlines())-1
  
