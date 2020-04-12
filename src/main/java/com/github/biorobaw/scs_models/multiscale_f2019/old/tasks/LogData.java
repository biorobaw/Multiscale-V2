package com.github.biorobaw.scs_models.multiscale_f2019.old.tasks;

import com.github.biorobaw.scs.experiment.Experiment;
import com.github.biorobaw.scs.utils.files.BinaryFile;

import edu.usf.micronsl.port.twodimensional.sparse.Float2dSparsePort;

public class LogData {
	
	int numEpisodes;
	int startPositions[];
	int stepsTaken[];
	
	public LogData() {
		// TODO Auto-generated constructor stub
		numEpisodes = Integer.parseInt(Experiment.get().getGlobal("numEpisodes").toString());
		startPositions = new int[numEpisodes];
		stepsTaken = new int[numEpisodes];
	}
	
	public void logSteps(int startPos,int steps) {
		int episode = Experiment.get().getGlobal("episode");
		startPositions[episode] = startPos;
		stepsTaken[episode] = steps;
	}

	public void storeLog(Float2dSparsePort[] V , Float2dSparsePort[] Q) {
		
		//get experiment configuration id:
		var g = Experiment.get();
		String logFolder = g.getGlobal("logPath").toString();
//		String configId = g.get("config").toString();
		String ratId	 = g.getGlobal("run_id").toString();
		
		//create folders
		String prefix = logFolder  +"/r" + ratId + "-";  
		
		var file = BinaryFile.openFileToWrite(prefix + "steps.bin");
		BinaryFile.writeArray(file, startPositions,true);
		BinaryFile.writeArray(file, stepsTaken,true);
		BinaryFile.close(file);
		
		for(int i=0;i<V.length;i++) {
			
//			BinaryFile.saveBinaryMatrix(V[i].getNonZero(), V[i].getNRows(), V[i].getNCols(), prefix + "V" + i+ ".bin", true);
//			BinaryFile.saveBinaryMatrix(Q[i].getNonZero(), Q[i].getNRows(), Q[i].getNCols(), prefix + "Q" + i+ ".bin", true);
		}
		
		
		
	}
	
}
