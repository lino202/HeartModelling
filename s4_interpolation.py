import os  
import argparse
import numpy as np
import meshio
from scipy.interpolate import RBFInterpolator, griddata
from auxiliar.rbm.utils import writeFibers4JSON

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--dataPath1',type=str, required=True, help='path to data')
parser.add_argument('--dataPath2',type=str, required=True, help='path to data')
parser.add_argument('--interpType', type=str, required=True, help='nearest or rbf')
parser.add_argument('--neighbours', type=int, required=True, help='neighbours to take into account, only used in rbf')
parser.add_argument('--nameValue', type=str, required=True, help='value to interp, layers_mi for GE/MI model or dti_fibers for exvivo dwi model')
parser.add_argument('--outPath',type=str, required=True)
args = parser.parse_args()

mesh1 = meshio.read(args.dataPath1)
mesh2 = meshio.read(args.dataPath2)

points1 = mesh1.points
points2 = mesh2.points
values = mesh1.point_data[args.nameValue]

if "cover" in mesh2.point_data.keys():
    realMyoIdxs = np.where(mesh2.point_data["cover"] == 0)[0]
    points2 = points2[realMyoIdxs]

if args.interpType == "nearest":
    values2 = griddata(points1, values, points2, method='nearest')
elif args.interpType == "rbf":
    values2 = RBFInterpolator(points1, values, neighbors=args.neighbours)(points2)
else: raise ValueError("Wrong interpolation type")

if "layers" in args.nameValue or "AHA" in args.nameValue or "LVRV" in args.nameValue: 
    finalValues2 = np.zeros((mesh2.points.shape[0]))
if "fibers" in args.nameValue: 
    finalValues2 = np.zeros((mesh2.points.shape[0], 3))
finalValues2[:] = np.nan 
if "cover" in mesh2.point_data.keys():
    finalValues2[realMyoIdxs] =  values2
else:
    finalValues2 = values2

#get round values for vtk and inp
if "layers" in args.nameValue or "AHA" in args.nameValue or "LVRV" in args.nameValue:
    finalValues2[finalValues2<np.nanmin(values)] = np.nanmin(values)
    finalValues2[finalValues2>np.nanmax(values)] = np.nanmax(values)
    finalValues2 = np.round(finalValues2)
elif "fibers" in args.nameValue:
    fibersNorm = np.linalg.norm(finalValues2, axis=1)
    finalValues2 = finalValues2 /  np.array([fibersNorm, fibersNorm, fibersNorm]).T
    outPath = "/".join(args.outPath.split("/")[:-1])
    writeFibers4JSON(os.path.join(outPath, "fibersJsonElectra.txt"), finalValues2)
else: raise ValueError("Wrong valueName")

mesh2.point_data[args.nameValue] = finalValues2
# fileOutName = args.outPath.split(".")[0] + "_{}.vtk".format(args.interpType)
mesh2.write(args.outPath)