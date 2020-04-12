package com.github.biorobaw.scs_models.multiscale_f2019.old.model.modules.c_rl;

import edu.usf.micronsl.module.Module;
import edu.usf.micronsl.port.singlevalue.Float0dPort;
import edu.usf.micronsl.port.twodimensional.Float2dPort;
import edu.usf.micronsl.port.twodimensional.sparse.Float2dSparsePortMatrix;

/**
 * Module updates V if action was optimal or if error > 0 
 * 
 */
public class UpdateQModule extends Module {


//	private Float2dSingleBlockMatrixPort oldPCs;
	private float learningRate;
	private boolean skip;
//	private float oldPCTotalActivation;

	public UpdateQModule(String name, float learningRate) {
		super(name);
		this.learningRate = learningRate;
	}

	public void run() {
		
		if(!skip) {
			
		
		
			//get error and optimality of action
			float lrErrorV 	= learningRate * ((Float0dPort) getInPort("errorQ")).get();
			var traces 		= ((Float2dSparsePortMatrix)getInPort("traces")).getNonZero();
//			boolean optimal = ((Bool0dPort)getInPort("wasActionOptimal")).get();
			
			
			//if error reduces value and action was not optimal, ignore the update
//			if( ( optimal || lrErrorV > 0 )  ) {
			
				//update the values
				Float2dPort V = (Float2dPort) getInPort("Q");
					
				
				for(var keyValue : traces.entrySet()) {
					int row = keyValue.getKey().i;
					int column = keyValue.getKey().j;
					V.set(row, column, V.get(row, column) + lrErrorV * keyValue.getValue());
				}
				
//				for(int i=0;i<oldPCs.getBlockRows();i++)
//					for(int j=0;j<oldPCs.getBlockRows();j++){
//						float pc = oldPCs.getBlock(i,j) / oldPCTotalActivation;
//						
//						int id = oldPCs.getBlockIndex(i, j);
//						V.set(id, 0, V.get(id, 0) + lrErrorV * pc);
//					}
				
			}
//		}

		skip = false;
//		((Float2dSingleBlockMatrixPort) getInPort("pcs")).copyDataTo(oldPCs);
//		oldPCTotalActivation = ((Float0dPort) getInPort("totalActivation")).get();
		

	}

	@Override
	public boolean usesRandom() {
		return false;
	}
	
	@Override
	public void newEpisode() {
		skip = true;
		//Float2dSingleBlockMatrixPort pcs = (Float2dSingleBlockMatrixPort) getInPort("pcs");
//		oldPCTotalActivation = 0;
//		oldPCs = pcs.copyPort();
	}

	//what is this function for?
//	public void savePCs() {
//		Float1dSparsePort actionPCs = (Float1dSparsePort) getInPort("actionPlaceCells");
//		oldActionPCs = new HashMap<Integer, Float>(actionPCs.getNonZero());
//		Float1dSparsePort valuePCs = (Float1dSparsePort) getInPort("valuePlaceCells");
//		oldValuePCs = new HashMap<Integer, Float>(valuePCs.getNonZero());
//	}
}
