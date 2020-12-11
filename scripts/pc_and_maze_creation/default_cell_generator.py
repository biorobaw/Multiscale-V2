
import pandas as pd
import numpy as np

def load_pc_df():
    """ This is the actual function that gets called"""
    return concentric_layer_for_maze_1_A()

def concentric_layer_for_maze_1_A():
    goal_x, goal_y = 0.1, 1.2
    gap_x, gap_y = 0.575, -0.12
    dummy_df = pd.DataFrame(columns=['x', 'y', 'r'])
    phase = np.pi/4
    try:

        """ place cells below gap """

        layer_params_gap = pd.DataFrame(
            columns=['origin_x', 'origin_y', 'num_cells', 'pc_radius', 'distance', 'phase'],
            data=[[0, 0, 1, 0.16, 0, 0],
                  [0, 0, 4, 0.25, 0.31, 0],
                  [0, 0, 4, 0.32, 0.61, phase],
                  [0, 0, 4, 0.48, 0.98, 0],
                  [0, 0, 4, 0.56, 1.33, phase],
                  # [0, 0, 4, 0.56, 1.53, 0],
                  # [0, 0, 4, 0.56, 1.45, phase],
                  # [0, 0, 4, 0.64, 1.57, 0],
                  # [0, 0, 4, 0.72, 1.87, phase],
                  ])
        layers_gap = [single_concentric_layer(row) for index, row in layer_params_gap.iterrows()]
        pcs_gap = pd.concat([dummy_df] + layers_gap, ignore_index=True)
        pcs_gap['x'] = pcs_gap['x'] + gap_x
        pcs_gap['y'] = pcs_gap['y'] + gap_y
        pcs_gap = filter_not_in_box(pcs_gap, -1.1, 1.1, -1.5, 0)
        pcs_gap = pcs_gap.drop([2, 5, 6, 9]) # remove cells
        pcs_gap = pcs_gap.reset_index(drop=True)

        pcs_gap.y[3] -= 0.02

        pcs_gap.y[6] -= 0.12
        pcs_gap.x[6] += 0.20
        pcs_gap.r[6]  = 0.4

        pcs_gap.x[8] += 0.28
        pcs_gap.y[8] -= 0.06
        pcs_gap.r[8] = 0.56

        pcs_gap.x[9] -= 0.45
        pcs_gap.y[9] -= 0.15
        pcs_gap.r[9] = 0.4


        pcs_gap.loc[len(pcs_gap)] = (-0.75, -0.4, 0.56)
        pcs_gap.loc[len(pcs_gap)] = (-0.75, -1.15, 0.56)

        print(pcs_gap)

        """ place cells above gap """

        pcs_gap_above = pcs_gap.copy()
        pcs_gap_above.y = -pcs_gap_above.y
        pcs_gap_above = pcs_gap_above.drop(list(range(6, 12)))
        pcs_gap_above = pcs_gap_above.drop([4])


        """ place cells around goal """

        layer_params_goal = pd.DataFrame(
            columns=['origin_x', 'origin_y', 'num_cells', 'pc_radius', 'distance', 'phase'],
            data=[[0, 0, 1, 0.08, 0, 0],
                  [0, 0, 4, 0.16, 0.20, 0],
                  [0, 0, 4, 0.24, 0.44, phase],
                  [0, 0, 4, 0.32, 0.64, 0],
                  [0, 0, 4, 0.40, 0.96, phase],
                  [0, 0, 4, 0.50, 1.12, 0],
                  [0, 0, 4, 0.56, 1.45, phase]
                  ])
        layers_goal = [single_concentric_layer(row) for index, row in layer_params_goal.iterrows()]
        pcs_goal = pd.concat([dummy_df] + layers_goal, ignore_index=True)
        pcs_goal['x'] = pcs_goal['x'] + goal_x
        pcs_goal['y'] = pcs_goal['y'] + goal_y
        pcs_goal = filter_not_in_box(pcs_goal, -1.1, 1.1, -1.5, 1.5)

        print(pcs_goal)
        pcs_goal = pcs_goal.drop([12, 13, 15 , 20]) # remove cells
        pcs_goal = pcs_goal.reset_index(drop=True)

        pcs_goal.r[4] += 0.02
        pcs_goal.r[1] = pcs_goal.r[4]
        pcs_goal.y[1] -= 0.02
        pcs_goal.x[1] += 0.02

        pcs_goal.y[4] -= 0.03
        pcs_goal.x[4] += 0.02


        pcs_goal.r[8] = 0.32
        pcs_goal.x[8] += 0.15
        pcs_goal.y[8] -= 0.05

        pcs_goal.r[12] -= 0.08
        pcs_goal.x[12] += 0.12
        pcs_goal.y[12] += 0.12

        pcs_goal.r[13] -= 0.12
        pcs_goal.x[13] -= 0.18
        pcs_goal.y[13] -= 0.02

        pcs_goal.r[14] = 0.44
        pcs_goal.x[14] += 0.09
        pcs_goal.y[14] -= 0.03

        pcs_goal.r[15] = 0.36
        pcs_goal.x[15] -= 0.30
        pcs_goal.y[15] += 0.13

        pcs_goal.r[16] = 0.52
        pcs_goal.x[16] += 0.1
        pcs_goal.y[16] += 0.15


        """ concat all pcs and then filter out """
        # pcs_gap = dummy_df
        # pcs_gap_above = dummy_df


        pcs_all = pd.concat([pcs_goal, pcs_gap_above, pcs_gap], ignore_index=True)

        # upper half first layer (closest to gap)
        pcs_all.loc[len(pcs_all)] = [-0.89, 0.43, 0.48]
        pcs_all.loc[len(pcs_all)] = [-0.49, 0.35, 0.4]
        pcs_all.loc[16] = [-0.15, 0.28, 0.32]
        pcs_all.loc[15] = [0.12, 0.22, 0.25]
        pcs_all.loc[19] = [0.35, 0.16, 0.20]
        pcs_all.loc[17] = [0.575, 0.12, 0.16]  # <--- gap
        pcs_all.loc[len(pcs_all)] = [0.80, 0.16, 0.20]
        pcs_all.loc[18] = [1.03, 0.22, 0.25]

        # upper half second layer

        pcs_all.loc[11] = [0.13, 0.59, 0.32]


        # lower half first layer (closest to gap)

        pcs_all.loc[len(pcs_all)] = [-0.89, -0.43, 0.48]
        pcs_all.loc[32] = [-0.49, -0.35, 0.4]
        pcs_all.loc[28] = [-0.15, -0.28, 0.32]
        pcs_all.loc[24] = [0.12, -0.22, 0.25]
        pcs_all.loc[22] = [0.35, -0.16, 0.20]
        pcs_all.loc[len(pcs_all)] = [0.575, -0.12, 0.16]  # <--- gap
        pcs_all.loc[len(pcs_all)] = [0.80, -0.16, 0.20]
        pcs_all.loc[23] = [1.03, -0.22, 0.25]



        # second layer of lower half

        d = 0.10
        pcs_all.loc[33] = [-0.88, -1.33, 0.56]
        pcs_all.loc[30] = [-0.20, -1.07, 0.56]
        pcs_all.loc[26] = [0.25,  -0.72, 0.40]
        pcs_all.loc[25] = [0.575, -0.40, 0.25]  # <--- aligned with gap
        pcs_all.loc[27] = [0.9,   -0.72, 0.40]

        # third layer of lower half

        pcs_all.loc[29] = [0.5750, -1.3, 0.48] # <-- aligned with gap
        pcs_all.loc[31] = [1.16, -1.28, 0.4]

        # pcs_all.loc[len(pcs_all)] = [0.425, -0.06, 0.08]
        # pcs_all.loc[len(pcs_all)] = [0.095, -0.06, 0.08]
        # pcs_all.loc[len(pcs_all)] = [-0.35, -0.1, 0.12]
        # pcs_all.loc[len(pcs_all)] = [-1, -0.1, 0.12]

        return pcs_all
    except:
        print("Error in concentric_layer_for_experiment_0_B")
        return dummy_df


def concentric_layer_for_maze_1_B():
    goal_x, goal_y = 0.1, 1.2
    gap_x, gap_y = 0.575, -0.12
    dummy_df = pd.DataFrame(columns=['x', 'y', 'r'])
    phase = np.pi/4
    try:

        """ place cells below gap """

        layer_params_gap = pd.DataFrame(
            columns=['origin_x', 'origin_y', 'num_cells', 'pc_radius', 'distance', 'phase'],
            data=[[0, 0, 1, 0.16, 0, 0],
                  [0, 0, 4, 0.25, 0.31, 0],
                  [0, 0, 4, 0.32, 0.61, phase],
                  [0, 0, 4, 0.48, 0.98, 0],
                  [0, 0, 4, 0.56, 1.33, phase],
                  # [0, 0, 4, 0.56, 1.53, 0],
                  # [0, 0, 4, 0.56, 1.45, phase],
                  # [0, 0, 4, 0.64, 1.57, 0],
                  # [0, 0, 4, 0.72, 1.87, phase],
                  ])
        layers_gap = [single_concentric_layer(row) for index, row in layer_params_gap.iterrows()]
        pcs_gap = pd.concat([dummy_df] + layers_gap, ignore_index=True)
        pcs_gap['x'] = pcs_gap['x'] + gap_x
        pcs_gap['y'] = pcs_gap['y'] + gap_y
        pcs_gap = filter_not_in_box(pcs_gap, -1.1, 1.1, -1.5, 0)
        pcs_gap = pcs_gap.drop([2, 5, 6, 9]) # remove cells
        pcs_gap = pcs_gap.reset_index(drop=True)

        pcs_gap.y[3] -= 0.02

        pcs_gap.y[6] -= 0.12
        pcs_gap.x[6] += 0.20
        pcs_gap.r[6]  = 0.4

        pcs_gap.x[8] += 0.28
        pcs_gap.y[8] -= 0.06
        pcs_gap.r[8] = 0.56

        pcs_gap.x[9] -= 0.45
        pcs_gap.y[9] -= 0.15
        pcs_gap.r[9] = 0.4


        pcs_gap.loc[len(pcs_gap)] = (-0.75, -0.4, 0.56)
        pcs_gap.loc[len(pcs_gap)] = (-0.75, -1.15, 0.56)

        print(pcs_gap)

        """ place cells above gap """

        pcs_gap_above = pcs_gap.copy()
        pcs_gap_above.y = -pcs_gap_above.y
        pcs_gap_above = pcs_gap_above.drop(list(range(6, 12)))
        pcs_gap_above = pcs_gap_above.drop([4])


        """ place cells around goal """

        layer_params_goal = pd.DataFrame(
            columns=['origin_x', 'origin_y', 'num_cells', 'pc_radius', 'distance', 'phase'],
            data=[[0, 0, 1, 0.08, 0, 0],
                  [0, 0, 4, 0.16, 0.20, 0],
                  [0, 0, 4, 0.24, 0.44, phase],
                  [0, 0, 4, 0.32, 0.64, 0],
                  [0, 0, 4, 0.40, 0.96, phase],
                  [0, 0, 4, 0.50, 1.12, 0],
                  [0, 0, 4, 0.56, 1.45, phase]
                  ])
        layers_goal = [single_concentric_layer(row) for index, row in layer_params_goal.iterrows()]
        pcs_goal = pd.concat([dummy_df] + layers_goal, ignore_index=True)
        pcs_goal['x'] = pcs_goal['x'] + goal_x
        pcs_goal['y'] = pcs_goal['y'] + goal_y
        pcs_goal = filter_not_in_box(pcs_goal, -1.1, 1.1, -1.5, 1.5)

        print(pcs_goal)
        pcs_goal = pcs_goal.drop([12, 13, 15 , 20]) # remove cells
        pcs_goal = pcs_goal.reset_index(drop=True)

        pcs_goal.r[4] += 0.02
        pcs_goal.r[1] = pcs_goal.r[4]
        pcs_goal.y[1] -= 0.02
        pcs_goal.x[1] += 0.02

        pcs_goal.y[4] -= 0.03
        pcs_goal.x[4] += 0.02


        pcs_goal.r[8] = 0.32
        pcs_goal.x[8] += 0.15
        pcs_goal.y[8] -= 0.05

        pcs_goal.r[12] -= 0.08
        pcs_goal.x[12] += 0.12
        pcs_goal.y[12] += 0.12

        pcs_goal.r[13] -= 0.12
        pcs_goal.x[13] -= 0.18
        pcs_goal.y[13] -= 0.02

        pcs_goal.r[14] = 0.44
        pcs_goal.x[14] += 0.09
        pcs_goal.y[14] -= 0.03

        pcs_goal.r[15] = 0.36
        pcs_goal.x[15] -= 0.30
        pcs_goal.y[15] += 0.13

        pcs_goal.r[16] = 0.52
        pcs_goal.x[16] += 0.1
        pcs_goal.y[16] += 0.15


        """ concat all pcs and then filter out """
        # pcs_gap = dummy_df
        # pcs_gap_above = dummy_df


        pcs_all = pd.concat([pcs_goal, pcs_gap_above, pcs_gap], ignore_index=True)

        # lower half
        pcs_all.loc[len(pcs_all)] = [-0.89, -0.43, 0.48]
        pcs_all.loc[32] = [-0.49, -0.35, 0.4]
        pcs_all.loc[28] = [-0.15, -0.28, 0.32]
        pcs_all.loc[24] = [0.12, -0.22, 0.25]
        pcs_all.loc[22] = [0.35, -0.16, 0.20]
        pcs_all.loc[len(pcs_all)] = [0.575, -0.12, 0.16]  # <--- gap
        pcs_all.loc[len(pcs_all)] = [0.80, -0.16, 0.20]
        pcs_all.loc[23] = [1.03, -0.22, 0.25]

        # upper half
        pcs_all.loc[len(pcs_all)] = [-0.89, 0.43, 0.48]
        pcs_all.loc[len(pcs_all)] = [-0.49, 0.35, 0.4]
        pcs_all.loc[16] = [-0.15, 0.28, 0.32]
        pcs_all.loc[15] = [0.12, 0.22, 0.25]
        pcs_all.loc[19] = [0.35, 0.16, 0.20]
        pcs_all.loc[17] = [0.575, 0.12, 0.16]  # <--- gap
        pcs_all.loc[len(pcs_all)] = [0.80, 0.16, 0.20]
        pcs_all.loc[18] = [1.03, 0.22, 0.25]


        # pcs_all.loc[len(pcs_all)] = [0.425, -0.06, 0.08]
        # pcs_all.loc[len(pcs_all)] = [0.095, -0.06, 0.08]
        # pcs_all.loc[len(pcs_all)] = [-0.35, -0.1, 0.12]
        # pcs_all.loc[len(pcs_all)] = [-1, -0.1, 0.12]

        return pcs_all
    except:
        print("Error in concentric_layer_for_experiment_0_B")
        return dummy_df


def concentric_layer_for_maze_0_FINAL():
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

        filtered = filtered.drop([12, 13]) # remove cells

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

def concentric_layer_for_maze_0_A():
    """ DEPRECATED BY concentric_layer_for_maze_0_FINAL """
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
    pcs = pcs[pcs.apply(lambda pc: pc_intersects_rectangle(pc, xmin, xmax, ymin, ymax), axis=1)]
    pcs = pcs.reset_index(drop=True)
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
