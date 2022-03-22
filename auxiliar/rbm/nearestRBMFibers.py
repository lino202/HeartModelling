'''Nearest neighbour search for the case when we have a rbm and we have changed the mesh resolution.
Mesh2 gets the nearest fibers directions from Mesh1'''

import meshio
import numpy as np
import os
from utils import getHugeNearest, writeFibers4JSON, readFibersfromElectraPre
import argparse

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--pathMesh1',type=str, required=True, help='path to data')
parser.add_argument('--pathMesh2',type=str, required=True, help='path to data')
parser.add_argument('--pathFibers1',type=str, required=True, help='path to data')
parser.add_argument('--pathOut',type=str, required=True, help='path to data')
args = parser.parse_args()


mesh1 = meshio.read(args.pathMesh1)
mesh2 = meshio.read(args.pathMesh2)
points1 = mesh1.points
points2 = mesh2.points

fibers1 = readFibersfromElectraPre(args.pathFibers1)
print("The number of nodes mesh1: {}, fibers1: {}, mesh2: {}".format(points1.shape, fibers1.shape, points2.shape))
idxs = getHugeNearest(points2, points1)
fibers2 = fibers1[idxs,:]
print("The number of nodes fibers2: {}".format(fibers2.shape))
point_data=mesh2.point_data
point_data["rbm-fibers-long"] = fibers2 
meshOut = meshio.Mesh(mesh2.points, mesh2.cells, point_data=point_data)

meshOut.write(os.path.join(args.pathOut, "mesh_rbm.vtk"))
writeFibers4JSON(os.path.join(args.pathOut, "rbm_fibers_long.txt"), fibers2)
