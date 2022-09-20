import math, functools, operator, numpy as np, pandas as pd
import os, sys, time, git
from shapely.geometry import Point, LineString
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


PRECISION = 0.001
HASH_SIZE = PRECISION

# Class that implements a hashable, sortable 2D point with float coordinates
class MyPoint:
    def __init__(self,x, y):
        self.x = x
        self.y = y

        self.x_id = int(x/HASH_SIZE)
        self.y_id = int(y/HASH_SIZE)
        self.hash_id = hash((self.x_id, self.y_id))

        self.point = Point(x,y)
        self.lines = set()
        self.sorted_lines = []
        self.id = -1 # user assigned

    def __hash__(self):
        return self.hash_id

    def __eq__(self, other):
        return max(abs(self.x - other.x), abs(self.y - other.y)) < PRECISION

    def __lt__(self,other):
        return self.x_id < other.x_id or (self.x_id == other.x_id and self.y_id < other.y_id)

    def __str__(self):
        return f'({self.x},{self.y})'


    def sort_lines(self, base_angle=0):
        self.sorted_lines = sorted(self.lines, key=lambda l : l.relative_orientation(base_angle))
        return self.sorted_lines , [ l.relative_orientation(base_angle) for l in self.sorted_lines ]


# Class that implements hashable line segments that can store intersections and then split them
# NOTE: we assume that equal points have same hashes which the user must guarantee
class MyLine:
    line_id = 0
    def __init__(self, p1 : MyPoint, p2 : MyPoint):
        self.p1, self.p2 = (p1,p2) if p1 < p2 else (p2,p1)
        self.vertexes = {self.p1,self.p2}
        self.intersections =  {self.p1,self.p2}
        self.line = LineString([self.p1.point, self.p2.point])

        self.dx = self.p2.x - self.p1.x
        self.dy = self.p2.y - self.p1.y
        self.hash_val = hash((self.p1,self.p2))

        self.id = MyLine.line_id # user defined
        MyLine.line_id+=1

        self.polygon_positive = None
        self.polygon_negative = None


        # print('creating: ' , self)
        # print("P1 < P2", p1 < p2, p1.hash_id, p2.hash_id)

    # returns points p1,p2 defining the segment where the lines intersect
    # if they intersect in one point then p1==p2, if no intersections exist, then they return None
    def intersect(self, line2):
        # NOTE: Shapely returns class Point if single intersection, 
        # otherwise it returns a linestring (even if there is no intersection)
        inter = self.line.intersection(line2.line) 
        if isinstance(inter,Point):
            # DO NOT add it to list of intersections, let user handle which intersections are saved
            p =  MyPoint(inter.x, inter.y)
            return p, p
        inter = inter.coords
        if len(inter) == 0:
            return None , None
        return MyPoint(inter[0][0], inter[0][1]) , MyPoint(inter[1][0], inter[1][1])


    # reset the list of stored intersections
    def reset_intersections(self):
        self.intersections = {self.p1, self.p2}


    # split the line along its stored intersections
    def split_line(self):
        slist = sorted(list(self.intersections), key= lambda p : p.x*self.dx + p.y*self.dy )
        return [ MyLine(p1,p2) for (p1,p2) in zip(slist[:-1], slist[1:]) ]

    def __hash__(self):
        return self.hash_val

    def __eq__(self,other):
        # print('HASH: ', hash(self.p1), hash(other.p1), hash(self.p2,), hash(other.p2))
        return self.p1 == other.p1 and self.p2 == other.p2

    def get_orientation(self):
        return math.atan2(self.dy, self.dx)

    def relative_orientation(self, angle):
        return relative_orientation(self.get_orientation(), angle)

    def __str__(self):
        return f'{{{self.id}: {self.p1}-{self.p2}}}'

    def get_other(self, p):
        return self.p2 if self.p1 == p else self.p1

    def sign(self, p):
        return self.dx*p.y-self.dy*p.x

    def add_polygon(self, polygon, next_point):
        if self.sign(next_point) > 0:
            self.polygon_positive = polygon
        else:
            self.polygon_negative = polygon

    def length(self):
        return self.line.length


class MyPolygon:
    def __init__(self, points):
        self.points = points
        self.ids = { p:p_id for p,p_id in zip(points,range(len(points))) }

    def get_next_point(point):
        id = self.ids[point]
        return self.points[ (id+1) % len(self.points) ]

    def get_prev_point(point):
        id = self.ids[point]
        return self.points[ (id+1) % len(self.points) ]

    def data_frame(self):
        return pd.DataFrame(columns=['x','y'], data=[[p.x,p.y] for p in self.points])



class MapVisibility:

    def __init__(self,wall_data = None):
        # create set of points and walls
        if wall_data is None:
            self.all_points = {}
            self.walls = {}
            visibility_lines = set()
            return

        self.all_points = {}
        self.walls = list({MyLine(self.add_point(w.x1, w.y1), self.add_point(w.x2, w.y2)) for id, w in wall_data.iterrows() }) # we first use the set to remove duplicates


        # find all intersections between walls
        for i , wi in zip(range(len(self.walls)-1), self.walls[:-1]):
            for wj in self.walls[i+1:]:
                inter, _ = wi.intersect(wj)  # find intersection
                if inter is None:         # skip if doesnt exist
                    continue

                # add point to map and lists of intersections
                inter = self.add_point(inter.x, inter.y) # add point to map
                wi.intersections.add(inter)
                wj.intersections.add(inter)


        # split each wall on intersections, concat all wall segments, and replace wall set
        self.walls = functools.reduce(operator.concat, [w.split_line() for w in self.walls])

        # add id to each line, and the line to each point
        for w_id, w in zip(range(len(self.walls)), self.walls):
            w.id = w_id
            w.p1.lines.add(w)
            w.p2.lines.add(w)

        # find visibility lines, a segment is visible if it is a wall segment or if there are no mid intersections
        points = list(self.all_points.keys())
        self.visibility_lines = set()
        add_lines = 0
        equality = 0
        for i , pi in zip(range(len(points)-1), points[:-1]):
            for pj in points[i+1:]:

                # find if both points have direct visibility
                l = MyLine(pi,pj)
                only_trivial_intersections = True
                for w in self.walls:
                    # if segment is a wall, it is visible
                    if l == w:
                        equality +=1 
                        l = w
                        break

                    # print("l ", l, "w", w)

                    # if not, check if there are any non trivial intersections
                    # intersection is not trivial if it intersects a full segment
                    # or if they intersect in a single point in the middle of the segment
                    i1, i2 = w.intersect(l)
                    if i1 is not None and ( i1 != i2 or (i1 != pi and i1 != pj) ):
                        only_trivial_intersections = False
                        break

                # if there were no non_trivial_intersectinos, the line is a visibility line
                if only_trivial_intersections:
                    add_lines +=1
                    self.visibility_lines.add(l)
                    pi.lines.add(l)
                    pj.lines.add(l)
        # print("TOTAL POINTS: ", len(points))
        # print("TOTAL VISIBIL: " , len(self.visibility_lines))
        # print("EQUALITY: ",equality)
        # print("TOTAL WALL SEGMENTS: ", len(self.walls))

        # for each point sort lines:
        for p in self.all_points.keys():
            p.sort_lines()

        # for each point , sort the lines according to their angle:



    def add_point(self,x,y):
        # first check if point has already been added
        p = self.get_point(x,y)
        if p is None:
            p = MyPoint(x,y)
            self.all_points[p] = p
        return p

    def get_point(self, x, y, missing=None):
        # check if point has already been added
        # we consider two points to be the same if they differ by at most PRECISION
        # also, points are hashed based on precision, so I need to check contiguous hash values
        for dx in range(-1,2):
            for dy in range(-1,2):
                p = MyPoint(x+dx*PRECISION, y+dy*PRECISION)

                # check if there is a point in nearby hash values
                # if there is, check the point is the same
                if p in self.all_points and self.all_points[p] == p:
                    # return the point found
                    return self.all_points[p]

        # if point not found, return None
        return missing

    def get_alias(self, point):
        return self.get_point(point.x, point.y, missing = point)

    def save(self, file_name):
        # saves the visibility information in the following format:
        # num_points; points ; num_segments ; segments ; num_wall_segments ; 
        # wall_segment ; (for each vertex p : p.num_segments ; p.segments)


        # get points, visibility segments and wall segments
        points = list(self.all_points.keys())
        vsegments = list(self.visibility_lines)
        wsegments = list(self.walls)



        for p_id, p in zip(range(len(points)), points):
            p.id = p_id

        for v_id, v in zip(range(len(vsegments)), vsegments):
            v.id = v_id

        with open(file_name, 'bw') as f:

            # store number of points and points:
            np.array([len(points)]).astype(np.float32).tofile(f)
            data = np.array([ [p.x,p.y] for p in points])
            data.reshape(-1).astype(np.float32).tofile(f)


            # store num segments and segments , each segment is a pair point ids:
            np.array([len(vsegments)]).astype(np.float32).tofile(f)
            np.array([ [v.p1.id, v.p2.id] for v in vsegments]).reshape(-1).astype(np.float32).tofile(f)

            # store the number of walls and the wall ids:
            np.array([len(wsegments)]).astype(np.float32).tofile(f)
            np.array([ w.id for w in wsegments]).astype(np.float32).tofile(f)

    def load(file_name):
        vmap = MapVisibility()
        with open(file_name, 'rb') as f:
            num_points = np.fromfile(f,np.float32, 1)
            points = [ vmap.add_point(x,y) for x,y in  np.fromfile(f,np.float32, 2*int(num_points)).reshape(-1,2) ]
            # for p in points:
            #     print(p)

            num_vsegments = np.fromfile(f, np.float32, 1)
            seg_ids = [ (int(id1), int(id2)) for id1, id2 in np.fromfile(f,np.float32, 2*int(num_vsegments)).reshape(-1,2) ]
            def creat_line(id1,id2):
                p1 = points[id1]
                p2 = points[id2]
                l = MyLine(p1,p2)
                p1.lines.add(l)
                p2.lines.add(l)
                return l
            vlines = [ creat_line(id1,id2) for id1, id2 in seg_ids]
            vmap.visibility_lines = vlines

            num_wsegments = np.fromfile(f, np.float32, 1)
            wsegments = [ vlines[int(id1)] for id1 in np.fromfile(f,np.float32, int(num_wsegments))]
            vmap.walls = wsegments

            for p in points:
                p.sort_lines()


        return vmap


    def plot(self,  plot):
            
        wall_df = pd.DataFrame(columns=['x1','y1','x2','y2'], data = [[w.p1.x, w.p1.y, w.p2.x, w.p2.y] for w in self.walls])
        visibility_df = pd.DataFrame(columns=['x1','y1','x2','y2'], data = [[w.p1.x, w.p1.y, w.p2.x, w.p2.y] for w in self.visibility_lines if w not in self.walls])
        
        # plot walls
        plot += geom_segment(aes(x='x1', y='y1', xend='x2', yend='y2'), data=wall_df, color='k', size=2)
        plot += geom_segment(aes(x='x1', y='y1', xend='x2', yend='y2'), data=visibility_df, color='r', size=0.1)
        # plot += geom_point(aes(x='x', y='y'), data=feeders, color='r', size=4)
        # plot += geom_point(aes(x='x', y='y'), data=start_positions, color='g', size=4)

        # ADD THEMES TO PLOT
        plot += coord_fixed(ratio = 1)
        plot += theme_void()
        
        return plot

    def generate_polygons(self):

        polygons = []
        line_hash = {(v.p1,v.p2):v for v in self.visibility_lines}
        for v in self.visibility_lines:
            line_hash[(v.p2,v.p1)] = v
        init_segment = self.visibility_lines[0]                 # segment to start creating the graph
        discovered = [(init_segment.p1, init_segment.p2)]       # segments that need processing
        discovered_hash = {(init_segment.p1, init_segment.p2)}  # has of discovered elements
        completed   = set()                                     # set of oriented segments that should no longer be checked
        added_lines = set()                                     # set of lines included in the polygons

        # process next
        times = 0
        while len(discovered) > 0 and times < 500:
            (p1, p2) = discovered.pop(0)
            discovered_hash.remove((p1,p2))
            if (p1,p2) in completed:
                continue
            completed.add((p1,p2))

            # angle = point_orientation(p1,p2)
            # get p3 so that p1 p3 and p2 p3 are visibility lines
            all_adjacent = [ l.get_other(p2) for l in p2.lines  if not line_intersects_any(l, added_lines)]
            all_adjacent = [ p for p in all_adjacent if p != p1 and (p2,p) not in completed and (p,p1) not in completed and not line_intersects_any(MyLine(p,p1),added_lines)]
            all_adjacent = sorted(all_adjacent, key = lambda p : relative_angle(p1,p2,p))

            possible = [ p for p in all_adjacent if (p1, p) in line_hash ]

            # adjacent_ideal = [p for p in possible if relative_angle(p1,p2,p) < np.pi - np.radians(5)]
            # if len(adjacent_ideal) == 0:
            #     continue
            # p3 = adjacent_ideal[-1]
            # angle = relative_angle(p1,p2, p3 )

            # if True:#angle <= 0:
            if len(possible) == 0:
                continue
            p3 = possible[-1]
            angle = relative_angle(p1,p2, p3 )
            

            if times==118:
                print(p1,p2,p3, angle)

            if angle > 0 :
                polygon = MyPolygon([p1, p2, p3])
                polygons.append(polygon)
                added_lines.add(MyLine(p1,p2))
                added_lines.add(MyLine(p2,p3))
                added_lines.add(MyLine(p3,p1))

                if (p3, p2) not in discovered_hash and (p3,p2) not in completed:
                    discovered_hash.add((p3,p2))
                    discovered.append((p3,p2))
                if (p1, p3) not in discovered_hash and (p1, p3) not in completed:
                    discovered_hash.add((p1,p3))
                    discovered.append((p1,p3))
                if (p2, p1) not in discovered_hash and (p2, p1) not in completed:
                    discovered_hash.add((p2,p1))
                    discovered.append((p2,p1))

                mark_completed_segments(p1,p2,p3,completed)
                mark_completed_segments(p2,p3,p1,completed)
                mark_completed_segments(p3,p1,p2,completed)

            # if times == 58:
            #     print(discovered)
            #     print()
            times +=1
        


        return [poly.data_frame() for poly in polygons], None

    def generate_polygons2(self):



        # SORT visibility lines by length:
        sorted_lines = sorted(self.visibility_lines, key=lambda l : l.length())

        # FIRST ADD ALL WALLS, then add:
        added_lines = {w for w in self.walls}
        for l in sorted_lines:
            if not line_intersects_any(l,added_lines):
                added_lines.add(l)
        
        # find which lines were used for each point
        point_to_lines = { p:set() for p in self.all_points}
        for l in added_lines:
            point_to_lines[self.get_alias(l.p1)].add(l)
            point_to_lines[self.get_alias(l.p2)].add(l)

        # generate triangles
        polygons = []
        processed = set()

        def process_oriented_segment(p1, p2, processed, triangles, point_to_lines):
            if (p1, p2) in processed:
                return

            p3_candidates = [ l.get_other(p2) for l in point_to_lines[self.get_alias(p2)]]
            p3_candidates.remove(p1)
            p3_candidates = [ p for p in p3_candidates if MyLine(p,p1) in added_lines]
            p3_candidates =  sorted(p3_candidates, key = lambda p : relative_angle(p1,p2,p))

            p3 = None if len(p3_candidates) == 0 else p3_candidates[-1]

            if p3 is not None and relative_angle(p1,p2,p3) > 0:
                processed.update({(p1,p2),(p2,p3),(p3,p1)})
                triangles.append(MyPolygon([p1, p2, p3]))
            else:
                processed.update({(p1,p2)})

        for i, line in zip(range(len(added_lines)),added_lines):
            process_oriented_segment(line.p1,line.p2,processed,polygons, point_to_lines)


        a = len(added_lines)
        p = len(polygons)
        print("num lines: ", a, "polys", p, "Verif (2a-4)/3 == p", (a*2-4)/3, p )
        lines_df = pd.DataFrame(columns=['x1','y1','x2','y2'], data=[[l.p1.x, l.p1.y, l.p2.x, l.p2.y] for l in added_lines])
        return [poly.data_frame() for poly in polygons], lines_df


def mark_completed_segments(p1,p2,p3, completed):
    all_adjacent = [ l.get_other(p2) for l in p2.lines if l.get_other(p2) != p1]
    all_adjacent = sorted(all_adjacent, key = lambda p : relative_angle(p1,p2,p))
    angles = [relative_angle(p1,p2,p) for p in all_adjacent]
    min_id = all_adjacent.index(p3)+1
    for p in all_adjacent[min_id:]:
        if relative_angle(p1,p2,p) > 0:
            completed.add((p2,p))
            completed.add((p,p2))



# checks for non trivial intersections, intersections resulting in segments are ignored
def line_intersects_any(line, line_set):
    for l in line_set:
        p1 , p2  = line.intersect(l)
        if  p1 is not None and p1 == p2 and  p1 != line.p1 and p1 != line.p2:
            return True
    return False

def filter_intersecting_lines(lines, intersections):
    return [ l for l in lines if not line_intersects_any(l,intersections)]

def load_visibility_map(file):
    return MapVisibility.load(file)

def map_visibility_from_pickles(wall_pickles):
    walls = pd.DataFrame(columns=['x1','y1','x2','y2'],  data=[ [w.x1(), w.y1(), w.x2(), w.y2()] for w in wall_pickles])
    return MapVisibility(walls)


def map_visibility_from_file(folder, maze_file):
    print('Mapping visibility in ', maze_file)
    full_path = os.path.join(folder, maze_file)
    walls, feeders, start_positions = MazeParser.parse_maze(full_path)
    visibility = MapVisibility(walls)

    save_name = full_path.replace('.xml', '_visibility_map.bin')
    print('Saving ', save_name)
    visibility.save(save_name)

    plot_name = full_path.replace('.xml', '_visibility_map.png')
    p = visibility.plot(ggplot())
    ggsave(p, plot_name, dpi=300, verbose = False)
    return ''


pool = None
def map_visibility(folder):
    debug = True
    if debug:
        map_visibility_from_file('tools/samples', 'M304.xml')
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


def relative_angle(x1, x2, x3):
    dx = x2.x - x1.x
    dy = x2.y - x1.y

    dx3 = x3.x - x2.x
    dy3 = x3.y - x2.y
    return relative_orientation(math.atan2(dy3,dx3), math.atan2(dy,dx))


def height(p1, p2, p3):
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    return dx*(p3.y-p1.y) - dy*(p3.x-p1.x)

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



def relative_orientation( angle, base_angle):
    diff = angle - base_angle
    if diff <= -np.pi:
        return diff + 2*np.pi
    if diff > np.pi:
        return diff - 2*np.pi
    return diff

def point_orientation(origin, destination):
    dx = destination.x - origin.x
    dy = destination.y - origin.y
    return math.atan2(dy,dx)
