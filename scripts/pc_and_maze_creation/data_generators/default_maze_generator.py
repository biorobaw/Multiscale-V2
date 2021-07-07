import pandas as pd
import numpy as np
from shapely.geometry import Point, LineString



def load_maze_df():
	# maze for bio experiments: 
	#		obstacle length = 0.19*sqrt(0.3538) = 0.113 # biology length * distance scale ratio 
	# 		num obstacles: 0, 6, 11, 23
	# maze for robot experiments:
	#		obstacle length 25cm
	#		num obstacles: 0, 10, 20, 30, 40, 50, 60
	# NOTE: min distance between obstacles set to 10cm
	walls = pd.concat([external_walls(), obstacles_maze_9(10, length=0.25), auxiliary_walls_maze_9()], ignore_index=True)
	feeders = feeders_maze_9()
	starts  = start_pos_maze_9()
	return walls, feeders, starts


def external_walls():
	return pd.DataFrame(columns=['x1', 'y1', 'x2', 'y2'],
						data=[
								[-1.1, -1.5, -1.1, 1.5],
								[-1.1, 1.5, 1.1, 1.5],
								[1.1, -1.5, 1.1, 1.5],
								[-1.1, -1.5, 1.1, -1.5]
							 ])


def dummy_walls():
	return pd.DataFrame(columns=['x1', 'y1', 'x2', 'y2'])


def obstacles_maze_0():
	return dummy_walls()


def auxiliary_walls_maze_0():
	return pd.DataFrame(
			columns=['x1', 'y1', 'x2', 'y2'],
			data=[
				[-1.1  ,  1.2   ,  1.1   ,  1.2 ],
				[ 0.1  ,  1.5   ,  0.1   , -1.5 ],
				[-1.1  ,  0     ,  0.4   ,  1.5 ],
				[-0.2  ,  1.5   ,  1.1   ,  0.2 ],
				[ 1.023,  1.5826, -1.10  ,  0.70],
				[-1.10 ,  1.70  ,  1.30  ,  0.70],
				[-0.09 ,  1.66  ,  1.2   , -1.48],
				[-1.086, -1.66  ,  0.29  ,  1.66]
			]
		)

def feeders_maze_0():
	return pd.DataFrame(
			columns=['fid','x','y'],
			data=[
				[1, 0.1, 1.2]
			]
		)

def start_pos_maze_0():
	return pd.DataFrame(
			columns=['x','y', 'w'],
			data=[
				[1    , 0.1  , 0], 	
				[0.9  , -0.1 , 0], 	
				[-1   , 0.1  , 0], 	
				[-0.9 , -0.1 , 0], 	
				[-0.1 , -1.3 , 0], 	
				[1    , -1.4 , 0], 	
				[-1   , -1.4 , 0]	
			]
		)

def obstacles_maze_1():
	return pd.DataFrame(columns=['x1', 'y1', 'x2', 'y2'],
		data=[
			[-1.1, 0, 0.5,  0],
			[0.65, 0, 1.1,  0]
		])


def auxiliary_walls_maze_1():
	aux_0 = auxiliary_walls_maze_0()

	aux_1 = pd.DataFrame(columns=['x1', 'y1', 'x2', 'y2'],
		data=[
			[-1.10, -0.054,  1.1   , -0.054 ],
			[0.575, -0.054,  0.575 , -1.5   ],
			[0.575, -0.054,  1.1   , -0.498 ],
			[0.575, -0.054,  -1.1  , -1.648 ],
			[-1.10, 0.054 ,  1.1   , 0.054  ],
			[0.575, 0.054 ,  0.575 , 1.5    ],
			[0.575, 0.054 ,  1.1   , 0.498  ],
			[0.575, 0.054 ,  -1.1  , 1.648  ],
			[0.575, -0.054,  1.13  , -0.284 ],
			[0.575, -0.054,  -1.13 , -0.762 ],
			[0.575, -0.054,  -0.037, -1.532 ],
			[0.575, -0.054,  1.187 , -1.532 ],
			[0.575, 0.054 ,  1.13  , 0.284  ],
			[0.575, 0.054 ,  -1.13 , 0.762  ],
			[0.575, 0.054 ,  -0.037, 1.532  ],
			[0.575, 0.054 ,  1.187 , 1.532  ]
		])

	return pd.concat([aux_0, aux_1], ignore_index=True)


def feeders_maze_1():
	return feeders_maze_0()

def start_pos_maze_1():
	return start_pos_maze_0()


def obstacles_maze8():
	return pd.DataFrame(columns=['x1', 'y1', 'x2', 'y2'],
		data=[
		   [-0.735, 1.35 , -0.735, 0.8  ],
		   [0.735 , 1.5  , 0.735 , 0.8  ],
		   [0.52  , 1.3  , 0.52  , 0.8  ],
		   [-0.9  , 0.52 , -0.47 , 0.52 ],
		   [-0.08 , 0.76 , 0.23  , 0.76 ],
		   [-0.83 , -0.72, 0     , -0.72]
		])


def auxiliary_walls_maze_8():
	return dummy_walls()

def feeders_maze_8():
	return feeders_maze_0()

def start_pos_maze_8():
	return pd.DataFrame(
		columns=['x','y', 'w'],
		data=[
			[1    , 0.1  , 0], 	
			[0.9  , 1.2  , 0], 	
			[-1   , 0.1  , 0], 	
			[-0.9 , 1.2  , 0], 	
			[1    , -1.4 , 0], 	
			[-1   , -1.4 , 0]	
		]
	)

def sample_random_wall(mx, Mx, my, My, length):
	angle = np.random.rand()*2*np.pi
	cx = np.random.rand() * (Mx - mx - length) +  (mx + length/2)
	cy = np.random.rand() * (My - my - length) +  (my + length/2)

	x1 = cx + np.cos(angle)*length/2
	y1 = cy + np.sin(angle)*length/2
	x2 = cx - np.cos(angle)*length/2
	y2 = cy - np.sin(angle)*length/2

	return x1, y1, x2, y2



def obstacles_maze_9(num_walls=60, maze_width = 2.2, maze_height = 3.0, length = 0.25, min_distance=0.10):
	
	mx = -maze_width/2
	Mx = maze_width/2
	my = -maze_height/2
	My = maze_height/2


	data = pd.DataFrame(columns=['x1', 'y1', 'x2', 'y2'])

	for i in range(0, num_walls):

		while True:

			x1, y1, x2, y2 = sample_random_wall(mx, Mx, my, My, length)
			wall_i = LineString( [[x1,y1], [x2,y2]] )

			intersects = False
			for j in range(0,i):
				wj = data.loc[j]
				wall_j = LineString( [[wj['x1'], wj['y1']], [wj['x2'], wj['y2']]] )

				if wall_i.distance(wall_j) < min_distance: # assume walls intersect if distance is less than 5 cm
					intersects = True
					break

			if not intersects:
				data.loc[i] = [x1, y1, x2, y2]
				break

	return data

def auxiliary_walls_maze_9():
	return dummy_walls()

def feeders_maze_9():
	return pd.DataFrame(
		columns=['fid', 'x', 'y'],
		data=[
                [1, 0.5,  1]
		]
	)

def start_pos_maze_9():
	return pd.DataFrame(
		columns=['x','y', 'w'],
		data=[
                [1   ,-1.4, 0],
                [-1  ,-1.4, 0],
                [-1  , 0.1, 0],
                [1   , 0.1, 0]
		]
	)


