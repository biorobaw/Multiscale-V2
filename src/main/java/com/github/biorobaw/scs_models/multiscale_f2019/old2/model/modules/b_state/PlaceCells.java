package com.github.biorobaw.scs_models.multiscale_f2019.old2.model.modules.b_state;





import org.apache.commons.lang3.ArrayUtils;

import com.github.biorobaw.scs.experiment.Experiment;
import com.github.biorobaw.scs.utils.math.Floats;

/**
 * Class to operate with place cells.
 * The class creates a set of place cells, 
 * and distributes them into bins to allow quick computation of non zero activation values.
 * @author bucef
 *
 */
public class PlaceCells {
	
	// minimum activation of a place cell (value at its border)
	static final float min_activation = 0.2f;
	static final float numerical_error_tolerance = 0.01f; // 1cm
	
	// total number of cells in the set
	public int num_cells;
	
	
	public float[] xs; // the x coordinates in the set
	public float[] ys; // the y coordinates in the set
	public float[] rs; // the radii of the cells
	public float[] ks; // the constant part of the pc equation e^(k*d^2) for each cell
	public int[]  ids; // the id associated to each cell in the set

	public float[] as; // the activation of each cell in the set
	public float[] r2s;// precalculated r squared values
	public float[] ns; // normalized activation
	
	public float total_a; // the total activation of the layer (the sum)
	
	
	/**
	 * Create a single layer of tesselated place cells.
	 * @param mazeWidth The width of the maze
	 * @param mazeHeight The height of the maze
	 * @param pcSizes The size (radius) of the place cells
	 * @param numPCx The number of pcs in the x direction
	 */
	public PlaceCells(float mazeWidth, float mazeHeight, float pcSize, int numPCx) {
		this(mazeWidth,mazeHeight,new float[] {pcSize}, new int[] {numPCx});
	}
	
	/**
	 * Create and combine multiple layers of tesselated place cells.
	 * @param mazeWidth	The width of the maze
	 * @param mazeHeight The height of the maze
	 * @param pcSizes The sizes (radii) of each layer
	 * @param numPCx The number of pcs in the x direction for each layer
	 */
	public PlaceCells(float mazeWidth, float mazeHeight, float[] pcSizes, int[] numPCx) {
		// get number of layers
		var numLayers = pcSizes.length;

		// calculate the number of pcs in the y direction given pcx, maze width and maze height
		var numPCy = new int[numLayers];
		var numPC = new int[numLayers];
		for (int i = 0; i < numLayers; i++) {
			numPCy[i] = (int) (numPCx[i] * mazeHeight / mazeWidth);
			numPC[i] = numPCy[i] * numPCx[i];
		}
		
		// find xMax,yMax for each layer (note xMin yMin are -xMax -yMax)
		var xmin = new float[numLayers];
		var xmax = new float[numLayers];
		var ymin = new float[numLayers];
		var ymax = new float[numLayers];
		for(int i=0; i<numLayers; i++) {
			xmax[i] = mazeWidth / 2 + pcSizes[i] - (mazeWidth + 2 * pcSizes[i]) / (numPCx[i] + 1);
			ymax[i] = mazeHeight / 2 + pcSizes[i] - (mazeHeight + 2 * pcSizes[i]) / (numPCy[i] + 1);
			xmin[i] = -xmax[i];
			ymin[i] = -ymax[i];
		}
		
		// create the place cells:
		copyShallow(new PlaceCells(xmin, xmax, numPCx, ymin, ymax, numPCy, pcSizes));
		
//		try {
//			System.out.println(Arrays.toString(xs));
//			System.out.println();
//			System.out.println(Arrays.toString(ys));
//			System.out.println(Arrays.toString(rs));
//			System.in.read();
//		} catch (IOException e1) {
//			// TODO Auto-generated catch block
//			e1.printStackTrace();
//		}
		
	}

	/**
	 * Creates a set of place cells by creating and merging multiple tesselated PC layers
	 * @param xmin	array containing the min x value for each layer
	 * @param xmax	array containing the max x value for each layer
	 * @param xnum	array containing the number of pcs in the x direction for each layer
	 * @param ymin	array containing the min y value for each layer
	 * @param ymax	array containing the max y value for each layer
	 * @param ynum	array containing the number of pcs in the x direction for each layer
	 * @param radii	array containing the maximum activation radius for each layer
	 */
	public PlaceCells(float[] xmin, float[] xmax, int[] xnum, 
			float[] ymin, float ymax[], int ynum[], float[] radii) {
		
		PlaceCells pcs = new PlaceCells(xmin[0], xmax[0], xnum[0], ymin[0], ymax[0], ynum[0], radii[0]);
		for(int i=1; i<xmin.length; i++) 
			pcs = concat(pcs,new PlaceCells(xmin[i], xmax[i], xnum[i], ymin[i], ymax[i], ynum[i], radii[i]));

		copyShallow(pcs);
		
	}
	
	/**
	 * Constructor that creates a single tesselated layer of pcs
	 * @param xmin	The min x value for each layer
	 * @param xmax	The max x value for each layer
	 * @param xnum	The number of pcs in the x direction for each layer
	 * @param ymin	The min y value for each layer
	 * @param ymax	The max y value for each layer
	 * @param ynum	The number of pcs in the x direction for each layer
	 * @param radii	The maximum activation radius for each layer
	 */
	public PlaceCells(float xmin, float xmax, int xnum, float ymin, float ymax, int ynum, float radius) {
		num_cells = xnum*ynum;
		xs = new float[num_cells];
		ys = new float[num_cells];
		rs = new float[num_cells];
		ks = new float[num_cells];
		as = new float[num_cells];
		r2s = new float[num_cells];
		ids = new int[num_cells];
		ns = new float[num_cells];
		
		float r2 = (radius+numerical_error_tolerance)*(radius+numerical_error_tolerance);
		float k = (float) Math.log(min_activation)/r2;
		float dx = xnum>1 ? (xmax-xmin)/(xnum-1) : 0;
		float dy = ynum>1 ? (ymax-ymin)/(ynum-1) : 0;
		
		for(int i=0; i<xnum; i++) {
			float x = xmin + dx*i;
			for(int j=0; j<ynum; j++) {
				int id = i*ynum + j;
				xs[id] = x;
				ys[id] = ymin + dy*j;
				rs[id] = radius;
				ks[id] = k;
				r2s[id] = r2;
				ids[id] = id;
			}
		}
	}
	
	/**
	 * Constructor that creates a wrapper around the function arguments and completes remaining fields.
	 * @param xs x coordinate of each pc
	 * @param ys y coordinate of each pc 
	 * @param rs radius of each pc
	 * @param ks constant of the activation equation of each pc
	 * @param ids id of each pc
	 */
	public PlaceCells(float[] xs, float[] ys, float[] rs, float[] ks, int[] ids) {
		this.xs = xs;
		this.ys = ys;
		this.rs = rs;
		this.ks = ks;
		this.ids = ids;
		
		num_cells = xs.length;
		as  = new float[num_cells];
		r2s = new float[num_cells];
		ns  = new float[num_cells];
		for(int i=0; i<num_cells; i++) r2s[i] = (rs[i]+numerical_error_tolerance)*(rs[i]+numerical_error_tolerance);
		
	}
	
	/**
	 * Concat two sets of place cells
	 * @param left
	 * @param right
	 * @return A new set of place cells concatenating the previous 2 sets.
	 * The ids of place cells in the right set get aumented by the number of cells in the left set.
	 */
	static private PlaceCells concat(PlaceCells left, PlaceCells right) {
		var xs  = ArrayUtils.addAll(left.xs,  right.xs);
		var ys  = ArrayUtils.addAll(left.ys,  right.ys);
		var rs  = ArrayUtils.addAll(left.rs,  right.rs);
		var ks  = ArrayUtils.addAll(left.ks,  right.ks);
		var ids = ArrayUtils.addAll(left.ids, right.ids);
		for(int i=left.num_cells; i<left.num_cells + right.num_cells; i++)
			ids[i]+=left.num_cells;
		return new PlaceCells(xs, ys, rs, ks, ids);
	}
	
	/**
	 * A shallow copy of a set of place cells
	 * @param from
	 * @return
	 */
	public PlaceCells copyShallow(PlaceCells from) {
		this.num_cells = from.num_cells;
		
		this.xs  = from.xs;
		this.ys  = from.ys;
		this.rs  = from.rs;
		this.ks  = from.ks;
		this.ids = from.ids;
		
		this.as  = from.as;
		this.r2s = from.r2s;
		this.ns = from.ns;
		this.total_a = from.total_a;
		return this;
		
	}
	
	/**
	 * Computes the activation of each place cell.
	 * The result is stored in the field `as` 
	 * @param x The robot's current x coordinate
	 * @param y The robot's current y coordinate
	 * @return Returns the pointer 'this' to allow chaining functions
	 */
	public float activate(float x, float y) {
		total_a = 0;
		for(int i=0; i<num_cells; i++) {
			var dx = xs[i] - x;
			var dy = ys[i] - y;
			var r2 = dx*dx + dy*dy;
//			System.out.println("r2: " +r2 + " " + r2s[i] );
			if(r2 <= r2s[i]) {
				as[i] = (float)Math.exp(ks[i]*r2);
				total_a +=as[i];
			}
			else as[i] = 0;
		}
		return total_a;
	}
	
	/**
	 * Normalizes the activations of the pcs by the given value
	 * @param value
	 */
	public void normalize(float value) {
		if(value==0) {
			System.err.println("ERROR: Division by 0, place cells normalization failed");
			var e = Experiment.get();
			System.err.println("Trial-Episode-cycle: " 
								+ e.getGlobal("tria") + " " 
								+ e.getGlobal("episode") + " " 
								+ e.getGlobal("cycle"));
			e.display.updateData();
			e.display.repaint();
//			try {
//				System.in.read();
//			} catch (IOException e1) {
//				// TODO Auto-generated catch block
//				e1.printStackTrace();
//			}
			System.exit(-1);
		}
		Floats.div(as, value, ns);
	}
	
	/**
	 * TEST CODE
	 * @param args
	 */
	public static void main(String[] args) {
		var xmin = new float[] {1, 11};
		var xmax = new float[] {5, 14};
		var xnum = new int[]  {5, 4};
		
		var ymin = new float[] {1, 11};
		var ymax = new float[] {3, 12};
		var ynum = new int[]  {3, 2};
		
		var radii = new float[] {2,3};
		
		var aux = new PlaceCells(xmin, xmax, xnum, ymin, ymax, ynum, radii);
		System.out.println(aux);
		
		
		// tests with Nd4j (library no longer used)
		
//		var v = pcs.getColumn(2);
//		System.out.println(v.getFloat(0));
//		
//		var ids = NDArrayIndex.indices(new long[]{0,3,1});
//		System.err.println("original: "+ v);
//		
//		var w= v.dup();
//		w.divi(2); // is in place
//		System.out.println("divided?: " + w);
//		
//		w=v.dup();
//		Transforms.floor(w); // not in place unless specified
//		System.out.println("floored?: " + w);
//		
//		w=v.dup();
//		w.get(ids).addi(10); // here get returns a new array, not a view
//		System.out.println("added?: " + w);
//		
//		w=v.dup();
//		w.get(ids).assign(w.get(ids).addi(10)); // does not work
//		System.out.println("assign?: "+ w);
//		
//		w=v.dup();
//		w.put(new INDArrayIndex[] {ids} , w.get(ids).addi(10)); // works!!!
//		System.out.println("put?: "+ w);
//		
//		
//		
//		
//		BooleanIndexing.replaceWhere(v, 0, Conditions.lessThan(1.2)); // replacing in v replaces in original marix
//		System.out.println("replaced?:" + v);
//		System.out.println(pcs);
//		System.out.println();
//		
//		v.put(new INDArrayIndex[] {ids} , v.get(ids).addi(10)); // works!!!
//		System.out.println("put2?: "+ v);
//		System.out.println(pcs);
//		System.out.println();
		

		
		
				
	}
	
	
}
