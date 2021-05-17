package com.github.biorobaw.scs_models.multiscale_f2019.gui.fx.drawers;

import java.util.Collection;
import java.util.HashMap;
import java.util.LinkedList;

import com.github.biorobaw.scs.experiment.Experiment;
import com.github.biorobaw.scs.gui.displays.java_fx.PanelFX;
import com.github.biorobaw.scs.gui.displays.java_fx.drawer.DrawerFX;
import com.github.biorobaw.scs.simulation.object.maze_elements.walls.Wall;
import com.github.biorobaw.scs_models.multiscale_f2019.model.MultiscaleModel;
import com.github.biorobaw.scs_models.multiscale_f2019.model.modules.c_rl.ObstacleBiases.WallData;

import javafx.scene.paint.Color;
import javafx.scene.shape.Line;


public class WallBiasHighlighterDrawer extends DrawerFX {
	
	MultiscaleModel model;
	LinkedList<DrawerGraphics> all_drawing_graphics = new LinkedList<>();
	
	
	// Data used by graphics, it can only be accessed by update function
	private LinkedList<Wall> walls = new LinkedList<>();
	private LinkedList<WallData> walls_visited	  		= new LinkedList<>();
	private LinkedList<WallData> walls_to_add  			= new LinkedList<>();
	private Collection<WallData> walls_considered 		= new LinkedList<>();
	private Collection<WallData> walls_considered_old 	= new LinkedList<>();
	private WallData wall_selected = null;
	
	boolean reset_walls_visited = false;
	
	// buffer data used to buffer information before updating
	private LinkedList<WallData> walls_newly_visited = new LinkedList<>();
	boolean new_episode_flag = false;
	
	
	Color color_wall_selected 	= Color.hsb(Color.RED.getHue(),    1, 1, 0.5);
	Color color_wall_considered = Color.hsb(Color.ORANGE.getHue(), 1, 1, 0.5);
	Color color_wall_missing 	= Color.hsb(Color.GREEN.getHue(), 0.8, 0.8, 0.5); 
	
	float wall_thickness = 0.03f;// wall thickness in meters
	
	public WallBiasHighlighterDrawer(float wallThickness, MultiscaleModel model) {
		this.wall_thickness = wallThickness;
		this.model = model;
		
		var m = Experiment.get().maze;
		for (var w : m.walls) walls.add((Wall)w);
		
	}
	

	
	@Override
	public void newEpisode() {
		new_episode_flag = true;
		walls_newly_visited.clear();
	}
	

	@Override
	public void appendData() {
		walls_newly_visited.addAll(model.obstacle_biases.walls_visited_this_cycle);
	}
	


	@Override
	public synchronized void updateData() {		
		// walls are not updated during an episode, thus do nothing
		if(new_episode_flag) {
			walls_to_add.clear();
			reset_walls_visited = true;
			new_episode_flag = false;
		}
		
		walls_considered_old = walls_considered;
		walls_considered = model.obstacle_biases.walls_considered_in_last_selection; // fixed set
		wall_selected = model.obstacle_biases.wall_chosen;
		
		walls_to_add.addAll(walls_newly_visited);
		
		
		walls_newly_visited.clear();
	}
	
	
	class DrawerGraphics extends DrawerScene {
		
		HashMap<Wall, WallGraphics> graphics = new HashMap<>();
		
		public DrawerGraphics(PanelFX panel) {
			super(panel);
			all_drawing_graphics.add(this);
			
			root.getChildren().clear();
			
			for (var w : walls) graphics.put(w, new WallGraphics(w));
						
		}
		


		
		@Override
		public void update() {
			if(reset_walls_visited) {
				for(var w : walls_visited) {
					var g = graphics.get(w.wall);
					g.setVisible(true);
					g.setStroke(color_wall_missing);
				}
				reset_walls_visited = false;
			}
			
			for(var w : walls_considered_old) {
				graphics.get(w.wall).setStroke(color_wall_missing);
			}
			
			for(var w : walls_considered) {
				graphics.get(w.wall).setStroke(color_wall_considered);
				
			}
			
			if(wall_selected != null) {
				graphics.get(wall_selected.wall).setStroke(color_wall_selected);
			}
			
			for(var w : walls_to_add) {
				graphics.get(w.wall).setVisible(false);
			}
			
			walls_visited.addAll(walls_to_add);
			walls_to_add.clear();

		}
		
		

		
		class WallGraphics extends Line {
			WallGraphics(Wall w){
				super(w.x1, w.y1, w.x2, w.y2);
				setStroke(color_wall_missing);
				setStrokeWidth(wall_thickness);
				root.getChildren().add(this);
			}
			
			void update() {
				
				
			}
		}
		
		
		
	}
	


	@Override
	protected DrawerScene createGraphics(PanelFX panel) {
		return new DrawerGraphics(panel);
	}

}
