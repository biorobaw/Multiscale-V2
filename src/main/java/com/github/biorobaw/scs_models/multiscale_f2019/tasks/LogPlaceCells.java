package com.github.biorobaw.scs_models.multiscale_f2019.tasks;

import com.github.biorobaw.scs.experiment.Experiment;
import com.github.biorobaw.scs.simulation.scripts.Script;
import com.github.biorobaw.scs.utils.files.BinaryFile;
import com.github.biorobaw.scs.utils.files.XML;
import com.github.biorobaw.scs_models.multiscale_f2019.model.MultiscaleModel;
import com.github.biorobaw.scs_models.multiscale_f2019.model.modules.b_state.PlaceCells;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;


public class LogPlaceCells implements Script {

	String subject_id = "";
	boolean log_pcs;

	public LogPlaceCells(XML xml) {
		subject_id =xml.getAttribute("subject_id");
		log_pcs = xml.getBooleanAttribute("save_pcs");
	}

	@Override
	public void endTrial() {
		if(!log_pcs) {
			System.out.println("NOT LOGGING PCS");
			return;
		}

		System.out.println("LOGGING PCS");
		var e = Experiment.get();
		String logFolder = e.getGlobal("logPath").toString();
		String ratId	 = e.getGlobal("run_id").toString();

		//create folders
		String prefix = logFolder  +"/r" + ratId + "-pc_layer";

		var model = (MultiscaleModel)e.getSubject(subject_id);
		for(int i=0; i<model.pcs.length; i++){
			log_pcs(model.pcs[i], prefix + i + ".csv");
		}
		
	}

	void log_pcs(PlaceCells pcs, String savename){
		try {
			var writer = new BufferedWriter(new FileWriter(savename));
			writer.write("x,y,r\n");
			for(int i=0; i<pcs.num_cells; i++){
				writer.write("" + pcs.xs[i] + "," + pcs.ys[i] + "," + pcs.rs[i] + "\n" );
			}
			writer.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	
	
}
