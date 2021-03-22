package com.github.biorobaw.scs_models.multiscale_f2019.model.modules.b_state;

import java.util.HashSet;

public class EligibilityTraces {
	
	
	private final int dimensions;	// number of dimensions (actions)
	private final int num_traces;	// number of traces
	private final float decay_rate; // the decay rate
	private final int init_count;	// initial number of decays until trace is assumed to be 0

	public float[][] traces;  			// value of all traces
	public int [][] counter;  			// remaining decays until trace set to zero
	public HashSet<Integer>[] non_zero; // sets with ids of non zero traces per dimension
	
	
	
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
		init_count = decay_rate == 0 ? 0 : (int)Math.ceil(Math.log(min_value)/Math.log(decay_rate));
		System.out.println("VTrace decay rate: " + decay_rate);
		System.out.println("VTrace min_value: " + min_value);
		System.out.println("VTrace init counter: " + init_count);
		
		traces = new float[dimensions][num_traces];
		counter  = new int[dimensions][num_traces];
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
			float[] d_traces = traces[d];
			var d_counts = counter[d];
			var d_non_zero = non_zero[d];
			d_non_zero.removeIf(i -> {
				d_counts[i]--;
				boolean set_zero = d_counts[i] <= 0;
				if(set_zero) d_traces[i] = 0;
				else d_traces[i]*=decay_rate;
				return set_zero;
			});
			
			// for the given dimesion augment traces
			if(d==dimension) for(int i=0; i<ids.length; i++) {
				var a = activations[i];
				if (a==0) continue;
				
				var id = ids[i];
				d_non_zero.add(id);
				d_counts[id] = init_count;
				if(a >= d_traces[id]) d_traces[id] = a;

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
