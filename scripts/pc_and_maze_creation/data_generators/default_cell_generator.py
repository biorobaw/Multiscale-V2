
import pandas as pd
import numpy as np


def load_pc_df():
    """ This is the actual function that gets called"""

    start_points_obstacle_experiment = pd.DataFrame(
            columns = ['x', 'y', 'r'],
            data = [
                [1   ,-1.4, 0.01],
                [-1  ,-1.4, 0.01],
                [-1  , 0.1, 0.01],
                [1   , 0.1, 0.01],
                [0.5,  1,  0.02]
            ]
        )

    dummy_points = pd.DataFrame(columns=['x', 'y', 'r'],
                                data=[
                                    [1  ,  0.1, 0.01], # d =
                                    [0.9, 1.2, 0.01],
                                    [-1  , 0.1, 0.01],
                                    [-0.9,1.2, 0.01],
                                    [-0.1,-1.3, 0.01],
                                    [1   ,-1.4, 0.01],
                                    [-1  ,-1.4, 0.01],
                                    [0.1 , 1.2, 0.02 ]
                                ])
    # return pd.DataFrame(columns=['x', 'y', 'r'])
    nx = 10
    radius = 0.56
    return distribute_uniformly(-1.1, 1.1, nx, -1.5, 1.5, int(np.ceil(nx*3.0/2.2)),radius)
    # return start_points_obstacle_experiment
    #return pd.concat([maze8_manual2(), dummy_points], ignore_index=True)
    
    # OLD CODE
    # return pd.concat([uniform_layer(4), dummy_points], ignore_index=True)
    # final layers used for each maze:
        # maze 0 : maze0_manual()
        # maze 1 : none of the functions below, instead a modification of maze1_manual2() done by hand and then saved
        # maze 8 : ???
    # return concentric_layer_for_maze_8_A()

def maze8_manual2():

    pcs = pd.DataFrame(columns=['x', 'y', 'r'])
    pcs.loc[len(pcs)] = [   -0.033,     0.510,      0.16]  # pcid=1
    pcs.loc[len(pcs)] = [   -1.025,     0.403,      0.16]  # pcid=2
    pcs.loc[len(pcs)] = [    0.172,     0.679,      0.12]  # pcid=3
    pcs.loc[len(pcs)] = [    0.809,    -1.307,      0.36]  # pcid=4
    pcs.loc[len(pcs)] = [   -0.537,    -0.847,      0.20]  # pcid=5
    pcs.loc[len(pcs)] = [    0.437,    -0.926,      0.24]  # pcid=6
    pcs.loc[len(pcs)] = [   -0.973,     1.483,      0.16]  # pcid=7
    pcs.loc[len(pcs)] = [   -0.846,     1.275,      0.16]  # pcid=8
    pcs.loc[len(pcs)] = [    0.228,     0.542,      0.16]  # pcid=9
    pcs.loc[len(pcs)] = [    0.390,    -0.019,      0.24]  # pcid=10
    pcs.loc[len(pcs)] = [   -0.982,    -1.048,      0.24]  # pcid=11
    pcs.loc[len(pcs)] = [    0.853,     1.077,      0.16]  # pcid=12
    pcs.loc[len(pcs)] = [    0.810,     0.810,      0.08]  # pcid=13
    pcs.loc[len(pcs)] = [   -0.997,    -1.386,      0.32]  # pcid=14
    pcs.loc[len(pcs)] = [   -0.832,     0.599,      0.12]  # pcid=15
    pcs.loc[len(pcs)] = [    1.004,     0.255,      0.24]  # pcid=16
    pcs.loc[len(pcs)] = [    0.439,    -0.616,      0.24]  # pcid=17
    pcs.loc[len(pcs)] = [    0.447,     0.839,      0.12]  # pcid=18
    pcs.loc[len(pcs)] = [    0.241,    -1.351,      0.32]  # pcid=19
    pcs.loc[len(pcs)] = [   -0.578,    -1.373,      0.32]  # pcid=20
    pcs.loc[len(pcs)] = [   -0.288,     0.630,      0.12]  # pcid=21
    pcs.loc[len(pcs)] = [   -1.016,    -0.702,      0.20]  # pcid=22
    pcs.loc[len(pcs)] = [   -1.066,     1.244,      0.16]  # pcid=23
    pcs.loc[len(pcs)] = [   -0.206,    -1.094,      0.24]  # pcid=24
    pcs.loc[len(pcs)] = [    0.789,     0.912,      0.08]  # pcid=25
    pcs.loc[len(pcs)] = [   -0.485,     0.448,      0.08]  # pcid=26
    pcs.loc[len(pcs)] = [    0.882,     0.679,      0.12]  # pcid=27
    pcs.loc[len(pcs)] = [   -0.005,     0.675,      0.12]  # pcid=28
    pcs.loc[len(pcs)] = [    0.078,    -0.046,      0.24]  # pcid=29
    pcs.loc[len(pcs)] = [    1.021,     1.069,      0.16]  # pcid=30
    pcs.loc[len(pcs)] = [    0.689,     0.083,      0.24]  # pcid=31
    pcs.loc[len(pcs)] = [   -0.630,     0.623,      0.16]  # pcid=32
    pcs.loc[len(pcs)] = [   -0.624,     1.012,      0.16]  # pcid=33
    pcs.loc[len(pcs)] = [   -1.022,     0.036,      0.24]  # pcid=34
    pcs.loc[len(pcs)] = [   -0.186,     0.774,      0.16]  # pcid=35
    pcs.loc[len(pcs)] = [   -0.630,     1.245,      0.16]  # pcid=36
    pcs.loc[len(pcs)] = [    0.618,     0.716,      0.08]  # pcid=37
    pcs.loc[len(pcs)] = [    0.175,    -0.751,      0.16]  # pcid=38
    pcs.loc[len(pcs)] = [   -0.811,     0.809,      0.12]  # pcid=39
    pcs.loc[len(pcs)] = [    0.920,     1.455,      0.20]  # pcid=40
    pcs.loc[len(pcs)] = [   -0.418,     1.136,      0.19]  # pcid=41
    pcs.loc[len(pcs)] = [   -0.360,     0.853,      0.16]  # pcid=42
    pcs.loc[len(pcs)] = [    0.624,     0.849,      0.12]  # pcid=43
    pcs.loc[len(pcs)] = [    0.634,     1.010,      0.16]  # pcid=44
    pcs.loc[len(pcs)] = [    0.583,    -0.407,      0.28]  # pcid=45
    pcs.loc[len(pcs)] = [    0.201,    -1.043,      0.24]  # pcid=46
    pcs.loc[len(pcs)] = [   -1.006,     0.590,      0.12]  # pcid=47
    pcs.loc[len(pcs)] = [   -0.323,    -0.840,      0.20]  # pcid=48
    pcs.loc[len(pcs)] = [    0.978,    -0.269,      0.36]  # pcid=49
    pcs.loc[len(pcs)] = [   -0.474,     0.625,      0.12]  # pcid=50
    pcs.loc[len(pcs)] = [    0.406,     0.619,      0.12]  # pcid=51
    pcs.loc[len(pcs)] = [    0.752,     0.480,      0.20]  # pcid=52
    pcs.loc[len(pcs)] = [   -0.079,    -0.846,      0.16]  # pcid=53
    pcs.loc[len(pcs)] = [   -0.326,    -0.587,      0.20]  # pcid=54
    pcs.loc[len(pcs)] = [    0.905,     0.897,      0.12]  # pcid=55
    pcs.loc[len(pcs)] = [   -0.375,     1.434,      0.20]  # pcid=56
    pcs.loc[len(pcs)] = [   -0.659,    -0.042,      0.28]  # pcid=57
    pcs.loc[len(pcs)] = [   -0.198,    -1.367,      0.32]  # pcid=58
    pcs.loc[len(pcs)] = [   -0.452,     0.261,      0.20]  # pcid=59
    pcs.loc[len(pcs)] = [   -0.820,     0.234,      0.20]  # pcid=60
    pcs.loc[len(pcs)] = [   -0.544,    -0.578,      0.20]  # pcid=61
    pcs.loc[len(pcs)] = [   -0.175,     0.033,      0.28]  # pcid=62
    pcs.loc[len(pcs)] = [    0.284,     0.287,      0.20]  # pcid=63
    pcs.loc[len(pcs)] = [   -0.354,     0.495,      0.12]  # pcid=64
    pcs.loc[len(pcs)] = [   -1.009,     0.772,      0.16]  # pcid=65
    pcs.loc[len(pcs)] = [    0.904,    -0.863,      0.32]  # pcid=66
    pcs.loc[len(pcs)] = [   -0.616,     0.802,      0.16]  # pcid=67
    pcs.loc[len(pcs)] = [   -0.575,    -1.062,      0.24]  # pcid=68
    pcs.loc[len(pcs)] = [    0.036,     0.257,      0.21]  # pcid=69
    pcs.loc[len(pcs)] = [    1.034,     0.821,      0.16]  # pcid=70
    pcs.loc[len(pcs)] = [    0.732,     0.721,      0.08]  # pcid=71
    pcs.loc[len(pcs)] = [    1.078,     0.550,      0.20]  # pcid=72
    pcs.loc[len(pcs)] = [   -0.086,    -0.564,      0.20]  # pcid=73
    pcs.loc[len(pcs)] = [   -0.630,     0.415,      0.16]  # pcid=74
    pcs.loc[len(pcs)] = [    0.332,     0.746,      0.08]  # pcid=75 
    pcs.loc[len(pcs)] = [    0.240,     0.829,      0.08]  # pcid=76
    pcs.loc[len(pcs)] = [   -0.270,    -0.300,      0.28]  # pcid=77
    pcs.loc[len(pcs)] = [    0.630,     1.245,      0.16]  # pcid=78
    pcs.loc[len(pcs)] = [   -0.211,     0.537,      0.12]  # pcid=79
    pcs.loc[len(pcs)] = [    0.518,     0.389,      0.20]  # pcid=80
    pcs.loc[len(pcs)] = [   -0.997,    -0.346,      0.24]  # pcid=81
    pcs.loc[len(pcs)] = [    0.833,     1.267,      0.16]  # pcid=82
    pcs.loc[len(pcs)] = [    1.052,     1.296,      0.16]  # pcid=83
    pcs.loc[len(pcs)] = [    0.581,     1.444,      0.16]  # pcid=84
    pcs.loc[len(pcs)] = [   -0.679,    -0.347,      0.20]  # pcid=85
    pcs.loc[len(pcs)] = [   -1.032,     1.008,      0.16]  # pcid=86
    pcs.loc[len(pcs)] = [   -0.771,    -0.844,      0.16]  # pcid=87
    pcs.loc[len(pcs)] = [   -0.595,     1.458,      0.16]  # pcid=88
    pcs.loc[len(pcs)] = [    0.172,    -0.392,      0.24]  # pcid=89
    pcs.loc[len(pcs)] = [   -0.193,     0.328,      0.16]  # pcid=90
    pcs.loc[len(pcs)] = [   -0.783,    -0.588,      0.16]  # pcid=91
    pcs.loc[len(pcs)] = [   -0.840,     1.032,      0.16]  # pcid=92
    pcs.loc[len(pcs)] = [   -0.830,     0.433,      0.12]  # pcid=93
    pcs.loc[len(pcs)] = [   -0.724,     1.448,      0.12]  # pcid=94

    # pcs.loc[len(pcs)] = [    1.078,     0.550,      0.20]  # pcid=96

    pcs = pcs.reset_index(drop=True)

    gx, gy = 0.1, 1.2
    pcs.loc[len(pcs)] = [gx, gy, 0.08]

    # GAOL
    add_concentric_pcs(pcs, gx, gy, 8, 0.08, 0, 0.140, 0, 8)
    add_concentric_pcs(pcs, gx, gy, 8, 0.16, 0, 0.315, 0, 8)
    # add_concentric_pcs(pcs, gx, gy, 8, 0.24, 0, 0.55, 3, 5)






    return pcs


def maze8_manual1():
    pcs = pd.DataFrame(columns=['x', 'y', 'r'])

    gx, gy = 0.1, 1.2
    pcs.loc[len(pcs)] = [gx, gy, 0.08]

    # GAOL
    add_concentric_pcs(pcs, gx, gy, 8, 0.08, 0, 0.140, 0, 8)
    add_concentric_pcs(pcs, gx, gy, 8, 0.16, 0, 0.315, 0, 8)
    #add_concentric_pcs(pcs, gx, gy, 8, 0.24, 0, 0.55, 0, 8)
    #add_concentric_pcs(pcs, gx, gy, 16, 0.36, 0, 0.9800, -1, 11)


    # define distance by which cells near corners are displaced
    parallel = 0.07
    delta_last = 0.025 # distance by which cells closest to wall in first ring must be shifted to cover all space
    # perpend  = 0.0


    # wall 0 - horizontal near goal
    gx, gy = 0.23 + parallel, 0.76
    pcs.loc[len(pcs)] = [gx, gy, 0.08]
    add_concentric_pcs(pcs, gx, gy, 8, 0.08, 0, 0.140, -3, 4)




    gx, gy = -0.08 - parallel, 0.76 
    pcs.loc[len(pcs)] = [gx, gy, 0.08]
    add_concentric_pcs(pcs, gx, gy, 8, 0.08, 0, 0.140, 1, 8)  


    # wall 0 - vertical left
    gx, gy = -0.735, 1.35 + parallel
    pcs.loc[len(pcs)] = [gx, gy, 0.08]
    add_concentric_pcs(pcs, gx, gy, 8, 0.08, 0, 0.140, -1, 6)  
    

    gx, gy = -0.735, 0.8 - parallel
    pcs.loc[len(pcs)] = [gx, gy, 0.08]
    add_concentric_pcs(pcs, gx, gy, 8, 0.08, 0, 0.140, -5, 2)     




    # wall 1 - vertical right
    # gx, gy = 0.735, 1.5  + parallel
    # pcs.loc[len(pcs)] = [gx, gy, 0.08]


    gx, gy = 0.735, 0.8 - parallel
    pcs.loc[len(pcs)] = [gx, gy, 0.08]
    add_concentric_pcs(pcs, gx, gy, 8, 0.08, 0, 0.140, -5, 2)     

    # wall 2 - vertical near goal
    gx, gy = 0.52,  1.3 + parallel  
    pcs.loc[len(pcs)] = [gx, gy, 0.08]


    gx, gy = 0.52, 0.8  - parallel
    pcs.loc[len(pcs)] = [gx, gy, 0.08]
    add_concentric_pcs(pcs, gx, gy, 8, 0.08, 0, 0.140, -5, 2)     

    # wall 3 - horizonatal left
    gx, gy = -0.47 + parallel, 0.52 
    pcs.loc[len(pcs)] = [gx, gy, 0.08]
    add_concentric_pcs(pcs, gx, gy, 8, 0.08, 0, 0.140, -3, 4)

    gx, gy = -0.9 - parallel,  0.52  
    pcs.loc[len(pcs)] = [gx, gy, 0.08]   
    add_concentric_pcs(pcs, gx, gy, 8, 0.08, 0, 0.140, 1, 8)  


    # wall 5 -  horizonatal bottom
    gx, gy = 0 + parallel, -0.72
    pcs.loc[len(pcs)] = [gx, gy, 0.08]
    add_concentric_pcs(pcs, gx, gy, 8, 0.08, 0, 0.140, -3, 4)


    gx, gy = -0.83 - parallel, -0.72
    pcs.loc[len(pcs)] = [gx, gy, 0.08] 
    add_concentric_pcs(pcs, gx, gy, 8, 0.08, 0, 0.140, 1, 8)  


    # back to wall 2 - vertical near goal
    gx, gy = 0.52,  1.3 + parallel
    add_concentric_pcs(pcs, gx, gy, 8, 0.08, 0, 0.140, -1, 6)  


    # second layers:
    add_concentric_pcs(pcs, 0.804, 0.829, 8, 0.16, 0, 0.23, 0, 2)  # top right corner
    add_concentric_pcs(pcs, -0.735, 1.420, 8, 0.16, 0, 0.312, 4, 6)  # top left corner
    add_concentric_pcs(pcs, -0.735, 0.73, 8, 0.16, 0, 0.312, 3, 5)  # top left corner (lower wall side)



    # accomodate cells and remove unnecessary:
    pcs.loc[24].y -= delta_last
    pcs.loc[18].y += delta_last
    pcs.loc[26].y -= delta_last
    pcs.loc[32].y += delta_last
    pcs.loc[73].y -= delta_last
    pcs.loc[67].y += delta_last
    pcs.loc[75].y -= delta_last
    pcs.loc[81].y += delta_last
    pcs.loc[89].y -= delta_last
    pcs.loc[83].y += delta_last
    pcs.loc[91].y -= delta_last
    pcs.loc[97].y += delta_last


    pcs.loc[42].x += delta_last
    pcs.loc[48].x -= delta_last
    pcs.loc[40].x += delta_last
    pcs.loc[34].x -= delta_last
    pcs.loc[50].x += delta_last
    pcs.loc[56].x -= delta_last
    pcs.loc[59].x += delta_last
    pcs.loc[65].x -= delta_last
    pcs.loc[104].x += delta_last
    pcs.loc[98].x -= delta_last



    pcs.loc[15] = [0.102, 0.94, 0.12]
    pcs.loc[24] = [0.182, 0.819, 0.08]
    pcs.loc[26] = [-0.024, .821, 0.08]
    pcs.loc[75] = [-0.837, 0.620, 0.12] 
    pcs.loc[46] = [-0.614, 0.603, 0.12]
    pcs.loc[59] = [0.422, 0.860, 0.12]
    pcs.loc[100] = [0.647, 1.422, 0.12]
    pcs.loc[109] = [-0.926, 1.001, 0.24]

    # add cells to close gaps
    pcs.loc[len(pcs)] = [0.078, 0.819, 0.08]
    pcs.loc[len(pcs)] = [0.436, 0.999, 0.12]

    # pcs in small path between two vertical walls
    pcs.loc[len(pcs)] = [0.629, 1.285, 0.12]
    pcs.loc[len(pcs)] = [0.629, 1.180, 0.12]
    pcs.loc[len(pcs)] = [0.627, 1.078, 0.12]
    pcs.loc[len(pcs)] = [0.629, 0.971, 0.12]
    pcs.loc[len(pcs)] = [0.550, 0.894, 0.04]
    pcs.loc[len(pcs)] = [0.707, 0.893, 0.04]

    # pcs in top right corner
    pcs.loc[len(pcs)] = [0.942, 1.454, 0.24]
    pcs.loc[len(pcs)] = [0.942, 1.221, 0.24]
    pcs.loc[len(pcs)] = [0.791, 1.043, 0.08]
    pcs.loc[len(pcs)] = [0.788, 0.928, 0.08]

    # pcs in top left corner:
    pcs.loc[len(pcs)] = [-0.831, 1.167, 0.160]





    # pcs = filter_not_in_box(pcs, -1.1, 1.1, -1.5, 1.5)
    pcs = pcs.drop([20,21,22,23,27,44 ,52, 98, 99, 102, 103, 104])  # remove cells
    pcs = pcs.reset_index(drop=True)

    return pcs



def maze1_manual2():
    pcs = pd.DataFrame(columns=['x', 'y', 'r'])

    gx, gy = 0.1, 1.2
    pcs.loc[len(pcs)] = [gx, gy, 0.08]

    # RINGS AROUND GOAL:
    add_concentric_pcs(pcs, gx, gy, 8, 0.08, 0, 0.140, 0, 8)
    add_concentric_pcs(pcs, gx, gy, 8, 0.16, 0, 0.315, 0, 8)
    add_concentric_pcs(pcs, gx, gy, 8, 0.24, 0, 0.55, 0, 8)
    add_concentric_pcs(pcs, gx, gy, 16, 0.36, 0, 0.9800, -1, 11)



    # PCS ABOVE GAP
    cx, cy  = 0.575, 0.054
    pcs.loc[len(pcs)] = [cx, cy, 0.10]
    add_concentric_pcs(pcs, cx, cy, 8, 0.08, 0, 0.140, 0, 5)
    add_concentric_pcs(pcs, cx, cy, 8, 0.16, 0, 0.315, 1, 4)
    add_concentric_pcs(pcs, cx, cy, 8, 0.24, 0, 0.55, 1, 4)
    pcs.loc[len(pcs)] = [cx+0.27, 0.093, 0.12]
    pcs.loc[len(pcs)] = [cx+0.43, 0.133, 0.16]
    pcs.loc[len(pcs)] = [cx-0.27, 0.093, 0.12]
    pcs.loc[len(pcs)] = [cx-0.43, 0.133, 0.16]
    pcs.loc[len(pcs)] = [cx-0.61, 0.173, 0.20]
    # pcs.loc[len(pcs)] = [cx-0.879, 0.315, 0.36]
    pcs.loc[len(pcs)] = [-0.965, 0.238, 0.28]
    # add_concentric_pcs(pcs, cx, cy, 8, 0.32, 0, 1.5, 5, 6)


    # CELLS BELOW GAP
    cy=-cy
    pcs.loc[len(pcs)] = [cx, cy, 0.10]  
    add_concentric_pcs(pcs, cx, cy, 8, 0.08, 0, 0.140, 4, 9)  
    add_concentric_pcs(pcs, cx, cy, 8, 0.20, 0, 0.355, 5, 8)
    pcs.loc[len(pcs)] = [cx+0.27, -0.093, 0.12]
    pcs.loc[len(pcs)] = [cx+0.43, -0.133, 0.16]
    add_concentric_pcs(pcs, cx, cy, 8, 0.32, 0, 0.645, 5, 8)
    add_concentric_pcs(pcs, cx, cy, 8, 0.48, 0, 1.100, 5, 8)
    add_concentric_pcs(pcs, cx, cy, 16, 0.56, 0, 1.800, 10, 16)
    # add_concentric_pcs(pcs, cx, cy, 8, 0.32, 0, 0.645, 1, 2)
    pcs.loc[len(pcs)] = [cx-0.27, -0.093, 0.12]
    pcs.loc[len(pcs)] = [cx-0.43, -0.133, 0.16]
    pcs.loc[len(pcs)] = [cx-0.61, -0.173, 0.20]
    pcs.loc[len(pcs)] = [cx-0.879, -0.315, 0.36]
    pcs.loc[len(pcs)] = [-0.648, -0.315, 0.36]
    pcs.loc[len(pcs)] = [-0.965, -0.238, 0.28]
    pcs.loc[len(pcs)] = [-1.088, -0.743, 0.44]





    # d = 0.6
    # r = 0.32
    # phase = 0
    # for i in range(1, 4):
    #     pcs.loc[len(pcs)] = [cx + d * np.cos(phase + i * np.pi / 4), cy + d * np.sin(phase + i * np.pi / 4), r]
    #     pass



    # d = 1.8
    # r = 0.56
    # phase = 0
    # n = 16
    # for i in range(0, n):
    #     pcs.loc[len(pcs)] = [0.1 + d * np.cos(phase + i * 2 * np.pi / n), 1.2 + d * np.sin(phase + i * 2 * np.pi / n),
    #                          r]
    #     pass

    # d = 2.51
    # r = 0.57
    # phase = 0
    # n = 16
    # for i in range(0, n):
    #     pcs.loc[len(pcs)] = [0.1 + d * np.cos(phase + i * 2 * np.pi / n), 1.2 + d * np.sin(phase + i * 2 * np.pi / n),
    #                          r]
    #     pass

    pcs = filter_not_in_box(pcs, -1.1, 1.1, -1.5, 1.5)
    

    #pcs.loc[25] = [-0.96, 1.14, 0.52]
    #pcs.loc[len(pcs)] = [-0.41, -0.05, 0.48]


    d = 0.03
    # pcs.loc[23].y-=d
    # pcs.loc[23].x+=d
    # pcs.loc[23].r = 0.363

    # pcs.loc[27] = [-0.96, 1.13, 0.52]

    d = 0.02
    # pcs.loc[28].y+=d
    # pcs.loc[28].x+=d

    # pcs = pcs.drop([25, 26, 65])  # remove cells
    pcs = pcs.reset_index(drop=True)

    # 60
    # 63
    # 62
    # pcs.loc[26] = [-0.725, 0.414, 0.44]
    # pcs.loc[42] = [-0.232, 0.207, 0.24]
    # pcs.loc[len(pcs)] = [-0.47, 0.206, 0.24]

    # pcs.loc[60] = [1.203, -0.867, 0.48]
    # pcs.loc[63] = [0.026, -1.546, 0.44]
    # pcs.loc[62] = [1.181, -1.529, 0.48]
    # pcs.loc[61] = [-0.698]


    return pcs


def maze0_manual2():
    pcs = pd.DataFrame(columns=['x', 'y', 'r'])
    pi_8 = np.pi/8

    pcs.loc[len(pcs)] = [0.1, 1.2, 0.08]

    # first ring
    d = 0.14
    r = 0.08
    phase = 0
    for i in range(0, 8):
        pcs.loc[len(pcs)] = [0.1 + d * np.cos(phase + i*np.pi/4), 1.2 + d*np.sin(phase + i*np.pi/4), r]
        pass


    d = 0.315
    r = 0.16
    phase = 0
    for i in range(0, 8):
        pcs.loc[len(pcs)] = [0.1 + d * np.cos(phase + i * np.pi / 4), 1.2 + d * np.sin(phase + i * np.pi / 4), r]
        pass

    # return pcs

    d = 0.645
    r = 0.32
    phase = 0
    n = 8
    for i in range(0, n):
        pcs.loc[len(pcs)] = [0.1 + d * np.cos(phase + i * 2 * np.pi / n), 1.2 + d * np.sin(phase + i * 2 * np.pi / n),
                             r]
        pass


    d = 1.1
    r = 0.48
    phase = 0
    n = 8
    for i in range(0, n):
        pcs.loc[len(pcs)] = [0.1 + d * np.cos(phase + i * 2 * np.pi / n), 1.2 + d * np.sin(phase + i * 2 * np.pi / n), r]
        pass




    d = 1.8
    r = 0.56
    phase = 0
    n = 16
    for i in range(0, n):
        pcs.loc[len(pcs)] = [0.1 + d * np.cos(phase + i * 2 * np.pi / n), 1.2 + d * np.sin(phase + i * 2 * np.pi / n),
                             r]
        pass

    d = 2.51
    r = 0.57
    phase = 0
    n = 16
    for i in range(0, n):
        pcs.loc[len(pcs)] = [0.1 + d * np.cos(phase + i * 2 * np.pi / n), 1.2 + d * np.sin(phase + i * 2 * np.pi / n),
                             r]
        pass

    pcs = filter_not_in_box(pcs, -1.1, 1.1, -1.5, 1.5)
    pcs = pcs.drop([25, 26, 31])  # remove cells
    pcs = pcs.reset_index(drop=True)

    pcs.loc[25] = [-0.96, 1.14, 0.52]
    pcs.loc[len(pcs)] = [-0.41, -0.05, 0.48]

    return pcs

def maze0_manual1():
    pcs = pd.DataFrame(columns=['x', 'y', 'r'])
    pi_8 = np.pi/8

    pcs.loc[len(pcs)] = [0.1, 1.2, 0.08]

    # first ring
    d = 0.23
    r = 0.16
    phase = 0
    for i in range(0, 8):
        pcs.loc[len(pcs)] = [0.1 + d * np.cos(phase + i*np.pi/4), 1.2 + d*np.sin(phase + i*np.pi/4), r]
        pass


    d = 0.6
    r = 0.32
    phase = 0
    for i in range(0, 8):
        pcs.loc[len(pcs)] = [0.1 + d * np.cos(phase + i * np.pi / 4), 1.2 + d * np.sin(phase + i * np.pi / 4), r]
        pass



    # d = 1.1
    # r = 0.4
    # phase = pi_8
    # n = 8
    # for i in range(0, n):
    #     pcs.loc[len(pcs)] = [0.1 + d * np.cos(phase + i * 2 * np.pi / n), 1.2 + d * np.sin(phase + i * 2 * np.pi / n),
    #                          r]
    #     pass


    d = 1.25
    r = 0.48
    phase = 0
    n = 16
    for i in range(0, n):
        pcs.loc[len(pcs)] = [0.1 + d * np.cos(phase + i * 2 * np.pi / n), 1.2 + d * np.sin(phase + i * 2 * np.pi / n), r]
        pass

    d = 1.8
    r = 0.56
    phase = 0
    n = 16
    for i in range(0, n):
        pcs.loc[len(pcs)] = [0.1 + d * np.cos(phase + i * 2 * np.pi / n), 1.2 + d * np.sin(phase + i * 2 * np.pi / n),
                             r]
        pass

    d = 2.51
    r = 0.57
    phase = 0
    n = 16
    for i in range(0, n):
        pcs.loc[len(pcs)] = [0.1 + d * np.cos(phase + i * 2 * np.pi / n), 1.2 + d * np.sin(phase + i * 2 * np.pi / n),
                             r]
        pass

    pcs = filter_not_in_box(pcs, -1.1, 1.1, -1.5, 1.5)
    pcs = pcs.drop([11, 28])  # remove cells
    pcs = pcs.reset_index(drop=True)

    return pcs


def maze1_manual():
    pcs = pd.DataFrame(columns=['x', 'y', 'r'])
    pi_8 = np.pi/8

    pcs.loc[len(pcs)] = [0.1, 1.2, 0.08]

    # first ring
    d = 0.23
    r = 0.16
    phase = 0
    for i in range(0, 8):
        pcs.loc[len(pcs)] = [0.1 + d * np.cos(phase + i*np.pi/4), 1.2 + d*np.sin(phase + i*np.pi/4), r]
        pass


    d = 0.6
    r = 0.32
    phase = 0
    for i in range(0, 8):
        pcs.loc[len(pcs)] = [0.1 + d * np.cos(phase + i * np.pi / 4), 1.2 + d * np.sin(phase + i * np.pi / 4), r]
        pass


    d = 1.25
    r = 0.48
    phase = 0
    n = 16
    for i in range(-1, n-6):
        pcs.loc[len(pcs)] = [0.1 + d * np.cos(phase + i * 2 * np.pi / n), 1.2 + d * np.sin(phase + i * 2 * np.pi / n), r]
        pass

    pcs.loc[len(pcs)] = [-0.79, 0.477, 0.48]
    pcs.loc[len(pcs)] = [-0.26, 0.362, 0.32]

    #
    # d = 1.8
    # r = 0.56
    # phase = 0
    # n = 16
    # for i in range(0, n):
    #     pcs.loc[len(pcs)] = [0.1 + d * np.cos(phase + i * 2 * np.pi / n), 1.2 + d * np.sin(phase + i * 2 * np.pi / n),
    #                          r]
    #     pass
    #
    # d = 2.51
    # r = 0.57
    # phase = 0
    # n = 16
    # for i in range(0, n):
    #     pcs.loc[len(pcs)] = [0.1 + d * np.cos(phase + i * 2 * np.pi / n), 1.2 + d * np.sin(phase + i * 2 * np.pi / n),
    #                          r]
    #     pass

    # pcs above gap
    # pcs.loc[len(pcs)] = [0.575, 0.027, 0.08]
    x = 0.125
    # pcs.loc[len(pcs)] = [0.575+x, 0.027+x, 0.16]
    # pcs.loc[len(pcs)] = [0.575, 0.027, 0.08]  # <==gap
    # pcs.loc[len(pcs)] = [0.575-x, 0.027+x, 0.16]
    # pcs.loc[len(pcs)] = [0.575+2*x, 0.027, 0.32]
    # pcs.loc[len(pcs)] = [0.575, 0.027, 0.08]
    # pcs.loc[len(pcs)] = [0.575, 0.027, 0.08]
    # pcs.loc[len(pcs)] = [0.575, 0.027, 0.08]
    # pcs.loc[len(pcs)] = [0.575, 0.027, 0.08]

    # pcs below gap
    cx, cy  = 0.575, -0.054
    #pcs.loc[len(pcs)] = [cx, cy, 0.08]


    # PCS ABOVE GAP

    dx = 2.136 / 19
    for i in range(-15, 6):
        pcs.loc[len(pcs)] = [cx + dx * i, 0.054, 0.08]

    # first ring
    d = 0.23
    r = 0.16
    phase = 0
    for i in range(1, 4):
        pcs.loc[len(pcs)] = [cx + d * np.cos(phase + i * np.pi / 4), cy + d * np.sin(phase + i * np.pi / 4), r]
        pass

    d = 0.6
    r = 0.32
    phase = 0
    for i in range(1, 4):
        pcs.loc[len(pcs)] = [cx + d * np.cos(phase + i * np.pi / 4), cy + d * np.sin(phase + i * np.pi / 4), r]
        pass





    # PCS BELOW GAP

    dx = 2.136 / 19
    for i in range(-15, 6):
        pcs.loc[len(pcs)] = [cx + dx * i, -0.054, 0.08]


    # first ring
    d = 0.23
    r = 0.16
    phase = 0
    for i in range(5, 8):
        pcs.loc[len(pcs)] = [cx + d * np.cos(phase + i * np.pi / 4), cy + d * np.sin(phase + i * np.pi / 4), r]
        pass

    d = 0.6
    r = 0.32
    phase = 0
    for i in range(5, 8):
        pcs.loc[len(pcs)] = [cx + d * np.cos(phase + i * np.pi / 4), cy + d * np.sin(phase + i * np.pi / 4), r]
        pass


    d = 1.25
    r = 0.48
    phase = 0
    n = 16
    for i in range(9, n):
        pcs.loc[len(pcs)] = [cx + d * np.cos(phase + i * 2 * np.pi / n), cy + d * np.sin(phase + i * 2 * np.pi / n), r]
        pass

    d = 1.8
    r = 0.56
    phase = 0
    n = 16
    for i in range(9, 11):
        pcs.loc[len(pcs)] = [cx + d * np.cos(phase + i * 2 * np.pi / n), cy + d * np.sin(phase + i * 2 * np.pi / n), r]
        pass





    # filler cells
    pcs.loc[len(pcs)] = [0.133, -0.165, 0.16]
    pcs.loc[len(pcs)] = [-0.192, -0.329, 0.32]
    pcs.loc[len(pcs)] = [0.966, -0.16, 0.16]
    pcs.loc[len(pcs)] = [-0.959, -0.169, 0.16]


    # d = 1.1
    # r = 0.4
    # phase = pi_8
    # n = 8
    # for i in range(0, n):
    #     pcs.loc[len(pcs)] = [0.1 + d * np.cos(phase + i * 2 * np.pi / n), 1.2 + d * np.sin(phase + i * 2 * np.pi / n),
    #                          r]
    #     pass

    # d = 1.25
    # r = 0.48
    # phase = 0
    # n = 16
    # for i in range(0, n):
    #     pcs.loc[len(pcs)] = [0.1 + d * np.cos(phase + i * 2 * np.pi / n), 1.2 + d * np.sin(phase + i * 2 * np.pi / n), r]
    #     pass
    #
    # d = 1.8
    # r = 0.56
    # phase = 0
    # n = 16
    # for i in range(0, n):
    #     pcs.loc[len(pcs)] = [0.1 + d * np.cos(phase + i * 2 * np.pi / n), 1.2 + d * np.sin(phase + i * 2 * np.pi / n),
    #                          r]
    #     pass
    #
    # d = 2.51
    # r = 0.57
    # phase = 0
    # n = 16
    # for i in range(0, n):
    #     pcs.loc[len(pcs)] = [0.1 + d * np.cos(phase + i * 2 * np.pi / n), 1.2 + d * np.sin(phase + i * 2 * np.pi / n),
    #                          r]
    #     pass


    pcs = filter_not_in_box(pcs, -1.1, 1.1, -1.5, 1.5)
    pcs = pcs.drop([11])  # remove cells
    # pcs = pcs.reset_index(drop=True)


    return pcs

def concentric_layer_for_maze_1_A():
    dummy_df = pd.DataFrame(columns=['x', 'y', 'r'])
    ang45 = np.deg2rad(45)
    ang90 = np.deg2rad(90)
    goal_x, goal_y = 0.1, 1.2
    gap_x, gap_y = 0.575, -0.12
    try:


        """ concat all pcs and then filter out """
        # pcs_gap = dummy_df
        # pcs_gap_above = dummy_df

        pcs_all = pd.DataFrame(columns=['x', 'y', 'r'])
        # pcs_all = pd.concat([pcs_goal, pcs_gap_above, pcs_gap], ignore_index=True)

        # upper half around goal

        # cell 0 at goal : 1-1
        pcs_all.loc[len(pcs_all)] = [0.1, 1.2, 0.08]

        # first ring around goal : 2-5
        l = 0.20
        pcs_all.loc[len(pcs_all)] = [ goal_x+l*np.cos(ang90*0), goal_y+l*np.sin(ang90*0), 0.16]
        pcs_all.loc[len(pcs_all)] = [ goal_x+l*np.cos(ang90*1), goal_y+l*np.sin(ang90*1), 0.16]
        pcs_all.loc[len(pcs_all)] = [ goal_x+l*np.cos(ang90*2), goal_y+l*np.sin(ang90*2), 0.16]
        pcs_all.loc[len(pcs_all)] = [ goal_x+l*np.cos(ang90*3), goal_y+l*np.sin(ang90*3), 0.16]
        pcs_all.loc[len(pcs_all)] = [ goal_x+l*np.cos(ang45+ang90*0), goal_y+l*np.sin(ang45+ang90*0), 0.16]
        pcs_all.loc[len(pcs_all)] = [ goal_x+l*np.cos(ang45+ang90*1), goal_y+l*np.sin(ang45+ang90*1), 0.16]
        pcs_all.loc[len(pcs_all)] = [ goal_x+l*np.cos(ang45+ang90*2), goal_y+l*np.sin(ang45+ang90*2), 0.16]
        pcs_all.loc[len(pcs_all)] = [ goal_x+l*np.cos(ang45+ang90*3), goal_y+l*np.sin(ang45+ang90*3), 0.16]

        # second ring around goal : 6-9
        l = 0.45
        pcs_all.loc[len(pcs_all)] = [goal_x+l*np.cos(ang90*0), goal_y+l*np.sin(ang90*0), 0.24]
        pcs_all.loc[len(pcs_all)] = [goal_x+l*np.cos(ang90*1), goal_y+l*np.sin(ang90*1), 0.24]
        pcs_all.loc[len(pcs_all)] = [goal_x+l*np.cos(ang90*2), goal_y+l*np.sin(ang90*2), 0.24]
        pcs_all.loc[len(pcs_all)] = [goal_x+l*np.cos(ang90*3), goal_y+l*np.sin(ang90*3), 0.24]

        # third ring around goal : 10-13
        l = 0.64
        pcs_all.loc[len(pcs_all)] = [goal_x+l*np.cos(ang45+ang90*0), goal_y+l*np.sin(ang45+ang90*0), 0.32]
        pcs_all.loc[len(pcs_all)] = [goal_x+l*np.cos(ang45+ang90*1), goal_y+l*np.sin(ang45+ang90*1), 0.32]
        pcs_all.loc[len(pcs_all)] = [goal_x+l*np.cos(ang45+ang90*2), goal_y+l*np.sin(ang45+ang90*2), 0.32] # [0.25,  -0.72, 0.40]
        pcs_all.loc[len(pcs_all)] = [goal_x+l*np.cos(ang45+ang90*3), goal_y+l*np.sin(ang45+ang90*3), 0.32]

        # fourth and final ring around goal : 14-15
        l=0.96
        pcs_all.loc[len(pcs_all)] = [goal_x+l*np.cos(ang90*0), goal_y+l*np.sin(ang90*0), 0.4]   # [-0.58, 0.52, 0.4] # [-.46, 0.64, 0.32]
        pcs_all.loc[len(pcs_all)] = [goal_x+l*np.cos(ang90*2), goal_y+l*np.sin(ang90*2), 0.4]


        # wall layer above  gap : 16 - 23
        d = 0.31
        pcs_all.loc[len(pcs_all)] =  [-0.89, 0.44, 0.49]
        pcs_all.loc[len(pcs_all)] = [-0.3525-d, 0.7475-d, 0.48]#[-0.89, 0.44, 0.49]
        pcs_all.loc[len(pcs_all)] = [-0.49, 0.35, 0.4]
        pcs_all.loc[len(pcs_all)] = [-0.15, 0.28, 0.32]
        pcs_all.loc[len(pcs_all)] = [0.12, 0.22, 0.25]
        pcs_all.loc[len(pcs_all)] = [0.35, 0.16, 0.20]
        pcs_all.loc[len(pcs_all)] = [0.575, 0.12, 0.16]  # <--- gap
        pcs_all.loc[len(pcs_all)] = [0.80, 0.16, 0.20]
        pcs_all.loc[len(pcs_all)] = [1.03, 0.22, 0.25]

        # second layer of wall cells above gap : 24 - 26
        pcs_all.loc[len(pcs_all)] = [0.22, 0.45, 0.17]
        pcs_all.loc[len(pcs_all)] = [0.57, 0.45, 0.24]
        pcs_all.loc[len(pcs_all)] = [1.00, 0.58, 0.32]


        # wall layer below  gap : 27 - 34

        pcs_all.loc[len(pcs_all)] = [-0.89, -0.43, 0.48]
        pcs_all.loc[len(pcs_all)] = [-0.49, -0.35, 0.4]
        pcs_all.loc[len(pcs_all)] = [-0.15, -0.28, 0.32]
        pcs_all.loc[len(pcs_all)] = [0.12, -0.22, 0.25]
        pcs_all.loc[len(pcs_all)] = [0.35, -0.16, 0.20]
        pcs_all.loc[len(pcs_all)] = [0.575, -0.12, 0.16]  # <--- gap
        pcs_all.loc[len(pcs_all)] = [0.80, -0.16, 0.20]
        pcs_all.loc[len(pcs_all)] = [1.03, -0.22, 0.25]

        # second layer of wall cells above gap : 35 - 39

        d = 0.10
        l0 = 0.05
        l = 0.35
        l2 = 0.3
        pcs_all.loc[len(pcs_all)] = [-0.34, -1.27, 0.56]
        pcs_all.loc[len(pcs_all)] = [-0.06, -1.01, 0.44]
        pcs_all.loc[len(pcs_all)] = [0.27, -0.68, 0.36]
        pcs_all.loc[len(pcs_all)] = [0.57, -0.39, 0.24]  # <--- aligned with gap
        pcs_all.loc[len(pcs_all)] = [0.87, -0.70, 0.36]

        # filler cells : 40-41

        pcs_all.loc[len(pcs_all)] = [0.40, -1.23, 0.4]  # <-- aligned with gap
        pcs_all.loc[len(pcs_all)] = [0.9, -1.23, 0.4]
        pcs_all.loc[len(pcs_all)] = [-0.89, -1.27, 0.56]


        return pcs_all
    except:
        print("Error in concentric_layer_for_experiment_0_B")
        return dummy_df

def concentric_layer_for_maze_8_A():
    pcs = pd.DataFrame(columns=['x', 'y', 'r'])
    ang45 = np.deg2rad(45)
    ang90 = np.deg2rad(90)
    goal_x, goal_y = 0.1, 1.2
    gap_x, gap_y = 0.575, -0.12

    # goal
    pcs.loc[len(pcs)] = [0.1, 1.2, 0.08]

    # top left wall
    pcs.loc[len(pcs)] = [-0.78, 1.44, 0.08]
    pcs.loc[len(pcs)] = [-0.68, 1.44, 0.08]
    pcs.loc[len(pcs)] = [-0.78, 0.73, 0.08]
    pcs.loc[len(pcs)] = [-0.68, 0.73, 0.08]

    # wall beneath top left wall
    pcs.loc[len(pcs)] = [-0.95, 0.57, 0.08]
    pcs.loc[len(pcs)] = [-0.95, 0.47, 0.08]
    pcs.loc[len(pcs)] = [-0.42, 0.57, 0.08]
    pcs.loc[len(pcs)] = [-0.42, 0.47, 0.08]

    # wall beneath goal
    pcs.loc[len(pcs)] = [-0.16, 0.77, 0.08]
    pcs.loc[len(pcs)] = [0.3, 0.77, 0.08]

    # wall right goal
    pcs.loc[len(pcs)] = [0.52, 0.73, 0.08]
    pcs.loc[len(pcs)] = [0.52, 1.41, 0.08]

    # right most wall ( at top )
    pcs.loc[len(pcs)] = [0.73, 0.73, 0.08]

    # bottom wall
    pcs.loc[len(pcs)] = [-0.9, -0.71, 0.08]
    pcs.loc[len(pcs)] = [0.07, -0.71, 0.08]

    return pcs


def concentric_layer_for_maze_1_E():
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
        pcs_all.loc[len(pcs_all)] = [-0.49, 0.16, 0.25]
        pcs_all.loc[16] = [-0.15, 0.28, 0.32]
        pcs_all.loc[15] = [0.12, 0.22, 0.25]
        pcs_all.loc[19] = [0.35, 0.16, 0.20]
        pcs_all.loc[17] = [0.575, 0.12, 0.16]  # <--- gap
        pcs_all.loc[len(pcs_all)] = [0.80, 0.16, 0.20]
        pcs_all.loc[18] = [1.03, 0.22, 0.25]

        # upper half around goal

        pcs_all.loc[0] = [0.1, 1.2, 0.08]

        pcs_all.loc[1] = [0.3, 1.2, 0.16]
        pcs_all.loc[2] = [0.1, 1.4, 0.16]
        pcs_all.loc[3] = [-0.1, 1.2, 0.16]
        pcs_all.loc[4] = [0.1, 1.0, 0.16]

        pcs_all.loc[5] = [0.41, 1.51, 0.24]
        pcs_all.loc[6] = [-0.21, 1.51, 0.24]
        pcs_all.loc[7] = [-0.21, 0.89, 0.24]
        pcs_all.loc[8] = [0.41, 0.89, 0.24]

        pcs_all.loc[9] = [0.74, 1.2, 0.32]
        pcs_all.loc[10] = [-0.54, 1.2, 0.32]
        pcs_all.loc[11] = [0.11, 0.56, 0.33] # [0.25,  -0.72, 0.40]

        # upper half, joining gap layer with goal layer


        pcs_all.loc[12] = [-0.58, 0.52, 0.4]   # [-0.58, 0.52, 0.4] # [-.46, 0.64, 0.32]
        pcs_all.loc[len(pcs_all)] = [0.7, 0.7, 0.28]


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

def concentric_layer_for_maze_1_D():
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

        # upper half around goal

        pcs_all.loc[0] = [0.1, 1.2, 0.08]

        pcs_all.loc[1] = [0.3, 1.2, 0.16]
        pcs_all.loc[2] = [0.1, 1.4, 0.16]
        pcs_all.loc[3] = [-0.1, 1.2, 0.16]
        pcs_all.loc[4] = [0.1, 1.0, 0.16]

        pcs_all.loc[5] = [0.41, 1.51, 0.24]
        pcs_all.loc[6] = [-0.21, 1.51, 0.24]
        pcs_all.loc[7] = [-0.21, 0.89, 0.24]
        pcs_all.loc[8] = [0.41, 0.89, 0.24]

        pcs_all.loc[9] = [0.74, 1.2, 0.32]
        pcs_all.loc[10] = [-0.54, 1.2, 0.32]
        pcs_all.loc[11] = [0.1, 0.56, 0.32] # [0.25,  -0.72, 0.40]

        # upper half, joining gap layer with goal layer


        pcs_all.loc[12] = [-0.58, 0.52, 0.4]   # [-0.58, 0.52, 0.4] # [-.46, 0.64, 0.32]
        pcs_all.loc[len(pcs_all)] = [0.78, 0.52, 0.4]


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

def concentric_layer_for_maze_1_C():
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


def uniform_layer(radius_cm):
    # layers from previous experiments
    single_layers = pd.DataFrame(columns=['pcSizes', 'minX', 'maxX', 'numX', 'minY', 'maxY', 'numY'])
    single_layers.loc[ 0] = (0.04, -1.084390243902439 , 1.084390243902439, 40, -1.485	, 1.485	           , 55)
    single_layers.loc[ 1] = (0.08, -1.0676190476190477, 1.0676190476190477, 20, -1.4710344827586208, 1.4710344827586208, 28)
    single_layers.loc[ 2] = (0.12, -1.0573333333333335, 1.0573333333333335, 14, -1.4657142857142857, 1.4657142857142857, 20)
    single_layers.loc[ 3] = (0.16, -1.05, 1.05, 11, -1.4525	, 1.4525	           , 15)
    single_layers.loc[ 4] = (0.2 , -1.04              , 1.04              , 9 , -1.457142857142857 , 1.457142857142857 , 13)
    single_layers.loc[ 5] = (0.24, -1.0050000000000001, 1.0050000000000001, 7, -1.4236363636363636, 1.4236363636363636, 10)
    single_layers.loc[ 6] = (0.28, -0.9857142857142858, 0.9857142857142858, 6, -1.424	, 1.424	           , 9 )
    single_layers.loc[ 7] = (0.32, -1.0142857142857145, 1.0142857142857145, 6 , -1.456	           , 1.456	           , 9 )
    single_layers.loc[ 8] = (0.36, -0.9733333333333334, 0.9733333333333334, 5 , -1.395	           , 1.395	           , 7 )
    single_layers.loc[ 9] = (0.4 , -1.0               , 1.0               , 5 , -1.4249999999999998, 1.4249999999999998, 7 )
    single_layers.loc[10] = (0.44, -0.924             , 0.924             , 4 , -1.3857142857142857, 1.3857142857142857, 6 )
    single_layers.loc[11] = (0.48, -0.9480000000000001, 0.9480000000000001, 4, -1.4142857142857141, 1.4142857142857141, 6)
    single_layers.loc[12] = (0.52, -0.972000000000000, 0.9720000000000001, 4, -1.4428571428571428, 1.4428571428571428, 6)
    single_layers.loc[13] = (0.56, -0.9960000000000001, 0.9960000000000001, 4, -1.4714285714285715, 1.4714285714285715, 6)

    layer_id = radius_cm/4 -1

    params = single_layers.loc[layer_id]

    xs = np.tile(np.linspace(params['minX'], params['maxX'], int(params['numX'])), int(params['numY']))
    ys = np.repeat(np.linspace(params['minY'], params['maxY'], int(params['numY'])), int(params['numX']))
    return pd.DataFrame({'x': xs, 'y': ys, 'r': radius_cm/100.0})

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
    return pcs


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


def add_concentric_pcs(pcs, cx, cy, num, radius, phase, distance, min, max):
    for i in range(min, max):
        pcs.loc[len(pcs)] = [cx + distance * np.cos(phase + i * 2 * np.pi / num), 
                             cy + distance * np.sin(phase + i * 2 * np.pi / num), 
                             radius]

def distribute_uniformly(mx, Mx, nx, my, My, ny, radius):
    xs = np.tile(np.linspace(mx, Mx, nx), ny)
    ys = np.repeat(np.linspace(my, My, ny), nx)
    return pd.DataFrame({'x': xs, 'y': ys, 'r': radius})
