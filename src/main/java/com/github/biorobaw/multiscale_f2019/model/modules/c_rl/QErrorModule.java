package com.github.biorobaw.multiscale_f2019.model.modules.c_rl;

import edu.usf.micronsl.module.Module;
import edu.usf.micronsl.port.onedimensional.Float1dPort;
import edu.usf.micronsl.port.singlevalue.Float0dPort;
import edu.usf.micronsl.port.singlevalue.Int0dPort;

/**
 * Module that computes error signal for V and Q policies according to the following formula:
 * errorV = r_t + gamma * V(s_t+1) - V(s_t) if action was optimal or errorV>0 
 *        = 0 otherwise
 * errorQ = r_t + gamma*V(s_t+1) - Q(s_t,a_t)
 * 
 */
public class QErrorModule extends Module {
	
	Float0dPort errorQ = new Float0dPort(this);
	
	float gamma; //discountFactor	
	
	boolean skipFirstUpdate;


	public QErrorModule(String name,float discountFactor) {
		super(name);
		gamma = discountFactor;
		this.addOutPort("errorV", errorQ);		
		
		skipFirstUpdate = true;
	}

	
	public void run() {
		
		if (skipFirstUpdate){
			errorQ.set(0);
		} else {
		
			float r = ((Float0dPort)getInPort("reward")).get();
			int   oldAction	= ((Int0dPort)getInPort("oldAction")).get();
			float newValue  = ((Float0dPort)getInPort("newValue")).get();
			float oldValue  = ((Float1dPort)getInPort("oldValues")).get(oldAction);
			
			errorQ.set( r + gamma*newValue - oldValue);
			
		}
			
		// Assumes Q is always the same size
		skipFirstUpdate = false;
		
	}

	public Float0dPort getErrorQPort() {
		return errorQ;
	}

	@Override
	public boolean usesRandom() {
		return false;
	}
	
	public void newEpisode() {
		skipFirstUpdate = true;
	}


}
