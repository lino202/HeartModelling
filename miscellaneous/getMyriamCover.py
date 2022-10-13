import os 
import numpy as np
import argparse
import meshio
from scipy.spatial import KDTree
from scipy.interpolate import RBFInterpolator

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--coveredMeshPath',type=str, required=True, help='path to data')
parser.add_argument('--atsMeshPath',type=str, required=True, help='path to data')
parser.add_argument('--layersFibMeshPath',type=str, required=True, help='path to data')
parser.add_argument('--outPath',type=str, required=True, help='path to data')
parser.add_argument('--tolDist',type=float, required=True, help='distance tolerance to mesh without cover')
args = parser.parse_args()

meshCovered = meshio.read(args.coveredMeshPath)
meshAT = meshio.read(args.atsMeshPath)
meshLayersFibs = meshio.read(args.layersFibMeshPath)

points1 = meshLayersFibs.points
points2 = meshCovered.points

#Define nodes from cover and from actual myocardium
toleranceDist = args.tolDist
tree = KDTree(points1)
dists , _ = tree.query(points2, k=1)
coverNodes = (dists>toleranceDist).astype(float)
meshCovered.point_data["cover"] = coverNodes


realMyoIdxs = np.where(coverNodes == 0)[0]
points2 = points2[realMyoIdxs]

#Interpolate layers into coarse covered mesh
values1 = meshLayersFibs.point_data["layers"]
values2 = RBFInterpolator(points1, values1, neighbors=100)(points2)
values2[values2<np.nanmin(values1)] = np.nanmin(values1)
values2[values2>np.nanmax(values1)] = np.nanmax(values1)
values2 = np.round(values2)
layers2 = np.zeros(meshCovered.points.shape[0])
layers2[:] = np.nan
layers2[realMyoIdxs] = values2
meshCovered.point_data["layers"] = layers2

#Interpolate fibers into coarse covered mesh
values1 = meshLayersFibs.point_data["dti-fibers"]
values2 = RBFInterpolator(points1, values1, neighbors=100)(points2)
fibersNorm = np.linalg.norm(values2, axis=1)
values2 = values2 /  np.array([fibersNorm, fibersNorm, fibersNorm]).T
fibers2 = np.zeros((meshCovered.points.shape[0], 3))
fibers2[:] = np.nan
fibers2[realMyoIdxs] = values2
meshCovered.point_data["dti-fibers"] = fibers2

#Interpolate ATs into coarse covered mesh
points1 = meshAT.points
values1 = meshAT.point_data["LAT"]
values2 = RBFInterpolator(points1, values1, neighbors=100)(points2)
ats2 = np.zeros(meshCovered.points.shape[0])
ats2[:] = np.nan 
ats2[realMyoIdxs] =  values2
meshCovered.point_data["LAT"] = ats2 - np.nanmin(ats2)


meshCovered.write(args.outPath)