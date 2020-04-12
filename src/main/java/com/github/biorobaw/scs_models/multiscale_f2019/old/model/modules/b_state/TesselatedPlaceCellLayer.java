package com.github.biorobaw.scs_models.multiscale_f2019.old.model.modules.b_state;

import java.util.ArrayList;
import java.util.List;

import com.vividsolutions.jts.geom.Coordinate;

import edu.usf.micronsl.module.Module;
import edu.usf.micronsl.port.onedimensional.array.Float1dPortArray;
import edu.usf.micronsl.port.onedimensional.vector.PointPort;
import edu.usf.micronsl.port.singlevalue.Float0dPort;
import edu.usf.micronsl.port.twodimensional.Float2dSingleBlockMatrixPort;

/**
 * This layer locates place cells in a tesselated grid laid over the
 * environment.
 * 
 * @author Martin Llofriu
 *
 */
public class TesselatedPlaceCellLayer extends Module {

	/**
	 * The list of all place cells
	 */
	private ArrayList<PlaceCell> cells;

	/**
	 * Whether the layer is active or not
	 */
	private boolean active;

	/**
	 * The activation output port. A sparse port is used for efficiency.
	 */
	private Float2dSingleBlockMatrixPort activationPort;
	private Float0dPort totalActivation;

	private String placeCellType;

	private float radius;
	private float distanceXBetweenCells;
	private float distanceYBetweenCells;

	private float xmin;

	private float ymin;

	private int numCellsX;
//	private int numCellsY;

	/**
	 * Creates all the place cells and locates them in a tesselated grid laid over
	 * the environment.
	 * 
	 * @param name          The module's name
	 * @param robot         A robot capable of providing localization information
	 * @param radius        The radius of the place cells
	 * @param numCellsX     Number of cells per side on the x axis
	 * @param numCellsY     Number of cells per side on the y axis
	 * @param placeCellType The type of place cells to use. Proportional and
	 *                      exponential place cells are supported.
	 * @param xmin          The minimum x value of the box in which place cells are
	 *                      located
	 * @param ymin          The minimum y value of the box in which place cells are
	 *                      located
	 * @param xmax          The maximum x value of the box in which place cells are
	 *                      located
	 * @param ymax          The maximum y value of the box in which place cells are
	 *                      located
	 */
	public TesselatedPlaceCellLayer(String name, float radius, int numCellsX, int numCellsY, String placeCellType,
			float xmin, float ymin, float xmax, float ymax) {
		super(name);

		this.active = true;
		this.placeCellType = placeCellType;
		this.radius = radius;

		this.cells = new ArrayList<PlaceCell>();

		distanceYBetweenCells = (ymax - ymin) / (numCellsY - 1);
		distanceXBetweenCells = (xmax - xmin) / (numCellsX - 1);
		this.xmin = xmin;
		this.ymin = ymin;
		this.numCellsX = numCellsX;
//		this.numCellsY = numCellsY;

		for (int i = 0; i < numCellsY; i++) {
			float y = ymin + i * distanceYBetweenCells;
			for (int j = 0; j < numCellsX; j++) {
				float x = xmin + j * distanceXBetweenCells;
				// Find if it intersects any wall
				cells.add(new ExponentialPlaceCell(new Coordinate(x, y), radius));


			}
		}

		int maxActivePlaCellRows = (int) (2 * radius / distanceYBetweenCells) + 1;
		int maxActivePlaCellCols = (int) (2 * radius / distanceXBetweenCells) + 1;

		// activationPort = new Float1dSparsePortMap(this, cells.size(), 4000);
		activationPort = new Float2dSingleBlockMatrixPort(this, numCellsY, numCellsX, maxActivePlaCellRows,
				maxActivePlaCellCols, 0, 0);
		
		totalActivation = new Float0dPort(this,0);
		addOutPort("total",totalActivation);
		addOutPort("activation", activationPort);

	}

	public TesselatedPlaceCellLayer(String name, float radius, int numCellsPerSide, String placeCellType, float xmin,
			float ymin, float xmax, float ymax) {
		this(name, radius, numCellsPerSide, numCellsPerSide, placeCellType, xmin, ymin, xmax, ymax);

	}

	/**
	 * Computes the current activation of all cells
	 */
	public void run() {
		run(((PointPort) getInPort("position")).get(), 0);
	}

	/**
	 * Computes the current activation of all cells given the current parameters.
	 * 
	 * @param pos        The current location of the animat
	 * @param distToWall The distance to the closest wall
	 */
	public void run(Coordinate pos, float distanceToClosestWall) {
//		MultiscaleModel1.tics[0] = Debug.tic();
		if (!active) {
			activationPort.clearBlock();
			totalActivation.set(0);
		} else {

			int firstCol = Math.max((int) Math.ceil((pos.x - radius - xmin) / distanceXBetweenCells), 0);
			int firstRow = Math.max((int) Math.ceil((pos.y - radius - ymin) / distanceYBetweenCells), 0);

			activationPort.setWindowOrigin(firstRow, firstCol);

			double total = 0;
			for (int i = 0; i < activationPort.getBlockRows(); i++)
				for (int j = 0; j < activationPort.getBlockCols(); j++) {

					// System.out.println("line: "+i + " " + j + " " + firstRow + " " + firstCol );
					float a = getCell(firstRow + i, firstCol + j).getActivation(pos, distanceToClosestWall);
					total+=a;
					activationPort.setBlock(i, j,a);

				}

			totalActivation.set((float)total);
			
//			activationPort
//			Map<Integer, Float> nonZero = activationPort.getNonZero();
//			nonZero.clear();
//			if (active) {
//				int i = 0;
//				float total = 0;
//				
//				for (PlaceCell pCell : cells) {
//					float val = pCell.getActivation(pos, distanceToClosestWall);
//					if (val != 0) {
//						nonZero.put(i, val);
//						total += val;
//					}
//					i++;
//				}
//				
//				if (Float.isNaN(total))
//					System.out.println("Numeric error");
//			}
		}
//		MultiscaleModel1.tocs[1] = Debug.toc(MultiscaleModel1.tics[0]);

	}

	public PlaceCell getCell(int i, int j) {
		return cells.get(i * numCellsX + j);
	}

	/**
	 * Returns the activation of all cells
	 * 
	 * @param pos The current position of the animat.
	 * @return An array of the activation values
	 */
	public float[] getActivationValues(Coordinate pos) {
		float distanceToClosestWall = 0; // value not used
		float[] res = new float[cells.size()];

		for (int i = 0; i < cells.size(); i++) {
			res[i] = cells.get(i).getActivation(pos, distanceToClosestWall);
		}

		return res;
	}

	public List<PlaceCell> getCells() {
		return cells;
	}

	public void deactivate() {
		active = false;
	}

	@Override
	public boolean usesRandom() {
		return false;
	}

	public void clear() {
		((Float1dPortArray) getOutPort("activation")).clear();
	}

//	public Float1dSparsePortMap getActivationPort(){
//		return activationPort;
//	}

	public Float2dSingleBlockMatrixPort getActivationPort() {
		return activationPort;
	}
	
	public Float0dPort getTotalPort() {
		return totalActivation;
	}

	public void setPCs(float[][] centers) {
		cells.clear();
		for (float[] c : centers) {
			float x = c[0];
			float y = c[1];
			if (placeCellType.equals("exponential"))
				cells.add(new ExponentialPlaceCell(new Coordinate(x, y), radius));

		}
	}

}
