package com.github.biorobaw.multiscale_f2019.model;

import java.awt.Color;
import java.util.List;
import java.util.stream.IntStream;

import com.github.biorobaw.multiscale_f2019.gui.PCDrawer;
import com.github.biorobaw.multiscale_f2019.gui.PolarDataDrawer;
import com.github.biorobaw.multiscale_f2019.gui.VDrawer;
import com.github.biorobaw.multiscale_f2019.gui.ValueTraceDrawer;
import com.github.biorobaw.multiscale_f2019.model.modules.a_input.DistancesInputModule;
import com.github.biorobaw.multiscale_f2019.model.modules.b_state.EligibilityTraces;
import com.github.biorobaw.multiscale_f2019.model.modules.b_state.TesselatedPlaceCellLayer;
import com.github.biorobaw.multiscale_f2019.model.modules.c_rl.ProportionalValueSingleBlockMatrix;
import com.github.biorobaw.multiscale_f2019.model.modules.c_rl.ProportionalVotesSingleBlockMatrix;
import com.github.biorobaw.multiscale_f2019.model.modules.c_rl.QErrorModule;
import com.github.biorobaw.multiscale_f2019.model.modules.c_rl.Reward;
import com.github.biorobaw.multiscale_f2019.model.modules.c_rl.UpdateQModule;
import com.github.biorobaw.multiscale_f2019.model.modules.c_rl.UpdateVModule;
import com.github.biorobaw.multiscale_f2019.model.modules.c_rl.VErrorModule;
import com.github.biorobaw.multiscale_f2019.model.modules.d_action.ActionBiasModule;
import com.github.biorobaw.multiscale_f2019.model.modules.d_action.ActionFromProbabilities;
import com.github.biorobaw.multiscale_f2019.model.modules.d_action.Softmax;
import com.github.biorobaw.multiscale_f2019.model.modules.d_action.WallGateModule;
import com.github.biorobaw.multiscale_f2019.tasks.LogData;
import com.github.biorobaw.multiscale_f2019.tasks.SetInitialPosition;
import com.github.biorobaw.scs.experiment.Experiment;
import com.github.biorobaw.scs.gui.Display;
import com.github.biorobaw.scs.gui.DrawPanel;
import com.github.biorobaw.scs.gui.drawer.CycleDataDrawer;
import com.github.biorobaw.scs.gui.drawer.FeederDrawer;
import com.github.biorobaw.scs.gui.drawer.PathDrawer;
import com.github.biorobaw.scs.gui.drawer.RobotDrawer;
import com.github.biorobaw.scs.gui.drawer.RuntimesDrawer;
import com.github.biorobaw.scs.gui.drawer.WallDrawer;
import com.github.biorobaw.scs.gui.utils.GuiUtils;
import com.github.biorobaw.scs.robot.Robot;
import com.github.biorobaw.scs.robot.commands.TranslateXY;
import com.github.biorobaw.scs.robot.modules.FeederModule;
import com.github.biorobaw.scs.robot.modules.localization.GlobalLocalization;
import com.github.biorobaw.scs.utils.files.XML;
import com.vividsolutions.jts.geom.Coordinate;

import edu.usf.micronsl.module.math.SumFloat0dModule;
import edu.usf.micronsl.module.math.WeightedAverageFloat0Module;
import edu.usf.micronsl.module.math.WeightedAverageFloat1Module;
import edu.usf.micronsl.port.onedimensional.vector.PointPort;
import edu.usf.micronsl.port.singlevalue.Bool0dPort;
import edu.usf.micronsl.port.singlevalue.Int0dPort;
import edu.usf.micronsl.port.twodimensional.sparse.Float2dSparsePort;
import edu.usf.micronsl.port.twodimensional.sparse.Float2dSparsePortMatrix;


public class NslModel extends edu.usf.micronsl.Model{
	// ============ PARAMETERS ===========================
		int numActions;

		String pcType;
		List<Float> pcSizes;
		List<Integer> numPCx;
		Integer[] numPCy;
		Integer[] numPC;
		int totalPCs;
		int numScales;
		
		List<Float> traceDecay;

		final float mazeWidth;
		final float mazeHeight;

		float discountFactor;
		float learningRate;
		float foodReward;
		

		// ============ MODEL VARIABLES =======================

		Float2dSparsePort VTables[];
		Float2dSparsePort QTables[];
		int episodeCycles = 0;

		// ============ MODEL MODULES =========================
		
		// input
		Bool0dPort subAte = new Bool0dPort(null, false);
		PointPort pos = new PointPort(null);
		DistancesInputModule inputDisntanceModule;
//		JoystickModule joystick;

		// cells
		private TesselatedPlaceCellLayer[] placeCellLayers;
		private SumFloat0dModule totalActivation;
		private EligibilityTraces[] valueTraces;
		private EligibilityTraces[] actionTraces;

		// bootstrap value calculation
		private ProportionalValueSingleBlockMatrix[] layerBootstrapStateValue; // V^t-1(s_t)
		private WeightedAverageFloat0Module bootstrapStateValue;

		// reward and rl related modules
		Reward reward;
		VErrorModule errorV;
		QErrorModule errorQ;
		UpdateVModule[] layerUpdateV;
		UpdateQModule[] layerUpdateQ;

		// state and action value calculation
		ProportionalValueSingleBlockMatrix[] layerStateValue; // V^t(s_t)
		WeightedAverageFloat0Module stateValue;
		ProportionalVotesSingleBlockMatrix[] layerActionValues;
		WeightedAverageFloat1Module actionValues;
		
		//action selection modules
		Softmax softmax;
		WallGateModule affordanceGateModule;
		ActionBiasModule biasModule;
		ActionFromProbabilities actionSelection;
		
		// output:
		Int0dPort actionTaken = new Int0dPort(null,0);
		Bool0dPort wasActionOptimal = new Bool0dPort(null, true);

		
		// Logger
		private LogData logger = new LogData();
		
		
		// ============ SIMULATOR VARIABLES ===================

		private Robot robot;

		private PolarDataDrawer probDrawer;

		// ============ CONSTRUCTOR ===========================

		public NslModel(XML params, Robot robot) {
			this.robot = robot;

			// ======== PARAMETERS ===============

			numActions = params.getIntAttribute("numActions");

			mazeWidth = params.getFloatAttribute("mazeWidth");
			mazeHeight = params.getFloatAttribute("mazeHeight");

			pcSizes = params.getFloatListAttribute("pcSizes");
			numPCx = params.getIntListAttribute("numPCx");
			numScales = pcSizes.size();
			
			traceDecay = params.getFloatListAttribute("traces");

			discountFactor = params.getFloatAttribute("discountFactor");
			learningRate = params.getFloatAttribute("learningRate");
			foodReward = params.getFloatAttribute("foodReward");

			// ======== INPUT MODULES ============

			
			//Create distance sensing module - calculates distances to all walls:
			float maxDistanceSensorDistance = 4f;
			inputDisntanceModule = new DistancesInputModule("distance input", robot, numActions, maxDistanceSensorDistance);
			addModule(inputDisntanceModule);
			
			
			// Joystick module for testing purposes:
//			joystick = new JoystickModule();

			// create distance sensing module
			// input distance module =

			// ========= CURRENT STATE ===========

			// Calculate the number of cells per side on each layer according to given
			// distribution
			numPCy = new Integer[numScales];
			numPC = new Integer[numScales];
			for (int i = 0; i < numScales; i++) {
				numPCy[i] = (int) (numPCx.get(i) * mazeHeight / mazeWidth);
				numPC[i] = numPCy[i] * numPCx.get(i);
			}

			// find xMax,yMax for each layer (note xMin yMin are -xMax -yMax)
			var xMax = IntStream.range(0, numScales)
					.mapToDouble(
							i -> mazeWidth / 2 + pcSizes.get(i) - (mazeWidth + 2 * pcSizes.get(i)) / (numPCx.get(i) + 1))
					.toArray();
			var yMax = IntStream.range(0, numScales)
					.mapToDouble(i -> mazeHeight / 2 + pcSizes.get(i) - (mazeHeight + 2 * pcSizes.get(i)) / (numPCy[i] + 1))
					.toArray();

			// Create pc layers and their traces
			totalActivation = new SumFloat0dModule("totalActivation");
			placeCellLayers = new TesselatedPlaceCellLayer[numScales];
			valueTraces		= new EligibilityTraces[numScales];
			actionTraces	= new EligibilityTraces[numScales];
			for (int i = 0; i < numScales; i++) {
				//create pc layer
				float xmax = (float) xMax[i];
				float ymax = (float) yMax[i];
				placeCellLayers[i] = new TesselatedPlaceCellLayer("PC Layer " + i, pcSizes.get(i), numPCx.get(i), numPCy[i],
						pcType, -xmax, -ymax, xmax, ymax);
				placeCellLayers[i].addInPort("position", pos);
				addModule(placeCellLayers[i]);
				
				//add it to total activation calculation
				totalActivation.addInPort(placeCellLayers[i].getTotalPort());
				
				
				//add state traces:
				int numCells=numPCx.get(i)*numPCy[i];
				valueTraces[i] = new EligibilityTraces("state trace " + i, traceDecay.get(i), placeCellLayers[i].getActivationPort(), numCells, 1);
				valueTraces[i].addInPort("placeCells",placeCellLayers[i].getActivationPort());
				valueTraces[i].addInPort("totalActivation",totalActivation.getSumPort());
				addModule(valueTraces[i]);
				
				//add action traces
				actionTraces[i] = new EligibilityTraces("action trace " + i, traceDecay.get(i), placeCellLayers[i].getActivationPort(), numCells, numActions);
				actionTraces[i].addInPort("placeCells",placeCellLayers[i].getActivationPort());
				actionTraces[i].addInPort("totalActivation",totalActivation.getSumPort());
				actionTraces[i].addInPort("lastAction",actionTaken);
				addModule(actionTraces[i]);

			}
			addModule(totalActivation);

			// ======== MODEL VARIABLES ==========

			// create state and action value tables
			QTables = new Float2dSparsePortMatrix[numScales];
			VTables = new Float2dSparsePortMatrix[numScales];
			for (int i = 0; i < numScales; i++) {
				QTables[i] = new Float2dSparsePortMatrix(null, numPCx.get(i) * numPCy[i], numActions);
				VTables[i] = new Float2dSparsePortMatrix(null, numPCx.get(i) * numPCy[i], 1);
			}

			// ===== VALUE OF (NEW STATE, OLD VQ) ===

			// Calculate V^(t-1) (s_t) (bootstrapped value of V)
			// V will be a weighted average of each layers V
			bootstrapStateValue = new WeightedAverageFloat0Module("bootstrap V");
			addModule(bootstrapStateValue);

			// create the layers V
			layerBootstrapStateValue = new ProportionalValueSingleBlockMatrix[numScales];
			for (int i = 0; i < numScales; i++) {

				layerBootstrapStateValue[i] = new ProportionalValueSingleBlockMatrix("bootstrap value " + i);
				layerBootstrapStateValue[i].addInPort("states", placeCellLayers[i].getActivationPort());
				layerBootstrapStateValue[i].addInPort("value", VTables[i]);
				layerBootstrapStateValue[i].addInPort("totalActivation", placeCellLayers[i].getTotalPort());
				addModule(layerBootstrapStateValue[i]);

				// Add it to the weighted sum, the weight
				bootstrapStateValue.addInPort(layerBootstrapStateValue[i].getValuePort(),
						placeCellLayers[i].getTotalPort());
				
				//create traces for the layer

			}

			// ======== LEARNING MODULES =========

			// Create reward module
			float nonFoodReward = 0;
			reward = new Reward("foodReward", foodReward, nonFoodReward);
			reward.addInPort("rewardingEvent", subAte); // reward
			addModule(reward);

			// Create error signal module for V
			errorV = new VErrorModule("vError", discountFactor);
			errorV.addInPort("reward", reward.getRewardPort());
			errorV.addInPort("newStateValue", bootstrapStateValue.getAveragePort());
			addModule(errorV);
			
			// Create error signal module for Q
			errorQ = new QErrorModule("qError", discountFactor);
			errorQ.addInPort("reward", reward.getRewardPort());
			errorQ.addInPort("newValue", bootstrapStateValue.getAveragePort());
			errorQ.addInPort("oldAction",actionTaken);
			addModule(errorQ);

			// Create update Q module
			// Module updateQ = new UpdateQModuleAC("updateQ", numActions, learningRate)
			layerUpdateV = new UpdateVModule[numScales];
			layerUpdateQ = new UpdateQModule[numScales];
			for (int i = 0; i < numScales; i++) {
				layerUpdateV[i] = new UpdateVModule("updateV " + i, learningRate);
				layerUpdateV[i].addInPort("errorV", errorV.getErrorVPort());
				layerUpdateV[i].addInPort("wasActionOptimal", wasActionOptimal);
				layerUpdateV[i].addInPort("V", VTables[i]);
				layerUpdateV[i].addInPort("traces",valueTraces[i].getTraces());
				//updateV[i].addInPort("pcs", placeCellLayers[i].getActivationPort());
				//updateV[i].addInPort("totalActivation", totalActivation.getSumPort());
				addModule(layerUpdateV[i]);
				
				
				layerUpdateQ[i] = new UpdateQModule("update! "+ i, learningRate);
				layerUpdateQ[i].addInPort("errorQ",errorV.getErrorVPort());
				//layerUpdateQ[i].addInPort("wasActionOptimal",wasActionOptimal);
				layerUpdateQ[i].addInPort("Q",QTables[i]);
				layerUpdateQ[i].addInPort("traces",actionTraces[i].getTraces());
				addModule(layerUpdateQ[i]);
				

			}

			// ======== VALUE OF (NEW STATE, NEW VQ) =========

			// Calculate V^(t) (s_t) (will be used in next cycle as V^(t-1)(s_(t-1))
			// V is the a weighted average of each layers V
			// same for Q^t(s_t) 
			stateValue = new WeightedAverageFloat0Module("state V");
			actionValues = new WeightedAverageFloat1Module("state Q", numActions);
			addModule(stateValue);
			addModule(actionValues);

			// create the layers V
			layerStateValue = new ProportionalValueSingleBlockMatrix[numScales];
			layerActionValues = new ProportionalVotesSingleBlockMatrix[numScales];
			for (int i = 0; i < numScales; i++) {

				layerStateValue[i] = new ProportionalValueSingleBlockMatrix("state value " + i);
				layerStateValue[i].addInPort("states", placeCellLayers[i].getActivationPort());
				layerStateValue[i].addInPort("value", VTables[i]);
				layerStateValue[i].addInPort("totalActivation", placeCellLayers[i].getTotalPort());
				layerStateValue[i].addPreReq(layerUpdateV[i]);
				addModule(layerStateValue[i]);

				// Add it to the weighted sum, the weight
				stateValue.addInPort(layerStateValue[i].getValuePort(), placeCellLayers[i].getTotalPort());
				
				
				layerActionValues[i] = new ProportionalVotesSingleBlockMatrix("action value " + i,numActions);
				layerActionValues[i].addInPort("states", placeCellLayers[i].getActivationPort());
				layerActionValues[i].addInPort("qValues", QTables[i]);
				layerActionValues[i].addInPort("totalActivation", placeCellLayers[i].getTotalPort());
				layerActionValues[i].addPreReq(layerUpdateQ[i]);
				addModule(layerActionValues[i]);

				// Add it to the weighted sum, the weight
				actionValues.addInPort(layerActionValues[i].getActionValuesPort(), placeCellLayers[i].getTotalPort());
				

			}

			// ======== ACTION SELECTION =========
			
			
			//Softmax
			softmax = new Softmax("softmax", numActions);
			softmax.addInPort("input",actionValues.getAveragePort());
			addModule(softmax);
			
			//Affordance gating
			float minDistance =0.08f + 0.1f; // step + radius robot
			affordanceGateModule =new WallGateModule("affordance gate", numActions, minDistance);
			affordanceGateModule.addInPort("input",softmax.getOutPort("probabilities"));
			affordanceGateModule.addInPort("distances", inputDisntanceModule.getOutPort("distances"));
			addModule(affordanceGateModule);		
			
			//Same action bias gating
			int numStartingPositions = Integer.parseInt(Experiment.get().getGlobal("numStartingPositions"));
			biasModule = new ActionBiasModule("bias", numActions,50*numStartingPositions);
			biasModule.addInPort("input", affordanceGateModule.getProbabilitiesPort());
			biasModule.addInPort("lastAction",actionTaken);
			addModule(biasModule);
			
			//Action selection
			actionSelection = new ActionFromProbabilities("actionFromProbabilities");
			actionSelection.addInPort("probabilities", biasModule.getOutPort("probabilities"));
			addModule(actionSelection);

			// = BACKWARD AND EXTRA DEPENDENCIES =

			errorV.addInPort("oldStateValue", stateValue.getAveragePort(), true);
			errorQ.addInPort("oldValues",actionValues.getAveragePort(),true);
			
//			for(int i=0;i<numScales;i++) {
//				actionTraces[i].addInPort("lastAction", port,true);
//			}

			// ======== GRAPHICAL INTERFACE ======

			setDisplay();

		}

		
		// ============ SIMULATION ============================

		@Override
		public void newEpisode() {
			super.newEpisode();
			episodeCycles=0;
		}

		@Override
		public void endEpisode() {
			super.endEpisode();
			
			int startPos = SetInitialPosition.getStartIndex();
			logger.logSteps(startPos, episodeCycles);
			
		}

		@Override
		public void newTrial() {
			super.newTrial();
		}
		
		@Override
		public void endTrial() {
			super.endTrial();
			logger.storeLog(VTables,QTables);
		}

		@Override
		public void run() {
			super.run();
		}

		@Override
		public void initialTask() {
			super.initialTask();
			FeederModule fm = robot.getModule("FeederModule");
			subAte.set(fm.ate());
			
			
			GlobalLocalization gl = robot.getModule("slam");
			var p = gl.getPosition();
			pos.set(new Coordinate(p.getX(),p.getY()));
			
//				Globals g = Globals.getInstance();
//				if((int)g.get("episode") == 39 && (int)g.get("cycle")==381) {
//					System.out.println("Reaching value");
//					SCSDisplay d = (SCSDisplay)Display.getDisplay();
//					d.toggleSync();
//					SimulationControl.togglePause();
//				}
		}

		@Override
		public void finalTask() {
			super.finalTask();
			episodeCycles +=1;
			int chosenAction = 0;

			chosenAction = actionSelection.getOutport().get();
			actionTaken.set(chosenAction);
//			probDrawer.setArrowDirection(chosenAction);
			
			// perform action
			float tita = chosenAction*2*(float)Math.PI/numActions;
			robot.getRobotProxy()
				.send_command(new TranslateXY(0.08f*(float)Math.cos(tita),
											  0.08f*(float)Math.sin(tita)));
//				AbsoluteAngleAffordance aff = (AbsoluteAngleAffordance) affRobot.getPossibleAffordances().get(chosenAction);
//				affRobot.executeAffordance(aff);
			
			// Tries to eat if it cans
			FeederModule fmodule = robot.getModule("FeederModule");
			fmodule.eatAfterMotion();

		}
		
		
		// ============ SAVE LOAD =============================

		@Override
		public void save() {
			super.save();
		}

		@Override
		public void load() {
			super.load();
		}

		// ============ GRAPHIC INTERFACE =====================

		public void setDisplay() {
			
			Display d = Experiment.get().display;

			//add cycle info to universe panel
			d.addDrawer("universe", "cycle info", new CycleDataDrawer());
			
			// UNIVERSE RELATED DRAWERS
			RobotDrawer rDrawer = new RobotDrawer(robot.getRobotProxy());
			WallDrawer wallDrawer = new WallDrawer( 1);
			wallDrawer.setColor(GuiUtils.getHSBAColor(0f, 0f, 0f, 1));
			FeederDrawer fDrawer = new FeederDrawer(0.1f);
			d.addDrawer("universe", "feeders", fDrawer);
			
			//Path drawer
			PathDrawer pathDrawer = new PathDrawer(robot.getRobotProxy());
			pathDrawer.setColor(Color.red);
			d.addDrawer("universe", "path", pathDrawer);

			// PC DRAWERS:

			// Create panels for Displaying PCs
			for (int i = 0; i < numScales; i++) {
				d.addPanel(new DrawPanel(300, 300), "pcPanel " + i, 0, i, 1, 1);
			}
			// PC DRAWERS
			PCDrawer[] pcDrawers = new PCDrawer[numScales];
			for (int i = 0; i < numScales; i++) {
				pcDrawers[i] = new PCDrawer(placeCellLayers[i].getCells(), placeCellLayers[i].getActivationPort());
			}
			// Add drawers to PC panels and universe panel:
			for (int i = 0; i < numScales; i++) {
				d.addDrawer("pcPanel " + i, "PC layer " + i, pcDrawers[i]);
				d.addDrawer("pcPanel " + i, "maze", wallDrawer);
				d.addDrawer("pcPanel " + i, "robot other", rDrawer);
			}
			d.addDrawer("universe", "maze", wallDrawer );
			

			// TRACES DRAWER:
			
			// Create panels for Displaying V
			for (int i = 0; i < numScales; i++) {
				d.addPanel(new DrawPanel(300, 300), "TPanel " + i, 1, i, 1, 1);
			}
			
			ValueTraceDrawer[] TDrawers = new ValueTraceDrawer[numScales];
			for (int i = 0; i < numScales; i++) {
				TDrawers[i] = new ValueTraceDrawer(placeCellLayers[i].getCells(), valueTraces[i].getTraces());
				TDrawers[i].distanceOption = 1; // use pc radis to draw PCs

			}

			// Add drawers to PC panels:
			for (int i = 0; i < numScales; i++) {
				d.addDrawer("TPanel " + i, "T layer " + i, TDrawers[i]);
				d.addDrawer("TPanel " + i, "maze", wallDrawer);
				d.addDrawer("TPanel " + i, "robot other", rDrawer);
			}
			
			// V DRAWERS:

			// Create panels for Displaying V
			for (int i = 0; i < numScales; i++) {
				d.addPanel(new DrawPanel(300, 300), "VPanel " + i, 2, i, 1, 1);
			}

			// V drawers
			VDrawer[] VDrawers = new VDrawer[numScales];
			for (int i = 0; i < numScales; i++) {
				VDrawers[i] = new VDrawer(placeCellLayers[i].getCells(), VTables[i]);
				VDrawers[i].distanceOption = 1; // use pc radis to draw PCs
			}

			// Add drawers to PC panels:
			for (int i = 0; i < numScales; i++) {
				d.addDrawer("VPanel " + i, "V layer " + i, VDrawers[i]);
				d.addDrawer("VPanel " + i, "maze", wallDrawer);
				d.addDrawer("VPanel " + i, "robot other", rDrawer);
			}
			
			
			
			//ADD DRAWERS FOR ACTIONS SELECTION:
			d.addPanel(new DrawPanel(300,300), "Q", 0, 3, 1, 1);
			d.addPanel(new DrawPanel(300,300), "Aff", 1, 3, 1, 1);
			d.addPanel(new DrawPanel(300,300), "bias", 2, 3, 1, 1);
			d.addPanel(new DrawPanel(300,300), "actions", 0, 4, 1, 1);
			
			PolarDataDrawer qDrawer = new PolarDataDrawer("Q softmax", softmax.probabilities);
			PolarDataDrawer affDrawer = new PolarDataDrawer("Affordances", affordanceGateModule.gates);
			PolarDataDrawer biasDrawer = new PolarDataDrawer("Bias", biasModule.biases);
			probDrawer = new PolarDataDrawer("Probs", biasModule.probabilities);
			
			d.addDrawer("Q", "qDrawer", qDrawer);
			d.addDrawer("Aff", "affDrawer", affDrawer);
			d.addDrawer("bias", "biasDrawer", biasDrawer);
			d.addDrawer("actions", "probDrawer", probDrawer);
			
			
			//ADD RUNTIMES DRAWER
			int numEpisodes = Integer.parseInt(Experiment.get().getGlobal("numEpisodes").toString());
			RuntimesDrawer runtimes = new RuntimesDrawer(numEpisodes, 0, 800);
			runtimes.doLines = false;
			d.addPanel(new DrawPanel(300,300), "runtimes", 1, 4, 1, 1);
			d.addDrawer("runtimes", "runtimes", runtimes);
			
			

		}

		

	}
