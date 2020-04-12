package com.github.biorobaw.scs_models.multiscale_f2019.old.model.modules.a_input;



import java.util.Set;

import org.apache.commons.math3.geometry.euclidean.threed.Vector3D;

import com.github.biorobaw.scs.experiment.Experiment;
import com.github.biorobaw.scs.robot.Robot;
import com.github.biorobaw.scs.simulation.object.maze_elements.walls.AbstractWall;
import com.github.biorobaw.scs.simulation.object.maze_elements.walls.Wall;
import com.vividsolutions.jts.geom.Coordinate;
import com.vividsolutions.jts.geom.LineSegment;

//import edu.usf.experiment.robot.AbsoluteDirectionRobot;
//import edu.usf.experiment.robot.Robot;
//import edu.usf.experiment.robot.affordance.Affordance;
//import edu.usf.experiment.robot.affordance.AffordanceRobot;
//import edu.usf.vlwsim.robot.AbsoluteDirectionVirtualRobot;
//import edu.usf.vlwsim.robot.VirtualRobot;
//import edu.usf.vlwsim.universe.VirtUniverse;
import edu.usf.micronsl.module.Module;
import edu.usf.micronsl.port.onedimensional.array.Float1dPortArray;

/**
 * Module that sets the probability of an action to 0 if the action can not be performed
 * It assumes actions are allocentric,  distributed uniformly in the range [0,2pi]
 * @author biorob
 * 
 */
public class DistancesInputModule extends Module {
	
	public float[] distances;
	public float[] angles;
	float maxDistance;

	private Robot robot;

	
	public DistancesInputModule(String name,Robot robot, int numActions,float maxDistance){
		super(name);
		angles = new float[numActions];
		for(int i= 0; i<numActions ; i++) angles[i]= (float)(2*Math.PI/numActions*i);
		distances =new float[angles.length];
		
		this.addOutPort("distances", new Float1dPortArray(this, distances));
		this.robot = robot;
		this.maxDistance = maxDistance;
		
	}
	
	public DistancesInputModule(String name, Robot robot, float[] angles,float maxDistance) {
		super(name);
		this.angles = angles;
		distances =new float[angles.length];
		
		this.addOutPort("distances", new Float1dPortArray(this, distances));
		this.robot = robot;
		this.maxDistance = maxDistance;
	}

	
	public void run() {
		for(int i=0;i<angles.length;i++) distances[i] = getDistance(angles[i],maxDistance);
		
	}


	@Override
	public boolean usesRandom() {
		return false;
	}
	
	
	float getDistance(float direction,float maxDistance) {
		var walls = Experiment.get().getMaze().walls;
		return distanceToNearestWall(walls, robot.getRobotProxy().getPosition() ,direction, maxDistance);
	}
	
	public static float distanceToNearestWall(Set<AbstractWall> walls, Vector3D robotPos, float angle, float distance) {
		var dx = (float)Math.cos(angle)*distance;
		var dy = (float)Math.sin(angle)*distance;
		return (float) distanceToNearestWall(walls, robotPos, dx, dy, distance);
	}
	
	public static double distanceToNearestWall(Set<AbstractWall> walls, Vector3D pos, float dx, float dy, float maxDistance) {
		
		Coordinate initCoordinate = new Coordinate(pos.getX(), pos.getY());
		Coordinate finalCoordinate = new Coordinate(pos.getX() + dx, pos.getY() + dy);

		double minDistance = maxDistance;
		LineSegment path = new LineSegment(initCoordinate, finalCoordinate);
		double distance;
		for (var w_abstract : walls) {
			Wall wall = (Wall)w_abstract;
			
			var s = new LineSegment(new Coordinate(wall.x1, wall.y1),
								    new Coordinate(wall.x2, wall.y2));
			distance = path.distance(s);
			
			if(distance < 0.001) {
				//segments do not intersect but a wall ends at a distance of 0.01 of the ray,
				//assuming it does intersect
				Coordinate[] closest = path.closestPoints(s);
				for(var c : closest) {
					if( (distance = initCoordinate.distance(c)) < minDistance )
						minDistance = distance;
				}
				
			}
			
		}

		return minDistance;
	}
	
	
}
