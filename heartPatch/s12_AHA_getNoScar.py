# this gets the pacing nodes corresponding to the endocardium of the AHA segments
 
import argparse
import meshio
import numpy as np
from scipy.spatial import KDTree
import os

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--meshNoScarVtk',type=str, required=True, help='path to data')
parser.add_argument('--meshNoScarInp',type=str, required=True, help='path to data')
parser.add_argument('--meshAHA',type=str, required=True)
parser.add_argument('--outPath',type=str, required=True, help='output path')
args = parser.parse_args()

meshNoScarVtk = meshio.read(args.meshNoScarVtk)
meshNoScarInp = meshio.read(args.meshNoScarInp)
meshAHA = meshio.read(args.meshAHA)

tree = KDTree(meshAHA.points)
_ , idxs = tree.query(meshNoScarVtk.points, k=1)


point_data_aha = meshAHA.point_data
for key in point_data_aha.keys():
    if 'stim_AHA' in key:
        # For now in Electra the nodesets should be in lowercase
        tmp = point_data_aha[key][idxs]
        number = key.replace('stim_AHA', '')
        meshNoScarVtk.point_data['stim_nodes_aha{}'.format(number)] = tmp
        meshNoScarInp.point_sets['stim_nodes_aha{}'.format(number)] = np.where(tmp == 1)[0]
    elif 'stim_nodes_aha' in key:
        tmp = point_data_aha[key][idxs]
        number = key.replace('stim_nodes_aha', '')
        meshNoScarVtk.point_data['stim_nodes_aha{}'.format(number)] = tmp
        meshNoScarInp.point_sets['stim_nodes_aha{}'.format(number)] = np.where(tmp == 1)[0]

#SAVE
meshNoScarVtk.write(os.path.join(args.outPath, 'mesh_no_scar.vtk'))
meshNoScarInp.write(os.path.join(args.outPath, 'mesh_no_scar.inp'))
