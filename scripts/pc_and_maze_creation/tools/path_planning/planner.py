import os, sys
import astar
from shapely.geometry import Point, LineString
import pandas as pd

# This file finds the shortest path (using euclidean distance) between the goal and the origin
# It assumes obstacles are segments that do not intercept each other.


sys.path.append('../utils')
import MazeParser
from data.Wall import Wall
from data.Feeder import Feeder
from data.StartPos import StartPos

class Node(Point):

    next_id = 0

    def __init__(self, *args, **kwargs):
        super(Node, self).__init__(*args, **kwargs)
        self.neighbors = []
        self.id = self.next_id
        self.next_id += 1

    def add_neighbor(self, node):
        self.neighbors += [node]
        node.neighbors += [self]

    def __hash__(self):
        return hash(id)

def init_map_graph(origin, goal, walls):

    # convert data to nodes:
    origin = Node(origin.x(), origin.y())
    goal = Node(goal.x(), goal.y())

    # generate segments and list of all vertexes:
    starts = [Node(w.x1(), w.y1()) for w in walls]
    ends = [Node(w.x2(), w.y2()) for w in walls]
    all_nodes = [origin, goal] + starts + ends

    # generate line segments
    wall_segments = [ LineString( [starts[i], ends[i]]) for i in range(0, len(starts))]

    # vertexes of same wall are adjacent
    for i in range(0, len(starts)):
        starts[i].add_neighbor(ends[i])


    # 2 vertexes not on the same wall are adjacent if they do not intersect any other wall
    for i in range(0, len(all_nodes)):
        n1 =   all_nodes[i]
        for j in range(i+1 , len(all_nodes)):
            n2 = all_nodes[j]

            segment = LineString([n1, n2])

            intersects_wall = False
            for w in wall_segments:
                if segment.intersects(w):
                    # ignore intersection if is at start or end of segment:
                    if n1.distance(w) > 0.001 and n2.distance(w):
                        intersects_wall = True
                        break

            if not intersects_wall:
                n1.add_neighbor(n2)


    return origin, goal, all_nodes





def find_path(origin, goal, walls):

    origin, goal, all_nodes = init_map_graph(origin, goal, walls)

    path =  astar.find_path(origin, goal, neighbors_fnct=lambda n: n.neighbors, heuristic_cost_estimate_fnct=distance, distance_between_fnct=distance)
    path = [[n.x, n.y] for n in path]
    d = LineString(path).length

    return path, d


def distance(n1, n2):
    return n1.distance(n2)



def generate_maze_metrics(folder):
    results = []
    for filename in os.listdir(folder):
        if filename.endswith(".xml"):
            try:
                print(filename, '', end='')
                full_path = os.path.join(folder, filename)
                walls_aux, feeders_aux, start_positions_aux = MazeParser.parse_maze(full_path)

                walls = [ Wall(float(row['x1']), float(row['y1']), float(row['x2']), float(row['y2']), None) for index, row in walls_aux.iterrows()]
                maze_results = []

                for _, f in feeders_aux.iterrows():
                    goal = Feeder(int(f['fid']), float(f['x']), float(f['y']), None)

                    for pos_id, s in start_positions_aux.iterrows():
                        start = StartPos( float(s['x']), float(s['y']), float(s['w']), None)
                        path, distance = find_path(goal, start, walls)
                        maze_results += [[filename, pos_id, distance]]
                
                results += maze_results        

                print()
            except:
                print('error')
                pass
    results = pd.DataFrame(columns= ['maze','pos','distance'], data = results)
    save_file = os.path.join(folder, 'mazeMetrics.csv')
    results.to_csv(save_file,index=False)
    print('created file ', save_file)

    return results



