//package com.github.biorobaw.multiscale_f2019.mazes;
//
//import java.io.BufferedReader;
//import java.io.FileWriter;
//import java.io.IOException;
//import java.io.InputStream;
//import java.io.InputStreamReader;
//import java.io.PrintWriter;
//import java.util.ArrayList;
//import java.util.LinkedList;
//import java.util.List;
//
//import com.github.biorobaw.scs.maze.Maze;
//import com.github.biorobaw.scs.simulation.object.maze_elements.walls.Wall;
//import com.github.biorobaw.scs.utils.XML;
//
//public class MazeMetrics {
//	public static void main(String[] args) {
//		
//		System.err.println("ERROR - needs to be fixed before it can be used");
//		System.exit(-1);
//		//OUT FILE
//		String outFolder = "./src/edu/usf/ratsim/model/pablo/multiscale_memory/mazes/";
//		String outFile   = outFolder + "mazeMetrics.csv";
//		
//		//GET THE LIST OF MAZE FILES
//		List<String> filenames = new ArrayList<>();
//		try (InputStream in = MazeMetrics.class.getResourceAsStream(".");
//				BufferedReader br = new BufferedReader(new InputStreamReader(in))) {
//			
//			String resource;
//			while ((resource = br.readLine()) != null) 
//				if(resource.matches("M\\d+\\.xml")) {
//					filenames.add(resource);
//				}
//			
//		}catch (Exception e) {
//		}
//		
//
//
//		try {
//			
//			FileWriter writer = new FileWriter(outFile);
//			PrintWriter printer = new PrintWriter(writer);
//						
//			//print column headers:
//			printer.println("maze,pos,distance");
//			
//			
//			//FOR EACH MAZE FILE, FOR EACH START POSITION FIND THE SHORTEST PATH TO THE FEEDER
//			
//			for(String mazeFile : filenames) {
//				
//				XML m_xml = new XML(mazeFile);
//				
//				Maze maze = new Maze(m_xml);
//				
//				LinkedList<Wall> mazeWalls = new LinkedList<>();
//				for(var m : maze.walls) mazeWalls.add((Wall)m);
//				
//				
//				//crate visibility graph for the maze
//				var graph = new VisibilityGraph(mazeWalls);
//				
//				
//				//add goal location:
//				var feederXml = maze.getChildren("feeder").get(0);
//				graph.addDestiny( new Float[] {feederXml.getChildFloat("x"), feederXml.getChildFloat("y")});
//				
//				
//				//for each origin find shortest distance, and log results
//				Integer posId = 0;
//				for(var p : maze.getChild("startPositions").getChildren("pos")) {
//					List<Float> pos = p.getFloatList();
//					graph.addOrigin(new Float[] {pos.get(0),pos.get(1),pos.get(2)});
//					Float d = (float)graph.getShortestPath().getWeight();	
//					
//					printer.println(mazeFile +"," +posId.toString() +","+d.toString());					
//					
//					posId++;
//				}
//			}
//			
//			printer.close();
//			
//		} catch (IOException e) {
//			// TODO Auto-generated catch block
//			e.printStackTrace();
//		}
//		
//		
//		
//	}
//}
