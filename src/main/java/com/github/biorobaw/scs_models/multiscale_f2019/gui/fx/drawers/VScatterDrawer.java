package com.github.biorobaw.scs_models.multiscale_f2019.gui.fx.drawers;



import java.util.LinkedList;

import com.github.biorobaw.scs.gui.displays.java_fx.PanelFX;
import com.github.biorobaw.scs.gui.displays.java_fx.drawer.plot.Plot;
import com.github.biorobaw.scs.utils.math.Doubles;
import com.github.biorobaw.scs.utils.math.Floats;
import com.github.biorobaw.scs.utils.math.RandomSingleton;
import com.github.biorobaw.scs_models.multiscale_f2019.model.modules.b_state.PlaceCells;

import javafx.scene.paint.Color;
import javafx.scene.shape.Ellipse;

public class VScatterDrawer extends Plot {

	// DRAWING PARAMETERS
	public double radius = 8;
	public Color color = Color.hsb(240, 0.8, 1, 0.1 );
	public float jitter_width_percentage = 0.03f;
	LinkedList<DrawerGraphics> all_graphics = new LinkedList<>(); // array with all JFX graphics 
	
	// DATA
	PlaceCells[] pcs;
	float[][] values;
	float[][] values_pointer;
	boolean update_data = false;
	boolean update_graphics = false;

	
	/**
	 * 
	 * @param pc_x
	 * @param pc_y
	 * @param values
	 * @param distance_option 0 to use fixed radius, 1 to choose automatically according to pc spacing
	 */
	public VScatterDrawer(double miny, double maxy, PlaceCells[] pcs, float[][] values) {
		
		double mx = Double.POSITIVE_INFINITY, Mx = Double.NEGATIVE_INFINITY;
		for(var p : pcs) {
			var min = Floats.min(p.rs);
			if(min < mx)  mx = min;
			
			var max = Floats.max(p.rs);
			if(max > Mx)  Mx = max;
		}
		
		resize_plot(mx - 0.04, -1.5, Mx+0.04, 1.5);
		
		this.pcs = pcs;
		this.values_pointer = values;
		
		this.values = new float[values.length][];
		for(int i=0; i<values.length; i++) {
			this.values[i] = new float[pcs[i].num_cells]; // init copy of pc values
			
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
			for(int i=0; i < values.length; i++) {
				Floats.copy(values_pointer[i], values[i]);		
			}
			
			update_data = false;
			update_graphics = true;
		}
	}
	

	@Override
	protected DrawerScene createGraphics(PanelFX panel) {
		return new DrawerGraphics(panel);
	}
	
	class DrawerGraphics extends PlotScene {

		Ellipse v_cicles[][] = new Ellipse[pcs.length][];
		
		double circle_radius_x = radius*pixel_x; // note: x and y scale factors are different
		double circle_radius_y = radius*pixel_y; // note: x and y scale factors are different
		
		
		
		public DrawerGraphics(PanelFX panel) {
			super(panel);
			all_graphics.add(this);
			label_x_axis.setText("radius");
			label_y_axis.setText("value");
			
			
			// Random to add jitter to points:
			var random = RandomSingleton.getInstance();
			var amplitude = (maxx-minx + 0.08)*jitter_width_percentage;  // 0.08 is the width that we always add to the plot
			
			// create circles
			for(int i=0; i<pcs.length; i++) {
				var pci = pcs[i];
				var vs = new Ellipse[pci.num_cells];
				for(int j=0; j < pci.num_cells; j++) {
					var jitter_x = amplitude*(2*random.nextDouble()-1);
					vs[j] = new Ellipse(pci.rs[i] + jitter_x, 0, circle_radius_x, circle_radius_y);
					vs[j].setFill(color);					
				}
				v_cicles[i] = vs;
				data.getChildren().addAll(vs);
			}

		}

		@Override
		public void update() {
			if(update_graphics) {
				for(var g : all_graphics) {
					for(int i=0; i<pcs.length; i++) {
						var v_circles = g.v_cicles[i];
						var vs = values[i];
						for( int j=0; j<vs.length; j++) {
							var vsj = vs[j];
							v_circles[j].setCenterY( vsj > maxy ? maxy : vsj < miny ? miny : vsj);
//							v_circles[j].setCenterY( vsj );
						}
					}
				}
				update_graphics = false;
			}
		}
		

	}
	
	
	
}
