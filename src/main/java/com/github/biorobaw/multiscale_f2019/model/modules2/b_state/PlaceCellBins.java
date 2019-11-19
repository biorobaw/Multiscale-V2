package com.github.biorobaw.multiscale_f2019.model.modules2.b_state;

import java.util.ArrayList;

import com.github.biorobaw.scs.utils.math.Floats;


/**
 * Class that divides space into squared bins.
 * Each bin stores all place cells that intersect the bins (or almost).
 * The class also provides utilities to compute the place cells. 
 * @author bucef
 *
 */
public class PlaceCellBins {
		
	final static float min_activation = (float)Math.log(0.2); 
	
	float minx, miny, bin_size; // min bin coordinates and size of bins
	int xbins, ybins;		   // number of bins in the x and y directions respectively
	
	
	PlaceCells pc_bins[][];
	int active_x_id, active_y_id; // x and y indeces of the active bin
	public PlaceCells active_pcs;
	
	/**
	 * Create and initialize the bins
	 * @param pcs  the place cells (expected in the format: [ [x] [y] [r] [k] ])
	 * @param minx the minx coordinate to divide space
	 * @param miny the maxx coordinate to divide space
	 * @param maxx the miny coordinate to divide space
	 * @param maxy the maxy coordinate to divide space
	 * @param bin_size the size of the bins in both x and y direction
	 */
	public PlaceCellBins(PlaceCells pcs, float bin_size) {
		// store bin size
		this.bin_size = bin_size;
		
		// find min and max coordinates in which pcs are active
		minx = Floats.min(Floats.sub(pcs.xs, pcs.rs));
		miny = Floats.min(Floats.sub(pcs.ys, pcs.rs));
		var maxx = Floats.max(Floats.add(pcs.xs, pcs.rs));
		var maxy = Floats.max(Floats.add(pcs.ys, pcs.rs));
		
		
		// find how many bins are necessary
		xbins = (int)Math.ceil((maxx-minx)/bin_size)+1; // we add one for the special case (maxx-minx)%binSize == 0
		ybins = (int)Math.ceil((maxy-miny)/bin_size)+1; // we add one for the special case (maxy-miny)%binSize == 0


		// create the bins
		pc_bins = new PlaceCells[xbins][ybins];

		
		// create auxiliary bins for holding ids
		@SuppressWarnings("unchecked")
		ArrayList<Integer>[][] aux_bins = new ArrayList[xbins][ybins];
		for(int i=0; i<xbins; i++)
			for(int j=0; j<ybins; j++)
				aux_bins[i][j] = new ArrayList<>();
		
		// calculate half the diagonal of the bin
		float half_bin_diagonal = (float)Math.sqrt(2)*bin_size/2;
		
		
		// add pcs to the bins
		for(int k=0; k < pcs.num_cells; k++ ) {
			
			// get pc data
			var id = k;		   // pc id
			var x = pcs.xs[k]; // pc x coordinte
			var y = pcs.ys[k]; // pc y coordinate
			var r = pcs.rs[k]; // pc radius
			
			// get bins that the place field may intersect
			var minBins = getBin(x-r, y-r);
			var maxBins = getBin(x+r, y+r);

			// fix values out of range
			if(minBins[0] < 0 ) minBins[0] = 0;
			if(minBins[1] < 0 ) minBins[1] = 0;
			if(maxBins[0] >= xbins ) maxBins[0] = xbins-1;
			if(maxBins[1] >= ybins ) maxBins[1] = ybins-1;
			
			for(int i=minBins[0]; i <=maxBins[0] ; i++) {
				float bx = minx + (i+0.5f)*bin_size; // x coordinate of the bin center
				float dx = x-bx; 
				
				for(int j=minBins[1]; j<=maxBins[1]; j++) {
					float by = miny + (j+0.5f)*bin_size; // y coordinate of the bin center
					float dy = y-by;
					
					// Add pc to bin only if its distance to the pc center
					// is less than its radius + half the bin's diagonal.
					// This is a simple necessary condition (not sufficient) 
					// for the intersection between a circle and a square.
					if( Math.sqrt(dx*dx+dy*dy) <= r + half_bin_diagonal){
						aux_bins[i][j].add(id);
					}
				}
				
			}
		}
		
		
		// create the actual bins
		for(int i=0; i<xbins; i++)
			for(int j=0; j<ybins; j++) {	
				var size = aux_bins[i][j].size();
				var b_ids = new int[size];
				var b_xs = new float[size];
				var b_ys = new float[size];
				var b_rs = new float[size];
				var b_ks = new float[size];
				
				for(int k=0; k <size; k++) {
					var id = aux_bins[i][j].get(k);
					b_ids[k] = id;
					b_xs[k] = pcs.xs[id];
					b_ys[k] = pcs.ys[id];
					b_rs[k] = pcs.rs[id];
					b_ks[k] = pcs.ks[id];
				}
				pc_bins[i][j] = new PlaceCells(b_xs, b_ys, b_rs, b_ks, b_ids);
				
			}
	}
	
	/**
	 * Computes the activation of all cell in the bin containing the given point
	 * @param x The point's x cooridnate
	 * @param y The point's y coordinate
	 * @return  Returns the x and y indices of the bin
	 */
	public float activateBin(float x, float y) {
		active_x_id = (int)Math.floor((x-minx)/bin_size);
		active_y_id = (int)Math.floor((y-miny)/bin_size);
		active_pcs = pc_bins[active_x_id][active_y_id];
		return active_pcs.activate(x, y);
	}
	
	/**
	 * Computes the bin containing a given point
	 * @param x The point's x cooridnate
	 * @param y The point's y coordinate
	 * @return  Returns the x and y indices of the bin
	 */
	private int[] getBin(float x, float y) {
		var xbin = (int)Math.floor((x-minx)/bin_size);
		var ybin = (int)Math.floor((y-miny)/bin_size);
		return new int[] {xbin, ybin} ;
	}
		
	public void clear() {
		active_pcs = null;
	}

}
