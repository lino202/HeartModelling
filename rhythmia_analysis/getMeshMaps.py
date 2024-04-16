import meshio
import os
import argparse
import time
from matlab_readers import load_mat

def main():

    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument('--dataPath',   type=str, required=True, help='path to data')
    args = parser.parse_args()

    # Get the anatomy and maps data
    anatomy = load_mat(os.path.join(args.dataPath, 'anatomy.mat'))
    maps    = load_mat(os.path.join(args.dataPath, 'maps.mat'))

    # Get points and cells
    points = anatomy['points']
    cells  = anatomy['cells'] - 1
    point_data = {}

    # Get the maps section 
    voltage_bipolar     = maps['maps_voltage_bi']
    voltage_unipolar    = maps['maps_voltage_uni']
    cutoutmask          = maps['maps_cutoutmask'].astype(int)
    activation_bipolar  = maps['maps_activation_bi']
    activation_unipolar = maps['maps_activation_uni']

    point_data['voltage_bipolar']     = voltage_bipolar
    point_data['voltage_unipolar']    = voltage_unipolar
    if cutoutmask.shape[0] == points.shape[0]:
        point_data['cutoutmask']          = cutoutmask
    point_data['activation_bipolar']  = activation_bipolar
    point_data['activation_unipolar'] = activation_unipolar

    # Save the mesh data
    cellsMeshio = [("triangle", cells)]
    mesh = meshio.Mesh(points, cells=cellsMeshio, point_data=point_data)
    mesh.write(os.path.join(args.dataPath, 'anatomy_and_maps.vtk'))

if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))