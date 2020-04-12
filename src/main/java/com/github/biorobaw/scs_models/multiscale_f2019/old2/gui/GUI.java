package com.github.biorobaw.scs_models.multiscale_f2019.old2.gui;

import java.awt.Color;


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
import com.github.biorobaw.scs_models.multiscale_f2019.old2.gui.drawers.PCDrawer;
import com.github.biorobaw.scs_models.multiscale_f2019.old2.gui.drawers.PolarDataDrawer;
import com.github.biorobaw.scs_models.multiscale_f2019.old2.gui.drawers.VDrawer;
import com.github.biorobaw.scs_models.multiscale_f2019.old2.model.MultiscaleModel;

public class GUI {
	
	// =========== PARAMETERS =====================
	static final int   wall_thickness = 1;
	static final Color wall_color 	  = GuiUtils.getHSBAColor(0f, 0f, 0f, 1);
	static final Color path_color 	  = Color.RED;
	
	// ============ VARIABLES =====================
	
	// reference to the display and model
	Display d = Experiment.get().display;
	MultiscaleModel model;
	
	// reference to drawers
	public WallDrawer wallDrawer;
	public PathDrawer pathDrawer;
	public RobotDrawer rDrawer;
	public FeederDrawer fDrawer;

	int numScales;
	public PCDrawer[] pcDrawers;
	public VDrawer[] TDrawers;
	public VDrawer[] VDrawers;
	
	
	public PolarDataDrawer qDrawer;
	public PolarDataDrawer affDrawer;
	public PolarDataDrawer biasDrawer;
	public PolarDataDrawer probDrawer;
	
	public RuntimesDrawer runtimes;
	
	public GUI(MultiscaleModel model) {
		numScales = model.pcs.length;
		this.model = model;
		createPanels();
		createDrawers();
		addDrawersToPanels();
		
	}
	
	private void createPanels() {
		// =========== CREATE PANELS =================
		// PC PANELS
		for (int i = 0; i < numScales; i++) {
			d.addPanel(new DrawPanel(300, 300), "pcPanel " + i, 0, i, 1, 1);
		}
		
		// TRACE PANELS
		for (int i = 0; i < numScales; i++) {
			d.addPanel(new DrawPanel(300, 300), "TPanel " + i, 1, i, 1, 1);
		}
		
		// VALUE PANELS
		for (int i = 0; i < numScales; i++) {
			d.addPanel(new DrawPanel(300, 300), "VPanel " + i, 2, i, 1, 1);
		}
		
		// ACTION SELECTION PANELS
		d.addPanel(new DrawPanel(300,300), "Q", 0, 3, 1, 1);
		d.addPanel(new DrawPanel(300,300), "Aff", 1, 3, 1, 1);
		d.addPanel(new DrawPanel(300,300), "bias", 2, 3, 1, 1);
		d.addPanel(new DrawPanel(300,300), "actions", 0, 4, 1, 1);
		
		d.addPanel(new DrawPanel(300,300), "runtimes", 1, 4, 1, 1);
	}
	
	private void createDrawers() {
		// =========== CREATE DRAWERS ===============
		

		// Maze related drawers
		wallDrawer = new WallDrawer( wall_thickness);
		wallDrawer.setColor(wall_color);
		
		pathDrawer = new PathDrawer(model.getRobot().getRobotProxy());
		pathDrawer.setColor(path_color);

		rDrawer = new RobotDrawer(model.getRobot().getRobotProxy());
		
		fDrawer = new FeederDrawer(0.1f);
		
		
		// PC drawers
		pcDrawers = new PCDrawer[numScales];
		for (int i = 0; i < numScales; i++) {
			var pc_bin = model.pc_bins[i];
			pcDrawers[i] = new PCDrawer(model.pcs[i],
						 				() -> pc_bin.active_pcs);
		}
		
		// Trace drawers:
		TDrawers = new VDrawer[numScales];
		for (int i = 0; i < numScales; i++) {
			var t = model.vTraces[i];
			TDrawers[i] = new VDrawer(model.pcs[i], t.traces[0]);
			TDrawers[i].setMinValue(t.min_value);
		}
		
		// V drawers
		VDrawers = new VDrawer[numScales];
		for (int i = 0; i < numScales; i++) {
			VDrawers[i] = new VDrawer(model.pcs[i], model.vTable[i]);
			VDrawers[i].distanceOption = 1; // use pc radis to draw PCs
		}
		
		// RL and action selection drawers
		
		qDrawer = new PolarDataDrawer("Q softmax",model.numActions ,() -> model.softmax );
		affDrawer = new PolarDataDrawer("Affordances",model.numActions , ()->model.affordances.affordances);
		biasDrawer = new PolarDataDrawer("Bias",model.numActions, ()->model.motionBias.getBias());
		probDrawer = new PolarDataDrawer("Probs",model.numActions, ()->model.motionBias.getProbabilities());
		probDrawer.setGetArrowFunction(()->model.chosenAction);
		
		int numEpisodes = Integer.parseInt(Experiment.get().getGlobal("numEpisodes").toString());
		runtimes = new RuntimesDrawer(numEpisodes, 0, 800);
		runtimes.doLines = false;
	}
	
	public void addDrawersToPanels() {

		// ======== ADD DRAWERS TO PANELS ============
		
		// UNIVERSE PANEL
//		d.addDrawer("universe", "pcs", TDrawers[0] );
		d.addDrawer("universe", "maze", wallDrawer );
		d.addDrawer("universe", "feeders", fDrawer);
		d.addDrawer("universe", "path", pathDrawer);
		d.addDrawer("universe", "robot", rDrawer);
		d.addDrawer("universe", "cycle info", new CycleDataDrawer());
		
		// RUNTIMES
		d.addDrawer("runtimes", "runtimes", runtimes);
		
		// PC PANELS
		for (int i = 0; i < numScales; i++) {
			d.addDrawer("pcPanel " + i, "PC layer " + i, pcDrawers[i]);
			d.addDrawer("pcPanel " + i, "maze", wallDrawer);
			d.addDrawer("pcPanel " + i, "robot other", rDrawer);
		}
		
		// TRACE PANELS:
		for (int i = 0; i < numScales; i++) {
			d.addDrawer("TPanel " + i, "T layer " + i, TDrawers[i]);
			d.addDrawer("TPanel " + i, "maze", wallDrawer);
			d.addDrawer("TPanel " + i, "robot other", rDrawer);
		}
		
		// VALUE PANELS:
		for (int i = 0; i < numScales; i++) {
			d.addDrawer("VPanel " + i, "V layer " + i, VDrawers[i]);
			d.addDrawer("VPanel " + i, "maze", wallDrawer);
			d.addDrawer("VPanel " + i, "robot other", rDrawer);
		}
		
		
		// ACTION SELECTION PANELS:
		d.addDrawer("Q", "qDrawer", qDrawer);
		d.addDrawer("Aff", "affDrawer", affDrawer);
		d.addDrawer("bias", "biasDrawer", biasDrawer);
		d.addDrawer("actions", "probDrawer", probDrawer);
		
		
		


	}
	
	
}
