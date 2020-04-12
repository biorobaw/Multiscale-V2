package com.github.biorobaw.scs_models.multiscale_f2019.old.model.modules.d_action;


import edu.usf.micronsl.module.Module;
import edu.usf.micronsl.port.onedimensional.array.Float1dPortArray;
import edu.usf.micronsl.port.singlevalue.Int0dPort;

public class ActionBiasModule extends Module {
	int numActions;	
	
	
	Float1dPortArray probabilitiesPort;
	Float1dPortArray biasesPort;
	
	int episodesToHalfLife = 50;
	float decay = (float)(1f/Math.pow(2, 1f/episodesToHalfLife));
	float interpolationValue = 1f/decay;
	float interpolationComplement;
	
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
	
	public float[] probabilities;		
	public float[] biases;


	private boolean skip;
	
	

	public ActionBiasModule(String name,int numActions,int episodesToHalfLife) {
		super(name);

		
		//TODO: if numbers are very small, when multiplying to low numbers we might get zeros
		//to prevent this, the precalculated bias should be re normalized removing values corresponding to zero entries
		
		this.numActions = numActions;
		
		this.episodesToHalfLife = episodesToHalfLife;
		this.decay = (float)(1f/Math.pow(2, 1f/episodesToHalfLife));
		this.interpolationValue = 1f/decay;
		
		
		probabilities = new float[numActions];
		probabilitiesPort = new Float1dPortArray(this, probabilities);
		addOutPort("probabilities", probabilitiesPort );
		
		biases = new float[numActions];
		biasesPort = new Float1dPortArray(this, biases);
		addOutPort("biases", biasesPort);
		
		
		for(int i=0;i<numActions;i++) biases[i] = 1f/numActions;
		

	}
	
	
	public Float1dPortArray getProbabilitiesPort() {
		return probabilitiesPort;
	}
	
	public Float1dPortArray getBiasesPort() {
		return biasesPort;
	}
	
	
	
	@Override
	public void run() {
		// TODO Auto-generated method stub
		
		float[] input = ((Float1dPortArray) getInPort("input")).getData();
		int lastAction = ((Int0dPort)getInPort("lastAction")).get();
		
		if(!skip)
			for(int i=0;i<numActions;i++) {
				biases[i] = precalculatedBias[(numActions + i - lastAction) % numActions ];
				biases[i] = biases[i]*interpolationValue + (1f/numActions)*interpolationComplement;
			}
		else for(int i=0;i<numActions;i++) biases[i] = 1f/numActions;
		
//		int episode = Experiment.get().getGlobal("episode");
		 
		
				
		float sum = 0;
		for(int i=0;i<numActions;i++) {
			probabilities[i] = input[i]*biases[i];
			sum+=probabilities[i];
		}
		if(sum==0) {
			System.err.println("WARNING: Probability sum is 0, setting uniform distribution (ActionBiasModule.java)");
			for(int i=0;i<numActions;i++) probabilities[i] = 1f/numActions;
		} else for(int i=0;i<numActions;i++) probabilities[i] /=sum;
		
		skip = false;
	}


	
	


	
	public void newEpisode(){
		skip = false;
		interpolationValue *=decay;
		interpolationComplement = 1-interpolationValue;
	}
	
	public void newTrial(){
		interpolationValue = 1f/decay;
	}
	


	@Override
	public boolean usesRandom() {
		return false;
	}



	
}
