package com.github.biorobaw.scs_models.multiscale_f2019.model.modules.d_action;

import com.github.biorobaw.scs.utils.math.Floats;

public class MotionBias {
	int numActions;	
	float[] biases;
	float uniform_value;
	
	int episodesToHalfLife = 50;
	float decay = (float)(1f/Math.pow(2, 1f/episodesToHalfLife));
	float interpolationValue = 1f/decay; // set to 1/decay since it is multiplied by decay before initial episode
	float interpolationComplement;
	
	private boolean compute_bias;
	
	final float sameDirectionBias = 0.83f;
	final float closestDirectionBias = 0.06f;
	final float otherDirections = (1-sameDirectionBias-2*closestDirectionBias)/5;
	float[] precalculatedBias = new float[] {
				sameDirectionBias,
				closestDirectionBias,
				otherDirections,
				otherDirections,
				otherDirections,
				otherDirections,
				otherDirections,
				closestDirectionBias
				};
	float[] interpolatedBias;
	
	
	public MotionBias(int numActions,int episodesToHalfLife) {
		this.numActions = numActions;
		
		this.episodesToHalfLife = episodesToHalfLife;
		this.decay = (float)(1f/Math.pow(2, 1f/episodesToHalfLife));
		this.interpolationValue = 1f/decay;
		
		biases = new float[numActions];
		interpolatedBias = new float[numActions];
		uniform_value=1f/numActions;
		
		
	}
	
	
	public float[] calculateBias(int lastAction) {
		if(compute_bias) // compute only from second cycle of each episode
			for(int i=0;i<numActions;i++)
				biases[i] = interpolatedBias[(numActions + i - lastAction) % numActions ];
		compute_bias = true;
		return biases;
	}
	
	
	
	public void newEpisode(){
		compute_bias = false;
		interpolationValue *=decay;
		for(int i=0;i<numActions;i++) {
			biases[i] = uniform_value;
			
			// interpolate the bias with a uniform so that the bias decays over time
			Floats.mul(precalculatedBias, interpolationValue, interpolatedBias);
			Floats.add(interpolatedBias, (1-interpolationValue)*uniform_value, interpolatedBias);
		}
	}
	
	public void newTrial(){
		interpolationValue = 1f/decay; // set to 1/decay since at new episode it gets multiplied by decay
	}
	
	public float[] getBias() {
		return biases;
	}
	

	
}


