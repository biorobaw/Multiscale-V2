package com.github.biorobaw.scs_models.multiscale_f2019.robot.modules.distance_sensing;

import com.github.biorobaw.scs.experiment.Experiment;
import com.github.biorobaw.scs.robot.modules.distance_sensing.SCSWallDistanceSensors;
import com.github.biorobaw.scs.utils.files.BinaryFile;
import com.github.biorobaw.scs.utils.files.XML;
import org.locationtech.jts.geom.*;

import java.io.DataInputStream;
import java.util.HashMap;

public class MySCSDistanceSensor extends SCSWallDistanceSensors {

    DistanceMap subgoalDistanceMap;
    DistanceMap closestWallDistanceMap;
    VisibilityMap visibilityMap;

    public MySCSDistanceSensor(XML xml) {
        super(xml);

        // need to get file, for now hordcode it:
        String maze_file = Experiment.get().getGlobal("maze");
        String subgoal_distance_file = maze_file.replace(".xml", "_subgoal_distances.bin");
        String closest_wall_distance_file = maze_file.replace(".xml", "_closest_wall_distances.bin");
        String visibility_file = maze_file.replace(".xml", "_visibility_map.bin");



        subgoalDistanceMap = new DistanceMap(subgoal_distance_file);
        closestWallDistanceMap = new DistanceMap(closest_wall_distance_file);
        visibilityMap = new VisibilityMap(visibility_file);
    }

    public float getDistanceToClosestSubgoal(){
        var pos = proxy.getPosition();
        return subgoalDistanceMap.getDistance((float)pos.getX(),(float)pos.getY());
    }

    public float getDistanceToClosestWall(){
        var pos = proxy.getPosition();
        return closestWallDistanceMap.getDistance((float)pos.getX(),(float)pos.getY());
    }

    public Polygon getVisibilityPolygon(){
        var pos = proxy.getPosition();
        return visibilityMap.getVisibility((float)pos.getX(),(float)pos.getY());
    }


    class Grid {
        float min_x, min_y, precision;
        int num_x, num_y;
        int num_elements;

        Grid(String file){
            var dimensions = BinaryFile.readFloats(file, 5, 0, true);
            min_x = dimensions[0];
            num_x = (int)dimensions[1];
            min_y = dimensions[2];
            num_y = (int)dimensions[3];
            precision = dimensions[4];
            num_elements = num_x * num_y;
        }

        int index(float x, float y){
            int i = (int) Math.floor( (y - min_y) / precision );
            int j = (int) Math.floor( (x - min_x) / precision);

            boolean invalid = i < 0 || j < 0 || i >= num_y || j >= num_x;
            return  invalid ? -1 : i*num_x + j;
        }
    }

    class DistanceMap {

        Grid grid;
        float[] distances;

        DistanceMap(String file){
            grid = new Grid(file);
            distances = BinaryFile.readFloats(file, grid.num_elements, 5, true);

        }

        float getDistance(float x, float y){
            var index = grid.index(x, y);
            return index < 0 ? Float.MAX_VALUE : distances[index];
        }
    }

    class VisibilityMap {
        Grid grid;
        Polygon[] polygons;
        HashMap<Integer,float[]> missing_polygons = new HashMap();

        VisibilityMap(String file) {
            grid = new Grid(file);
            polygons = new Polygon[grid.num_elements];

            // Get binary file and remove grid data already loaded
            var binary_file = BinaryFile.read(file);
            BinaryFile.readFloats(binary_file,5,0,true); // skip first 5 floats

            // Read and generate each polygon
            GeometryFactory geometryFactory = new GeometryFactory();
            for(int i=0; i<grid.num_elements; i++){
                int num_points = (int)(BinaryFile.readFloats(binary_file,1,0,true)[0]);

                if(num_points>0) {
                    polygons[i] = readPolygon(binary_file,num_points,geometryFactory);
                }
                else {
                    missing_polygons.put(i, BinaryFile.readFloats(binary_file,3,0,true));
                }

            }

        }

        Polygon readPolygon(DataInputStream binary_file, int num_points, GeometryFactory geometryFactory){
            // read data
            float[] data = BinaryFile.readFloats(binary_file,num_points*2,0,true);

            // create array of coordinates
            var shell = new Coordinate[num_points+1];
            for(int j=0 ; j<num_points; j++)
                shell[j] = new Coordinate(data[2*j], data[2*j+1]);
            shell[num_points] = shell[0];

            // return polygon
            return geometryFactory.createPolygon(shell);
        }


        Polygon getVisibility(float x, float y){

            var index = grid.index(x, y);
            if (index < 0) return null;

            var polygon = polygons[index];

            if(polygon == null){
                var vector = missing_polygons.get(index);
                var is_positive_side = x*vector[0]+y*vector[1] > vector[2];
                var dx = is_positive_side ? vector[0] : -vector[0];
                var dy = is_positive_side ? vector[1] : -vector[1];

                for(int i=0; i<3 && polygon == null; i++){
                    x+=dx;
                    y+=dy;
                    index = grid.index(x, y);
                    if (index < 0) return null;
                    polygon = polygons[index];
                }
            }
            if(polygon == null){
                System.err.println("ERROR: visibility polygon is null");
            }
            return polygon;
        }
    }
}
