package com.github.biorobaw.scs_models.multiscale_f2019.gui.fx.drawers;


import java.util.LinkedList;

import com.github.biorobaw.scs.gui.displays.java_fx.PanelFX;
import com.github.biorobaw.scs.gui.displays.java_fx.drawer.DrawerFX;
import com.github.biorobaw.scs.utils.math.Doubles;

import javafx.scene.Group;
import javafx.scene.control.Label;
import javafx.scene.layout.AnchorPane;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.Pane;
import javafx.scene.layout.StackPane;
import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;
import javafx.scene.shape.Line;
import javafx.scene.shape.LineTo;
import javafx.scene.shape.MoveTo;
import javafx.scene.shape.Path;
import javafx.scene.shape.Rectangle;
import javafx.scene.transform.Rotate;
import javafx.scene.transform.Scale;
import javafx.scene.transform.Translate;

public class PolarDataDrawer extends DrawerFX {
	
	String title;				// plot title

	// DATA
	LinkedList<PolarData> data = new LinkedList<>();
	LinkedList<Arrow> data_arrows = new LinkedList<>();
	
	boolean normalize;			// defines whether to normalize data or not
	double max_value = 1;		// max value of the data

	
	
	// DATA SYNCHRONIZATION
	boolean new_data = false;	// flag indicating whether new data needs to be processed
	
	// PLOTTING PARAMETERS
	float relativeRadius;		// max plot radius
	
	
	
	/**
	 * Draws a polar graph
	 * @param title	Plot title
	 * @param radius 	Max radius
	 * @param normalize	  Determines whether the data should be normalized
	 */
	public PolarDataDrawer(String title,float radius, boolean normalize){

		this.relativeRadius = radius;
		this.title 			= title;
		this.normalize 		= normalize;		

	}
	
	/**
	 * Draws a polar graph
	 * @param title	Plot title
	 * @param radius 	Max radius

	 */
	public PolarDataDrawer(String title, float radius) {
		this(title, radius, true);
	}
	
	/**
	 * Draws a polar graph
	 * @param title	Plot title
	 */
	public PolarDataDrawer(String title) {
		this(title,0.95f, true);
	}


	
	public void addData(String id, double[] angles, GetDoubleArray getData) {
		data.add(new PolarData(id, angles, getData));
	}

	public void addArrow(GetDouble getAngle) {
		data_arrows.add(new Arrow(getAngle));
	}
	
	@Override
	public void updateData() {
		for(var d : data) d.update();
		for(var d : data_arrows) d.update();
		new_data = true; // set to null so that graphics know they have to update
		
	}
	
	void processData() {
		if(!new_data) return;
		new_data = false;
		
		for(var d : data) d.process();
		for(var d: data_arrows) d.process();
		
	}
	
	
	
	public interface GetDoubleArray{
		float[] get();
	}
	
	public interface GetDouble {
		double get();
	}
	

	@Override
	protected DrawerScene createGraphics(PanelFX panel) {
		return new DrawerGraphics(panel);
	}
	
	class DrawerGraphics extends DrawerScene {
		
		// DATA PANE
		Scale dataScale = new Scale(relativeRadius, relativeRadius);
		double pixel_size = 2.0/300; // approximation of a pixel in local coordinates
		Circle max_circle = new Circle(0, 0, 1);
		Pane data_pane = new Pane(max_circle);
		
		// LEGNED PANE
		GridPane   legend_pane = new GridPane();
		AnchorPane lengend_achor_pane = new AnchorPane(legend_pane);
		
		// ROOT PANE
		StackPane stack_pane = new StackPane(data_pane, lengend_achor_pane);
		
		
		// PLOTS
		LinkedList<PolarGraph> graphs = new LinkedList<>();
		LinkedList<ArrowGraph> arrows = new LinkedList<>();
		

		
		public DrawerGraphics(PanelFX panel) {
			super(panel);
			
			// set root pane, and define anchors
			root = stack_pane;
			AnchorPane.setTopAnchor(legend_pane, -3.);
			AnchorPane.setLeftAnchor(legend_pane, 5.);
			
			// add transformations
			setUnits(data_pane, Units.LOCAL);			
			data_pane.getTransforms().addAll( dataScale );
		

			// set line strokes and colors for max circle:
			max_circle.setStrokeWidth(pixel_size*3);
			max_circle.setFill(Color.TRANSPARENT);
			max_circle.setStroke(Color.GRAY);
			
			// add space between tags in legend:
			legend_pane.setHgap(5);
			
			
			// CREATE AND ADD ARROWS:
			for(var d : data_arrows ) {
				var a = new ArrowGraph(d);
				arrows.add(a);
				data_pane.getChildren().add(a.arrow);
			}

			// CREATE AND ADD POLAR PLOTS:
			// add after arrows so they wont be overshadowed by them
			int i = 0;
			for(var d : data) {
				// CREATE AND ADD PLOT
				var p = new PolarGraph(d);
				graphs.add(p);
				data_pane.getChildren().add(p.plot);
				
				// ADD LEGEND AND SET COLOR
				legend_pane.add(p.tag_mark, 0, i);
				legend_pane.add(p.tag, 		1, i);
				p.setColor(Color.hsb(i*360./(data.size()+1), 0.8, 0.8, 0.8));
				i++;
			}
			
			
//			Line l1 = new Line (0,-1,0,1);
//			Line l2 = new Line (-1,0,1,0);
//			l1.setStrokeWidth(stroke_width);
//			l2.setStrokeWidth(stroke_width);
//			l1.setStroke(Color.RED);
//			l2.setStroke(Color.RED);
//			data_pane.getChildren().addAll(l1,l2);
			
			

			
		}
		
		@Override
		public void update() {
			processData();
			
			for(var g : graphs) g.update();
			for(var a : arrows) a.update();
			 
		}
		
		class PolarGraph {
			Label tag;
			Rectangle tag_mark = new Rectangle(5, 5);
			
			PolarData data;
			Path plot = new Path();
			
			MoveTo start = new MoveTo(0, 0);
			LineTo lines[];
			
			
			
			PolarGraph(PolarData data){
				this.data = data;
				
				lines = new LineTo[data.length];
				for(int i=0; i<data.length; i++) lines[i] = new LineTo(0,0);
				plot.getElements().add(start);
				plot.getElements().addAll(lines);
				plot.setStrokeWidth(pixel_size*3); 
				
				tag = new Label(data.id);
				
			}
			
			void update() {
				start.setX(data.data_x[data.length-1]);
				start.setY(data.data_y[data.length-1]);
				
				for(int i=0; i<data.length; i++) {
					lines[i].setX(data.data_x[i]);
					lines[i].setY(data.data_y[i]);
				}
			}
			
			void setColor(Color color) {
				plot.setStroke(color);
				tag_mark.setFill(color);
			}
		}
		
		class ArrowGraph {
			Arrow data;
			Line arrow_line  = new Line(0,0,0,0);
			Line arrow_head1 = new Line(0,0,-8*pixel_size, 5*pixel_size);
			Line arrow_head2 = new Line(0,0,-8*pixel_size, -5*pixel_size);
			Group arrow 	 = new Group(arrow_line, arrow_head1, arrow_head2);
			
			Rotate arrowRotate = new Rotate(0);
			Translate arrowTranslate = new Translate(0,0);
			
			ArrowGraph(Arrow data){
				this.data = data;
				arrow_head1.getTransforms().addAll(arrowTranslate, arrowRotate);
				arrow_head2.getTransforms().addAll(arrowTranslate, arrowRotate);
				var segments = new Line[] {arrow_line, arrow_head1, arrow_head2}; 
				
				// SET STROKE AND COLOR
				for(var l : segments) {
					l.setStrokeWidth(pixel_size*4);
					l.setStroke(Color.RED);
				}
				
			}
			
			void update() {
				// stretch line
				arrow_line.setEndX(data.x_end);
				arrow_line.setEndY(data.y_end);
				
				// place
				arrowTranslate.setX(data.x_end);
				arrowTranslate.setY(data.y_end);
				arrowRotate.setAngle(data.angle_deg);
			}
			
			void setVisible(boolean value) {
				arrow.setVisible(value);
			}
		}
		
	}
	

	class PolarData {
		String id;
		int length;
		double[] data;			// data to be plotted 
		double[] data_x;		// data x coordinates			
		double[] data_y;		// data y coordinates
		
		// PRECOMPUTED UNIT VECTORS:
		double[] angles_deg;		// precomputed angles in degrees
		double[] cosines;			// precomputed cosines of each direction
		double[] sines;				// precomputed	
		
		GetDoubleArray getData;
		
		PolarData(String id, double[] angles_rad, GetDoubleArray getData) {
			this.id = id;
			this.getData = getData;
			this.length = angles_rad.length;
			
			data 		= new double[length];	// data to be plotted 
			data_x 		= new double[length];	// data x coordinates			
			data_y 		= new double[length];	// data y coordinates
			angles_deg 	= Doubles.mul(angles_rad, 180./Math.PI);
			cosines 	= Doubles.cos(angles_rad);
			sines   	= Doubles.sin(angles_rad);
			
		}
		
		void update() {
			data = Doubles.copy(getData.get());
		}
		
		void process() {
			// calculate maximum and normalize
			max_value = Doubles.max(data);
			if(normalize && max_value!=0) Doubles.div(data, max_value, data);
			
			// calculates x and y coordinates:
			Doubles.mul(data, cosines, 	data_x);
			Doubles.mul(data, sines, 	data_y);
		}
		
		double x(int i) {
			return  data_x[i < 0 ? length + i : i]; 
		}
		
		double y(int i) {
			return  data_y[i < 0 ? length + i : i]; 
		}
		
	}
	
	class Arrow {
		double angle_rad = 0;
		double angle_deg = 0;
		double length = 1;
		
		double x_end, y_end; 
		GetDouble getAngle;
		
		Arrow(GetDouble getAngle){
			this.getAngle = getAngle;
		}
		
		void process() {
			angle_deg = Math.toDegrees(angle_rad);
			x_end = Math.cos(angle_rad)*length;
			y_end = Math.sin(angle_rad)*length;
		}
		
		void update() {
//			this.length = length;
			angle_rad = getAngle.get();
			
//			direc = nextDirec;
//			if(getArrow!=null) direc = getArrow.get();
			
			//Data for highlighting a directions:
//			int direc = -1;	
//			int nextDirec = -1;
		}
		

		
	}

}
