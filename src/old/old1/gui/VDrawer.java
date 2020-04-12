package com.github.biorobaw.scs_models.multiscale_f2019.old.gui;


import java.awt.Color;
import java.awt.Graphics;
import java.util.HashMap;
import java.util.List;

import com.github.biorobaw.scs.gui.Drawer;
import com.github.biorobaw.scs.gui.utils.GuiUtils;
import com.github.biorobaw.scs.gui.utils.Scaler;
import com.github.biorobaw.scs.gui.utils.Window;
import com.github.biorobaw.scs_models.multiscale_f2019.old.model.modules.b_state.PlaceCell;

import edu.usf.micronsl.port.twodimensional.sparse.Entry;
import edu.usf.micronsl.port.twodimensional.sparse.Float2dSparsePort;

public class VDrawer extends Drawer {

	float[][] centers;
	Float2dSparsePort stateValues;
	public int distanceOption = 1; //0 to use radius and diam, 1 to use minDist and choose automatically
	float minDist = Float.POSITIVE_INFINITY;
	int radius = 2;
	
	
	float maxValue = Float.NEGATIVE_INFINITY;
	
	HashMap<Entry,Float> nonZero = new HashMap<>();
	

	public VDrawer(List<PlaceCell> pcs,Float2dSparsePort stateValuePort) {
		centers = new float[pcs.size()][];
		for(int i=0;i<pcs.size();i++){
			var c = pcs.get(i).getPreferredLocation();
			centers[i]= new float[] {(float)c.x,(float)c.y} ;
		}
		stateValues = stateValuePort;
		
		for(int i=0;i<pcs.size();i++)
			for(int j=i+1;j<pcs.size();j++){
				double dx = centers[i][0]-centers[j][0];
				double dy = centers[i][1]-centers[j][1];
				minDist = (float)Math.min(minDist, dx*dx+dy*dy);
			}
		minDist = (float)Math.sqrt(minDist)/2;
		
	}

	@Override
	public void draw(Graphics g, Window<Float> panelCoordinates) {
		if(!doDraw) return;
		
		
		
		
		Scaler s = new Scaler(worldCoordinates, panelCoordinates, true);
		
		int coords[][] = s.scale(centers);
		
		int r = radius;
		if(distanceOption==1) r = Math.round(s.scaleDistanceX(minDist));
		int d = 2*r;

		
		
		
		for(int i=0; i <stateValues.getNRows();i++){
			
			Float value = nonZero.get(new Entry(i, 0));
			if(value==null) value = 0f;
			
			g.setColor(getColor(value,maxValue));
			g.fillOval(coords[0][i]-r, coords[1][i]-r, d, d);
			
		}
		
		g.setColor(Color.BLACK);
		g.drawString("MAX:   " + maxValue, 20, 20);

	}

	@Override
	public void endEpisode() {
		
	}

	@Override
	public void updateData() {
		nonZero.clear();
//		if(stateValues.getNonZero().size() > 0 ) {
//			System.out.println("NON ZERO!!!!!!!!!!");
//		}
		nonZero.putAll(stateValues.getNonZero());
		maxValue = GuiUtils.findMaxInMap(nonZero);
		
	}
	

	
	public Color getColor(float val,float max){
		
		float h = val < 0 ? 0.66f : 0f;
		float s = (float)Math.abs(val)/max;
		float b = 0.8f;
		float alpha = 0.5f;

		return  GuiUtils.getHSBAColor(h,s,b,alpha);
	}
	
	
	public void setRadius(int r){
		radius = r;
	}
}
