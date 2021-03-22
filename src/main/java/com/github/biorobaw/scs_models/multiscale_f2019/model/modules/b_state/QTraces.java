package com.github.biorobaw.scs_models.multiscale_f2019.model.modules.b_state;

import java.util.HashSet;

public class QTraces {
	
	private final int dimensions;	// number of dimensions (actions)
	private final int num_traces;	// number of traces
	private final float decay_rate; // the decay rate
	private final int init_count;	// initial number of decays until trace is assumed to be 0
	
	
	public float[][] traces;  // value of all traces
	public int [] counter;
	public HashSet<Integer> non_zero; // sets with ids of non zero traces per dimension
		
	
	
	/**
	 * Create a set of eligibility traces
	 * @param dimensions number of dimensions
	 * @param num_traces number of traces per dimension
	 * @param decay_rate the exponential decay rate
	 */
	@SuppressWarnings("unchecked")
	public QTraces(int dimensions, int num_traces, float decay_rate, float min_value) {
		this.dimensions = dimensions;
		this.num_traces = num_traces;
		this.decay_rate = decay_rate;
		init_count = decay_rate == 0 ? 0 : (int)Math.ceil(Math.log(min_value)/Math.log(decay_rate));
		System.out.println("QTrace decay rate: " + decay_rate);
		System.out.println("QTrace min_value: " + min_value);
		System.out.println("QTrace init counter: " + init_count);
		
		traces = new float[dimensions][num_traces];
		counter  = new int[num_traces];
		non_zero = new HashSet<>();
		
	}
	
	/**
	 * Exponentially decrease the traces according to the following:
	 * t[i,j] = (i!=dimension) ? decay_rate*t[i,j] : max(decay_rate*t, activation[i,j])
	 * values below the a given threshold are removed from the non zero set,
	 * although they aren't explicityly set to 0
	 * @param activations
	 * @param ids
	 * @param dimension dimension to augment the traces 
	 * @param probabilities probabilities of performing each action
	 */
	public void update(float[] activations, int[] ids, int dimension, float[] probabilities) {
		
		// exponentially decrease traces, and set them to 0 if below minimum (i.e. counter expired):
		non_zero.removeIf(i -> {
			counter[i]--;
			boolean set_zero = counter[i] <= 0;
			if(set_zero) 
				for(int d=0; d<dimensions; d++) traces[d][i] = 0;
			else 
				for(int d=0; d<dimensions; d++) traces[d][i]*=decay_rate;
			
			return set_zero;
		});
		
		
		// reset counters of active cells:
		for(int i=0; i<ids.length; i++)
			if( activations[i] > 0) {
				non_zero.add(ids[i]);
				counter[ids[i]] = init_count;
			}
			
		// update traces of active cells:
		for(int d=0; d<dimensions; d++) {

			// calculate direction delta_p in which distribution is updated
			float delta_p =  -probabilities[d];
			if(d==dimension) delta_p += 1;
			if(delta_p == 0) continue; // if dimension is 0, skip dimension
			
			// update trace for each non zero place cell
			float[] d_traces = traces[d]; // get dimension traces
			for(int i=0; i<ids.length; i++) {
				var a  = activations[i];
				if(a > 0) d_traces[ids[i]]+= delta_p*a;
			}			
		}
		
		
	}
	
	
	
	/**
	 * clear all traces, should be called at the start of each episode
	 */
	public void clear() {
		for(int d=0; d<dimensions; d++)
			for(var id : non_zero) 
				traces[d][id] = 0;
		non_zero.clear();			
	}


	
	
	
}
