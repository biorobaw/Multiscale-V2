package com.github.biorobaw.scs_models.multiscale_f2019.gui.fx.drawers;



import java.text.DecimalFormat;
import java.util.Vector;

import com.github.biorobaw.scs.gui.displays.java_fx.PanelFX;
import com.github.biorobaw.scs.gui.displays.java_fx.drawer.DrawerFX;
import com.github.biorobaw.scs.utils.math.Floats;

import com.github.biorobaw.scs_models.multiscale_f2019.model.modules.b_state.PlaceCells;
import javafx.scene.control.Label;
import javafx.scene.layout.AnchorPane;
import javafx.scene.layout.Pane;
import javafx.scene.layout.StackPane;
import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;
import javafx.scene.transform.NonInvertibleTransformException;
import javafx.scene.transform.Translate;

public class VDrawer extends DrawerFX {

	PlaceCells pcs;
	float[] pc_x;		 // x coordinate of each cell
	float[] pc_y;		 // y coordinate of each cell
	float[] pc_r;
	int num_cells;

	float[][] vtables;
	int layer;
	float[] v_copy = null;	// copy of values


	public int distanceOption = 1; //0 to use predefined radius, 1 to use minDist and choose automatically
	public double radius = 0.01;
		
	float maxValue = Float.NEGATIVE_INFINITY;
	float minValue = 0; // min value, below this value, no hue is used
	
	float maxData = 0;
	float minData = 0;
	
	public boolean fixed_range = false;
	
	/**
	 * 
	 * @param get_xs function to get pcs x coordinate
	 * @param get_ys function to get pcs y coordinate
	 * @param get_vs function to get pcs values
	 * @param distance_option 0 to use fixed radius, 1 to choose automatically according to pc spacing
	 */
	public VDrawer(PlaceCells cells, float[][] vtables, int layer, int distance_option) {
		this.pcs = cells;
		this.vtables = vtables;
		this.layer = layer;

		this.v_copy = Floats.copy(vtables[layer]);
		this.pc_x = pcs.xs;
		this.pc_y = pcs.ys;
		this.pc_r = pcs.rs;
		num_cells = pc_x.length;


		// If choose radius automatically
		if(distance_option == 1) {
			radius = Double.MAX_VALUE;
			for(int i=0;i<num_cells;i++)
				for(int j=i+1;j<num_cells;j++){
					float dx = pc_x[i]-pc_x[j];
					float dy = pc_y[i]-pc_y[j];
					radius = Math.min(radius, dx*dx+dy*dy);
				}
			radius = Math.sqrt(radius)/2;
		}

		
		
	}

	public VDrawer(PlaceCells cells, float[][] vtables, int layer){
		this(cells,vtables,layer,1);
	}

	@Override
	public void updateData() {

		this.v_copy = Floats.copy(vtables[layer]);
		this.pc_x = pcs.xs;
		this.pc_y = pcs.ys;
		this.pc_r = pcs.rs;
		num_cells = pc_x.length;

		maxData = Floats.max(v_copy);
		minData = Floats.min(v_copy);
		if(!fixed_range) maxValue = maxData;
		
//		if(maxValue == 0) maxValue = Float.NEGATIVE_INFINITY;
	}
	
	public void setMinValue(float min) {
		minValue = min;
	}
	
	public void setMaxValue(float max) {
		maxValue = max;
	}
	

	
	public Color getColor(float val,float max){
//		if (val<minValu e) val = 0;
		var h = val < 0 ? Color.BLUE.getHue() : Color.RED.getHue();
		var s = Math.abs(val)/max;
		if(s>1) s = 1;
		float b = 0.8f;
		float alpha = 0.05f;
		
		return  Color.hsb(h, s, b, alpha);
//		var hue = Color.BLUE.getHue() + ()
//		return Color.hsb(hue, 1, 1, 0.5);
		
	}

	@Override
	protected DrawerScene createGraphics(PanelFX panel) {
		return new DrawerGraphics(panel);
	}
	
	class DrawerGraphics extends DrawerScene {

		Vector<Circle> cells = new Vector<>();
		
		Translate label_pos = new Translate(3, 0);
		
		Label label_range = new Label("Range: ");
		AnchorPane anchor_pane = new AnchorPane(label_range);
		Pane data_panel = root;
		StackPane stack_pane = new StackPane(data_panel, anchor_pane);
		
		DecimalFormat format = new DecimalFormat("0.###");
		
		public DrawerGraphics(PanelFX panel) {
			super(panel);
			root = stack_pane;

			addCells();

			AnchorPane.setBottomAnchor(label_range, 5.);
			AnchorPane.setLeftAnchor(label_range, 3.);
		}

		@Override
		public void update() {
			addCells();

			// set color of all cells
			for(int i=0; i<num_cells; i++) {
				cells.get(i).setFill(getColor(v_copy[i],maxValue));
				if(v_copy[i] > 0 ) cells.get(i).toFront();
			}
			label_range.setText("Range: " + format.format(minData) + " ~ " + format.format(maxData));
		}

		public void addCells(){
			int current_count = cells.size();
			for(int i=current_count; i<num_cells; i++) {
				var cell = new Circle(pc_x[i], pc_y[i], pc_r[i], Color.TRANSPARENT);
				cells.add(cell);
				data_panel.getChildren().add(cell);
			}

		}
		

	}
	
	
	
}
