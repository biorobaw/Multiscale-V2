package com.github.biorobaw.scs_models.multiscale_f2019.old.model.modules.d_action;



import edu.usf.micronsl.module.Module;
import edu.usf.micronsl.port.onedimensional.array.Float1dPortArray;

/**
 * Module that sets the probability of an action to 0 if the action can not be performed
 * It assumes actions are allocentric,  distributed uniformly in the range [0,2pi]
 * @author biorob
 * 
 */
public class WallGateModule extends Module {
	
	public Float1dPortArray probabilitiesPort;
	public float[] probabilities;
	public float[] gates;

	int numActions ;
	float minDistance;
	
	
	public WallGateModule(String name,int numActions,float minDistance) {
		super(name);
		this.numActions = numActions;
		
		this.minDistance = minDistance;
		
		probabilities = new float[numActions];
		gates = new float[numActions];
		probabilitiesPort = new Float1dPortArray(this, probabilities);
		this.addOutPort("probabilities", probabilitiesPort);

	}
	
	
	public Float1dPortArray getProbabilitiesPort() {
		return probabilitiesPort;
	}

	
	public void run() {
		Float1dPortArray input = (Float1dPortArray) getInPort("input");
		Float1dPortArray distances = (Float1dPortArray) getInPort("distances");
		
		
		
		float sum = 0;
		for (int i =0;i<numActions;i++)
		{
//			double distance = universe.distanceToNearestWall(endPoints[i].x,endPoints[i].y, maxDistance);
			if(distances.get(i) <= minDistance) probabilities[i] = gates[i] = 0;
			else{
				//System.out.println("action "+i+" posible");
				probabilities[i] =  input.get(i);
				gates[i] = 1f;
				sum += probabilities[i];
			}
			
		}
		
		if(sum==0) {
			//policy is assigning probability of 0 to the only possible actions.
			//Instead assign uniform probabilities for possible actions:
			sum = 0;
			for(int i=0;i<numActions;i++) {
				probabilities[i] = gates[i];
				sum+=1;
			}
		}
		for (int i =0;i<numActions;i++) probabilities[i]/=sum;
		

	}


	@Override
	public boolean usesRandom() {
		return false;
	}
}
