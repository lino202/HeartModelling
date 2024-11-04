import os 
import numpy as np
import argparse
import meshio
from scipy.spatial import KDTree
from scipy.interpolate import RBFInterpolator

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--coveredMeshPath',   type=str,   required=True, help='path to data')
parser.add_argument('--layersMeshPath',    type=str,   required=True, help='path to data')
parser.add_argument('--outPath',           type=str,   required=True, help='path to data')
parser.add_argument('--atsMeshPath',       type=str,   help='path to data')
parser.add_argument('--fibsMeshPath',      type=str,   help='path to data')
parser.add_argument('--pointDataMeshPath', type=str,   help='path to data')
parser.add_argument('--infarctedcellDataMeshPath', type=str,   help='path to data')


parser.add_argument('--layersName',        type=str)
parser.add_argument('--fibersNames',       type=str, nargs='+')
parser.add_argument('--atName',            type=str)
parser.add_argument('--pointDataNames',    type=str, nargs='+')
parser.add_argument('--infarctedCellDataName',    type=str)

parser.add_argument('--usePlane',          action='store_true')
parser.add_argument('--planeOrigin',       type=float, nargs=3)
parser.add_argument('--planeNormal',       type=float, nargs=3)
parser.add_argument('--tolDist',           type=float, required=True, help='distance tolerance to mesh without cover')
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

# coverElemsIdxs = coverElemsIdxs[counts==4]
# coverElems = np.zeros(meshCovered.cells_dict["tetra"].shape[0])
# coverElems[coverElemsIdxs] = 1
# meshCovered.cell_data["cover_allCoverNodes"] = coverElems

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
if args.fibersNames:
    meshFibs = meshio.read(args.fibsMeshPath)
    for fiberName in args.fibersNames:
        values1 = meshFibs.point_data[fiberName]
        values2 = RBFInterpolator(meshFibs.points, values1, neighbors=100)(points2)
        fibersNorm = np.linalg.norm(values2, axis=1)
        values2 = values2 /  np.array([fibersNorm, fibersNorm, fibersNorm]).T
        fibers2 = np.zeros((meshCovered.points.shape[0], 3))
        fibers2[:] = np.nan
        fibers2[realMyoIdxs] = values2
        meshCovered.point_data[fiberName] = fibers2

if args.pointDataNames:
    meshPointData = meshio.read(args.pointDataMeshPath)
    for pointDataName in args.pointDataNames:
        values1 = meshPointData.point_data[pointDataName]
        values2 = RBFInterpolator(meshPointData.points, values1, neighbors=100)(points2)
        values2[values2<np.nanmin(values1)] = np.nanmin(values1)
        values2[values2>np.nanmax(values1)] = np.nanmax(values1)
        values2 = np.round(values2)
        layers2 = np.zeros(meshCovered.points.shape[0])
        layers2[:] = np.nan
        layers2[realMyoIdxs] = values2
        meshCovered.point_data[pointDataName] = layers2


#Interpolate ATs into coarse covered mesh
if args.atName:
    meshAT = meshio.read(args.atsMeshPath)
    values1 = meshAT.point_data[args.atName]
    values2 = RBFInterpolator(meshAT.points, values1, neighbors=100)(points2)
    ats2 = np.zeros(meshCovered.points.shape[0])
    ats2[:] = np.nan 
    ats2[realMyoIdxs] =  values2
    meshCovered.point_data["LAT"] = ats2 - np.nanmin(ats2)


# Cell data interpolation can be use to interpolate cell data info for example the MI 
# Here we suppose we only have one type of cells and that type is tets
if args.infarctedCellDataName:

    infarctedMeshCellData = meshio.read(args.infarctedcellDataMeshPath)
    cells1 = infarctedMeshCellData.cells_dict["tetra"]
    values1 = infarctedMeshCellData.cell_data[args.infarctedCellDataName][0]
    points1 = np.mean(infarctedMeshCellData.points[cells1,:], axis=1)  # cell centers
    values2 = RBFInterpolator(points1, values1, neighbors=100)(meshCovered.points)
    
    values2[values2<np.nanmin(values1)] = np.nanmin(values1)
    values2[values2>np.nanmax(values1)] = np.nanmax(values1)
    values2 = np.round(values2)
        
    # We have cell data on points of the covered mesh so pass to cells
    # we make the cells with at least one node infarcted as infarcted 
    cells2 = meshCovered.cells[0].data
    idxs = np.unique(np.where(values2[cells2].astype(int)==1)[0])
    idxs_cover = np.isin(idxs, np.where(meshCovered.cell_data["cover_atLeastOneCoverNode"]==1 )[0])
    idxs = idxs[~idxs_cover]
    infarcted_cells = np.zeros(cells2.shape[0])
    infarcted_cells[idxs] = 1 
    meshCovered.cell_data[args.infarctedCellDataName] = infarcted_cells


meshCovered.write(args.outPath)