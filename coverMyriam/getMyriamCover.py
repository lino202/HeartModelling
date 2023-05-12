import os 
import numpy as np
import argparse
import meshio
from scipy.spatial import KDTree
from scipy.interpolate import RBFInterpolator

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--coveredMeshPath', type=str,   required=True, help='path to data')
parser.add_argument('--atsMeshPath',     type=str,   required=True, help='path to data')
parser.add_argument('--layersMeshPath',  type=str,   required=True, help='path to data')
parser.add_argument('--fibsMeshPath',    type=str,   required=True, help='path to data')
parser.add_argument('--outPath',         type=str,   required=True, help='path to data')
parser.add_argument('--layersName',      type=str)
parser.add_argument('--fibersName',      type=str)
parser.add_argument('--atName',          type=str)
parser.add_argument('--usePlane',        action='store_true')
parser.add_argument('--planeOrigin',     type=float, nargs=3)
parser.add_argument('--planeNormal',     type=float, nargs=3)
parser.add_argument('--tolDist',         type=float, required=True, help='distance tolerance to mesh without cover')
args = parser.parse_args()


meshCovered = meshio.read(args.coveredMeshPath)
meshLayers = meshio.read(args.layersMeshPath)

points1 = meshLayers.points
points2 = meshCovered.points

#Define nodes from cover and from actual myocardium
toleranceDist = args.tolDist
tree = KDTree(points1)
dists , _ = tree.query(points2, k=1)
coverNodes = (dists>toleranceDist).astype(float)

if args.usePlane:
    pointsFromPlane = meshCovered.points - args.planeOrigin
    dots = np.dot(pointsFromPlane, args.planeNormal)

    idxsNoCoverByPlane = np.where(dots < 0)[0]
    coverNodes[idxsNoCoverByPlane] = 0

#As myriam needs cover elements we calculated the elems with all four nodes
#set as cover node
coverNodesIdxs = np.where(coverNodes==1)[0]
coverElemsIdxs, counts = np.unique(np.isin(meshCovered.cells_dict["tetra"], coverNodesIdxs).nonzero()[0], return_counts=True)
coverElems = np.zeros(meshCovered.cells_dict["tetra"].shape[0])
coverElems[coverElemsIdxs] = 1
meshCovered.cell_data["cover_atLeastOneCoverNode"] = coverElems

coverElemsIdxs = coverElemsIdxs[counts==4]
coverElems = np.zeros(meshCovered.cells_dict["tetra"].shape[0])
coverElems[coverElemsIdxs] = 1
meshCovered.cell_data["cover_allCoverNodes"] = coverElems

meshCovered.point_data["cover"] = coverNodes

realMyoIdxs = np.where(coverNodes == 0)[0]
points2 = points2[realMyoIdxs]

#Interpolate layers into coarse covered mesh
if args.layersName:
    values1 = meshLayers.point_data[args.layersName]
    values2 = RBFInterpolator(meshLayers.points, values1, neighbors=100)(points2)
    values2[values2<np.nanmin(values1)] = np.nanmin(values1)
    values2[values2>np.nanmax(values1)] = np.nanmax(values1)
    values2 = np.round(values2)
    layers2 = np.zeros(meshCovered.points.shape[0])
    layers2[:] = np.nan
    layers2[realMyoIdxs] = values2
    meshCovered.point_data["layers"] = layers2

#Interpolate fibers into coarse covered mesh
if args.fibersName:
    meshFibs = meshio.read(args.fibsMeshPath)
    values1 = meshFibs.point_data[args.fibersName]
    values2 = RBFInterpolator(meshFibs.points, values1, neighbors=100)(points2)
    fibersNorm = np.linalg.norm(values2, axis=1)
    values2 = values2 /  np.array([fibersNorm, fibersNorm, fibersNorm]).T
    fibers2 = np.zeros((meshCovered.points.shape[0], 3))
    fibers2[:] = np.nan
    fibers2[realMyoIdxs] = values2
    meshCovered.point_data["fibers"] = fibers2

#Interpolate ATs into coarse covered mesh
if args.atName:
    meshAT = meshio.read(args.atsMeshPath)
    values1 = meshAT.point_data[args.atName]
    values2 = RBFInterpolator(meshAT.points, values1, neighbors=100)(points2)
    ats2 = np.zeros(meshCovered.points.shape[0])
    ats2[:] = np.nan 
    ats2[realMyoIdxs] =  values2
    meshCovered.point_data["LAT"] = ats2 - np.nanmin(ats2)


meshCovered.write(args.outPath)