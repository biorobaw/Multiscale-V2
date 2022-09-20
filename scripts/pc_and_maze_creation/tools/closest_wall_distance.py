import math, functools, operator, numpy as np, pandas as pd
import os, sys, time, git
from shapely.geometry import Point, LineString, Polygon, MultiPolygon
from multiprocessing import Pool
from plotnine import *



# sys.path.append('../utils')
git_root = git.Repo('.', search_parent_directories=True).git.rev_parse("--show-toplevel")
sys.path.append(git_root + "/scripts/utils")
sys.path.append(git_root + "/scripts/pc_and_maze_creation")
import MazeParser
from data.Wall import PickableWall as Wall
from data.Feeder import PickableFeeder as Feeder
from data.StartPos import PickableStartPos as StartPos



OUTTER_MINX, OUTTER_MAXX, OUTTER_MINY, OUTTER_MAXY = -1.2, 1.2, -1.6, 1.6 # coordinates of outter bounds
OUTTER_POLYGON = Polygon([(OUTTER_MINX,OUTTER_MINY),(OUTTER_MINX,OUTTER_MAXY),(OUTTER_MAXX,OUTTER_MAXY),(OUTTER_MAXX,OUTTER_MINY)]) # polygon representing outter bounds
MAXLENGTH = np.linalg.norm(np.array([ OUTTER_MAXX, OUTTER_MAXY ]) - np.array([OUTTER_MINX, OUTTER_MINY]) ) * 2 # max distance for any point to be outside of bounds
PRECISION = 0.005 # precision to be used for tesselating the space


# Find visibility polygons from all cell centers in a tesselation of the maze
def find_all_distances(walls, precision):
    min_x, num_x, min_y, num_y = get_grid_and_coordinates(walls, PRECISION)
    all_distances = np.array([ [ find_closest_distance(walls, min_x + PRECISION * (i+0.5), min_y + PRECISION * (j+0.5)) for i in range(num_x)] for j in range(num_y)])
    return min_x, num_x, min_y, num_y, all_distances



def find_closest_distance(walls, cx, cy ):
    c  = Point(np.array([cx,cy]))
    return np.min( [wall_to_line_string(w).distance(c) for w_id, w in walls.iterrows()])
        

def wall_to_line_string(w):
    w = w.to_numpy()
    return LineString([w[:2],w[2:]])


# return the data representing the tesselated maze
def get_grid_and_coordinates(walls, precision):
    min_x = np.min([walls.x1.min(), walls.x2.min()]) - precision/2
    max_x = np.max([walls.x1.max(), walls.x2.max()]) + precision/2
    min_y = np.min([walls.y1.min(), walls.y2.min()]) - precision/2
    max_y = np.max([walls.y1.max(), walls.y2.max()]) + precision/2

    num_x = int(np.ceil((max_x - min_x)/precision))
    num_y = int(np.ceil((max_y - min_y)/precision))
    
    return min_x, num_x, min_y, num_y




def save(file_name, min_x, num_x, min_y, num_y, all_distances):

    with open(file_name, 'bw') as f:

        # store grid information:
        np.array( [ min_x, num_x, min_y, num_y ] ).astype(np.float32).tofile(f)
        all_distances.reshape(-1).astype(np.float32).tofile(f)



# plots missing polygons for debugging
def plot_distances( walls, min_x, num_x, min_y, num_y, all_distances, precision, plot = None):

    plot = plot if plot is not None else ggplot()
     
    # prev_ids = np.fromfile(f, np.float32, int(num_x*num_y))
    [ys, xs] = np.mgrid[0:num_y,0:num_x].reshape(2,-1)
    xs = xs*precision + min_x
    ys = ys*precision + min_y
    distance_df = pd.DataFrame({'x':xs,'y':ys,'d':all_distances.reshape(-1)})
    plot += geom_tile(aes(x='x',y='y',fill='d'), data=distance_df)

    # plot maze
    plot += geom_segment(aes(x='x1', y='y1', xend='x2', yend='y2'), data=walls, color='k', size=1.5)
    # plot += geom_point(aes(x='x', y='y'), data=feeders, color='r', size=4)
    # plot += geom_point(aes(x='x', y='y'), data=start_positions, color='g', size=4)

    # ADD THEMES TO PLOT
    plot += coord_fixed(ratio = 1)
    plot += theme_void()
    return plot
    


def map_distances_from_pickles(wall_pickles):
    walls = pd.DataFrame(columns=['x1','y1','x2','y2'],  data=[ [w.x1(), w.y1(), w.x2(), w.y2()] for w in wall_pickles])
    min_x, num_x, min_y, num_y, all_distances = find_all_distances(walls, PRECISION)
    return min_x, num_x, min_y, num_y, all_distances


def map_distances_from_file(folder, maze_file):
    print('Mapping closest wall distances in ', maze_file)
    full_path = os.path.join(folder, maze_file)
    walls, feeders, start_positions = MazeParser.parse_maze(full_path)
    
    # FIND DISTANCES
    min_x, num_x, min_y, num_y, all_distances = find_all_distances(walls, PRECISION)
    
    # SAVE DISTANCES
    save_name = full_path.replace('.xml', '_closest_wall_distances.bin')
    print('Saving ', save_name)
    save(save_name, min_x, num_x, min_y, num_y, all_distances)

    # PLOT DISTANCE MAP FOR DEBUGGING
    plot_name = full_path.replace('.xml', '_closest_wall_distances.png')
    plot = plot_distances(walls, min_x, num_x, min_y, num_y, all_distances, PRECISION,ggplot())
    ggsave(plot, plot_name, dpi=300, verbose = False)
    print('Done with: ', maze_file)
    return ''


pool = None
def map_closest_wall_distances(folder):
    debug = False
    if debug:
        map_distances_from_file('tools/samples', 'M304.xml')
        # map_visibility_from_file('../../experiments/mazes/obstacles/', 'M304.xml')
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
        pool.starmap_async(map_distances_from_file, args, callback=finished_all_files)


def finished_all_files(results):
    global pool
    print('finished mapping closest wall distances!')
    pool.close()
    pool = None
    errors = [r for r in results if r!='']
    if(len(errors)>0):
        print('Error with files: {errors}')
    else:
        print('No errors!')

