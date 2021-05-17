package com.github.biorobaw.scs_models.multiscale_f2019.gui.fx.drawers;



import com.github.biorobaw.scs.gui.displays.java_fx.PanelFX;
import com.github.biorobaw.scs.gui.displays.java_fx.drawer.DrawerFX;
import com.github.biorobaw.scs.utils.math.Floats;
import com.github.biorobaw.scs.utils.math.Integers;

import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;



public class PCDrawer extends DrawerFX {

	
	final static double GRAY_VALUE = 180.0/256;
	final static Color GRAY = new Color(GRAY_VALUE, GRAY_VALUE, GRAY_VALUE, 1);
	
	float[] pc_x;		 // x coordinate of each cell
	float[] pc_y;		 // y coordinate of each cell
	float[] pc_r;		 // radius of each cell
	int num_cells;		 // total number of cells
	
	float[] activations; // activity of active cells
	int[] ids;			 // ids of active cells
	
	GetActiveValues getActiveValues; // function to get activity of active cells
	GetActiveIds getActiveIds;		 // function to get ids of active cells
	
	float radius = -1; // used when all pcs have the same radius
	boolean constant = false;
	
//	HashMap<Integer, Float> values = new HashMap<>();
	

	public PCDrawer(float[] pc_x, float[] pc_y, float[] pc_r, GetActiveValues getActiveValues, GetActiveIds getActiveIds) {
		this.getActiveValues = getActiveValues;
		this.getActiveIds = getActiveIds;
		this.pc_x = pc_x;
		this.pc_y = pc_y;
		this.pc_r  = pc_r;
		
		num_cells = pc_x.length;
		radius = Floats.max(pc_r);
		constant = radius == Floats.min(pc_r);
	}


	@Override
	public void newEpisode() {
		super.newEpisode();
		ids = null;
	}

	@Override
	public void updateData() {
		ids = getActiveIds.get();
		if(ids!=null) {
			activations = Floats.copy(getActiveValues.get());
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
	
	public  interface GetActiveValues {
		float[] get();
	}
	
	public interface GetActiveIds {
		int[] get();
	}
	


	@Override
	protected DrawerScene createGraphics(PanelFX panel) {
		return new DrawerGraphics(panel);
	}
	
	class DrawerGraphics extends DrawerScene {

		Circle base_circles[] = new Circle[num_cells];
		Circle active_circles[] = new Circle[num_cells];
		
		int[] old_ids = new int[] {};
		
		public DrawerGraphics(PanelFX panel) {
			super(panel);
			for(int i=0; i<num_cells; i++) {
				base_circles[i] = new Circle(pc_x[i], pc_y[i], pc_r[i], GRAY);
				root.getChildren().add(base_circles[i]);
			}
			
			for(int i=0; i<num_cells; i++) {
				active_circles[i] = new Circle(pc_x[i], pc_y[i], pc_r[i], Color.TRANSPARENT);
				root.getChildren().add(active_circles[i]);
			}
		}
		


		@Override
		public void update() {
			// clear old ids:
			for(var id : old_ids)
				active_circles[id].setFill(Color.TRANSPARENT);
			if(ids == null) return;
			old_ids = Integers.copy(ids);
			
			for(int i = 0; i < old_ids.length; i++) {
				
				active_circles[old_ids[i]].setFill(getColor(activations[i]));
			}
			
		}
		
	}
	
}
