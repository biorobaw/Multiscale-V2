package com.github.biorobaw.scs_models.multiscale_f2019.robot.modules.distance_sensing;

import com.github.biorobaw.scs.experiment.Experiment;
import com.github.biorobaw.scs.robot.modules.distance_sensing.SCSWallDistanceSensors;
import com.github.biorobaw.scs.utils.files.BinaryFile;
import com.github.biorobaw.scs.utils.files.XML;

public class MySCSDistanceSensor extends SCSWallDistanceSensors {

    float min_x, min_y, precision;
    int num_x, num_y;
    int len_data;
    float[] data;

    public MySCSDistanceSensor(XML xml) {
        super(xml);

        // need to get file, for now hordcode it:
        String maze_file = Experiment.get().getGlobal("maze");
        String distance_file = maze_file.replace(".xml", "_subgoal_distances.bin");
        var dimensions = BinaryFile.readFloats(distance_file, 5, 0, true);
        min_x = dimensions[0];
        num_x = (int)dimensions[1];
        min_y = dimensions[2];
        num_y = (int)dimensions[3];
        precision = dimensions[4];

        data = BinaryFile.readFloats(distance_file, num_x*num_y, 5, true);

    }

    public float getDistanceToClosestSubgoal(){
        var pos = proxy.getPosition();

        var i = (int) Math.floor( (pos.getY() - min_y) / precision );
        var j = (int) Math.floor( (pos.getX() - min_x) / precision );

        if ( i < 0 || j < 0 || i >= num_y || j >= num_x)
            return Float.MAX_VALUE;

        return data[i*num_x + j];
    }
}
