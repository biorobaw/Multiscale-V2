package com.github.biorobaw.scs_models.multiscale_f2019.tasks;

import java.io.OutputStream;
import java.util.LinkedList;

import org.apache.commons.lang3.ArrayUtils;

import com.github.biorobaw.scs.experiment.Experiment;
import com.github.biorobaw.scs.robot.modules.localization.GlobalLocalization;
import com.github.biorobaw.scs.tasks.cycle.CycleTask;
import com.github.biorobaw.scs.utils.files.BinaryFile;
import com.github.biorobaw.scs.utils.files.XML;


public class LogLastPaths extends CycleTask {
	
	LinkedList<Float> path = new LinkedList<>();
	int first_episode_to_log;
	String subject_id = "";
	OutputStream saveFile = null;
	
	public LogLastPaths(XML xml) {
		super(xml);
		subject_id =xml.getAttribute("subject_id");
	}
	
	@Override
	public void newTrial() {
		int numEpisodes = Experiment.get().getGlobal("trial_episodes");
		int positions = SetInitialPosition.getNumberOfStrartingPositions();
		first_episode_to_log = numEpisodes - positions;
		
		// create file to store results
		var e = Experiment.get();
		String logFolder = e.getGlobal("logPath").toString();
		String ratId	 = e.getGlobal("run_id").toString();
		String prefix = logFolder  +"/r" + ratId + "-"; 
		saveFile = BinaryFile.openFileToWrite(prefix + "paths.bin");
		
	}
	
	@Override
	public void endTrial() {
		if(saveFile!= null) {
			BinaryFile.close(saveFile);
			System.out.println("saved \"paths\" file");
		}
	}
	
	@Override
	public void endEpisode() {
		if(path.size() > 0) {
			System.out.println("logging path episode: " + Experiment.get().getGlobal("episode"));
			var aux = path.toArray(new Float[0]);
			BinaryFile.writeArray(saveFile, ArrayUtils.toPrimitive(aux), true);
			path.clear();
		}
		
	}

	@Override
	public long perform() {
		// if last batch of episodes log rat position
		var e = Experiment.get();
		int episode = e.getGlobal("episode");
		
		// do not reschedule task if not logging the episode
		if(episode < first_episode_to_log) return -1;
		
		
		var subject = e.getSubject(subject_id);
		
		var slam = (GlobalLocalization)subject.getRobot().getModule("slam");
		var pos = slam.getPosition();
		path.add((float)pos.getX());
		path.add((float)pos.getY());

		// reschedule at cycle time
		return 0;
	}	
	
	
}
