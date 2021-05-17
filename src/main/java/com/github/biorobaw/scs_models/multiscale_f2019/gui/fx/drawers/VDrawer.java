package com.github.biorobaw.scs_models.multiscale_f2019.gui.fx.drawers;



import java.text.DecimalFormat;

import com.github.biorobaw.scs.gui.displays.java_fx.PanelFX;
import com.github.biorobaw.scs.gui.displays.java_fx.drawer.DrawerFX;
import com.github.biorobaw.scs.utils.math.Floats;

import javafx.scene.control.Label;
import javafx.scene.layout.AnchorPane;
import javafx.scene.layout.Pane;
import javafx.scene.layout.StackPane;
import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;
import javafx.scene.transform.NonInvertibleTransformException;
import javafx.scene.transform.Translate;

public class VDrawer extends DrawerFX {

	float[] pc_x;
	float[] pc_y;
	int num_cells;
	
	float[] values;	// pointer to actual values
	float[] v_copy = null;	// copy of values

	public int distanceOption = 1; //0 to use predefined radius, 1 to use minDist and choose automatically
	double radius = 0.01;
		
	float maxValue = Float.NEGATIVE_INFINITY;
	float minValue = 0; // min value, below this value, no hue is used
	
	float maxData = 0;
	float minData = 0;
	
	public boolean fixed_range = false;
		

	
	/**
	 * 
	 * @param pc_x
	 * @param pc_y
	 * @param values
	 * @param distance_option 0 to use fixed radius, 1 to choose automatically according to pc spacing
	 */
	public VDrawer(float[] pc_x, float[] pc_y, float[] values, int distance_option) {
		this.values = values;

		this.pc_x = pc_x;			
		this.pc_y = pc_y;
		num_cells = pc_x.length;
		
		v_copy = new float[num_cells]; // init copy of pc values
		
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
	
	public VDrawer(float[] pc_x, float[] pc_y, float[] values) {
		this(pc_x, pc_y, values, 1);
	}



	@Override
	public void updateData() {
		Floats.copy(values, v_copy);
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
		float alpha = 0.5f;
		
		return  Color.hsb(h, s, b, alpha);
//		var hue = Color.BLUE.getHue() + ()
//		return Color.hsb(hue, 1, 1, 0.5);
		
	}

	@Override
	protected DrawerScene createGraphics(PanelFX panel) {
		return new DrawerGraphics(panel);
	}
	
	class DrawerGraphics extends DrawerScene {

		Circle cells[] = new Circle[num_cells];
		
		Translate label_pos = new Translate(3, 0);
		
		Label label_range = new Label("Range: ");
		AnchorPane anchor_pane = new AnchorPane(label_range);
		Pane data_panel = root;
		StackPane stack_pane = new StackPane(data_panel, anchor_pane);
		
		DecimalFormat format = new DecimalFormat("0.###");
		
		public DrawerGraphics(PanelFX panel) {
			super(panel);
			root = stack_pane;
			for(int i=0; i<num_cells; i++) {
				cells[i] = new Circle(pc_x[i], pc_y[i], radius, Color.TRANSPARENT);
				data_panel.getChildren().add(cells[i]);
			}
			AnchorPane.setBottomAnchor(label_range, 5.);
			AnchorPane.setLeftAnchor(label_range, 3.);
		}

		@Override
		public void update() {
			// set color of all cells
			for(int i=0; i<num_cells; i++) {
				cells[i].setFill(getColor(v_copy[i],maxValue));
			}
			label_range.setText("Range: " + format.format(minData) + " ~ " + format.format(maxData));
		}
		

	}
	
	
	
}
