
import pandas as pd
import numpy as np

def load_pc_df():
    """ This is the actual function that gets called"""
    return concentric_layer_for_experiment_0_B()

def concentric_layer_for_experiment_0_B():
    cx, cy = 0.1, 1.2
    dummy_df = pd.DataFrame(columns=['x', 'y', 'r'])
    phase = np.pi/4
    try:
        layer_params = pd.DataFrame(columns=['origin_x', 'origin_y', 'num_cells', 'pc_radius', 'distance', 'phase'],
                                    data=[[0, 0, 1, 0.08, 0, 0],
                                          [0, 0, 4, 0.16, 0.20, 0],
                                          [0, 0, 4, 0.24, 0.44, phase],
                                          [0, 0, 4, 0.32, 0.64, 0],
                                          [0, 0, 4, 0.40, 0.96, phase],
                                          [0, 0, 4, 0.50, 1.12, 0],
                                          [0, 0, 4, 0.56, 1.45, phase],
                                          #[0, 0, 4, 0.64, 1.57, 0],
                                          #[0, 0, 4, 0.72, 1.87, phase],
                                          ])
        generated_layers = [single_concentric_layer(row) for index, row in layer_params.iterrows()]
        concatenated = pd.concat([dummy_df] + generated_layers, ignore_index=True)
        concatenated['x'] = concatenated['x'] + cx
        concatenated['y'] = concatenated['y'] + cy
        filtered = filter_not_in_box(concatenated, -1.1, 1.1, -1.5, 1.5)

        filtered = filtered.drop([13, 14]) # remove cells

        # fill remaining space
        r = 0.64
        a = 0.09
        x, y = 0, -0.4-r
        d = 0.8
        remaining = pd.DataFrame(columns=['x', 'y', 'r'],
                                 data=[[-0.4-a, -0.5, r],
                                       [0.6+a, -0.5, r],
                                       [x-d, y, r],
                                       [x, y, r],
                                       [x+d, y, r],
                                       ]
                                 )

        return pd.concat([filtered, remaining])
    except:
        print("Error in concentric_layer_for_experiment_0_B")
        return dummy_df

def concentric_layer_for_experiment_0_A():

    dummy_df = pd.DataFrame(columns=['x', 'y', 'r'])
    try:
        cx, cy = 0.1, 1.2
        tolerance = 0.0001
        radii = [0.08, 0.16, 0.32, 0.48, 0.7, 1.2]
        cover_radius = [0 for i in range(len(radii))]
        distance = [0 for i in range(len(radii))]
        phase = [0 for i in range(len(radii))]

        for i in range(1,len(radii)):
            cover_radius[i] = distance[i-1] + radii[i-1]
            distance[i] = get_coverage_distance(cover_radius[i], radii[i]) - tolerance
            phase[i] = ((i-1) % 2) * np.pi/8


        layer_params = pd.DataFrame({'origin_x': cx,
                                     'origin_y': cy,
                                     'num_cells': 8,
                                     'pc_radius': radii,
                                     'distance': distance,
                                     'phase': phase})
        generated_layers = [single_concentric_layer(row) for index, row in layer_params.iterrows()]
        concatenated = pd.concat([dummy_df] + generated_layers)
        return filter_not_in_box(concatenated, -1.1, 1.1, -1.5, 1.5)

    except:
        print("Error in concentric_layer_for_experiment_0")
        return dummy_df


def single_concentric_layer(params) -> pd.DataFrame:
    """ This function creates a layer of concentric cell at given distance of a given point.
    :params is a map with expected entries: origin_x, origin_y, distance, phase, num_cells, pc_radius
    """
    angles = np.linspace(0, 2*np.pi, int(params['num_cells'])+1)[0:-1] + params['phase']
    xs = np.cos(angles)*params['distance'] + params['origin_x']
    ys = np.sin(angles)*params['distance'] + params['origin_y']

    return pd.DataFrame({'x': xs, 'y': ys, 'r': params['pc_radius']})



def dummy_demo_pc_df():
    """ This is a dummy for sample purposes"""
    return pd.DataFrame(data=[[0, -0.2, 0.1],
                            [0.1, -0.1, 0.3]],
                        columns=["x", "y", "r"])


def filter_not_in_box(pcs : pd.DataFrame, xmin, xmax, ymin, ymax ) -> pd.DataFrame:
    return pcs[pcs.apply(lambda pc: pc_intersects_rectangle(pc, xmin, xmax, ymin, ymax), axis=1)]


def pc_intersects_rectangle(pc, xmin, xmax, ymin, ymax):

    # take cordinates relative to rectangle center, use abs to reduce symmetrical scenarios
    dx = abs(pc.x - (xmin + xmax)/2)
    dy = abs(pc.y - (ymin + ymax)/2)

    # find signed distance to border of rectangle (notice border is now at half the rectangle distance)
    d_right = dx - (xmax - xmin)/2
    d_top = dy - (ymax - ymin)/2

    # check if circle center outside of rectable + buffer
    if d_right > pc.r or d_top > pc.r:
        return False

    ret_val = d_right <= 0 or d_top <= 0 or d_right*d_right + d_top*d_top <= pc.r*pc.r
    return ret_val

def get_coverage_distance(circle_radius, pc_radius):
    angle = np.pi/8
    sin = np.sin(angle)
    if pc_radius < circle_radius* np.sin(angle):
        print(f"ERROR: can't cover circle of radius {circle_radius} with 8 PCs of size {pc_radius}")
    return circle_radius*np.cos(angle) + np.sqrt(pc_radius*pc_radius - circle_radius*circle_radius*sin*sin)

def get_next_radius(previous_distance, previous_pc_radius):
    angle = np.pi/8
    sin, cos = np.sin(angle), np.cos(angle)

    pc2 = previous_pc_radius*previous_pc_radius
    d2sin2 = previous_distance*previous_distance*sin*sin
    return previous_distance*cos + np.sqrt(pc2 - d2sin2)
