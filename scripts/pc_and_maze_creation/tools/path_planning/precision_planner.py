import os, sys, time
import astar
from shapely.geometry import Point, LineString
import pandas as pd
import math
from multiprocessing import Pool


# This file finds the shortest path between the goal and the origin considering the actions the robot can make on each time step
# Contrary to the regular planner, this planner is a much more precise approximation.
# Note, here we consider two nodes to be equal if they
# It assumes obstacles are segments that do not intercept each other.


sys.path.append('../utils')
import MazeParser
from data.Wall import PickableWall as Wall
from data.Feeder import PickableFeeder as Feeder
from data.StartPos import PickableStartPos as StartPos

ROBOT_STEP = 0.08
FEEDING_DISTANCE = 0.1
AFFORDANCE_DISTANCE = 0.1
NUM_ACTIONS = 8

DELTA_ANGLE = 2*math.pi / NUM_ACTIONS
ANGLES = [DELTA_ANGLE*i for i in range(NUM_ACTIONS)]
DELTA_XY = [[ROBOT_STEP*math.cos(theta), ROBOT_STEP*math.sin(theta)] for theta in ANGLES]
EXTENDED_XY = [[AFFORDANCE_DISTANCE*math.cos(theta), AFFORDANCE_DISTANCE*math.sin(theta)] for theta in ANGLES]

pool = None


class Node(Point):

    next_id = 0

    def __init__(self, graph_nodes, wall_segments, *args, **kwargs):
        super(Node, self).__init__(*args, **kwargs)

        self.wall_segments = wall_segments
        self.neighbors = None

        self.id = self.next_id
        self.next_id += 1
        self.graph_nodes = graph_nodes

    def get_neigbors(self):
        if self.neighbors is None:
            self.find_neighbors()

        # print(f'NEGH of {str(self)}: ', [str(n) for n in self.neighbors])
        return self.neighbors

    def find_neighbors(self):
        candidates = [Node( self.graph_nodes, self.wall_segments, self.x + xy[0], self.y + xy[1]) for xy in DELTA_XY ]
        extended   = [Point( self.x + xy[0], self.y + xy[1]) for xy in EXTENDED_XY ]

        self.neighbors = [n.alias() for (n,e) in zip(candidates, extended) if self.is_reachable(e)]


    def is_reachable(self, point):
        segment = LineString([self, point])
        for w in self.wall_segments:
            if segment.distance(w) < 0.00142: # require wall at least sqrt(2) mm away from segment (motion line)
                return False
        return True

    def __hash__(self):
        return hash(id)

    def __str__(self):
        return f'({self.x:.2f}, {self.y:.2f})'

    def alias(self):
        id1 = round(self.x * 1000)
        id2 = round(self.y * 1000)

        if id1 not in self.graph_nodes:
            self.graph_nodes[id1] = {id2:self}
            return self

        id1_nodes = self.graph_nodes[id1]
        if id2 not in id1_nodes:
            id1_nodes[id2] = self
            return self

        return  id1_nodes[id2]




def wall_to_line_string(w):
    p1 = Point(w.x1(), w.y1())
    p2 = Point(w.x2(), w.y2())
    return LineString([p1, p2])

def init_map_graph(origin, goal, walls):
    # global MIN_DISTANCE
    # MIN_DISTANCE = 3
    # convert data to nodes:
    wall_segments = [ wall_to_line_string(w) for w in walls]
    graph_nodes = {} 
    origin = Node(graph_nodes, wall_segments, origin.x(), origin.y())
    goal = Node(graph_nodes, wall_segments, goal.x(), goal.y())

    origin.alias() # this adds the origin to the graph nodes
    return origin, goal, wall_segments


# def fin_path_single_arg(data):
#     print('DATA' , data)
#     find_path(data[0], data[1], data[2])

def find_path(id, origin, goal, walls):

    start_time = time.time()

    origin, goal, wall_segments = init_map_graph(origin, goal, walls)


    path =  astar.find_path(origin, goal, 
        neighbors_fnct=lambda n: n.get_neigbors(), 
        heuristic_cost_estimate_fnct=distance, 
        distance_between_fnct=distance,
        is_goal_reached_fnct=is_goal_reached_fnct
        )
    

    path = [[n.x, n.y] for n in path]
    d = LineString(path).length
    # print("path: ", origin, path[0][0], path[0][1], len(path), d)

    print(f'Path {id} found in {time.time() - start_time : 0.2f} seconds with {len(path)} steps and {d:.2f} m')

    return path, d


def distance(n1, n2):
    return n1.distance(n2)

def under_estimation(n1, n2):
    dx = abs(math.abn1.x - n2.x)
    dy = abs(n1.y - n2.y)
    return max( 0, sqrt(2)*min(dx,dy) + abs(dx-dy) - FEEDING_DISTANCE)

def is_goal_reached_fnct(node, goal):
    d = node.distance(goal)
    reached =  d < FEEDING_DISTANCE and node.is_reachable(goal)
    return reached

def generate_maze_metrics(folder):
    global pool, filenames, positions, result_file_name, start_time
    if(pool is not None):
        print("PROCESS POOL ALREADY OPEN")
        return

    results = []

    args = []
    filenames = []
    positions = []
    for filename in os.listdir(folder):
        if filename.endswith(".xml"):
            try:
                print(filename, '', end='')
                full_path = os.path.join(folder, filename)
                walls_aux, feeders_aux, start_positions_aux = MazeParser.parse_maze(full_path)

                walls = [ Wall(float(row['x1']), float(row['y1']), float(row['x2']), float(row['y2'])) for index, row in walls_aux.iterrows()]
                goals = [ Feeder(int(f['fid']), float(f['x']), float(f['y'])) for _, f in feeders_aux.iterrows() ]
                starts = [ (id, StartPos( float(s['x']), float(s['y']), float(s['w']) )) for id , s in start_positions_aux.iterrows() ]

                args += [(s , g, walls) for g in goals for (id,s) in starts ]
                filenames += [ filename for g in goals for (id,s) in starts ]
                positions += [ id       for g in goals for (id,s) in starts ]     

            except:
                print('error')
                pass
    print()
    args = [ (i,) + a for (i,a) in zip(range(len(args)), args) ]
    result_file_name = os.path.join(folder, 'mazeMetrics.csv')
    pool = Pool(12)
    start_time = time.time()
    pool.starmap_async(find_path, args, callback=save_maze_metrics)




def save_maze_metrics(results):
    global pool, filenames, positions
    time_lapse = time.time() - start_time
    paths = [ path for (path, distance) in results]
    distances = [ distance for (path, distance) in results ]
    steps = [ len(p)-1 for p in paths]

    # generate dataframe and save results to file
    results_df = pd.DataFrame({'maze' : filenames, 'pos' : positions, 'steps' : steps, 'distance' : distances, 'path':paths}) # !!!!! HERE WE ASSUME ONLY ONE GOAL!!!!
    results_df.to_csv(result_file_name,index=False)
    print('created file ', result_file_name)
    print('Total ellapsed time: ', time_lapse)

    pool.terminate()
    pool = None
