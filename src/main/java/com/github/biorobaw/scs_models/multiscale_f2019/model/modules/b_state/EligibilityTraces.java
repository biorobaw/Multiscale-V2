package com.github.biorobaw.scs_models.multiscale_f2019.model.modules.b_state;

import java.util.HashSet;

public class EligibilityTraces {
	
	// min value for a trace to be considered as active
	public final float min_value;
	
	
	public int dimensions;			  // number of dimensions (actions)
	public float[][] traces;  // value of all traces
	public int num_traces;	  // number of traces
	public HashSet<Integer>[] non_zero; // sets with ids of non zero traces per dimension
	
	public float decay_rate; // the decay rate
	
	
	
	/**
	 * Create a set of eligibility traces
	 * @param dimensions number of dimensions
	 * @param num_traces number of traces per dimension
	 * @param decay_rate the exponential decay rate
	 */
	@SuppressWarnings("unchecked")
	public EligibilityTraces(int dimensions, int num_traces, float decay_rate, float min_value) {
		this.dimensions = dimensions;
		this.num_traces = num_traces;
		this.decay_rate = decay_rate;
		this.min_value = min_value;
		
		traces = new float[dimensions][num_traces];
		non_zero = new HashSet[dimensions];
		for(int i=0; i<dimensions; i++) non_zero[i] = new HashSet<>();
		
	}
	
	/**
	 * Exponentially decrease the traces according to the following:
	 * t[i,j] = (i!=dimension) ? decay_rate*t[i,j] : max(decay_rate*t, activation[i,j])
	 * values below the a given threshold are removed from the non zero set,
	 * although they aren't explicityly set to 0
	 * @param activations
	 * @param ids
	 * @param dimension dimension to augment the traces 
	 */
	public void update(float[] activations, int[] ids, int dimension) {
		
		for(int d=0; d<dimensions; d++) {

			// exponentially decrease traces, and remove them form set if below minimum:
			float[] vals = traces[d];
			non_zero[d].removeIf(i -> (vals[i]*=decay_rate)<min_value );
			
			// for the given dimesion augment traces
			if(d==dimension) for(int i=0; i<ids.length; i++) {
				var a = activations[i];
				if(a >= min_value) {
					var id = ids[i];
					if(a >= vals[id]) {
						vals[id] = a;
						non_zero[d].add(id);
					}
				}
			}
		}	
	}
	
	
	
	/**
	 * clear all traces, should be called at the start of each episode
	 */
	public void clear() {
		for(int i=0; i<dimensions; i++) {
			for(var id : non_zero[i]) traces[i][id] = 0;
			non_zero[i].clear();			
		}
	}


	
	
	
}
