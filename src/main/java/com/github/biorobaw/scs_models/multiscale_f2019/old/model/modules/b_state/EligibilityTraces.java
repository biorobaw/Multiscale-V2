package com.github.biorobaw.scs_models.multiscale_f2019.old.model.modules.b_state;

import java.util.Map.Entry;

import edu.usf.micronsl.module.Module;
import edu.usf.micronsl.port.singlevalue.Float0dPort;
import edu.usf.micronsl.port.singlevalue.Int0dPort;
import edu.usf.micronsl.port.twodimensional.Float2dSingleBlockMatrixPort;
import edu.usf.micronsl.port.twodimensional.sparse.Float2dSparsePort;
import edu.usf.micronsl.port.twodimensional.sparse.Float2dSparsePortMatrix;

/**
 * Computes eligibility traces for each cell: Q and V require the traces of the
 * previous state / action,
 * 
 */

public class EligibilityTraces extends Module {

	Float2dSparsePortMatrix traces;
	
	Float2dSingleBlockMatrixPort oldPCs;
	float oldTotalActivation = 0;

	float traceDiscount; // discountFactor

	final float minActivation;
	int numValues;
	
	boolean skip = true;

	public EligibilityTraces(String name, float traceDiscount, Float2dSingleBlockMatrixPort pcPort ,  int numCells, int numValues) {
		super(name);
		this.traceDiscount = traceDiscount;
		minActivation = 0.05f / traceDiscount;
		this.numValues = numValues;

		traces = new Float2dSparsePortMatrix(this, numCells, numValues);
		this.addOutPort("traces", traces);
		
		oldPCs = pcPort.copyPort();

	}

	public void run() {

		if (!skip) {

			int lastAction = 0;
			if (numValues > 1)
				lastAction = ((Int0dPort) getInPort("lastAction")).get();

			// exponentially decrease traces
			var keyValues = traces.getNonZero().entrySet().toArray();
			for (int i = 0; i < keyValues.length; i++) {
				@SuppressWarnings("unchecked")
				var ev = (Entry<edu.usf.micronsl.port.twodimensional.sparse.Entry, Float>) keyValues[i];
				traces.set(ev.getKey().i, ev.getKey().j,
						ev.getValue() < minActivation ? 0 : ev.getValue() * traceDiscount);
			}

			// for active pcs choose between current activation and trace decay
			if(oldTotalActivation!=0)
				for (int i = 0; i < oldPCs.getBlockRows(); i++)
					for (int j = 0; j < oldPCs.getBlockCols(); j++) {
						int index = oldPCs.getBlockIndex(i, j);
						float newVal = oldPCs.getBlock(i, j) / oldTotalActivation;
						float currentVal = traces.get(index);
//						System.out.println("trace: " + newVal + " " + currentVal + " " + index + " " + lastAction);
						if (newVal > currentVal)
							traces.set(index, lastAction, newVal);
					}
		}

		skip = false;
		
		((Float2dSingleBlockMatrixPort) getInPort("placeCells")).copyDataTo(oldPCs);;
		oldTotalActivation = ((Float0dPort) getInPort("totalActivation")).get();
	}

	
	public Float2dSparsePort getTraces() {
		return traces;
	}

	@Override
	public boolean usesRandom() {
		return false;
	}

	public void newEpisode() {
		traces.clear();
		skip = true;
	}

}
