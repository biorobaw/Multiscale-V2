package com.github.biorobaw.scs_models.multiscale_f2019.model;




import com.github.biorobaw.scs.experiment.Experiment;
import com.github.biorobaw.scs.experiment.Subject;
import com.github.biorobaw.scs.gui.displays.DisplaySwing;
import com.github.biorobaw.scs.robot.commands.TranslateXY;
import com.github.biorobaw.scs.robot.modules.FeederModule;
import com.github.biorobaw.scs.robot.modules.localization.SlamModule;
import com.github.biorobaw.scs.simulation.SimulationControl;
import com.github.biorobaw.scs.utils.Debug;
import com.github.biorobaw.scs.utils.files.BinaryFile;
import com.github.biorobaw.scs.utils.files.XML;
import com.github.biorobaw.scs.utils.math.DiscreteDistribution;
import com.github.biorobaw.scs.utils.math.Floats;
import com.github.biorobaw.scs.utils.math.RandomSingleton;
import com.github.biorobaw.scs_models.multiscale_f2019.gui.fx.GUI;
import com.github.biorobaw.scs_models.multiscale_f2019.model.modules.a_input.Affordances;
import com.github.biorobaw.scs_models.multiscale_f2019.model.modules.b_state.EligibilityTraces;
import com.github.biorobaw.scs_models.multiscale_f2019.model.modules.b_state.PlaceCellBins;
import com.github.biorobaw.scs_models.multiscale_f2019.model.modules.b_state.PlaceCells;
import com.github.biorobaw.scs_models.multiscale_f2019.model.modules.b_state.QTraces;
import com.github.biorobaw.scs_models.multiscale_f2019.model.modules.c_rl.ObstacleBiases;
import com.github.biorobaw.scs_models.multiscale_f2019.model.modules.d_action.MotionBias;
import com.github.biorobaw.scs_models.multiscale_f2019.robot.modules.distance_sensing.MySCSDistanceSensor;
import org.apache.commons.math3.geometry.euclidean.threed.Vector3D;

import java.util.Random;
import java.util.Vector;

public class MultiscaleModel extends Subject{

	// Model Parameters: Place cells
	public float[] pc_generation_threshold;
	public String pc_generation_method;
	public boolean pc_generation_active_layers_only;

	// Model Parameters: RL
	public float[] v_traceDecay;
	public float[] q_traceDecay;
	public float[] v_learningRate;
	public float[] q_learningRate;
	public float discountFactor;
	public float foodReward;
	public int num_layers;

	// Model Parameters: Action Space
	public int numActions;
	public float certainty_threshold;

	// Model Parameters: Wall Bias option
	final int obstacle_bias_method; // 1 = wall reward, 2 = bias to closest elements


	// Model Variables: input
	public SlamModule slam;
	public FeederModule feederModule;
	public ObstacleBiases obstacle_biases;
	public MySCSDistanceSensor distance_sensors;
	
	
	// Model Variables: state
	public boolean independent_pcs;
	public PlaceCells[] pcs;
	public PlaceCellBins[] pc_bins;
	public PCgereratorInterface pc_generator;
	public float[] pc_modulator_array;
	public PCmodulationInterface pc_modulator;
	public float[] layer_radii = null;
	
	public EligibilityTraces[] vTraces;
	public QTraces[] qTraces;
	
	// Model Variables: RL
	public float[][] vTable;	// v[layer][pc]
	public float[][] vTableCopy; // a copy made to compare changes between start and end of episode
	public float     episodeDeltaV; // max abs difference between vTable and vTableCopy
	public float[][][] qTable;  // q[layer][pc][action]
	public float[] qValues;
	
	// Model Variables: action selection
	public Affordances affordances;
	public MotionBias motionBias;   // Module to add bias to probabilities
	public float[] softmax;  // probability after applying softmax
	public float[] possible; // probability after applying affordances
	public float[] action_selection_probs;
	public int chosenAction;
	private float[] learning_dist;

	Random random = RandomSingleton.getInstance();
	
	// GUI
	com.github.biorobaw.scs_models.multiscale_f2019.gui.swing.GUI gui_old;
	GUI gui;
	private float[] aff_values;


	public MultiscaleModel(XML xml) {
		super(xml);
		
		// ======== GENERAL PARAMETERS ===============

		numActions = xml.getIntAttribute("numActions");
		float mazeWidth = xml.getFloatAttribute("mazeWidth");
		float mazeHeight = xml.getFloatAttribute("mazeHeight");

		// ======== MODEL INPUT ======================
		
		// get robot modules
		slam = robot.getModule("slam");
		feederModule = robot.getModule("FeederModule");
		distance_sensors = robot.getModule("distance_sensors");
		
		
		//Create affordances / distance sensing module
		affordances = new Affordances( robot, numActions, 0.1f);
		
		// Joystick module for testing purposes:
		// joystick = new JoystickModule();
		
		// ======== MODEL STATE =======================

		independent_pcs = xml.getBooleanAttribute("independent_pcs");

		var pc_bin_size  = xml.getFloatAttribute("pc_bin_size");
		pcs = PlaceCells.load(xml);
		num_layers = pcs.length;
		
		pc_bins = new PlaceCellBins[num_layers];
		for(int i=0; i<num_layers; i++)
			pc_bins[i] = new PlaceCellBins(pcs[i], -1.15f ,1.15f, -1.55f, 1.55f, pc_bin_size );

		// pc generation model:
		pc_generation_threshold  = xml.getFloatArrayAttribute("pc_generation_threshold");
		pc_generation_method = xml.getAttribute("pc_generation_method");
		pc_generation_active_layers_only = xml.getBooleanAttribute("pc_generation_active_layers_only");
		System.out.println("PC generation method: " + pc_generation_method);
		System.out.println("PC generation threshold: "+ Floats.toString(pc_generation_threshold) );
		pc_generator = switch(pc_generation_method) {
			case "none" -> ((layer, closest_subgoal) -> 0f);
			case "layer" -> {
				System.out.println("PC generation radii: " + xml.getAttribute("pc_generation_radii"));
				layer_radii = xml.getFloatArrayAttribute("pc_generation_radii");
				yield ((layer, closest_subgoal) -> layer_radii[layer]);
			}
			case "subgoal" -> {
				System.out.println("PC GEN METHOD NOT YET IMPLEMENTED");
				System.exit(-1);
				yield ((layer, closest_subgoal) -> 0f);
			}
			default -> {
				System.out.println("ERROR: PC Generation method does not exist");
				System.exit(-1);
				yield ((layer, closest_subgoal) -> 0f);
			}
		};

		// PC layer modulation:
		var pc_modulation_method = xml.getAttribute("pc_modulation_method");
		System.out.println("PC modulation method: " + pc_modulation_method);
		pc_modulator_array = Floats.constant(1, pcs.length); // Default modulator values
		pc_modulator = choose_modulation_method(pc_modulation_method);
		
		// ======== TRACES =============================
		
		v_traceDecay = xml.getFloatArrayAttribute("v_traces");
		q_traceDecay = xml.getFloatArrayAttribute("q_traces");
		
		vTraces = new EligibilityTraces[num_layers];
		qTraces = new QTraces[num_layers];
		
		
		// need to find average number of active place cells:
//		float average_active_pcs = 0;
//		for (var bins : pc_bins) average_active_pcs += bins.averageBinSize;
//		System.out.println("average active pcs: " + average_active_pcs);


		//  create traces
		for(int i=0; i<num_layers; i++) {
			// choose min trace threshold (traces below the threshold are set to 0)
//			float v_min = (float)Math.pow(v_traceDecay[i], 3) / average_active_pcs;
//			float q_min = (float)Math.pow(q_traceDecay[i], 3) / average_active_pcs;
//			System.out.println("min activation layer "+ i + " : " + v_min);

//			vTraces[i] = new EligibilityTraces(1, pcs[i].num_cells, v_traceDecay[i], v_min);
//			qTraces[i] = new QTraces(numActions, pcs[i].num_cells, q_traceDecay[i], q_min);
			
			vTraces[i] = new EligibilityTraces(1, pcs[i].num_cells, v_traceDecay[i], 0.0001f);
			qTraces[i] = new QTraces(numActions, pcs[i].num_cells, q_traceDecay[i], 0.0001f);
		}
		
		// ======== REINFORCEMENT LEARNING ===========
		
		boolean load_model	= xml.hasAttribute("load_model") && xml.getBooleanAttribute("load_model");
		v_learningRate 		= xml.getFloatArrayAttribute("v_learningRate");
		q_learningRate 		= xml.getFloatArrayAttribute("q_learningRate");
		discountFactor 		= xml.getFloatAttribute("discountFactor");
		foodReward 	   		= xml.getFloatAttribute("foodReward");
		
		vTable = new float[num_layers][];
		vTableCopy = new float[num_layers][];
		qTable = new float[num_layers][][];
		qValues = new float[numActions];
		
		
		for(int i=0; i<num_layers; i++) {
			
			if(!load_model) {
				vTable[i] = new float[pcs[i].num_cells];
				qTable[i] = new float[pcs[i].num_cells][numActions];
				
			} else {
				
				var e = Experiment.get();
				String logFolder   = e.getGlobal("logPath").toString();
				String ratId	   = e.getGlobal("run_id").toString();
				String save_prefix = logFolder  +"/r" + ratId + "-";
//				System.out.println(save_prefix);
				vTable[i] = BinaryFile.loadFloatVector(save_prefix + "V" + i+ ".bin", true);
				qTable[i] = BinaryFile.loadMatrix(save_prefix + "Q" + i+ ".bin", true);				
				
			}
			
		}
		
		
		// ======== ACTION SELECTION =======================

		certainty_threshold 		= xml.getFloatAttribute("certainty_threshold");
		var wall_selection_weights 	= xml.getFloatArrayAttribute("wall_selection_weights");
		int numStartingPositions 	= Integer.parseInt(Experiment.get().getGlobal("numStartingPositions"));
		motionBias 				= new MotionBias(numActions, 50*numStartingPositions);
		softmax 				= new float[numActions];
		possible 				= new float[numActions];
		action_selection_probs 	= new float[numActions];

		
		
		obstacle_bias_method = xml.getIntAttribute("wall_bias_method");
		float wall_reached_distance = xml.getFloatAttribute("wall_reached_distance");
		float wall_reward = xml.getFloatAttribute("wall_reward");
		float bin_distance = obstacle_bias_method == 1 ? wall_reached_distance : xml.getFloatAttribute("wall_detection_distance"); 
		float bin_size = 0.1f;
		obstacle_biases = new ObstacleBiases(bin_size, bin_distance, wall_reached_distance, wall_reward, wall_selection_weights); // bin size, bin_distance, reward distance, reward value
		
		
		// ======== GUI ====================================
		
		if(Experiment.get().display instanceof DisplaySwing) {
			gui_old = new com.github.biorobaw.scs_models.multiscale_f2019.gui.swing.GUI(this);
		} else gui = new GUI(this);

	}

	static public long cycles = 0;
	static final int num_tics = 10;
	static public long[]  tics= new long[num_tics];
	static public float[]  tocs= new float[num_tics];
	static public float[] averages=new float[num_tics];
	

	
	@Override
	public long runModel() {
		cycles++;
		
		
		// ==================== DEBUG =================================
		
//		int debug_episode = 80000;
//		long debug_cycle  = 7;
//		int episode = (Integer)Experiment.get().getGlobal("episode");
//		long cycle = (Long)Experiment.get().getGlobal("cycle");
//		
//		boolean is_debug_episode =  episode == debug_episode;
//		boolean is_debug_cycle = is_debug_episode &&  cycle == debug_cycle;
//		boolean is_above_debug_cycle = is_debug_episode && cycle >= debug_cycle;

//		if(is_debug_cycle) {
//			System.out.println("cycle: " + cycles);
//			simulationPauseAndPaint();
//		}
		
		// ================= END DEBUG =================================
		
		
		// profile full code
		tics[tics.length-1] = Debug.tic();
		
		// GET ROBOT INPUTS
		tics[0] = Debug.tic();
		inputs.get();
		tocs[0] = Debug.toc(tics[0]);


		// CALCULATE CURRENT STATE
		tics[1] = Debug.tic();
		updatePlaceCells();
		tocs[1] = Debug.toc(tics[1]);





		// UPDATE RL WEIGHTS AND CALCULATE Q VALUES
		tics[2] = Debug.tic();
		if(independent_pcs) independent_cells_update(inputs.reward);
		else regular_rl_update(inputs.reward);
		tocs[2] = Debug.toc(tics[2]);


		// PERFORM ACTION SELECTION
		actionSelection();


		
		// UPDATE TRACES
		tics[5] = Debug.tic();
		for(int i=0; i<num_layers; i++) {
			var pcs = pc_bins[i].active_pcs;
			vTraces[i].update(pcs.ns, pcs.ids, 0);
			qTraces[i].update(pcs.ns, pcs.ids, chosenAction, learning_dist);
//			System.out.println("num non zero pcs: " + pcs.ids.length);
//			System.out.println("m,M Pc: " + Floats.min(pcs.ns) + " " + Floats.max(pcs.ns) );
//			System.out.println("m,M T: " + Floats.min(vTraces[i].traces[0]) + " " + Floats.max(vTraces[i].traces[0]));
		}
		
		// PERFROM ACTION
		double tita = 2*Math.PI/numActions*chosenAction;
		robot.getRobotProxy().send_command(new TranslateXY(0.08f*(float)Math.cos(tita), 0.08f*(float)Math.sin(tita)));
		feederModule.eatAfterMotion();
		tocs[5] = Debug.toc(tics[5]);


		// PROFILING CODE:
		tocs[tocs.length-1] = Debug.toc(tics[tocs.length-1]);
		if(cycles==1) {
			Floats.copy(tocs,averages);
		} else {
			Floats.mul(averages, 0.95f, averages);
			Floats.add(averages, Floats.mul(tocs, 0.05f), averages);
		}

//		var percentual = Floats.div(averages, averages[tocs.length-1]/100f);
//		System.out.println("instants: "+ Arrays.toString(tocs));
//		System.out.println("averages: "+ Arrays.toString(averages));
//		System.out.println("percentual:"+ Arrays.toString(percentual));
		
//		debug();
		return 0;
	}

	private void simulationPauseAndDisplay() {
		// This is old code - might need reviewing
		var old_value = Experiment.get().display.setSync(true);
		Experiment.get().display.updateData();
		Experiment.get().display.repaint();
		Experiment.get().display.setSync(old_value);
		SimulationControl.setPause(true);
	}

	@Override
	public void newEpisode() {
		super.newEpisode();
		motionBias.newEpisode();
		obstacle_biases.newEpisode();
		
		for(int i=0; i<num_layers; i++) {
			vTraces[i].clear();
			qTraces[i].clear();
			pc_bins[i].clear();
		}
	
		chosenAction = -1;

		
		// copy state values to measure changes per episode:
		for(int i=0; i < num_layers; i++)
			vTableCopy[i] = Floats.copy(vTable[i]);
				
	}
	
	@Override
	public void endEpisode() {
		super.endEpisode();
		
		// print tocs:
//		System.out.println("Episode: " + Experiment.get().getGlobal("episode"));
//		var percentual = Floats.div(averages, averages[tocs.length-1]/100f);
//		System.out.println("instants: "+ Arrays.toString(tocs));
//		System.out.println("averages: "+ Arrays.toString(averages));
//		System.out.println("percentual:"+ Arrays.toString(percentual));
		
		episodeDeltaV = 0;
		for(int i=0; i < num_layers; i++) {
			var dif = Floats.sub(vTable[i], vTableCopy[i]);
			episodeDeltaV = Math.max(episodeDeltaV, Floats.max(Floats.abs(dif,dif)));
			
		}
		
		// DEBUG CODE BLOCK
//		if(episodeDeltaV > 1) {
//			System.out.println("" + Experiment.get().getGlobal("episode")
//					+ ", " + cell_id
//					+ ": " + episodeDeltaV);
//			System.out.println("ERROR: DeltaV = " + episodeDeltaV);
//			System.out.println("At episode: " + Experiment.get().getGlobal("episode"));
//			System.exit(-1);
//			SimulationControl.togglePause();
//		}
//		System.out.println(episodeDeltaV);
		
	}
	
	@Override
	public void newTrial() {
		super.newTrial();
		obstacle_biases.newTrial();
		motionBias.newTrial();
		
	}
	
	@Override
	public void endTrial() {
		super.endTrial();
	}
	
	@Override
	public void newExperiment() {
		super.newExperiment();
	}
	
	@Override
	public void endExperiment() {
		super.endExperiment();

	}
	
	int angle_to_index(float angle) {
		double dtita = Math.PI*2 / numActions;
		var res = (int)Math.round(angle/dtita) % numActions;
		return res < 0 ? res + numActions : res;
	}
	
	void addMultiplicativeBias(float[] bias, float[] input, float[] output) {
		Floats.mul(bias, input, output);
		var sum = Floats.sum(output);
		
		if(sum!=0) Floats.div(output, sum, output);
		else {
			System.err.println("WARNING: Probability sum is 0, setting uniform distribution (MultiscaleModel.java)");
			for(int i=0; i<numActions; i++) output[i] = 1.0f/numActions;
		}
	}
	
	float[] addMultiplicativeBias(float[] bias, float[] input) {
		var output = Floats.mul(bias, input);
		var sum = Floats.sum(output);
		
		if(sum!=0) Floats.div(output, sum, output);
		else {
			System.err.println("WARNING: Probability sum is 0, setting uniform distribution (MulytiscaleModel.java)");
			Floats.uniform(output);			
		}
		return output;
	}


	interface PCgereratorInterface {
		float choose_radius(int layer, float closest_subgoal);
	}

	interface PCmodulationInterface {
		void calculate_layer_modulators(float closest_subgoal_distance);
	}


	ModelInputs inputs = new ModelInputs();
	class ModelInputs {

		private Vector3D pos = null;
		private float orientation;
		private float reward;
		private float[] distances;
		private float distance_to_closest_subgoal;

		void get() {
			pos = slam.getPosition();
			orientation = slam.getOrientation2D();
			reward = feederModule.ate() ? foodReward : 0f;

			// obstacle_bias_method 1 gives a reward for reaching walls
			if(obstacle_bias_method == 1)
				if(reward == 0) {
					reward = obstacle_biases.getReward(pos);
//				if (reward > 0) System.out.println(cycles + "Wall reward: " + reward);
				}

			// get alocentric distances from egocentric measures:
			float[] ego_distances = distance_sensors.getDistances();
			distances = new float[numActions];
			int id0 = angle_to_index(orientation);
			for(int i=0; i<numActions; i++) {
				distances[i] = ego_distances[(i + id0) % numActions];
			}
			distance_to_closest_subgoal = distance_sensors.getDistanceToClosestSubgoal();
		}
	}

	void updatePlaceCells(){
		var pos = inputs.pos;
		var distance_to_closest_subgoal = inputs.distance_to_closest_subgoal;

		pc_modulator.calculate_layer_modulators(distance_to_closest_subgoal);
		float totalActivity =0;
		for(int i=0; i<num_layers; i++) {

			// save old state:
			var bins_i = pc_bins[i];
			bins_i.storeOldBin();

			// If there are no pcs with activity above threshold, create a new pc
			var modulator = pc_modulator_array[i];
			var max_active = bins_i.activateBin((float) pos.getX(), (float) pos.getY(), modulator);
			if( max_active < pc_generation_threshold[i] && (!pc_generation_active_layers_only || modulator > 0) ) {
				addCellToLayer(i, (float)pos.getX(), (float)pos.getY(), distance_to_closest_subgoal, 0, Floats.constant(0,numActions));
				bins_i.activateBin((float) pos.getX(), (float) pos.getY(), modulator) ;
			}
			totalActivity += pc_bins[i].active_pcs.total_a;
		}
		for(int i=0; i<num_layers; i++) pc_bins[i].active_pcs.normalize(totalActivity);
	}

	void addCellToLayer(int layer, float x, float y, float closest_subgoal, float initial_v, float[] initial_q ){

		// TODO: as pcs are now generated incrementally, current data structures are very inefficient.
		// Note: this does not seem to have a great impact on the code, but it does on the gui

		// Choose x, y, r and id
		float r = pc_generator.choose_radius(layer, closest_subgoal);
		int id = pcs[layer].num_cells;

		// Add cell to layer and bins
		pcs[layer].addCell(id, x, y, r);
		pc_bins[layer].addCell(id, x, y, r);

		// Associate v value to cell (add entry in the copy as well)
		vTable[layer] = Floats.concat(vTable[layer], initial_v);
		vTableCopy[layer] = Floats.concat(vTableCopy[layer], 0);
		var old_qlayer = qTable[layer];

		// Associate q values to place cell
		qTable[layer] = new float[old_qlayer.length+1][numActions];
		for(int i=0; i< old_qlayer.length; i++)
			Floats.copy(old_qlayer[i], qTable[layer][i]);

		for(int j=0; j < numActions; j++)
			Floats.copy(initial_q, qTable[layer][old_qlayer.length]);

		// Add v and q traces
		vTraces[layer].addTrace();
		qTraces[layer].addTrace();

	}


	void regular_rl_update(float reward){
//		System.out.println("Regular update");
		// IF NOT FIRST CYCLE, UPDATE RL WEGIHTS
		if(chosenAction!=-1) {
			// calculate bootstraps
			float bootstrap = reward;
			if(reward==0 ) {
				// only calculate next state value if non terminal state
				float value = 0;
				for(int i=0; i<num_layers; i++) {
					value += calculate_V(pc_bins[i].active_pcs, vTable[i]);
				}
				bootstrap+= value*discountFactor;
			}

			// calculate old value:
			float old_value = 0;
			for(int i=0; i<num_layers; i++) {
				old_value += calculate_V(pc_bins[i].previous_pcs, vTable[i]);
			}

			// calculate rl error
			float error = bootstrap - old_value;

			// update RL
			for(int i=0; i<num_layers; i++) {
				// update V
				// v = v + error*learning_rate*trace
				var traces = vTraces[i].traces[0];
				for(var id : vTraces[i].non_zero[0]) {
					vTable[i][id] +=  v_learningRate[i]*traces[id]*error;
				}

				// update Q
				for(int j=0; j<numActions; j++) {
					traces = qTraces[i].traces[j];
					for(var id : qTraces[i].non_zero)
						qTable[i][id][j] += q_learningRate[i]*traces[id]*error;
				}
			}
		}

		// CALCULATE Q VALUES:
		tics[3] = Debug.tic();
		qValues = new float[numActions];
		for(int i=0; i<num_layers; i++) {
			var pcs = pc_bins[i].active_pcs;
			var ids = pcs.ids;

			for(int j=0; j<pcs.num_cells; j++) {
				for(int k=0; k<numActions; k++)
					qValues[k]+= qTable[i][ids[j]][k]*pcs.ns[j];
			}
		}
		tocs[3] = Debug.toc(tics[3]);

	}

	Vector<Float> non_zero_activations = new Vector<>();
	Vector<Float> non_zero_values = new Vector<>();
	void add_nonzero_pcs(PlaceCells layer, float[] values){
		for (int i = 0; i < layer.num_cells; i++) {
			if (layer.as[i] != 0) {
				non_zero_activations.add(layer.as[i]);
				non_zero_values.add(values[layer.ids[i]]);
			}
		}
	}


	float sample_value(int samples){
		float value = 0;
		float total_a = 0;
		for(int i=0; i <samples; i++){
			int id = random.nextInt(non_zero_activations.size());
			var a = non_zero_activations.get(id);
			value += (a * non_zero_values.get(id));
			total_a += a;
		}
		return value/total_a;
	}

	void independent_cells_update(float reward){
		// NOTE: this method is experimental

//		System.out.println("Independent update");
		// IF NOT FI RST CY CLE, UPDATE RL WEGIHTS
		if(chosenAction!=-1) {

			float full_bootstrap = reward;
			if(reward==0 ) {
				// only calculate next state value if non terminal state
				float value = 0;
				for(int i=0; i<num_layers; i++) {
					value += calculate_V(pc_bins[i].active_pcs, vTable[i]);
				}
				full_bootstrap+= value*discountFactor;
			}


			// calculate old value:
			float old_value = 0;
			for(int i=0; i<num_layers; i++) {
				old_value += calculate_V(pc_bins[i].previous_pcs, vTable[i]);
			}

			// calculate rl error
			float full_error = full_bootstrap - old_value;



			// GET ARRAY OF NON ZERO TO SAMPLE indices
			// NOTE: WE MAY PREFER TO DO THIS PER LAYER
			non_zero_activations.clear();
			non_zero_values.clear();
			for(int l=0; l<num_layers; l++) {
				add_nonzero_pcs(pc_bins[l].active_pcs, vTable[l]);
			}
//			System.out.println(non_zero_activations.size());


			// sample_bootstrap
			var constant_bootstrap= reward;
			if(reward==0 ) {
				constant_bootstrap += (discountFactor * sample_value(5));
			}

			// FOR EACH ACTIVE CELL IN PREVIOUS CYCLE:
			for(int l=0; l<num_layers; l++){
				var pcs_l = pc_bins[l].previous_pcs;
				var values_l = vTable[l];

				for(int i=0; i<pcs_l.num_cells; i++){
					var activation_i = pcs_l.as[i];
					if(activation_i==0) continue;
					var id_i = pcs_l.ids[i];

					// ESTIMATE BOOTSTRAP (if non terminal state)
					var bootstrap= reward;
					if(reward==0 ) {
						bootstrap += (discountFactor * sample_value(5));
					}
					var rl_error = bootstrap-values_l[id_i];

					// UPDATE VALUES
//					values_l[id_i] +=  v_learningRate[l]*pcs_l.ns[i]*(full_bootstrap - old_value); // regular RL
					values_l[id_i] +=  0.4*pcs_l.as[i]*(bootstrap - values_l[id_i]); // independent



					// update Q
//					var cell_policy = Floats.softmax(qTable[l][id_i]);
					var cell_policy = Floats.softmaxWithWeights(qTable[l][id_i], aff_values);
					for(int j=0; j<numActions; j++) {
						var traces = qTraces[l].traces[j]; // note traces are sorted first by action then by pc
//						qTable[l][id_i][j] += q_learningRate[l]*traces[id_i]*(full_bootstrap - old_value);
						var delta_ij = j == chosenAction ? 1 : 0;
						var normalizer = 1;//cell_policy[j]/learning_dist[j];// Math.min(cell_policy[j]/learning_dist[j], 0.1);
//						System.out.println("normalizer: " + normalizer)
//						qTable[l][id_i][j] += q_learningRate[l]*(full_bootstrap - old_value) * (delta_ij-learning_dist[j]) * pcs_l.ns[i];
						qTable[l][id_i][j] += 0.4*normalizer*(delta_ij-learning_dist[j])*( bootstrap - values_l[id_i]) * pcs_l.as[i];
					}

				}

			}

		}

//		// CALCULATE Q VALUES:
//		tics[3] = Debug.tic();
//		qValues = new float[numActions];
//		for(int i=0; i<num_layers; i++) {
//			var pcs = pc_bins[i].active_pcs;
//			var ids = pcs.ids;
//
//			for(int j=0; j<pcs.num_cells; j++) {
//				for(int k=0; k<numActions; k++)
//					qValues[k]+= qTable[i][ids[j]][k]*pcs.ns[j];
//			}
//		}
//		tocs[3] = Debug.toc(tics[3]);

		// Calculate the softmax for each cell, then average results
		// NOTE: we could actually avoid computing the average for each cell
		// if instead we choose a random cell based on probabilities pcs.ns[i]
		Floats.constant(0, softmax);
		var cell_soft_max = Floats.constant(0, numActions);
		for(int l=0; l<num_layers; l++) {
			var pcs = pc_bins[l].active_pcs;
			var ids = pcs.ids;

			for(int i=0; i<pcs.num_cells; i++) {
				int j_i = pcs.ids[i];
				Floats.softmaxWithWeights(qTable[l][j_i], aff_values, cell_soft_max);
				Floats.mul(cell_soft_max, pcs.ns[i], cell_soft_max);
				Floats.add(cell_soft_max,softmax,softmax);
			}
		}
		tocs[3] = Debug.toc(tics[3]);


	}


	void actionSelection(){

		tics[4] = Debug.tic();
//		System.out.println(Arrays.toString(qValues));
		aff_values = affordances.calculateAffordances(inputs.distances);

		// METHOD 1
//		Floats.softmax(qValues, softmax);
//		Floats.mul(softmax, aff_values, possible);
//		var p_sum = Floats.sum(possible);
//		if(p_sum == 0 ) Floats.div(aff_values, Floats.sum(aff_values), possible);
//		else Floats.div(possible, p_sum, possible);
//		var biased = motionBias.addBias(chosenAction, possible);
//		learning_dist = softmax;

		// METHOD 2, get soft max then calculate certainty:
		if(!independent_pcs) Floats.softmaxWithWeights(qValues, aff_values, softmax);
		float non_zero = Floats.sum(aff_values);
		float certainty = 1 - Floats.entropy(softmax, non_zero > 1 ? non_zero : 2f);


		// If Q policy is not certain enough, use bias, else, don't use it
//		System.out.prin tln("Certainty: " + certainty );
		if(certainty < certainty_threshold ) {

			// calculate motion bias
			var bias_motion = motionBias.calculateBias(chosenAction);

			// calculate obstacle bias if necessary
			if(obstacle_bias_method==2) {
				var bias_obstacles = obstacle_biases.calculateBias(inputs.pos);
				Floats.mul(bias_motion, bias_obstacles, action_selection_probs);
			} else Floats.copy(bias_motion, action_selection_probs);


			// Combine bias, then add bias to softmax to get resulting probabilities
			addMultiplicativeBias(action_selection_probs, softmax, action_selection_probs);
		} else Floats.copy(softmax,action_selection_probs);



		learning_dist = softmax;


//		Floats.softmaxWithWeights(qValues, biased, biased);


		chosenAction = DiscreteDistribution.sample(action_selection_probs);

		tocs[4] = Debug.toc(tics[4]);
	}


	float calculate_V(PlaceCells pcs, float[] values){
		float value = 0;
		for(int j=0; j<pcs.num_cells; j++ ) value+= values[pcs.ids[j]]*pcs.ns[j];
		return value;
	}

	PCmodulationInterface choose_modulation_method(String pc_modulation_method){
		return switch (pc_modulation_method){
			case "none" -> ( (closest_subgoal_distance) -> {});
			case "method1" -> {
				if(layer_radii==null){
					System.out.println("ERROR (MultiscaleModel.java): " +
							"pc modulation method 1 is incompatible because layer_radii was not defined");
					System.exit(-1);
				}

				var sin22_5 = 1  ; // Math.sin(Math.toRadians(22.5));
				yield (closest_subgoal_distance) -> {
					// This method assumes best distance is proportional to distance to closest subgoal
					// proportionality ratio chosen based on
					// the number of actions and areas where action should remain constant
					var best_radius = closest_subgoal_distance * sin22_5;

					// find field size closest to best radius:
					Floats.constant(0,pc_modulator_array);
					var closet = Double.POSITIVE_INFINITY;
					var best_id = 0;
					for(int i=0; i<pcs.length; i++){
						var diff = Math.abs(best_radius - layer_radii[i]);
						if(diff < closet){
							closet = diff;
							best_id = i;
						}
					}
					pc_modulator_array[best_id] = 1;
//					System.out.println("best: " + closest_subgoal_distance + " " +best_radius + " " + best_id);

//					if(best_id + 1 < pcs.length) pc_modulator_array[best_id + 1 ] = 0.5f;
//					if(best_id - 1 >= 0) pc_modulator_array[best_id - 1 ] = 0.5f;

				};
			}
			default -> {
				System.out.println("ERROR: PC Modulation method does not exist");
				System.exit(-1);
				yield (a)->{};
			}
		};
	}

}
