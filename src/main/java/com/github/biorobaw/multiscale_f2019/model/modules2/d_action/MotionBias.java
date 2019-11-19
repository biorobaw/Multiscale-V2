package com.github.biorobaw.multiscale_f2019.model.modules2.d_action;

import com.github.biorobaw.scs.utils.math.Floats;

public class MotionBias {
	int numActions;	
	float[] biases;
	float[] probabilities;
	float uniform_value;
	
	int episodesToHalfLife = 50;
	float decay = (float)(1f/Math.pow(2, 1f/episodesToHalfLife));
	float interpolationValue = 1f/decay;
	float interpolationComplement;
	
	private boolean skip;
	
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
	
	
	public MotionBias(int numActions,int episodesToHalfLife) {
		this.numActions = numActions;
		
		this.episodesToHalfLife = episodesToHalfLife;
		this.decay = (float)(1f/Math.pow(2, 1f/episodesToHalfLife));
		this.interpolationValue = 1f/decay;
		
		biases = new float[numActions];
		probabilities = new float[numActions];
		uniform_value=1f/numActions;
		
	}
	
	
	public float[] addBias(int lastAction, float[] p_input) {
				
		if(skip) for(int i=0;i<numActions;i++) biases[i] = 1f/numActions;
		else for(int i=0;i<numActions;i++) {
				biases[i] = precalculatedBias[(numActions + i - lastAction) % numActions ];
				biases[i] = biases[i]*interpolationValue + (1f/numActions)*interpolationComplement;
		}

		Floats.mul(biases, p_input,probabilities);
		var sum = Floats.sum(probabilities);
		
		if(sum!=0) Floats.div(probabilities, sum, probabilities);
		else {
			System.err.println("WARNING: Probability sum is 0, setting uniform distribution (MotionBias.java)");
			for(int i=0; i<numActions; i++) probabilities[i] = uniform_value;
		}
		
		skip = false;
		
		return probabilities;
	}
	
	
	public void newEpisode(){
		skip = true;
		interpolationValue *=decay;
		interpolationComplement = 1-interpolationValue;
	}
	
	public void newTrial(){
		interpolationValue = 1f/decay;
	}
	
	public float[] getBias() {
		return biases;
	}
	
	public float[] getProbabilities() {
		return probabilities;
	}
	
}


