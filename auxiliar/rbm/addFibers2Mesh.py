'''Add the fibers from ElectraPre to the mesh in .vtk for visual inspection in paraview'''

import os
import numpy as np
import argparse
import meshio
from utils import writeFibers4JSON, readFibersfromElectraPre

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--dataPath',type=str, required=True, help='path to data')
parser.add_argument('--mesh3dPath',type=str, required=True, help='path to data')
parser.add_argument('--outName',type=str, required=True, help='output name')
args = parser.parse_args()

mesh = meshio.read(os.path.join(args.mesh3dPath, "rbm_mesh.vtk"))
rbmVersors = readFibersfromElectraPre(os.path.join(args.dataPath, "long_fibers.txt"))
print("Mesh nodes {} and fibers {}\n".format(mesh.points.shape, rbmVersors.shape) )
point_data=mesh.point_data
point_data["rbm-fibers-long"] = rbmVersors 

meshOut = meshio.Mesh(mesh.points, mesh.cells, point_data=point_data)
meshOut.write(os.path.join(args.dataPath, "{}.vtk".format(args.outName)))

writeFibers4JSON(os.path.join(args.dataPath, "rbm_fibers.txt"), rbmVersors)

