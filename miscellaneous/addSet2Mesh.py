#This receiveis and set mesh and putted in an input meshed from which it was obtained in paraview.
 
import argparse
import meshio
import numpy as np
from scipy.spatial import KDTree

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--meshIn',type=str, required=True, help='path to data')
parser.add_argument('--meshSet',type=str, required=True, help='output path')
parser.add_argument('--setName',type=str, required=True)
parser.add_argument('--outPath',type=str, required=True)
parser.add_argument('--setType',type=str, required=True, help="can be node_node, cell_cell, node_cell, cell_node")
args = parser.parse_args()

mesh = meshio.read(args.meshIn)
meshSet =  meshio.read(args.meshSet)

tree = KDTree(mesh.points)
idxs = tree.query(meshSet.points)[1]


if args.setType == "node":
    tmp = np.zeros(mesh.points.shape[0])   
    tmp[idxs] = 1
    mesh.point_data[args.setName] = tmp
elif args.setType == "cell":

    idxs, count = np.unique(np.isin(mesh.cells[0].data, idxs).nonzero()[0], return_counts=True)

    # tmp = np.zeros(mesh.cells[0].data.shape[0])
    # tmp[idxs] = 1
    # mesh.cell_data["{}_atLeastOneNode".format(args.setName)] = tmp

    tmp = np.zeros(mesh.cells[0].data.shape[0])
    idxs = idxs[count==4]
    tmp[idxs] = 1
    # mesh.cell_data["{}_allNodes".format(args.setName)] = tmp
    mesh.cell_data[args.setName] = tmp
else:
    raise ValueError("Wrong set type")

#SAVE you can take to inp with mesh2inp
mesh.write(args.outPath)
