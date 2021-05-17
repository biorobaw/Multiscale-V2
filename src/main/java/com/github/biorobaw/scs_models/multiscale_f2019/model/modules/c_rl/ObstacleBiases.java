package com.github.biorobaw.scs_models.multiscale_f2019.model.modules.c_rl;

import java.util.Collection;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.PriorityQueue;

import org.apache.commons.math3.geometry.euclidean.threed.Vector3D;
import org.locationtech.jts.geom.Coordinate;
import org.locationtech.jts.geom.GeometryFactory;
import org.locationtech.jts.geom.LineString;
import org.locationtech.jts.geom.Point;
import org.locationtech.jts.operation.distance.DistanceOp;
import com.github.biorobaw.scs.experiment.Experiment;
import com.github.biorobaw.scs.simulation.object.maze_elements.walls.Wall;
import com.github.biorobaw.scs.utils.math.DiscreteDistribution;
import com.github.biorobaw.scs.utils.math.Floats;

//org.locationtech.jts.geom



public class ObstacleBiases {
	
	// WALLS
	public LinkedList<WallData> walls 						 = new LinkedList<WallData>(); 	// all walls
	public LinkedList<WallData> walls_visited 				 = new LinkedList<>();		   	// walls already visited in the episode
	public LinkedList<WallData> walls_visited_this_cycle 	 = new LinkedList<>();			// walls visited on this cycle
	public Collection<WallData> walls_considered_in_last_selection  = new LinkedList<>();			// walls considered for choosing next bias
	
	public WallData wall_chosen = null;			// wall chosen in chosen this cycle
	final WallData dummy_wall = new WallData();	// dummy wall for searching closest wall
	
	// BINNING - for quickly finding list of walls close to robot
	float bin_size;
	float bin_distance;

	HashMap<Integer,Collection<WallData>> bins;
	double minx, maxx, miny, maxy; 
	int max_bin_x, max_bin_y, num_bins_x, num_bins_y;
	
	// RL REWARD
	float reward_distance;
	float initial_reward_value;
	float reward_value;
	
	// DIRECT MOTION BIAS
	static final int 	 numActions = 8;
	static final float 	 u_value = 1.0f / numActions;
	static final float[] uniform = new float[numActions];
	{
		for(int i=0; i<numActions; i++) uniform[i] = u_value;
	}
	static final float mainDirectionBias 	= 0.83f;
	static final float nextDirection_bias 	= 0.06f;
	static final float otherDirections 		= (1-mainDirectionBias-2*nextDirection_bias)/5;
	static final float[] initialBias 		= new float[] {
				mainDirectionBias,
				nextDirection_bias,
				otherDirections,
				otherDirections,
				otherDirections,
				otherDirections,
				otherDirections,
				nextDirection_bias
				};
	static float[] interpolatedBias 		= new float[numActions];
	public float[] biases					= new float[numActions];;
	
	// bias has exponential decay rate to uniform distribution
	static final int episodesToHalfLife = 100000;
	static final float decay = (float)(1f/Math.pow(2, 1f/episodesToHalfLife));
	static final float interpolation_step = (1-decay)*u_value;
	
	
	// Methods to chooose next wall:
	Comparator<WallData> wall_data_comparator;
	float[] selection_weights;
	int max_elements;
	
	// GEOMETRIC PROPORTY PROCESSING
	GeometryFactory geom_factory = new GeometryFactory();
	
	public ObstacleBiases(float bin_size, float bin_distance, float reward_distance, float reward_value, float[] selection_weights) {
		// Binning parameters:
		this.bin_size = bin_size;
		this.bin_distance = bin_distance;
		
		// Reward parameters
		this.reward_distance = reward_distance;
		this.initial_reward_value = reward_value;
		
		this.selection_weights = selection_weights;
		this.max_elements = selection_weights.length;
		
		this.wall_data_comparator = new Comparator<ObstacleBiases.WallData>() {
			@Override
			public int compare(WallData o1, WallData o2) {
				return Double.compare(o1.distance , o2.distance); 
			}
		};
		this.wall_data_comparator = Collections.reverseOrder(this.wall_data_comparator); // sort ascending, not descending
				
	}
	
	public void newTrial() {
		// reinitialize bins and wall reward value
		
		
		// get walls and initialize bins
		for(var w : Experiment.get().getMaze().walls) walls.add(new WallData((Wall)w));
		initializeBins(walls);
		
		// reset reward value
		reward_value = initial_reward_value;
		
		// reinitialize interpolation value:
		// OBS: b(e+1) = \gamma * b(e) + (1-\gamma)*u
		// THUS: b(-1) = \gamma * b(0) + (1-\gamma)*u
		for(int i=0; i<numActions;i++) interpolatedBias[i] = (initialBias[i] - interpolation_step) / decay; // need to divide by decay since at new episode it gets multiplied by decay
	}
	
	public void newEpisode() {
		// reset rewarded sites:
		wall_chosen = null;
		walls_visited_this_cycle.clear();
		
		for( var w : walls_visited) w.visited = false;
		
		// update bias
		for(int i=0;i<numActions;i++) {
			// OBS: b(e+1) = \gamma * b(e) + (1-\gamma)*u
			Floats.mul(interpolatedBias, decay, interpolatedBias);
			Floats.add(interpolatedBias, interpolation_step, interpolatedBias);
		}
		
	}
	
	public float getReward(Vector3D pos) {
		walls_considered_in_last_selection = new LinkedList<>();
		walls_visited_this_cycle.clear();

		var bin = bins.get(getIndex(pos));
		if(bin==null) return 0;
		
//		walls_considered_this_cycle = bin; // uncomment to see walls in bin
		
		// convert pos to point:
		var point = geom_factory.createPoint(new Coordinate(pos.getX(), pos.getY()));
		
		for(var wall : bin) 
			if( !wall.visited && wall.visit(point)) {
				wall_chosen = wall;
				return reward_value;
			}
		

		
		return 0;
	}
	
	

	
	public float[] calculateBias(Vector3D pos) {
		// clear walls visited this cycle
		walls_visited_this_cycle.clear();
		
		// convert point to coordinate:
		var point = geom_factory.createPoint(new Coordinate(pos.getX(), pos.getY()));
		
		// find new wall if necessary:
		boolean choose_new_wall = wall_chosen == null || wall_chosen.visit(point);
		if(choose_new_wall) wall_chosen = chooseNextWall(point);
				
		// if no wall was chosen, return uniform distribution
		if (wall_chosen == null) {
			return uniform;
		}
		
		// else, get distribution to move towards nearest point in chosen wall
		var nearest = wall_chosen.getClosestPoint(point);
		
		var angle = Math.atan2(nearest.y - pos.getY(), nearest.x - pos.getX());
		if(angle<0) angle += 2*Math.PI;
		int closest_dir = (int)Math.round(angle/(2*Math.PI/numActions)) % numActions;
		
		
		// set biases
		for (int i=0; i<8; i++) biases[i] = interpolatedBias[(8+i-closest_dir) % 8];
		
		return biases;
	}
	
	
	WallData chooseNextWall(Point pos) {
		// reset old data:
		walls_considered_in_last_selection = new LinkedList<>();
		
		// find bin
		var bin = bins.get(getIndex(pos));
		if(bin==null) return null; // if no bin, return null
		
		// find N non visited walls with highest priority (priority set in visit function)
		// NOTE: queue sorted in reverse order to allow removing least important element.
		var queue = new PriorityQueue<>(wall_data_comparator);
		for(var wall : bin) 
			if( !wall.visited && !wall.visit(pos)) {
				queue.add(wall);
				if(queue.size() > max_elements) queue.poll(); // 
			}
		
		
		// store set of walls considered in this cycle's decision for debugging in display
		walls_considered_in_last_selection.addAll(queue);
		
		// Choose a random wall according to probability distribution:
		// OBS: queue is sorted in ascending priority, thus a chosen id of 0 means the last element in the queue
		int queue_size = queue.size();
		if(queue_size > 0) {
			int chosen_id = DiscreteDistribution.sample(selection_weights, queue_size);
			int remove_elements = queue_size - chosen_id;
			
			while(--remove_elements > 0) queue.poll();
			return queue.poll();
		} 
		
		return null;
		
		 
	}
	

	
	int getIndex(Vector3D pos) {
		var bx = getBinX(pos.getX());
		var by = getBinY(pos.getY());
		return  getBinId(bx, by);
	}
	
	int getIndex(Point pos) {
		var bx = getBinX(pos.getX());
		var by = getBinY(pos.getY());
		return  getBinId(bx, by);
	}
	
	int getBinId(int bin_x, int bin_y) {
		return num_bins_x * bin_y + bin_x;
	}
	
	int getBinX(double x) {
		return (x <= minx) ? 0 : (x >= maxx) ? max_bin_x : (int)Math.floor((x-minx)/bin_size);
	}
	
	int getBinY(double y) {
		return (y <= miny) ? 0 : (y >= maxy) ? max_bin_y : (int)Math.floor((y-miny)/bin_size);
	}
	
	
	
	void setBinningCoordinates(Collection<WallData> walls) {
		// Find minimum and maximum coordinates to divide space:
		minx = miny = Integer.MAX_VALUE;
		maxx = maxy = Integer.MIN_VALUE;
		for (var w_data : walls) {
			var w = w_data.wall;
			// note: as opposed to following for loop, here we do not need to ignore outer walls
			var mx = (w.x1 < w.x2 ? w.x1 : w.x2);
			if(mx < minx) minx = mx; 
			
			var Mx = (w.x1 > w.x2 ? w.x1 : w.x2);
			if(Mx > maxx) maxx = Mx;
			
			var my = (w.y1 < w.y2 ? w.y1 : w.y2);
			if(my < miny) miny = my;
			
			
			var My = (w.y1 > w.y2 ? w.y1 : w.y2);
			if(My > maxy) maxy = My;
		}
		// add buffer to min and max coordinates:
		double buffer = 0.01;
		minx-=buffer;
		miny-=buffer;
		maxx+=buffer;
		maxy+=buffer;
		
		// find number of bins and max bin:
		num_bins_x = (int)Math.ceil((maxx - minx)/bin_size);
		max_bin_x = num_bins_x -1;
		num_bins_y = (int)Math.ceil((maxy - miny)/bin_size);
		max_bin_y = num_bins_y -1;
		
		bins = new HashMap<>();
	}
	
	void addWallsToBins(Collection<WallData> walls) {
		
		
		for(var w_data : walls) {
			var w = w_data.wall;
			if(w.length > 0.5) continue; // only consider obstacles, ignore outer walls
			
			
			// find bins that are close enough to wall
			// only test bins near to the walls
			var mbx = getBinX((w.x1 < w.x2 ? w.x1 : w.x2) - bin_distance);
			var Mbx = getBinX((w.x1 > w.x2 ? w.x1 : w.x2) + bin_distance);
			var mby = getBinY((w.y1 < w.y2 ? w.y1 : w.y2) - bin_distance);
			var Mby = getBinY((w.y1 > w.y2 ? w.y1 : w.y2) + bin_distance);
			
			// iterate over bins
			// if wall close enough, add it to bin
			for(var bx = mbx; bx <= Mbx; bx++)
				for(var by = mby; by <= Mby; by++) {
					
					// get bin coordinates
					double lowerx = minx + bx*bin_size;
					double upperx = minx + (bx+1)*bin_size;
					
					double lowery = miny + by*bin_size;
					double uppery = miny + (by+1)*bin_size;
					
					// create bin polygon:
					var bin_geom = geometry_factory.createPolygon(new Coordinate[] {
							new Coordinate(lowerx, lowery),
							new Coordinate(lowerx, uppery),
							new Coordinate(upperx, uppery),
							new Coordinate(upperx, lowery),
							new Coordinate(lowerx, lowery)
					});

					// check if wall within binning distance of bin
					if(bin_geom.distance(w_data.geometry) < bin_distance) {
						// add wall to bin (make sure bin is already in hash)
						int bin_id = getBinId(bx, by);
						var bin = bins.get(bin_id);
						if(bin == null) {
							bin = new LinkedList<>();
							bins.put(bin_id, bin );
						}
						bin.add(w_data);
					}
				}


		}
	}
	
	void initializeBins(Collection<WallData> walls) {
		// place the different walls into the bins:
		setBinningCoordinates(walls);
		addWallsToBins(walls);
		
	}
	




	
	
	static GeometryFactory geometry_factory = new GeometryFactory();
	public class WallData {
		LineString geometry;
		public Wall wall;
		
		boolean visited = false;
		
		double distance = Double.POSITIVE_INFINITY; // distance to current rat position
		Coordinate  closest_point = null;
		
		WallData(Wall w){
			wall = w;
			geometry = geometry_factory.createLineString(new Coordinate[] {
					new Coordinate(w.x1, w.y1),
					new Coordinate(w.x2, w.y2)
			});
		}
		
		WallData(){
			
		}
		
		
		boolean visit(Point pos) {
			// assumes wall has not yet been visited
			visited = (distance = geometry.distance(pos)) < reward_distance;
			if(visited) {
				walls_visited_this_cycle.add(this);
				walls_visited.add(this);				
			};
			return visited;
			
		}
		
		Coordinate getClosestPoint(Point point) {
			closest_point = DistanceOp.nearestPoints(point, wall_chosen.geometry)[1];
			return closest_point;
		}
		
		@Override
		public String toString() {
			// TODO Auto-generated method stub
			return wall.toString() + ", d: " + Wall.format.format(distance);
		}
	}
	

	
}
