import os
import meshio
import numpy as np 
import argparse
from lib.utils import saveVtkInpMesh1D


parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--data_path',type=str, required=True, help='path to data')
parser.add_argument('--out_name',type=str, required=True, help='output file name')
args = parser.parse_args()

#Inputs
mesh = meshio.read(os.path.join(args.data_path, "cs_subendo_intramyo.vtu"))
points = mesh.points
edges = mesh.cells_dict["line"]
nsets = mesh.point_data

for set in nsets.keys():
    nsets[set] = np.nonzero(nsets[set])[0]

endnodesPurk, count = np.unique(edges.flatten(), return_counts=True)
nsets["purk_endnodes"] = endnodesPurk[count==1]

# Save
print("-----------Saving------------")
saveVtkInpMesh1D(points, edges, nsets, args.data_path, args.out_name)
