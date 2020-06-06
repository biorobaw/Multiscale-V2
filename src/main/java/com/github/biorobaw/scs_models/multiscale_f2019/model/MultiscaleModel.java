package com.github.biorobaw.scs_models.multiscale_f2019.model;




import java.io.IOException;
import java.util.Arrays;

import com.github.biorobaw.scs.experiment.Experiment;
import com.github.biorobaw.scs.experiment.Subject;
import com.github.biorobaw.scs.robot.commands.TranslateXY;
import com.github.biorobaw.scs.robot.modules.FeederModule;
import com.github.biorobaw.scs.robot.modules.distance_sensing.DistanceSensingModule;
import com.github.biorobaw.scs.robot.modules.localization.SlamModule;
import com.github.biorobaw.scs.utils.Debug;
import com.github.biorobaw.scs.utils.files.XML;
import com.github.biorobaw.scs.utils.math.DiscreteDistribution;
import com.github.biorobaw.scs.utils.math.Floats;
import com.github.biorobaw.scs_models.multiscale_f2019.gui.GUI;
import com.github.biorobaw.scs_models.multiscale_f2019.model.modules.a_input.Affordances;
import com.github.biorobaw.scs_models.multiscale_f2019.model.modules.b_state.EligibilityTraces;
import com.github.biorobaw.scs_models.multiscale_f2019.model.modules.b_state.PlaceCellBins;
import com.github.biorobaw.scs_models.multiscale_f2019.model.modules.b_state.PlaceCells;
import com.github.biorobaw.scs_models.multiscale_f2019.model.modules.b_state.QTraces;
import com.github.biorobaw.scs_models.multiscale_f2019.model.modules.d_action.MotionBias;

public class MultiscaleModel extends Subject{
	
	// Model Parameters: RL
	public float[] v_traceDecay;
	public float[] q_traceDecay;
	public float[] v_learningRate;
	public float[] q_learningRate;
	public float discountFactor;
	public float foodReward;
	public int numScales;

	// Model Parameters: Action Space
	public int numActions;
	
	// Model Variables: input
	public SlamModule slam;
	public FeederModule feederModule;
	public DistanceSensingModule distance_sensors;
	
	
	// Model Variables: state
	public PlaceCells[] pcs;
	public PlaceCellBins[] pc_bins;
	
	public EligibilityTraces[] vTraces;
	public QTraces[] qTraces;
	
	// Model Variables: RL
	public float[][] vTable;	// v[layer][pc]
	public float[][][] qTable;  // q[layer][pc][action]
	public Float oldStateValue = null;
	public float[] qValues;
	
	// Model Variables: action selection
	public float[] softmax;  // probability after applying softmax
	public Affordances affordances;
	public float[] possible; // probability after applying affordances
	public MotionBias motionBias;   // Module to add bias to probabilities
	public int chosenAction;
	public boolean actionWasOptimal = false;
	
	
	
	// GUI
	GUI gui;
	
	public MultiscaleModel(XML xml) {
		super(xml);
		
		// ======== PARAMETERS ===============

		numActions = xml.getIntAttribute("numActions");

		float mazeWidth = xml.getFloatAttribute("mazeWidth");
		float mazeHeight = xml.getFloatAttribute("mazeHeight");

		var pcSizes = xml.getFloatArrayAttribute("pcSizes");
		var minX  = xml.getFloatArrayAttribute("minX");
		var maxX  = xml.getFloatArrayAttribute("maxX");
		var numX  = xml.getIntArrayAttribute("numX");
		var minY  = xml.getFloatArrayAttribute("minY");
		var maxY  = xml.getFloatArrayAttribute("maxY");
		var numY  = xml.getIntArrayAttribute("numY");
		numScales = pcSizes.length;
		var pc_bin_size  = xml.getFloatAttribute("pc_bin_size");
		
		v_traceDecay = xml.getFloatArrayAttribute("v_traces");
		v_learningRate = xml.getFloatArrayAttribute("v_learningRate");
		q_traceDecay = xml.getFloatArrayAttribute("q_traces");
		q_learningRate = xml.getFloatArrayAttribute("q_learningRate");
		discountFactor = xml.getFloatAttribute("discountFactor");

		foodReward = xml.getFloatAttribute("foodReward");
		
		// ======== Model Input ====================
		
		// get robot modules
		slam = robot.getModule("slam");
		feederModule = robot.getModule("FeederModule");
		distance_sensors = robot.getModule("distance_sensors");
		
		//Create affordances / distance sensing module
		affordances = new Affordances( robot, numActions, 0.1f);
		
		// Joystick module for testing purposes:
		// joystick = new JoystickModule();

		
		// ======== Model Variables: STATE AND RL ==========
		pcs = new PlaceCells[numScales];
		pc_bins = new PlaceCellBins[numScales];
		vTraces = new EligibilityTraces[numScales];
		qTraces = new QTraces[numScales];
		
		vTable = new float[numScales][];
		qTable = new float[numScales][][];
		qValues = new float[numActions];
		
		float average_active_pcs = 0;
		for(int i=0; i<numScales; i++) {
			System.out.println("layer: " 
						+ minX[i] + " " + maxX[i] + " " + numX[i] + " " 
						+ minY[i] + " " + maxY[i]+ " " + numY[i] + " " + pcSizes[i]);
			pcs[i] = new PlaceCells(minX[i], maxX[i], numX[i],minY[i], maxY[i], numY[i], pcSizes[i]);
			pc_bins[i] = new PlaceCellBins(pcs[i], pc_bin_size);
			
			average_active_pcs += pc_bins[i].averageBinSize;
			
			vTable[i] = new float[pcs[i].num_cells];
			qTable[i] = new float[pcs[i].num_cells][numActions];
			
		}
		
		for(int i=0; i<numScales; i++) {
			float minActivation = 0.7f*0.7f*0.7f / average_active_pcs;
			vTraces[i] = new EligibilityTraces(1, pcs[i].num_cells, v_traceDecay[i], minActivation);
			qTraces[i] = new QTraces(numActions, pcs[i].num_cells, q_traceDecay[i], minActivation);
		}
		
		
		// Model variables: action selection
		int numStartingPositions = Integer.parseInt(Experiment.get().getGlobal("numStartingPositions"));
		motionBias = new MotionBias(numActions, 50*numStartingPositions);
		softmax = new float[numActions];
		possible = new float[numActions];
		
		gui = new GUI(this);
		
	}

	static public long cycles = 0;
	static final int num_tics = 10;
	static public long  tics[]= new long[num_tics];
	static public float  tocs[]= new float[num_tics];
	static public float averages[]=new float[num_tics];
	
	@Override
	public long runModel() {
		cycles++;
		
//		System.out.println("cycle: " + cycles);

		tics[tics.length-1] = Debug.tic();
		
		
		tics[0] = Debug.tic();
		// get inputs
		var pos = slam.getPosition();
		float reward = feederModule.ate() ? foodReward : 0f;
		float[] distances = distance_sensors.getDistances();
		tocs[0] = Debug.toc(tics[0]);
		
		tics[1] = Debug.tic();
		// calculate state
		float totalActivity =0;
		for(int i=0; i<numScales; i++) 
			totalActivity+=pc_bins[i].activateBin((float)pos.getX(), (float)pos.getY());
		for(int i=0; i<numScales; i++) pc_bins[i].active_pcs.normalize(totalActivity);
		tocs[1] = Debug.toc(tics[1]);
		
		
		
		
		tics[2] = Debug.tic();
		// If not initial cycle, update state and action values
		if(oldStateValue!=null) {			
			// calculate bootstraps
			float bootstrap = reward;
			if(reward==0 ) {
				// only calculate next state value if non terminal state
				float value = 0;
				for(int i=0; i<numScales; i++) {
					var pcs = pc_bins[i].active_pcs;
					for(int j=0; j<pcs.num_cells; j++ ) {
						value+= vTable[i][pcs.ids[j]]*pcs.ns[j];
					}
				}
				bootstrap+= value*discountFactor;
			}
			
			// calculate rl error
			float error = bootstrap - oldStateValue;
			
			// update RL
			for(int i=0; i<numScales; i++) {
				// update V
				// v = v + error*learning_rate*trace
				if(actionWasOptimal || error >0  || true) {
					var traces = vTraces[i].traces[0];
					for(var id : vTraces[i].non_zero[0]) {
						vTable[i][id]+=  error*v_learningRate[i]*traces[id];
					}
				}
			
				
				// update Q
				for(int j=0; j<numActions; j++) {
					var traces = qTraces[i].traces[j];
					for(var id : qTraces[i].non_zero[j])
						qTable[i][id][j] += error*q_learningRate[i]*traces[id];
				}
			}
		}
		tocs[2] = Debug.toc(tics[2]);
		
		
		// calculate V,Q
		tics[3] = Debug.tic();
		oldStateValue = 0f;
		qValues = new float[numActions];
//		System.out.println("new cycle");
//		System.out.println(Arrays.toString(qValues));
		for(int i=0; i<numScales; i++) {
			var pcs = pc_bins[i].active_pcs;
			var ids = pcs.ids;
			
//			System.out.println(Arrays.toString(pcs.ns));
			for(int j=0; j<pcs.num_cells; j++) {
				var activation = pcs.ns[j];
				oldStateValue+= vTable[i][ids[j]]*activation;

				for(int k=0; k<numActions; k++)
					qValues[k]+= qTable[i][ids[j]][k]*activation;
					
			}

		}
		tocs[3] = Debug.toc(tics[3]);
		
		// perform action selection
		tics[4] = Debug.tic();
//		System.out.println(Arrays.toString(qValues));
		

		var aff_values = affordances.calculateAffordances(distances);
		float[] learning_dist;
		float[] optimal_action_dist;
		
		// METHOD 1
//		Floats.softmax(qValues, softmax);
//		Floats.mul(softmax, aff_values, possible);
//		var p_sum = Floats.sum(possible);
//		if(p_sum == 0 ) Floats.div(aff_values, Floats.sum(aff_values), possible);
//		else Floats.div(possible, p_sum, possible);
//		var biased = motionBias.addBias(chosenAction, possible);
//		learning_dist = softmax;
//		optimal_action_dist = biased;
			
		// METHOD 2
		Floats.softmaxWithWeights(qValues, aff_values, softmax);
		var biased = motionBias.addBias(chosenAction, softmax);
		learning_dist = softmax;
//		optimal_action_dist = softmax;
		optimal_action_dist = biased;
		
		
//		Floats.softmaxWithWeights(qValues, biased, biased);
		
		
		
		
		
		
		chosenAction = DiscreteDistribution.sample(biased);
		actionWasOptimal = optimal_action_dist[chosenAction] == Floats.max(optimal_action_dist);
		
		
		
		tocs[4] = Debug.toc(tics[4]);

		
		// update traces
		tics[5] = Debug.tic();
		for(int i=0; i<numScales; i++) {
			var pcs = pc_bins[i].active_pcs;
			vTraces[i].update(pcs.ns, pcs.ids, 0);
			qTraces[i].update(pcs.ns, pcs.ids, chosenAction, learning_dist);
//			System.out.println("num non zero pcs: " + pcs.ids.length);
//			System.out.println("m,M Pc: " + Floats.min(pcs.ns) + " " + Floats.max(pcs.ns) );
//			System.out.println("m,M T: " + Floats.min(vTraces[i].traces[0]) + " " + Floats.max(vTraces[i].traces[0]));
		}
		
		// perform action
		double tita = 2*Math.PI/numActions*chosenAction;
		robot.getRobotProxy().send_command(new TranslateXY(0.08f*(float)Math.cos(tita), 0.08f*(float)Math.sin(tita)));
		feederModule.eatAfterMotion();
		tocs[5] = Debug.toc(tics[5]);
		
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
		
		return 0;
	}
	
	@Override
	public void newEpisode() {
		super.newEpisode();
		motionBias.newEpisode();
		
		for(int i=0; i<numScales; i++) {
			vTraces[i].clear();
			qTraces[i].clear();
			pc_bins[i].clear();
		}
	
		oldStateValue = null;
		chosenAction = -1;
		actionWasOptimal = false;
				
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
		
	}
	
	@Override
	public void newTrial() {
		super.newTrial();
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
		
		// TODO: erase try catch
//		try {
//			System.in.read();
//		} catch (IOException e) {
//			e.printStackTrace();
//		}
	}
}
