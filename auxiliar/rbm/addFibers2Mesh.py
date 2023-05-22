'''Add the fibers from ElectraPre to the mesh in .vtk for visual inspection in paraview'''

import os
import numpy as np
import argparse
import meshio
from utils import writeFibers4JSON, readFibersfromElectraPre
from scipy.spatial import KDTree

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--dataPath',type=str, required=True, help='path to data')
parser.add_argument('--mesh3DPath',type=str, required=True, help='path to data')
parser.add_argument('--fiberMeshName',type=str, required=True, help='path to data')
parser.add_argument('--fiberMethod',type=str, required=True, help='method from which the fibers where generated')
parser.add_argument('--writeFibersElectra', action='store_true', help='if json for electra must be created')
parser.add_argument('--dataPointName', type=str, required=True, help='name for data point in out vtk')
parser.add_argument('--outName',type=str, required=True, help='output name')
args = parser.parse_args()

mesh = meshio.read(args.mesh3DPath)
meshPoints = mesh.points
if args.fiberMethod == "ElectraPre":
    rbmVersors = readFibersfromElectraPre(os.path.join(args.dataPath, "long_fibers.txt"))
elif args.fiberMethod == "LDRB":
    import h5py
    with h5py.File(os.path.join(args.dataPath, "{}.h5".format(args.fiberMeshName)), "r") as f:
        # List all groups
        fiberPoints = np.array(f["fiber"]["coordinates"])
        rbmVersors = np.array(f["fiber"]["vector"])   #already normalized
        angles = np.array(f["fiber"]["scalar"])

    tree = KDTree(fiberPoints)
    _ , idxs = tree.query(meshPoints, k=1)
    rbmVersors = rbmVersors[idxs,:]
    angles = angles[idxs]

else: raise ValueError("Fibers Method not implemented")

print("Mesh nodes {} and fibers {}\n".format(meshPoints.shape, rbmVersors.shape) )
point_data=mesh.point_data
point_data["rbm_{}".format(args.dataPointName)] = rbmVersors 
point_data["{}_angle".format(args.dataPointName)] = angles

meshOut = meshio.Mesh(mesh.points, mesh.cells, point_data=point_data)
meshOut.write(os.path.join(args.dataPath, "{}.vtk".format(args.outName)))

if args.writeFibersElectra:
    writeFibers4JSON(os.path.join(args.dataPath, "rbm_{}.txt".format(args.dataPointName)), rbmVersors)

