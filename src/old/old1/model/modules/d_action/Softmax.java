package com.github.biorobaw.scs_models.multiscale_f2019.old.model.modules.d_action;

import edu.usf.micronsl.module.Module;
import edu.usf.micronsl.port.onedimensional.Float1dPort;
import edu.usf.micronsl.port.onedimensional.array.Float1dPortArray;

/**
 * Module to generate random actions when the agent hasnt moved (just rotated)
 * for a while
 * 
 * @author biorob
 * 
 */
public class Softmax extends Module {
	public float[] probabilities;
	int numActions;
	
	private final float TAU = 1;

	public Softmax(String name,int numActions) {
		super(name);

		probabilities = new float[numActions];
		this.numActions = numActions;
		addOutPort("probabilities", new Float1dPortArray(this, probabilities));

	}

	public void run() {
		Float1dPort input = (Float1dPort) getInPort("input");

		float max = -Float.MAX_VALUE;
		for (int i =0; i < numActions; i++)
			max = Math.max(input.get(i), max);
			
		float sum = 0;
		for (int i=0;i<numActions;i++){
			// Use the max to normalize - this takes care of too high values and also too low values
			probabilities[i] = (float)Math.exp((input.get(i)-max)/TAU);
			sum+=probabilities[i];
		}
//		System.out.print("\nsum: "+sum+"\nP: ");
		
//		System.out.print("Softmax output: ");
		if (sum==Float.POSITIVE_INFINITY){ 
			System.out.println("inputs: ");
			for(int i=0; i<numActions;i++)  System.out.print(input.get(i) + " " );
			System.err.println("Softmax sum is infinity");
			System.exit(-1);
		}
		if (sum==0) {
			System.err.println("Softmax sum is 0");
			System.exit(-1);
			
		}
		
		// Normalize
		for (int i=0;i<numActions;i++){
			probabilities[i]/=sum;
		}

		

	}


	@Override
	public boolean usesRandom() {
		return false;
	}
}
