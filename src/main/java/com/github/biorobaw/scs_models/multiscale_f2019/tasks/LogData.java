package com.github.biorobaw.scs_models.multiscale_f2019.tasks;

import com.github.biorobaw.scs.experiment.Experiment;
import com.github.biorobaw.scs.simulation.scripts.Script;
import com.github.biorobaw.scs.utils.files.BinaryFile;
import com.github.biorobaw.scs.utils.files.XML;
import com.github.biorobaw.scs.utils.math.Floats;
import com.github.biorobaw.scs.utils.math.Integers;
import com.github.biorobaw.scs_models.multiscale_f2019.model.MultiscaleModel;

import java.io.File;
import java.util.Collection;


public class LogData implements Script {
	
	
	int numEpisodes;
	int[] startPositions;
	int[] stepsTaken;
	float[] maxDeltaV;
	String subject_id;
	
	public LogData(XML xml) {
		subject_id =xml.getAttribute("subject_id");
	}
	
	@Override
	public void newTrial() {
		numEpisodes = Experiment.get().getGlobal("trial_episodes");
		startPositions = new int[numEpisodes];
		stepsTaken = new int[numEpisodes];
		maxDeltaV  = new float[numEpisodes];

	}
	
	@Override
	public void endEpisode() {
		// Log steps taken at the end of the episode
//		System.out.println("Logging data...");
		
		var e = Experiment.get();
		int episode = e.getGlobal("episode");
		startPositions[episode] = SetInitialPosition.getStartIndex();
		stepsTaken[episode] = (int)(long)e.getGlobal("cycle");
		
		var model = (MultiscaleModel)e.getSubject(subject_id);
		maxDeltaV[episode] = model.episodeDeltaV;
		
	}
	
	
	@Override
	public void endTrial() {

		// save logs: cycles per episode, state and action values during last episode
		
		
		//	System.out.println("Saving log...");
		var e = Experiment.get();
		String logFolder = e.getGlobal("logPath").toString();
		String ratId	 = e.getGlobal("run_id").toString();
		
		//create folders
		String prefix = logFolder  +"/r" + ratId + "-";

		// SAVE SEED
		BinaryFile.saveBinaryVector(new long[] {e.getGlobal("seed")}, prefix + "seed.bin", true);

		// SAVE NUMBER OF STEPS PER EPISODE AND SHORTEST PATH:
		var steps_combined = save_number_of_steps(prefix);
		var shortest_path = save_shortest_path_distance(prefix); // returns -1 if not pre calculated

		// SAVE LEARNING TIME IF SHORTEST PATH WAS CALCULATED:
		int learning_time = save_learning_time(steps_combined, shortest_path, prefix);

		// SAVE STATE AND ACTION VALUES AFTER LAST EPISODE
		saveStateAndActionValues(prefix);

		// SAVE DUMMY FILE TO INDICATE LOG COMPLETED
		BinaryFile.saveBinaryVector(new int[]{}, prefix + "dummy.bin", true);

		// PRINT DATA (Number of place cells, final steps, total steps, shortest path, learning time, extra steps ratio):
		var model = (MultiscaleModel)Experiment.get().getSubject(subject_id);
		var final_steps = steps_combined[steps_combined.length-1];
		for(int i=0; i<model.pcs.length; i++) System.out.println("PCS(" + i +"): " + model.pcs[i].num_cells);
		System.out.println("FINAL STEPS TAKEN:  " + final_steps);
		System.out.println("TOTAL STEPS TAKEN:  " + Integers.sum(steps_combined));
		System.out.println("SHORTEST PATH:      " + shortest_path);
		System.out.println("LEARNING TIME:      " + learning_time);
		if(shortest_path!=-1)
			System.out.println("EXTRA STEPS RATIO : " + (float)(final_steps-shortest_path)/shortest_path);

	}




	int[] save_number_of_steps(String prefix){
		// OLD CODE:
		// var file = BinaryFile.openFileToWrite(prefix + "steps.bin");
		// BinaryFile.writeArray(file, startPositions,true); // we no longer store each position
		// BinaryFile.writeArray(file, stepsTaken,true); // we no longer store all steps taken
		// BinaryFile.close(file);


		// NEW CODE: save cycles per episode
		var num_positions = SetInitialPosition.getNumberOfStrartingPositions();
		var steps_combined = new int[stepsTaken.length / num_positions];
		for(int i=0; i<steps_combined.length; i++)
			steps_combined[i] = (int)Integers.sum(stepsTaken, i*num_positions, (i+1)*num_positions);
		BinaryFile.saveBinaryVector(steps_combined, prefix + "steps.bin",true);
		return steps_combined;
	}


	int save_shortest_path_distance(String prefix){
		var maze = (String)Experiment.get().getGlobal("maze");
		var distance_file = maze.replace(".xml", "_optimal_paths.bin");
		if( ! new File(distance_file).exists() ) return -1;
		var grid = new FloatGrid(distance_file, 5, 0);
		var combined_shortest_paths = (int)Floats.sum(grid.getElements(SetInitialPosition.positions));
		BinaryFile.saveBinaryVector(new int[] {combined_shortest_paths}, prefix + "shortest_path.bin", true);
		return combined_shortest_paths;
	}

	int save_learning_time(int[] steps_combined, int shortest_path, String prefix) {
		if(shortest_path == -1) return -1;
		int episodes = 0;
		for( var steps : steps_combined){
			episodes++;
			if(steps < 2*shortest_path) break; // first episode where extra steps ratio is smaller than 1
		}
		BinaryFile.saveBinaryVector(new int[] {episodes}, prefix + "learning_time.bin", true);
		return episodes;
	}


	void saveStateAndActionValues(String prefix){
		var model = (MultiscaleModel)Experiment.get().getSubject(subject_id);
		var numActions = model.numActions;
		for(int i=0; i<model.num_layers; i++) {
			int num_pcs = model.vTable[i].length;
			BinaryFile.saveBinaryVector(model.vTable[i], prefix + "V" + i+ ".bin", true);
			BinaryFile.saveBinaryMatrix(model.qTable[i], num_pcs, numActions , prefix + "Q" + i+ ".bin", true);
		}

		// save deltaV
		// BinaryFile.saveBinaryVector(maxDeltaV, prefix + "deltaV.bin", true);
	}


	static class FloatGrid {

		float[] data;
		float min_x, min_y, precision;
		int num_x, num_y;


		/**
		 * Reads a grid of floats from a binary file
		 * @param binary_file binary file with floating point numbers storing the grid
		 * @param data_skip   number of floats to skip from the start of the file before reading the dimensions
		 * @param dimension_skip number of floats to skip from the start of the file before reading the grid elements
		 */
		FloatGrid(String binary_file, int data_skip, int dimension_skip) {
			var dimensions = BinaryFile.readFloats(binary_file, 5, dimension_skip, true);
			min_x = dimensions[0];
			num_x = (int)dimensions[1];
			min_y = dimensions[2];
			num_y = (int)dimensions[3];
			precision = dimensions[4];
			data = BinaryFile.readFloats(binary_file, num_x*num_y, data_skip, true);
		}

		float getElement(float x, float y){
			var j = (int)Math.floor( (x - min_x) / precision);
			var i = (int)Math.floor( (y - min_y) / precision);

			var id = i*num_x + j;
			return data[id];
		}

		float[] getElements(Collection<Float[]> xy_positions){
			float[] elements = new float[xy_positions.size()];
			int i = 0;
			for(var xy : xy_positions) elements[i++] = getElement(xy[0], xy[1]);
			return elements;
		}

	}
	
	
	
}
