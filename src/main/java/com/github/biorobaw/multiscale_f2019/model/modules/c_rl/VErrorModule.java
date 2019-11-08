package com.github.biorobaw.multiscale_f2019.model.modules.c_rl;

import edu.usf.micronsl.module.Module;
import edu.usf.micronsl.port.onedimensional.array.Float1dPortArray;
import edu.usf.micronsl.port.singlevalue.Bool0dPort;
import edu.usf.micronsl.port.singlevalue.Float0dPort;
import edu.usf.micronsl.port.singlevalue.Int0dPort;

/**
 * Module that computes error signal for V and Q policies according to the following formula:
 * errorV = r_t + gamma * V(s_t+1) - V(s_t) if action was optimal or errorV>0 
 *        = 0 otherwise
 * errorQ = r_t + gamma*V(s_t+1) - Q(s_t,a_t)
 * 
 */
public class VErrorModule extends Module {
	
	Float0dPort errorV = new Float0dPort(this);
	
	float gamma; //discountFactor	
	
	boolean skipFirstUpdate;


	public VErrorModule(String name,float discountFactor) {
		super(name);
		gamma = discountFactor;
		this.addOutPort("errorV", errorV);		
		
		skipFirstUpdate = true;
	}

	
	public void run() {
		
		if (skipFirstUpdate){
			errorV.set(0);
		} else {
		
			float r = ((Float0dPort)getInPort("reward")).get();
			float newStateValue  = ((Float0dPort)getInPort("newStateValue")).get();
			float oldStateValue  = ((Float0dPort)getInPort("oldStateValue")).get();
			
			errorV.set( r + gamma*newStateValue - oldStateValue);
			
		}
			
		// Assumes Q is always the same size
		skipFirstUpdate = false;
		
	}

	public Float0dPort getErrorVPort() {
		return errorV;
	}

	@Override
	public boolean usesRandom() {
		return false;
	}
	
	public void newEpisode() {
		skipFirstUpdate = true;
	}


}
