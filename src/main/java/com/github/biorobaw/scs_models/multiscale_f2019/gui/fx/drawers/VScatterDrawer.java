package com.github.biorobaw.scs_models.multiscale_f2019.gui.fx.drawers;



import java.util.LinkedList;
import java.util.Random;
import java.util.Vector;

import com.github.biorobaw.scs.gui.displays.java_fx.PanelFX;
import com.github.biorobaw.scs.gui.displays.java_fx.drawer.plot.Plot;
import com.github.biorobaw.scs.utils.math.Floats;
import com.github.biorobaw.scs.utils.math.Integers;
import com.github.biorobaw.scs.utils.math.RandomSingleton;
import com.github.biorobaw.scs_models.multiscale_f2019.model.modules.b_state.PlaceCells;

import javafx.scene.paint.Color;
import javafx.scene.shape.Ellipse;

public class VScatterDrawer extends Plot {

	// DRAWING PARAMETERS
	public double radius = 4;
	public Color color = Color.hsb(240, 0.8, 1, 0.1 );
	public float jitter_width_percentage = 0.03f;
	LinkedList<DrawerGraphics> all_vscatter_drawers = new LinkedList<>(); // array with all JFX graphics
	
	// DATA
	PlaceCells[] pcs;
	float[][] values;
	float[][] values_pointer;
	boolean update_data = false;
	boolean update_graphics = false;
	int num_cells[];

	double min_radius = Double.POSITIVE_INFINITY;
	double max_radius = 0;

	
	/**
	 * Plots PC values vs PC radius, updated after each episode
	 *
	 * @param miny min y coordinate
	 * @param maxy max y coordinate
	 * @param pcs  pointer to the place cell layers
	 * @param values pointer to the values of the pc layers
	 */
	public VScatterDrawer(double miny, double maxy, PlaceCells[] pcs, float[][] values) {

		// init number of cells
		this.pcs = pcs;
		this.values_pointer = values;
		num_cells = Integers.constant(0, pcs.length);

		updateMinMaxRadius();
		resize_plot(0, -1.5, 0.60, 1.5);


		this.values = new float[values.length][];

	}

	void updateMinMaxRadius(){
		for(int layer=0; layer<pcs.length; layer++){
			var pcs_layer = pcs[layer];
			for(int i=num_cells[layer]; i< pcs_layer.num_cells; i++){
				if(pcs_layer.rs[i] < min_radius) min_radius = pcs_layer.rs[i];
				if(pcs_layer.rs[i] > max_radius) max_radius = pcs_layer.rs[i];
			}
		}
	}

	@Override
	public void newEpisode() {
		// At new episode raise data changed flag
		update_data = true;
	}


	@Override
	public void updateData() {
		// at update, if data changed, copy data and raise flag to update graphics
		if(update_data) {

//			updateMinMaxRadius();
			for(int i=0; i < values.length; i++) {
				values[i] = Floats.copy(values_pointer[i]);
				num_cells[i] = values[i].length;
			}

			update_data = false;
			update_graphics = true;
//			resize_plot(min_radius - 0.04, -1.5, max_radius+0.04, 1.5);
		}
	}
	

	@Override
	protected DrawerScene createGraphics(PanelFX panel) {
		return new DrawerGraphics(panel);
	}
	
	class DrawerGraphics extends PlotScene {

		Vector<Ellipse>[] v_circles = new Vector[pcs.length];
		
		double circle_radius_x = radius*pixel_x; // note: x and y scale factors are different
		double circle_radius_y = radius*pixel_y; // note: x and y scale factors are different
		double amplitude;
		Random random;
		
		
		public DrawerGraphics(PanelFX panel) {
			super(panel);
			all_vscatter_drawers.add(this);
			label_x_axis.setText("radius");
			label_y_axis.setText("value");
			
			
			// Random to add jitter to points:
			random = RandomSingleton.getInstance();
			amplitude = (maxx-minx)*jitter_width_percentage;  // 0.08 is the width that we always add to the plot

			for(int i=0; i<pcs.length; i++) v_circles[i] = new Vector<>();


		}

		@Override
		public void update() {
			if(update_graphics) {

				addData();

				for(var d : all_vscatter_drawers) {
					for(int i=0; i<pcs.length; i++) {
						var v_circles = d.v_circles[i];
						var vs = values[i];
						for( int j=0; j<vs.length; j++) {
							var vsj = vs[j];
							v_circles.get(j).setCenterY( vsj > maxy ? maxy : vsj < miny ? miny : vsj);
//							v_circles[j].setCenterY( vsj );
						}
					}
				}
				update_graphics = false;
			}
		}

		void addData(){
			// create circles
			var children = data.getChildren();
			for(int i=0; i<pcs.length; i++) {
				var pci = pcs[i];
				var v_circlesi = v_circles[i];
				for(int j=0; j < num_cells[i]; j++) {
					var jitter_x = amplitude*(2*random.nextDouble()-1);
					var e = new Ellipse(pci.rs[i] + jitter_x, 0, circle_radius_x, circle_radius_y);
					e.setFill(color);
					v_circlesi.add(e);
					children.add(e);
				}

			}
			System.out.println("Resizing plot  " + min_radius + " " +  max_radius);
		}
		

	}
	
	
	
}
