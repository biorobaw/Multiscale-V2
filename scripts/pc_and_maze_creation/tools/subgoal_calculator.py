import os, sys, time
from shapely.geometry import Point, LineString
import pandas as pd
import math
from multiprocessing import Pool
import numpy as np


# This file divides space in a grid, and for each cell it approximates the distance to the closest subgoal (obstacle corner) - feeders are ignored


sys.path.append('../utils')
import MazeParser
from data.Wall import PickableWall as Wall
from data.Feeder import PickableFeeder as Feeder
from data.StartPos import PickableStartPos as StartPos


pool = None





def get_grid_and_coordinates(walls, precision):
    min_x = np.min([walls.x1.min(), walls.x2.min()]) - precision/2
    max_x = np.max([walls.x1.max(), walls.x2.max()]) + precision/2
    min_y = np.min([walls.y1.min(), walls.y2.min()]) - precision/2
    max_y = np.max([walls.y1.max(), walls.y2.max()]) + precision/2

    num_x = int(np.ceil((max_x - min_x)/precision))
    num_y = int(np.ceil((max_y - min_y)/precision))
    

    return min_x, num_x, min_y, num_y


def get_id(x, y, min_x, min_y, precision):
    row = int(np.floor( (y - min_y) / precision ))
    col = int(np.floor( (x - min_x) / precision ))
    return row, col

def get_coordinates(i,j, min_x, min_y, precision):
    x = min_x + (j+0.5)*precision
    y = min_y + (i+0.5)*precision
    return x,y


def point_in_wall(point, wall):
    return point.distance(wall) < 0.005 # at most 5mm away from wall


def wall_to_line_string(w):
    p1 = Point(w.x1, w.y1)
    p2 = Point(w.x2, w.y2)
    return LineString([p1, p2])

        

neighbors = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
def get_wall_indeces(wall, min_x, min_y, precision, num_x, num_y):
    (x,y) = wall.coords[0]
    id0 = get_id(x, y, min_x, min_y, precision)
    indices = set(id0)
    process_queue = [id0]

    # repeat until no more elements need to be processed
    while len(process_queue) > 0:
        (i0,j0) = process_queue.pop()

        # check all neighbors
        for (di, dj) in neighbors:
            i = i0 + di
            j = j0 + dj

            # if not valid or already processed, skip cell
            if i < 0 or j < 0 or i >= num_y or j >= num_x or (i,j) in indices:
                continue

            # get cell center and check if lays within wall
            point = Point(get_coordinates(i,j, min_x, min_y, precision))
            if point_in_wall(point, wall):
                indices.add((i,j))
                process_queue.append((i,j))
    return indices


def calculate_subgoal_distances(folder, maze_file):
    precision = 0.005
    try:
        full_path = os.path.join(folder, maze_file)
        walls, feeders, start_positions = MazeParser.parse_maze(full_path)


        min_x, num_x, min_y, num_y = get_grid_and_coordinates(walls, precision = precision) # 5 mm grid
        walls = [ wall_to_line_string(w) for id, w in walls.iterrows() ] # Convert to line strings
        obstacles = [w for w in walls if w.length < 1.8] # only keep walls that are obstacles
        subgoal_ids = [ get_id(x, y, min_x, min_y, precision) for w in obstacles for (x,y) in w.coords]
        subgoal_ids += [ get_id(f.x, f.y, min_x, min_y, precision) for f_id,f in feeders.iterrows() ]
        obstacle_ids = set()
        for o in obstacle_ids:
            obstacle_ids = obstacle_ids.union(get_wall_indeces(o, min_x, min_y, precision, num_x, num_y))


        # get dimensions and find table of distances (use np.array for easily storing results as bins)
        dimensions = np.array([ min_x, num_x, min_y, num_y, precision], np.float64  )
        distances = np.zeros((num_y, num_x)) + 10000 # init to infinity
        closest_subgoal = [[None for j in range(num_x)] for i in range(num_y)]


        # init distances of goal locations to 0:
        for s in subgoal_ids:
            distances[s[0],s[1]] = 0
            closest_subgoal[s[0]][s[1]] = s


        to_process = subgoal_ids
        while len(to_process)>0:
            processing = to_process
            to_process = set()

            # process cells in buffer
            for (i1,j1) in processing:
                subgoal = closest_subgoal[i1][j1]

                # process all neighbors
                for di, dj in neighbors:
                    # get neighbor
                    i = i1 + di 
                    j = j1 + dj

                    # check neighbor is inside grid
                    if i < 0 or i >= num_y or j < 0 or j >= num_x:
                        continue

                    # compute new distance to subgoal, update if closer
                    new_distance = precision*np.sqrt((i-subgoal[0])**2 + (j-subgoal[1])**2)
                    if new_distance < distances[i,j]:
                        distances[i,j] = new_distance
                        closest_subgoal[i][j] = subgoal

                        # if neighbor is not a wall, add it to process it later
                        if (i,j) not in obstacle_ids:
                            to_process.add((i,j))

        save_name = full_path.replace('.xml', '_subgoal_distances.bin')
        with open(save_name,'bw') as f:
            # print(dimensions.dtype, distances.dtype)
            dimensions.astype('float32').tofile(f)
            distances.astype('float32').tofile(f)
        return ''

    except:
        return maze_file


def finished_all_mazes(results):
    global pool
    print('finished calculated subgoal distances:')
    errors = [r for r in results if r!='']
    if(len(errors)>0):
        print('Error with files: {errors}')
    else:
        print('No errors!')
    pool.close()
    pool = None

def calculate_all_subgoal_distances(folder):
    debug = False
    if debug:
        calculate_subgoal_distances('tools/samples', 'M304.xml')
        print('done')
    else:
        global pool, start_time
        if(pool is not None):
            print("PROCESS POOL ALREADY OPEN")
            return

        # results = []
        args = [(folder, filename) for filename in os.listdir(folder) if filename.endswith(".xml") ]

        print()
        pool = Pool(12)
        start_time = time.time()
        pool.starmap_async(calculate_subgoal_distances, args, callback=finished_all_mazes)

