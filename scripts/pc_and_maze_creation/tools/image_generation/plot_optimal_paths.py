import os, sys, pandas as pd, numpy as np
from pandas.api.types import CategoricalDtype
from plotnine import *

sys.path.append('../utils')
import MazeParser




def plot_file(maze_file_path):
    print('plotting', maze_file_path)

    distance_file = maze_file_path.replace('.xml', '_optimal_paths.bin')
    save_name = maze_file_path.replace('.xml', '_optimal_paths.png')

    p = ggplot()
        
    # If maze file is not none and it has distance file, plot distance heatmap first
    if os.path.exists(distance_file):
        with open(distance_file,'rb') as f:
            [min_x, num_x, min_y, num_y, precision] = np.fromfile(f, np.float32, 5)
            distances = np.fromfile(f, np.float32, int(num_x*num_y))
            distances[ distances == 10000 ] = -0.1
            prev_ids = np.fromfile(f, np.float32, int(num_x*num_y))
            [ys, xs] = np.mgrid[0:num_y,0:num_x].reshape(2,-1)
            xs = xs*precision + min_x
            ys = ys*precision + min_y
            distance_df = pd.DataFrame({'x':xs,'y':ys,'d':distances})
            p += geom_tile(aes(x='x',y='y',fill='d'), data=distance_df)
    else:
        print(f'plot_optimal_paths.py: distance file deos not exist! {distance_file}')
    
    # plot walls
    walls, feeders, start_positions = MazeParser.parse_maze(maze_file_path)
    p += geom_segment(aes(x='x1', y='y1', xend='x2', yend='y2'), data=walls, color='k', size=1.5)
    p += geom_point(aes(x='x', y='y'), data=feeders, color='r', size=4)
    p += geom_point(aes(x='x', y='y'), data=start_positions, color='g', size=4)
        

    # Plot paths:
    for id, start in start_positions.iterrows():
        path = generate_path(start.x, start.y, prev_ids, min_x, num_x, min_y, num_y, precision)
        path_df = pd.DataFrame(columns = ['x','y'], data = path)
        p += geom_path(aes(x='x',y='y'), data=path_df, size = 0.8, color = 'white')

    # ADD THEMES TO PLOT
    p += coord_fixed(ratio = 1)
    p += theme_void()
    
    ggsave(p, save_name, dpi=300, verbose = False)



def generate_path(x,y, prev_ids, min_x, num_x, min_y, num_y, precision):
    # Get initial id an create result array
    num_x = int(num_x)
    start_i, start_j = get_id(x,y, min_x, min_y, precision)
    starting_id = int(start_i * num_x + start_j)
    res = [(x,y)]

    # follow path, until the end
    while prev_ids[starting_id] != starting_id:
        starting_id = int(prev_ids[starting_id])
        res.append( (get_coordinates( starting_id // num_x, starting_id % num_x, min_x, min_y, precision)) )
    return res


def get_id(x, y, min_x, min_y, precision):
    row = int(np.floor( (y - min_y) / precision ))
    col = int(np.floor( (x - min_x) / precision ))
    return row, col

def get_coordinates(i,j, min_x, min_y, precision):
    x = min_x + (j+0.5)*precision
    y = min_y + (i+0.5)*precision
    return x,y
