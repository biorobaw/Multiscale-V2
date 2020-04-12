package com.github.biorobaw.scs_models.multiscale_f2019.old.model.modules.c_rl;

import edu.usf.micronsl.module.Module;
import edu.usf.micronsl.port.singlevalue.Float0dPort;
import edu.usf.micronsl.port.twodimensional.Float2dPort;
import edu.usf.micronsl.port.twodimensional.Float2dSingleBlockMatrixPort;

/**
 * Class to set the votes for actions depending both in the state activation and
 * a value function.
 * 
 *
 */
public class ProportionalValueSingleBlockMatrix extends Module {

	public Float0dPort valuePort;

	public ProportionalValueSingleBlockMatrix(String name) {
		super(name);
		valuePort = new Float0dPort(this);
		addOutPort("value",valuePort);
		
	}

	public void run() {
		
		//get PC total activation:
		float totalActivation = ((Float0dPort) getInPort("totalActivation")).get();
		
		//
		float valueEst = 0f;
		if(totalActivation!=0) {
			
			Float2dSingleBlockMatrixPort states = (Float2dSingleBlockMatrixPort) getInPort("states");
			Float2dPort stateValues = (Float2dPort) getInPort("value");
			
			
			for(int i=0; i<states.getBlockRows();i++)
				for(int j=0;j<states.getBlockCols();j++){
					
						valueEst += states.getBlock(i,j)/totalActivation * stateValues.get(states.getBlockIndex(i, j), 0);
				}
			
		}
		
		

		//Get PC total:
		

		// Max value is food reward
		
		valuePort.set(valueEst);
		

	}

	public Float0dPort getValuePort() {
		return valuePort;
	}
	
	@Override
	public boolean usesRandom() {
		return false;
	}

}
