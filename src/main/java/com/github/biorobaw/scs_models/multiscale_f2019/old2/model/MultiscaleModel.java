package com.github.biorobaw.scs_models.multiscale_f2019.old2.model;





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
import com.github.biorobaw.scs_models.multiscale_f2019.old2.gui.GUI;
import com.github.biorobaw.scs_models.multiscale_f2019.old2.model.modules.a_input.Affordances;
import com.github.biorobaw.scs_models.multiscale_f2019.old2.model.modules.b_state.EligibilityTraces;
import com.github.biorobaw.scs_models.multiscale_f2019.old2.model.modules.b_state.PlaceCellBins;
import com.github.biorobaw.scs_models.multiscale_f2019.old2.model.modules.b_state.PlaceCells;
import com.github.biorobaw.scs_models.multiscale_f2019.old2.model.modules.d_action.MotionBias;

public class MultiscaleModel extends Subject{
	
	// Model Parameters: RL
	public float[] traceDecay;
	public float discountFactor;
	public float learningRate;
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
	public EligibilityTraces[] qTraces;
	
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
		var numPCx  = xml.getIntArrayAttribute("numPCx");
		numScales = pcSizes.length;
		var pc_bin_size  = xml.getFloatAttribute("pc_bin_size");
		
		traceDecay = xml.getFloatArrayAttribute("traces");

		discountFactor = xml.getFloatAttribute("discountFactor");
		learningRate = xml.getFloatAttribute("learningRate");
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
		qTraces = new EligibilityTraces[numScales];
		
		vTable = new float[numScales][];
		qTable = new float[numScales][][];
		qValues = new float[numActions];
		
		for(int i=0; i<numScales; i++) {
			pcs[i] = new PlaceCells(mazeWidth, mazeHeight, pcSizes[i], numPCx[i]);
			pc_bins[i] = new PlaceCellBins(pcs[i], pc_bin_size);
			
			vTraces[i] = new EligibilityTraces(1, pcs[i].num_cells, traceDecay[i], 0.05f);
			qTraces[i] = new EligibilityTraces(numActions, pcs[i].num_cells, traceDecay[i], 0.05f);
			
			vTable[i] = new float[pcs[i].num_cells];
			qTable[i] = new float[pcs[i].num_cells][numActions];
			
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
				if(actionWasOptimal || error >0) {
					var traces = vTraces[i].traces[0];
					for(var id : vTraces[i].non_zero[0]) {
						vTable[i][id]+=  error*learningRate*traces[id];
					}
				}
			
				
				// update Q
				for(int j=0; j<numActions; j++) {
					var traces = qTraces[i].traces[j];
					for(var id : qTraces[i].non_zero[j])
						qTable[i][id][j] += error*learningRate*traces[id];
				}
			}
		}
		tocs[2] = Debug.toc(tics[2]);
		
		
		// calculate V,Q
		tics[3] = Debug.tic();
		oldStateValue = 0f;
		qValues = new float[numActions];
		for(int i=0; i<numScales; i++) {
			var pcs = pc_bins[i].active_pcs;
			var ids = pcs.ids;
			
			
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
		Floats.softmax(qValues, softmax);
		var aff_values = affordances.calculateAffordances(distances);
		Floats.mul(softmax, aff_values, possible);
		var p_sum = Floats.sum(possible);
		if(p_sum == 0 ) Floats.div(aff_values, Floats.sum(aff_values), possible);
		else Floats.div(possible, p_sum, possible);
		
		var biased = motionBias.addBias(chosenAction, possible);
		chosenAction = DiscreteDistribution.sample(biased);
		actionWasOptimal = biased[chosenAction] == Floats.max(biased);
			
		tocs[4] = Debug.toc(tics[4]);

		
		// update traces
		tics[5] = Debug.tic();
		for(int i=0; i<numScales; i++) {
			var pcs = pc_bins[i].active_pcs;
			vTraces[i].update(pcs.ns, pcs.ids, 0);
			qTraces[i].update(pcs.ns, pcs.ids, chosenAction);
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
	}
}
