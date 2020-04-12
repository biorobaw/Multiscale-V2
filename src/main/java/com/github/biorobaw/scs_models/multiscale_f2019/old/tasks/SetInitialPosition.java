package com.github.biorobaw.scs_models.multiscale_f2019.old.tasks;

import java.util.ArrayList;
import java.util.stream.IntStream;

import org.apache.commons.math3.geometry.euclidean.threed.Vector3D;

import com.github.biorobaw.scs.experiment.Experiment;
import com.github.biorobaw.scs.simulation.object.RobotProxy;
import com.github.biorobaw.scs.simulation.scripts.Script;
import com.github.biorobaw.scs.utils.files.XML;
import com.github.biorobaw.scs.utils.math.RandomSingleton;


public class SetInitialPosition implements Script{
	
	static ArrayList<Float[]> positions = new ArrayList<>();

	static int[] permutation;
	static int currentPos = -1;
	
	RobotProxy robot = null;
	
	public SetInitialPosition(XML params) {
		if(positions.size()!=0) return;
		String mazeFile = Experiment.get().getGlobal("maze");
		var xml = new XML(mazeFile);
		for(var p : xml.getChild("startPositions").getChildren()) {
			positions.add(new Float[] {p.getFloatAttribute("x"),
									   p.getFloatAttribute("y"),
									   p.getFloatAttribute("w")});
		}
		
		robot = Experiment.get()
						  .subjects
						  .get(params.getAttribute("subject_id"))
						  .getRobot()
						  .getRobotProxy();
		
	}
	
	@Override
	public void newEpisode() {
		//move current position
		currentPos = (currentPos+1) % positions.size();
		
		//if at start of new cycle, generate new random permutation
		if(currentPos==0) permutation = generatePermutation(positions.size());
		
		// set the position
		var pos = positions.get(getStartIndex());
		robot.setPosition(new Vector3D(pos[0],pos[1],0));
		robot.setOrientation2D(pos[2]);


	}
	
	static public int getStartIndex() {
		return permutation[currentPos];
	}

	static private int[] generatePermutation(int size) {
		var random = RandomSingleton.getInstance();
		var perm = IntStream.range(0, size).toArray();
		for(int i=size-1; i>0 ;i--) {
			int j = random.nextInt(i+1);
			var aux = perm[i];
			perm[i] = perm[j];
			perm[j] = aux;
		}
		//System.out.println("Perm: " + perm[0] + " " + perm[1]);
		//System.out.println("Positions: " + currentPos + "/" + positions.size());
		return perm;
	}
}
