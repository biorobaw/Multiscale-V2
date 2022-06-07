package com.github.biorobaw.scs_models.multiscale_f2019.gui.fx.drawers;


import com.github.biorobaw.scs.gui.displays.java_fx.PanelFX;
import com.github.biorobaw.scs.gui.displays.java_fx.drawer.DrawerFX;
import com.github.biorobaw.scs.simulation.object.RobotProxy;
import javafx.scene.paint.Color;
import javafx.scene.paint.Paint;
import javafx.scene.shape.Circle;
import javafx.scene.transform.Translate;

import java.util.function.DoubleSupplier;

public class RobotDistanceRingDrawer extends DrawerFX {

	private double radius = 0; // in meters

	RobotProxy robot;
	DoubleSupplier get_distance;
	float[] position = new float[] {-1000000f,-1000000f};

	public RobotDistanceRingDrawer(RobotProxy robot, DoubleSupplier get_distance_function) {
		this.robot = robot;
		get_distance = get_distance_function;
	}


	@Override
	public void updateData() {
		var pos = robot.getPosition();
		position = new float[] {(float)pos.getX(), (float)pos.getY()};
		radius = get_distance.getAsDouble();
	}

	
	
	@Override
	protected DrawerScene createGraphics(PanelFX panel) {
		return new DrawerGraphhics(panel);
	}

	
	class DrawerGraphhics extends DrawerScene {
		
		final Color default_color = Color.BLACK;

		RingGraphics ring_graphic = new RingGraphics();
		
		
		public DrawerGraphhics(PanelFX panel) {
			super(panel);
			root.getChildren().add(ring_graphic.circle);
		}
		
		
		@Override
		public void update() {
			ring_graphic.pos.setX(position[0]);
			ring_graphic.pos.setY(position[1]);
			ring_graphic.circle.setRadius(radius);
		}
		
		class RingGraphics {
			Circle circle = new Circle(0, 0, radius);
			
			Translate pos = new Translate(0,0);

			// initialize data structure
			{
				circle.setFill(Color.TRANSPARENT);
				setStroke(default_color);
				setStrokeWidth(0.005);
				circle.getTransforms().addAll(pos);
			}
			
			void setStroke(Paint paint) {
				circle.setStroke(paint);
			}
			
			void setStrokeWidth(double width) {
				circle.setStrokeWidth(width);
			}
			
		}
		
	}



}
