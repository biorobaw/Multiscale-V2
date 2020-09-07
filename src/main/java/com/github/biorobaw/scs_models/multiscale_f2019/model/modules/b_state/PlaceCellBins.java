package com.github.biorobaw.scs_models.multiscale_f2019.model.modules.b_state;

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
	
	float minx, miny, maxx, maxy, bin_size; // min bin coordinates and size of bins
	int xbins, ybins;		   // number of bins in the x and y directions respectively
	
	public float averageBinSize = 0;  // average number of elements in a bin
	
	private PlaceCells pc_bins[][];
	private PlaceCells dummyBin = new PlaceCells();
	private int active_x_id, active_y_id; // x and y indeces of the active bin
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
		maxx = Floats.max(Floats.add(pcs.xs, pcs.rs));
		maxy = Floats.max(Floats.add(pcs.ys, pcs.rs));
//		System.out.println("mx,Mx,my,My: " + minx + " " + maxx + " " + miny + " " + maxy);
		
		
		// find how many bins are necessary
		xbins = (int)Math.ceil((maxx-minx)/bin_size)+1; // we add one for the special case (maxx-minx)%binSize == 0
		ybins = (int)Math.ceil((maxy-miny)/bin_size)+1; // we add one for the special case (maxy-miny)%binSize == 0

//		System.out.println("bin size: " + bin_size + " " + xbins + " " + ybins);
		
		// create the bins
		pc_bins = new PlaceCells[xbins][ybins];

		
		// create auxiliary bins for holding ids
		@SuppressWarnings("unchecked")
		ArrayList<Integer>[][] aux_bins = new ArrayList[xbins][ybins];
		for(int i=0; i<xbins; i++)
			for(int j=0; j<ybins; j++)
				aux_bins[i][j] = new ArrayList<>();
		
		
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
				float min_bin_x = minx + i*bin_size;
				float max_bin_x = min_bin_x + bin_size;
				
				for(int j=minBins[1]; j<=maxBins[1]; j++) {
					float min_bin_y = miny + j*bin_size;
					float max_bin_y = min_bin_y + bin_size;
					
					// if place cell intersects bin, add it
					if(circleIntersectsRectangle(x, y, r, min_bin_x, max_bin_y, max_bin_x, min_bin_y))
						aux_bins[i][j].add(id);
					
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
				averageBinSize+=size;
			}
		averageBinSize/=(xbins*ybins);
	}
	
	/**
	 * Computes the activation of all cell in the bin containing the given point
	 * @param x The point's x cooridnate
	 * @param y The point's y coordinate
	 * @return  returs the total activation of the active bin
	 */
	public float activateBin(float x, float y) {
		if( minx < x && x < maxx && miny < y && y < maxy ) {
			active_x_id = (int)Math.floor((x-minx)/bin_size);
			active_y_id = (int)Math.floor((y-miny)/bin_size);
			active_pcs = pc_bins[active_x_id][active_y_id];
		} else {
			active_x_id = -1;
			active_y_id = -1;
			active_pcs  = dummyBin; 
				
		}
//		System.out.println("active " + active_x_id + " " + active_y_id + " " + x + " " + y + pc_bins.length + " " + pc_bins[0].length );
//		System.out.println("x,y: " + x + " " + y +" " +  active_x_id + " " + active_y_id);
//		System.out.println("active length: " + active_pcs.num_cells);
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
	
	public boolean circleIntersectsRectangle(float cx, float cy, float radius, float left, float top, float right, float bottom)
	{
	   float closestX = (cx < left ? left : (cx > right ? right : cx));
	   float closestY = (cy > top ? top : (cy < bottom ? bottom : cy));
	   float dx = closestX - cx;
	   float dy = closestY - cy;

	   return ( dx * dx + dy * dy ) <= radius * radius;
	}

}
