package com.github.biorobaw.multiscale_f2019.gui;


import java.awt.Color;
import java.awt.Graphics;
import java.util.ArrayList;

import com.github.biorobaw.scs.experiment.Experiment;
import com.github.biorobaw.scs.gui.Drawer;
import com.github.biorobaw.scs.gui.utils.Scaler;
import com.github.biorobaw.scs.gui.utils.Window;


public class RuntimesDrawer extends Drawer {


	Window<Float> localCoordinates; 
	
	float origin[] = {0.1f,0.1f};
	float lengths[] = {0.8f, 0.8f};
	
	
		
	ArrayList<float[]> runtimes = new ArrayList<>();
	int numEpisodes = 0;
	int minY;
	int maxY;

	public boolean doLines = true;
	public int markerSize = 2;

	public RuntimesDrawer(int numEpisodes,int minY, int maxY) {
		
		localCoordinates = new Window<Float>(0f,0f,1f,1f);
		this.numEpisodes = numEpisodes;
		this.minY = minY;
		this.maxY = maxY;
	}

	@Override
	public void draw(Graphics g, Window<Float> panelCoordinates) {
		if(!doDraw) return;
		
		
		Scaler s = new Scaler(localCoordinates, panelCoordinates, false);
		
		
		var o = s.scale(origin);
		var x = s.scale(new float[] {origin[0]+lengths[0],origin[0]});
		var y = s.scale(new float[] {origin[0],origin[0]+lengths[1]});
		
		
		g.setColor(Color.black);
		
		
		
		
		int coords[][] = s.scale(runtimes);
		

		//draw X and Y axis
		g.drawLine(o[0], o[1], x[0], x[1]);
		g.drawLine(o[0], o[1], y[0], y[1]);
		
		//Draw Line
		if(doLines) g.drawPolyline(coords[0], coords[1], runtimes.size());
		
		//Draw Markers
		for(int i=0; i < runtimes.size() ; i ++){
			g.drawOval(coords[0][i]-markerSize, coords[1][i]-markerSize,2*markerSize ,	2*markerSize);
			
		}
		

	}

	@Override
	public void endEpisode() {
		updateData();
		nextValue = 0;
		int nextID = runtimes.size();
		float x = origin[0]+lengths[0]*(float)nextID/numEpisodes;
		float y = origin[1];
		runtimes.add(new float[] {x,y});
	}

	long nextValue;
	@Override 
	public void appendData(){
		nextValue = Experiment.get().getGlobal("cycle");
	}

	@Override
	public void updateData() {
		if(runtimes.size()==0) return;
		long cycle = nextValue > maxY ? maxY : ( nextValue < minY ?  minY : nextValue);
		float y = origin[1] + lengths[1]*(float)cycle/(maxY-minY);
		runtimes.get(runtimes.size()-1)[1] = y;		
	}
	
	
	
}
