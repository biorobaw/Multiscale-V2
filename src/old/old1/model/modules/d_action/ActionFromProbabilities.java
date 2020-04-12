package com.github.biorobaw.scs_models.multiscale_f2019.old.model.modules.d_action;

import com.github.biorobaw.scs.utils.math.RandomSingleton;

import edu.usf.micronsl.module.Module;
import edu.usf.micronsl.port.onedimensional.array.Float1dPortArray;
import edu.usf.micronsl.port.singlevalue.Int0dPort;

/**
 * 
 * @author biorob
 * 
 */
public class ActionFromProbabilities extends Module {	
	
	Int0dPort outport  = new Int0dPort(this);

	public ActionFromProbabilities(String name) {
		super(name);

		addOutPort("action", outport);

	}
	
	public Int0dPort getOutport() {
		return outport;
	}

	public void run() {
		Float1dPortArray input = (Float1dPortArray) getInPort("probabilities");

		float u = RandomSingleton.getInstance().nextFloat();
		int i=1;
		for (float sum = input.get(0);  sum < u;  i++)
			sum+=input.get(i);
		outport.set(i-1);

		
	}


	@Override
	public boolean usesRandom() {
		return true;
	}
}
