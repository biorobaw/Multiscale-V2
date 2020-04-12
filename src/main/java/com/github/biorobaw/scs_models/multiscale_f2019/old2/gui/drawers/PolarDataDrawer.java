package com.github.biorobaw.scs_models.multiscale_f2019.old2.gui.drawers;

import java.awt.Color;
import java.awt.FontMetrics;
import java.awt.Graphics;
import java.awt.Point;


import com.github.biorobaw.scs.gui.Drawer;
import com.github.biorobaw.scs.gui.utils.GuiUtils;
import com.github.biorobaw.scs.gui.utils.Scaler;
import com.github.biorobaw.scs.gui.utils.Window;
import com.github.biorobaw.scs.utils.math.Floats;
import com.vividsolutions.jts.geom.Coordinate;

public class PolarDataDrawer extends Drawer {
	

	Window<Float> localCoordinates = new Window<>(-1f,-1f,2f,2f);
	GetData getData;
	GetArrowDirection getArrow;
	
	float relativeRadius;
	float x;
	float y;
	
//	float[] data;
//	float[] dataCopy;
	float[] data = null;
	int dataSize;
	float max;
	
	Coordinate[] relativeVectors;
	
	int[][] function;
	
	String title;
	
	boolean normalize;

	private float[] relativeCenter;
	private float[] relativeUpperLeft;
	
	public boolean debug = false;
	
	
	
	//Data for highlighting a directions:
	int direc = -1;	
	int nextDirec = -1;
	
	Color arrowColor = Color.red;
	int arrowHeadSize = 8;
	int arrowLineWidth =2;
	
	
	
	
	
	

	/**
	 * Draws a polar graph
	 * @param x		 Center of circle x coord	
	 * @param y		 Center of circle y coord
	 * @param radius 
	 * @param data
	 */
	
	public PolarDataDrawer(String title,float x,float y,float radius,int dataSize,GetData getData) {
		this(title,x,y,radius,dataSize,getData,true);
	}
	
	public PolarDataDrawer(String title,int dataSize,GetData getData) {
		this(title,0f,0f,0.95f,dataSize,getData,true);
	}
	
	public PolarDataDrawer(String title,float x,float y,float radius,int dataSize,GetData getData,boolean normalize){

		relativeCenter = new float[] {x,y};
		this.relativeRadius = radius;
		this.dataSize = dataSize;
		
		this.getData = getData;
		this.title = title;
		this.normalize = normalize;
		
		relativeUpperLeft = new float[] {x-radius,y+radius};
		
		
		float deltaAngle = 2*(float)Math.PI/dataSize;
		relativeVectors = new Coordinate[dataSize];
		function = new int[2][dataSize];
		
		float angle = 0;
		for (int i=0;i<dataSize;i++){
			
			relativeVectors[i] = new Coordinate(radius*(float)Math.cos(angle),radius*(float)Math.sin(angle));			
			angle+=deltaAngle;
		}
		

	}

	@Override
	public void draw(Graphics g, Window<Float> panelCoordinates) {
		if(!doDraw) return;
		
		Scaler s = new Scaler(localCoordinates,panelCoordinates,true);
		
		var upperLeft = s.scale(relativeUpperLeft);
		float radius = s.scaleDistanceX(relativeRadius);
		
		g.setColor(Color.BLACK);
		g.drawOval(upperLeft[0], upperLeft[1], (int)(2*radius), (int)(2*radius));
		
		if(data==null) return;
		
		var center = s.scale(relativeCenter);
		Point vectors[] = s.scaleDistance(relativeVectors,true);
		
		for (int i=0;i<dataSize;i++){
			function[0][i] = (int)(center[0] + data[i]*vectors[i].x);
			function[1][i] = (int)(center[1] + data[i]*vectors[i].y);			
		}
		
		FontMetrics metrics =  g.getFontMetrics();
		g.drawString(title+ "-"+max, (int)(center[0]-metrics.stringWidth(title)/2), (int)(Math.min(center[1]+radius+metrics.getHeight(),panelCoordinates.height)));
		g.setColor(Color.orange);
		
		g.drawPolygon(function[0], function[1], dataSize);
		
		
		
		if(direc!=-1){
			
			GuiUtils.drawArrow(center[0], center[1], function[0][direc], function[1][direc], arrowColor, arrowHeadSize, arrowLineWidth, g);
		}
		
		
		
	}

	@Override
	public void updateData() {
		data = Floats.copy(getData.get());
		max = Floats.max(data);
		if(normalize && max!=0) Floats.div(data, max, data);
		
		if(debug) System.out.println("Updating data...");
		direc = nextDirec;
		if(getArrow!=null) direc = getArrow.get();

	}
	
	
	
	public void setArrowParams(Color c,int lineWidth,int arrowHeadSize){
		this.arrowColor = c;
		this.arrowLineWidth = lineWidth;
		this.arrowHeadSize = arrowHeadSize;
	}
	
	
	public interface GetData{
		float[] get();
	}
	
	public interface GetArrowDirection {
		int get();
	}
	
	public void setGetArrowFunction(GetArrowDirection function) {
		getArrow = function;
	}

}
