import meshio
import os
import argparse
import time
import numpy as np
from matlab_readers import load_mat


def main():

    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument('--dataPath',   type=str, required=True, help='path to data')
    parser.add_argument('--full', action='store_true')
    args = parser.parse_args()

    # Get the anatomy and maps data
    surfElectrodes = load_mat(os.path.join(args.dataPath, 'surfaceElectrodes.mat'))

    points = surfElectrodes['se_location']
    cellsMeshio = [("triangle", [[0,1,2]])] # just to make meshio work
    point_data = {}

    # Get the static point data
    voltage_bipolar     = surfElectrodes['se_voltage_bi']
    voltage_unipolar    = surfElectrodes['se_voltage_uni']
    se_projected_dist   = surfElectrodes['se_projected_dist']
    activation_bipolar  = surfElectrodes['se_activation_bi']
    activation_unipolar = surfElectrodes['se_activation_uni']

    point_data['voltage_bipolar']     = voltage_bipolar
    point_data['voltage_unipolar']    = voltage_unipolar
    point_data['se_projected_dist']   = se_projected_dist
    point_data['activation_bipolar']  = activation_bipolar
    point_data['activation_unipolar'] = activation_unipolar

    # Get the time series (dynamic point data)
    if args.full:
        mapping_sigs_uni = surfElectrodes['se_mappingsigs_unipolar']
        mapping_sigs_bi = surfElectrodes['se_mappingsigs_bipolar']

    # # Save the mesh data
    mesh = meshio.Mesh(points, cells=cellsMeshio, point_data=point_data)
    mesh.write(os.path.join(args.dataPath, 'surfElectrodes_static.vtk'))

    
    # Save a point cloud with the actual surface measurements
    if args.full:
        times = np.arange(mapping_sigs_uni.shape[1]) * (1/surfElectrodes['sampleFreq'])
        with meshio.xdmf.TimeSeriesWriter(os.path.join(args.dataPath, 'surfElectrodes_dynamic.xdmf')) as writer:
            writer.write_points_cells(points, cellsMeshio)
            for i,t in enumerate(times):
                writer.write_data(t, point_data={"mapping_sigs_uni": mapping_sigs_uni[:,i],
                                                "mapping_sigs_bi": mapping_sigs_bi[:,i]})

    # Pay attention that .h5 file was saved in wrong place in previous meshio versions
    

if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))