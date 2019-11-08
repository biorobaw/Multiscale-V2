package com.github.biorobaw.multiscale_f2019.model;

import com.github.biorobaw.scs.experiment.Subject;
import com.github.biorobaw.scs.utils.XML;

public class MultiscaleModel2 extends Subject{
	
	NslModel model;
	
	public MultiscaleModel2(XML xml) {
		super(xml);
		model = new NslModel(xml, robot);
	}

	@Override
	public long runModel() {
		model.run();
		return 0;
	}
	
	@Override
	public void newEpisode() {
		super.newEpisode();
		model.newEpisode();
	}
	
	@Override
	public void endEpisode() {
		super.endEpisode();
		model.endEpisode();
	}
	
	@Override
	public void newTrial() {
		super.newTrial();
		model.newTrial();
	}
	
	@Override
	public void endTrial() {
		super.endTrial();
		model.endTrial();
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
