import os, sys, pandas as pd, numpy as np
from pandas.api.types import CategoricalDtype
from plotnine import *

sys.path.append('../utils')
import MazeParser

def plot_file(maze_file_path):
    print('plotting', maze_file_path)

    distance_file = maze_file_path.replace('.xml', '_subgoal_distances.bin')
    save_name = maze_file_path.replace('.xml', '_subgoal_distances.png')

    p = ggplot()
        
    # If maze file is not none and it has distance file, plot distance heatmap first
    if os.path.exists(distance_file):
        with open(distance_file,'rb') as f:
            [min_x, num_x, min_y, num_y, precision] = np.fromfile(f, np.float32, 5)
            distances = np.fromfile(f, np.float32, int(num_x*num_y))
            distances[ distances == 10000 ] = -0.1
            # prev_ids = np.fromfile(f, np.float32, int(num_x*num_y))
            [ys, xs] = np.mgrid[0:num_y,0:num_x].reshape(2,-1)
            xs = xs*precision + min_x
            ys = ys*precision + min_y
            distance_df = pd.DataFrame({'x':xs,'y':ys,'d':distances})
            p += geom_tile(aes(x='x',y='y',fill='d'), data=distance_df)
    else:
        print(f'plot_subgoal_distances.py: distance file deos not exist! {distance_file}')
    
    
    walls, feeders, start_positions = MazeParser.parse_maze(maze_file_path)
    p += geom_segment(aes(x='x1', y='y1', xend='x2', yend='y2'), data=walls, color='k', size=1.5)
    p += geom_point(aes(x='x', y='y'), data=feeders, color='r', size=4)
    p += geom_point(aes(x='x', y='y'), data=start_positions, color='g', size=4)
        
    # ADD THEMES TO PLOT
    p += coord_fixed(ratio = 1)
    p += theme_void()
    
    ggsave(p, save_name, dpi=300, verbose = False)
