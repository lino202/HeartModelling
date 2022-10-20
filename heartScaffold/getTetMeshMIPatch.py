import os 
import numpy as np
import argparse
import meshio
from scipy.interpolate import RBFInterpolator

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--baseMesh',type=str, required=True)
parser.add_argument('--shellMesh',type=str, required=True)
parser.add_argument('--layersMesh',type=str, required=True)
parser.add_argument('--outPath',type=str, required=True)
args = parser.parse_args()

fields2interpolate = ["all", "rbm-fibers-long"]
baseMesh = meshio.read(args.baseMesh)
shellMesh = meshio.read(args.shellMesh)
layersMesh = meshio.read(args.layersMesh)

# First interpolate myo layers and define patch nodes
point_data = {}
for field in fields2interpolate:
    values2 = RBFInterpolator(baseMesh.points, layersMesh.point_data[field], neighbors=100)(layersMesh.points)
    point_data[field] = values2



# if "layers" in args.nameValue: finalValues2 = np.zeros((mesh2.points.shape[0]))
# if "dti" in args.nameValue: finalValues2 = np.zeros((mesh2.points.shape[0], 3))
# finalValues2[:] = np.nan 


# #get round values for vtk and inp
# if args.nameValue == "layers_mi" or args.nameValue == "layers":
#     finalValues2[finalValues2<np.nanmin(values)] = np.nanmin(values)
#     finalValues2[finalValues2>np.nanmax(values)] = np.nanmax(values)
#     finalValues2 = np.round(finalValues2)
# elif args.nameValue == "dti-fibers" or args.nameValue == "dti_fibers":
#     fibersNorm = np.linalg.norm(finalValues2, axis=1)
#     finalValues2 = finalValues2 /  np.array([fibersNorm, fibersNorm, fibersNorm]).T
#     outPath = "/".join(args.outPath.split("/")[:-1])
#     writeFibers4JSON(os.path.join(outPath, "fibersJsonElectra.txt"), finalValues2)
# else: raise ValueError("Wrong valueName")

# mesh2.point_data[args.nameValue] = finalValues2
# fileOutName = args.outPath.split(".")[0] + "_{}.vtk".format(args.interpType)
# mesh2.write(fileOutName)







baseMesh.point_data = point_data
baseMesh.write(args.outPath)