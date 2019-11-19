package com.github.biorobaw.multiscale_f2019.model;

import java.util.Arrays;


import com.github.biorobaw.scs.experiment.Subject;
import com.github.biorobaw.scs.utils.Debug;
import com.github.biorobaw.scs.utils.files.XML;
import com.github.biorobaw.scs.utils.math.Floats;

public class MultiscaleModel1 extends Subject{
	
	NslModel model;
	
	public MultiscaleModel1(XML xml) {
		super(xml);
		model = new NslModel(xml, robot);
	}

	
	static public long cycles = 0;
	static final int num_tics = 4;
	static public long  tics[]= new long[num_tics];
	static public float  tocs[]= new float[num_tics];
	static public float averages[]=new float[num_tics];
	@Override
	public long runModel() {
//		cycles++;
		tics[tics.length-1] = Debug.tic();
		model.run();
		tocs[tics.length-1] = Debug.toc(tics[tics.length-1]);
		
//		if(cycles==1) {
//			Floats.copy(tocs,averages);
//		} else {
//			Floats.mul(averages, 0.95f, averages);
//			Floats.add(averages, Floats.mul(tocs, 0.05f), averages);
//		}
//		var percentual = Floats.div(averages, averages[tocs.length-1]/100f);
//		System.out.println("instants: "+ Arrays.toString(tocs));
//		System.out.println("averages: "+ Arrays.toString(averages));
//		System.out.println("percentual:"+ Arrays.toString(percentual));
		
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
