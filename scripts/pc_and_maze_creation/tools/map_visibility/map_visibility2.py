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
PRECISION = 0.01 # precision to be used for tesselating the space


# Find visibility polygons from all cell centers in a tesselation of the maze
def find_all_visibility_polygons(walls, precision):
    min_x, num_x, min_y, num_y = get_grid_and_coordinates(walls, PRECISION)
    all_polygons = [ [ find_visibility_polygon(walls, min_x + PRECISION * (j+0.5), min_y + PRECISION * (i+0.5),PRECISION) for j in range(num_x)] for i in range(num_y)]
    return min_x, num_x, min_y, num_y, all_polygons

# Find the visibility polygon from position (cx, cy)
def find_visibility_polygon(walls, cx, cy, precision):
    # Get bounding polygon, then cull remove a culling polygon generated from each wall
    visibility = OUTTER_POLYGON
    c  = np.array([cx,cy]) # center
    for w_id, w in walls.iterrows():
        p1, p1prime = expand(w.x1, w.y1, c, MAXLENGTH)
        p2, p2prime = expand(w.x2, w.y2, c, MAXLENGTH)
        if LineString([p1,p2]).distance(Point(c)) < precision:
            return w_id
        try:
            cull_polygon = Polygon( [ p1, p1prime, p2prime, p2 ] )
            visibility = visibility.difference(cull_polygon)
        except:
            pass

    # remove artifacts by contracting and then dilating
    visibility = visibility.buffer(-0.002).buffer(0.002)

    # if instance of multipolygon - only keep polygon that contains center
    if isinstance(visibility,MultiPolygon):
        for p in visibility:
            if p.contains(Point(c)):
                visibility = p
                break

    visibility = visibility.simplify(0.005)



    return visibility

# Extend point so that it lies outside the boundary
def expand(x,y, center, length):
    p = np.array([x,y])
    dp = p-center
    size = np.linalg.norm(dp)
    return p, center + dp*(length/size) if size > 0 else p

# return the data representing the tesselated maze
def get_grid_and_coordinates(walls, precision):
    min_x = np.min([walls.x1.min(), walls.x2.min()]) - precision/2
    max_x = np.max([walls.x1.max(), walls.x2.max()]) + precision/2
    min_y = np.min([walls.y1.min(), walls.y2.min()]) - precision/2
    max_y = np.max([walls.y1.max(), walls.y2.max()]) + precision/2

    num_x = int(np.ceil((max_x - min_x)/precision))
    num_y = int(np.ceil((max_y - min_y)/precision))
    
    return min_x, num_x, min_y, num_y




def save(file_name, min_x, num_x, min_y, num_y, all_polygons, walls, precision):

    remaining = 5
    with open(file_name, 'bw') as f:

        # store grid information:
        np.array( [ min_x, num_x, min_y, num_y, precision ] ).astype(np.float32).tofile(f)

        for i in range(num_y):
            for j in range(num_x):
                # get polygon, for each polygon store the number of points followed by the points
                if isinstance(all_polygons[i][j], Polygon):
                    polygon = np.array( all_polygons[i][j].exterior )
                    polygon = polygon[:-1] # last point is the same as first point, thus remove it
                    np.array([len(polygon)]).astype(np.float32).tofile(f)
                    polygon.reshape(-1).astype(np.float32).tofile(f)
                    if remaining > 0:
                        print("Polygon: " , len(polygon), '\n', polygon)
                        remaining-=1
                else:
                    # if it is not a polygon, then grid i,j is within precision of an obstacle and it stores the id of the obstacle
                    # get obstacle and compute normalized vector of length 'precision'
                    w_id = all_polygons[i][j]
                    w = walls.iloc[w_id].to_numpy()

                    delta = w[2:] - w[:2]
                    length = np.linalg.norm(delta)
                    delta = delta * (precision / length)


                    # in the file, set length as 0 (to indicate it is not a polygon) then save perpendicular vector of length precision and the value of the point times the vector
                    np.array( [ 0 , -delta[1], delta[0], delta[0]*w[1] - delta[1]*w[0] ]).astype(np.float32).tofile(f)



# plots missing polygons for debugging
def plot_missing_polygons( walls, min_x, num_x, min_y, num_y, all_polygons, precision, plot = None):
    missing = [ (min_x + precision * (j+0.5), min_y + precision * (i+0.5)) for j in range(num_x) for i in range(num_y) if not isinstance(all_polygons[i][j], Polygon)]

    plot = plot if plot is not None else ggplot()
    # plot maze
    plot += geom_segment(aes(x='x1', y='y1', xend='x2', yend='y2'), data=walls, color='k', size=1.5)
    # plot += geom_point(aes(x='x', y='y'), data=feeders, color='r', size=4)
    # plot += geom_point(aes(x='x', y='y'), data=start_positions, color='g', size=4)

    # plot missing polygons
    plot += geom_point(aes(x='x', y='y'), data=pd.DataFrame({'x':[x for (x,y) in missing], 'y':[y for (x,y) in missing]}), color='b', size=0.2)
        
    # ADD THEMES TO PLOT
    plot += coord_fixed(ratio = 1)
    plot += theme_void()
    return plot
    


def map_visibility_from_pickles(wall_pickles):
    walls = pd.DataFrame(columns=['x1','y1','x2','y2'],  data=[ [w.x1(), w.y1(), w.x2(), w.y2()] for w in wall_pickles])
    min_x, num_x, min_y, num_y, all_polygons = find_all_visibility_polygons(walls, PRECISION)
    return min_x, num_x, min_y, num_y, all_polygons


def map_visibility_from_file(folder, maze_file):
    print('Mapping visibility in ', maze_file)
    full_path = os.path.join(folder, maze_file)
    walls, feeders, start_positions = MazeParser.parse_maze(full_path)
    
    # FIND POLYGONS
    min_x, num_x, min_y, num_y, all_polygons = find_all_visibility_polygons(walls, PRECISION)
    
    # SAVE POLYGONS
    save_name = full_path.replace('.xml', '_visibility_map.bin')
    print('Saving ', save_name)
    save(save_name, min_x, num_x, min_y, num_y, all_polygons, walls, PRECISION)

    # PLOT MISSING POLYGONS TO CHECK FOR ERRORS
    plot_name = full_path.replace('.xml', '_missing_visibility_polygons.png')
    plot = plot_missing_polygons(walls, min_x, num_x, min_y, num_y, all_polygons, PRECISION,ggplot())
    ggsave(plot, plot_name, dpi=300, verbose = False)
    print('Done with: ', maze_file)
    return ''


pool = None
def map_visibility(folder):
    debug = False
    if debug:
        map_visibility_from_file('tools/samples', 'M4.xml')
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
        pool.starmap_async(map_visibility_from_file, args, callback=finished_all_files)


def finished_all_files(results):
    global pool
    print('finished mapping visibility in all mazes!')
    pool.close()
    pool = None
    errors = [r for r in results if r!='']
    if(len(errors)>0):
        print('Error with files: {errors}')
    else:
        print('No errors!')


# def relative_angle(x1, x2, x3):
#     dx = x2.x - x1.x
#     dy = x2.y - x1.y

#     dx3 = x3.x - x2.x
#     dy3 = x3.y - x2.y
#     return relative_orientation(math.atan2(dy3,dx3), math.atan2(dy,dx))


# def height(p1, p2, p3):
#     dx = p2.x - p1.x
#     dy = p2.y - p1.y
#     return dx*(p3.y-p1.y) - dy*(p3.x-p1.x)

# def relative_orientation( angle, base_angle):
#     diff = angle - base_angle
#     if diff <= -np.pi:
#         return diff + 2*np.pi
#     if diff > np.pi:
#         return diff - 2*np.pi
#     return diff

# def point_orientation(origin, destination):
#     dx = destination.x - origin.x
#     dy = destination.y - origin.y
#     return math.atan2(dy,dx)
