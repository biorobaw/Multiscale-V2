package com.github.biorobaw.multiscale_f2019.model.modules.c_rl;

import java.util.Map;

import edu.usf.micronsl.module.Module;
import edu.usf.micronsl.port.onedimensional.array.Float1dPortArray;
import edu.usf.micronsl.port.onedimensional.sparse.Float1dSparsePort;
import edu.usf.micronsl.port.singlevalue.Float0dPort;
import edu.usf.micronsl.port.twodimensional.Float2dPort;
import edu.usf.micronsl.port.twodimensional.Float2dSingleBlockMatrixPort;
//import edu.usf.ratsim.nsl.modules.actionselection.Voter;

/**
 * Class to set the votes for actions depending both in the state activation and
 * a value function.
 * 
 * @author ludo
 *
 */
public class ProportionalVotesSingleBlockMatrix extends Module { //implements Voter {

	public float[] actionVote;
	Float1dPortArray actionValuesPort;
	private int numActions;

	public ProportionalVotesSingleBlockMatrix(String name, int numActions) {
		super(name);
		this.numActions = numActions;
		actionVote = new float[numActions];
		actionValuesPort = new Float1dPortArray(this, actionVote);
		addOutPort("votes", actionValuesPort);
	}

	public void run() {
		
		for (int action = 0; action < numActions; action++)
			actionVote[action] = 0f;
		
		float totalActivation = ((Float0dPort) getInPort("totalActivation")).get();
		if(totalActivation > 0) {
			Float2dSingleBlockMatrixPort states = (Float2dSingleBlockMatrixPort) getInPort("states");
			Float2dPort value = (Float2dPort) getInPort("qValues");
			
			
			// float cantStates = states.getSize();
			for(int i=0;i<states.getBlockRows();i++)
				for(int j=0;j<states.getBlockCols();j++) {
					float stateVal = states.getBlock(i, j) / totalActivation;
					if (stateVal != 0) {
						int id = states.getBlockIndex(i, j);
						for (int action = 0; action < numActions; action++) 
								actionVote[action] += (float) (stateVal * value.get(id, action));
					}
				}
		}
		

	}

	public String voteString() {
		String res = "";
		for (float a : actionVote)
			res += a + ", ";
		return res;
	}

	public Float1dPortArray getActionValuesPort() {
		return actionValuesPort;
	}
	
	//@Override
	public float[] getVotes() {
		return actionVote;
	}

	@Override
	public boolean usesRandom() {
		return false;
	}

}
