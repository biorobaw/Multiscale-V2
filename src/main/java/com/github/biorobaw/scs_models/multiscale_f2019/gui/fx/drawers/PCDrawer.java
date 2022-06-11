package com.github.biorobaw.scs_models.multiscale_f2019.gui.fx.drawers;



import com.github.biorobaw.scs.gui.displays.java_fx.PanelFX;
import com.github.biorobaw.scs.gui.displays.java_fx.drawer.DrawerFX;
import com.github.biorobaw.scs.utils.math.Floats;
import com.github.biorobaw.scs.utils.math.Integers;

import com.github.biorobaw.scs_models.multiscale_f2019.model.modules.b_state.PlaceCellBins;
import com.github.biorobaw.scs_models.multiscale_f2019.model.modules.b_state.PlaceCells;
import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;

import java.util.Vector;


public class PCDrawer extends DrawerFX {

	
	final static double GRAY_VALUE = 180.0/256;
	final static Color GRAY = new Color(GRAY_VALUE, GRAY_VALUE, GRAY_VALUE, 1);
	
	PlaceCells cells;    // pointer to the actual place cells
	PlaceCellBins bins;  // point to the actual place cell bins
	float[] pc_x;		 // x coordinate of each cell
	float[] pc_y;		 // y coordinate of each cell
	float[] pc_r;		 // radius of each cell
	int num_cells;		 // total number of cells
	
	float[] activations; // activity of active cells
	int[] ids;			 // ids of active cells
	
	float radius = -1; // used when all pcs have the same radius

//	HashMap<Integer, Float> values = new HashMap<>();


	public PCDrawer(PlaceCells cells, PlaceCellBins bins) {
		this.cells = cells;
		this.bins = bins;
		this.pc_x = cells.xs;
		this.pc_y = cells.ys;
		this.pc_r = cells.rs;
		num_cells = pc_x.length;
		radius = Floats.max(pc_r);
	}


	@Override
	public void newEpisode() {
		super.newEpisode();
		ids = null;
	}

	@Override
	public void updateData() {
		// must check if number of cells is still the same, if not, must copy new cells

		this.pc_x = cells.xs;
		this.pc_y = cells.ys;
		this.pc_r = cells.rs;
		num_cells = pc_x.length;

		ids = bins.active_pcs.ids;
		if(ids != null) {
			activations = Floats.copy(bins.active_pcs.as);
		} else {
			activations = new float[0]; // dummy, not active cells
		}
		
	}
	
	
	static public Color getColor(float val){
		float i = 0.4f;
		float alpha = i+(1f-i)*(val-0.2f)/(1f-0.2f);
		alpha =0.8f;
		float m = 0.2f;
		float beta  = m+(0.73f-m)*(val-0.2f)/(1f-0.2f);
//		max = (float)Math.max(max, alpha);
//		alpha = (float)Math.sqrt(alpha);
		return  new Color(0f, 0.9f, alpha, beta);
	}


	@Override
	protected DrawerScene createGraphics(PanelFX panel) {
		return new DrawerGraphics(panel);
	}
	
	class DrawerGraphics extends DrawerScene {

		Vector<Circle> base_circles = new Vector<>();
		Vector<Circle> active_circles = new Vector<>();
		
		int[] old_ids = new int[] {};
		
		public DrawerGraphics(PanelFX panel) {
			super(panel);
			addCells();
		}
		


		@Override
		public void update() {
			// add new cells if necessary:
			addCells();

			// clear old ids:
			for(var id : old_ids){
				active_circles.get(id).setFill(Color.TRANSPARENT);
				active_circles.get(id).setVisible(false);
			}
			if(ids == null) return;
			old_ids = Integers.copy(ids);
			
			for(int i = 0; i < old_ids.length; i++) {
				var active = active_circles.get(old_ids[i]);
				if(activations[i] == 0) continue;
				active.setVisible(true);
				active.setFill(getColor(activations[i]));
				active.toFront();
			}
			
		}

		private void addCells(){
			int current_count = base_circles.size();
			for(int i=current_count; i<num_cells; i++) {
				var c = new Circle(pc_x[i], pc_y[i], pc_r[i], Color.TRANSPARENT);
				c.setStroke(Color.GRAY);
					c.setStrokeWidth(0.01);
				base_circles.add( c );
				root.getChildren().add( c );
				c.toBack();
			}

			for(int i=current_count; i<num_cells; i++) {
				var c = new Circle(pc_x[i], pc_y[i], pc_r[i], Color.TRANSPARENT);
				active_circles.add(c);
				root.getChildren().add(c);
				c.setVisible(false);

			}
		}
		
	}
	
}
