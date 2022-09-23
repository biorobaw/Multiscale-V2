package com.github.biorobaw.scs_models.multiscale_f2019.gui.fx.drawers;


import com.github.biorobaw.scs.gui.displays.java_fx.PanelFX;
import com.github.biorobaw.scs.gui.displays.java_fx.drawer.DrawerFX;
import com.github.biorobaw.scs.simulation.object.RobotProxy;
import javafx.scene.paint.Color;
import javafx.scene.paint.Paint;
import javafx.scene.shape.Circle;
import javafx.scene.shape.Polygon;
import javafx.scene.transform.Translate;
import org.locationtech.jts.geom.LinearRing;

import java.util.LinkedList;
import java.util.function.DoubleSupplier;
import java.util.function.Supplier;

public class PolygonDrawer extends DrawerFX {

	private org.locationtech.jts.geom.Polygon polygon = null;

	RobotProxy robot;
	Supplier<org.locationtech.jts.geom.Polygon> get_polygon;
	float[] position = new float[] {-1000000f,-1000000f};

	public PolygonDrawer(RobotProxy robot, Supplier get_distance_function) {
		this.robot = robot;
		get_polygon = get_distance_function;
	}


	@Override
	public void updateData() {
		var pos = robot.getPosition();
		position = new float[] {(float)pos.getX(), (float)pos.getY()};
		polygon = get_polygon.get();
	}

	
	
	@Override
	protected DrawerScene createGraphics(PanelFX panel) {
		return new DrawerGraphhics(panel);
	}

	
	class DrawerGraphhics extends DrawerScene {
		
		final Color default_color = Color.BLACK;
		Polygon fx_polygon;


//		RingGraphics ring_graphic = new RingGraphics();

		
		public DrawerGraphhics(PanelFX panel) {
			super(panel);
			fx_polygon = new Polygon();
			root.getChildren().add(fx_polygon);
			fx_polygon.setOpacity(0.2);
			fx_polygon.setFill(Color.rgb(0,0,200));
		}
		
		
		@Override
		public void update() {
			if(polygon == null) {
				fx_polygon.getPoints().clear();
			}
			else{
				LinkedList<Double> points = new LinkedList<>();
				for (var p : polygon.getCoordinates()){
					points.add(p.x);
					points.add(p.y);
				}
				fx_polygon.getPoints().setAll(points);
			}

		}
		
//		class RingGraphics {
//			Circle circle = new Circle(0, 0, radius);
//
//			Translate pos = new Translate(0,0);
//
//			// initialize data structure
//			{
//				circle.setFill(Color.TRANSPARENT);
//				setStroke(default_color);
//				setStrokeWidth(0.005);
//				circle.getTransforms().addAll(pos);
//			}
//
//			void setStroke(Paint paint) {
//				circle.setStroke(paint);
//			}
//
//			void setStrokeWidth(double width) {
//				circle.setStrokeWidth(width);
//			}
//
//		}
		
	}



}
