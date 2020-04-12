package com.github.biorobaw.scs_models.multiscale_f2019.old2.gui.drawers;


import java.awt.Color;
import java.awt.Graphics;
import java.util.HashMap;

import com.github.biorobaw.scs.gui.Drawer;
import com.github.biorobaw.scs.gui.utils.GuiUtils;
import com.github.biorobaw.scs.gui.utils.Scaler;
import com.github.biorobaw.scs.gui.utils.Window;
import com.github.biorobaw.scs.utils.math.Floats;
import com.github.biorobaw.scs_models.multiscale_f2019.old2.model.modules.b_state.PlaceCells;

import edu.usf.micronsl.port.twodimensional.sparse.Entry;

public class VDrawer extends Drawer {

	float[] pc_x;
	float[] pc_y;
	int numCells;
	float[] values;
	float[] v_copy = null;

	public int distanceOption = 1; //0 to use radius and diam, 1 to use minDist and choose automatically
	float minDist = Float.POSITIVE_INFINITY;
	int radius = 2;
	
	float maxValue = Float.NEGATIVE_INFINITY;
	float minValue = 0; // min value, below this value, no hue is used
	
	HashMap<Entry,Float> nonZero = new HashMap<>();
	

	public VDrawer(PlaceCells pcs, float[] values) {
		this.values = values;

		pc_x = pcs.xs;
		pc_y = pcs.ys;
		numCells = pcs.num_cells;
		
		for(int i=0;i<numCells;i++)
			for(int j=i+1;j<numCells;j++){
				float dx = pc_x[i]-pc_x[j];
				float dy = pc_y[i]-pc_y[j];
				minDist = (float)Math.min(minDist, dx*dx+dy*dy);
			}
		minDist = (float)Math.sqrt(minDist)/2;
		
		v_copy = new float[numCells];
		
	}

	@Override
	public void draw(Graphics g, Window<Float> panelCoordinates) {
		if(!doDraw) return;
		
		Scaler s = new Scaler(worldCoordinates, panelCoordinates, true);
		var scaled_x = s.scaleX(pc_x);
		var scaled_y = s.scaleY(pc_y);

		float r = radius;
		if(distanceOption==1) r = s.scaleDistanceX(minDist);
		int d = Math.round(2*r);


		for(int i=0; i <numCells;i++){
			
			g.setColor(getColor(v_copy[i],maxValue));
			g.fillOval(Math.round(scaled_x[i]-r),
					   Math.round(scaled_y[i]-r), 
					   d, d);
			
		}
		
		g.setColor(Color.BLACK);
		g.drawString("MAX:   " + maxValue, 20, 20);

	}

	@Override
	public void endEpisode() {
		
	}

	@Override
	public void updateData() {
		Floats.copy(values, v_copy);
		maxValue = Floats.max(v_copy);	
		if(maxValue == 0) maxValue = Float.NEGATIVE_INFINITY;
	}
	
	public void setMinValue(float min) {
		minValue = min;
	}
	

	
	public Color getColor(float val,float max){
		if (val<minValue) val = 0;
		float h = val < minValue ? 0.66f : 0f;
		float s = (float)Math.abs(val)/max;
		float b = 0.8f;
		float alpha = 0.5f;

		return  GuiUtils.getHSBAColor(h,s,b,alpha);
	}
	
	
	public void setRadius(int r){
		radius = r;
	}
	
}
