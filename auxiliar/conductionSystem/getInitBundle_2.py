import numpy as np
import pygeodesic.geodesic as geodesic
import meshio
import os
import json
from lib.utils import checkRepeatedPoints, getLinearPath, getLinearPath, getGeodesicPath, resampleGeodesic
import argparse

#XDMF from paraview has time attribute which does not work with meshio
#and .vtk legacy has a KeyError: 'vtkidtype' which seemed to be solved but it is not
# that is the reason why I am using .vtu

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--data_path',required=True, help='path to data')
parser.add_argument('--gen_obj', action='store_true', help='if specified, generate .obj surface endo meshes for fractal Purkinje network algo')
args = parser.parse_args()

#Inputs
dataPath = args.data_path
rvEndoSurf = os.path.join(dataPath, "rv_endo.obj")
lvEndoSurf = os.path.join(dataPath, "lv_endo.obj")
purkInitNodes =  os.path.join(dataPath, "purkInitNodes.json")

#Outputs
outName = "mainCSBundle"    # generates .inp and .vtk
genOBJ = args.gen_obj             # if true generates xv_endo.obj for fractal algo

meshRV = meshio.read(rvEndoSurf)
meshLV = meshio.read(lvEndoSurf)
nsets = {}

meshRVPoints = meshRV.points
meshLVPoints = meshLV.points
for cellCluster in meshRV.cells:
    if cellCluster[0] =='triangle':
        meshRVFaces =  cellCluster[1]
for cellCluster in meshLV.cells:
    if cellCluster[0] =='triangle':
        meshLVFaces =  cellCluster[1]

# Select all the points for generating the bundle - Import nodes info-----------------------------------
with open(purkInitNodes, 'r')as file:
    nodesData = json.load(file)
commonNodes = nodesData["Common_Nodes"]
rvNodes = nodesData["RV_Nodes"]
lvNodes = nodesData["LV_Nodes"]

# Create linear/non geodesic paths-----------------------------------------------------------------
points, edges =  getLinearPath(commonNodes["AV_Node"], commonNodes["HIS_Node"])
avNode = 0
hisIdx = points.shape[0] -1
nsets["av_node"] = [avNode]     # nsets must be iterable
nsets["av_his"] = [nodeIdx for nodeIdx in range(points.shape[0])]
nsets["his_bifur_node"] = [hisIdx]

tmpPoints, tmpEdges =  getLinearPath(commonNodes["HIS_Node"], rvNodes["Init"])
tmpEdges = tmpEdges + points.shape[0] -1
nsets["his_rv_linear"] = [nodeIdx for nodeIdx in range(points.shape[0] , points.shape[0] + tmpPoints.shape[0] -1 )]
tmpEdges[0, 0] = hisIdx
edges = np.concatenate((edges, tmpEdges), axis=0)
points = np.concatenate((points, tmpPoints[1:,:]), axis=0)
rvInitIdx = points.shape[0] -1

tmpPoints, tmpEdges =  getLinearPath(commonNodes["HIS_Node"], lvNodes["Init"])
tmpEdges = tmpEdges + points.shape[0] -1 
nsets["his_lv_linear"] = [nodeIdx for nodeIdx in range(points.shape[0] , points.shape[0] + tmpPoints.shape[0] -1 )]
tmpEdges[0,0] = hisIdx
edges = np.concatenate((edges, tmpEdges), axis=0)
points = np.concatenate((points, tmpPoints[1:,:]), axis=0)
lvInitIdx = points.shape[0] -1

# Geodesic o non linear paths-------------------------------------------------------------------------

tmpPoints, _ =  getGeodesicPath(meshRVPoints, meshRVFaces, rvNodes["Init"], rvNodes["Join"])
tmpPoints, tmpEdges = resampleGeodesic(tmpPoints)
tmpEdges = tmpEdges + points.shape[0] -1
nsets["his_rv_geo"] = [nodeIdx for nodeIdx in range(points.shape[0] , points.shape[0] + tmpPoints.shape[0] -1 )]
tmpEdges[0,0] = rvInitIdx
edges = np.concatenate((edges, tmpEdges), axis=0)
points = np.concatenate((points, tmpPoints[1:,:]), axis=0)
rvJoinIdx = points.shape[0] -1

tmpPoints, _ =  getGeodesicPath(meshLVPoints, meshLVFaces, lvNodes["Init"], lvNodes["Join"])
tmpPoints, tmpEdges = resampleGeodesic(tmpPoints)
tmpEdges = tmpEdges + points.shape[0] -1
nsets["his_lv_geo"] = [nodeIdx for nodeIdx in range(points.shape[0] , points.shape[0] + tmpPoints.shape[0] -1 )]
tmpEdges[0,0] = lvInitIdx
edges = np.concatenate((edges, tmpEdges), axis=0)
points = np.concatenate((points, tmpPoints[1:,:]), axis=0)
lvJoinIdx = points.shape[0] -1

nsets["his_lv_rv"] = [nodeIdx for nodeIdx in range(hisIdx + 1 ,points.shape[0])]

#Geodesic endpoints-----------------------------------------------------------------------------------------
for key in lvNodes.keys():
    if "lv" in key:
        tmpPoints, _ =  getGeodesicPath(meshLVPoints, meshLVFaces, lvNodes["Join"], lvNodes[key])
        tmpPoints, tmpEdges = resampleGeodesic(tmpPoints)
        tmpEdges = tmpEdges + points.shape[0] -1
        nsets[key] = [nodeIdx for nodeIdx in range(points.shape[0] , points.shape[0] + tmpPoints.shape[0] -1 )]
        tmpEdges[0,0] = lvJoinIdx
        edges = np.concatenate((edges, tmpEdges), axis=0)
        points = np.concatenate((points, tmpPoints[1:,:]), axis=0)
        nsets["{}_end".format(key.lower())] = [points.shape[0]-1]


for key in rvNodes.keys():
    if "rv" in key:
        tmpPoints, _ =  getGeodesicPath(meshRVPoints, meshRVFaces, rvNodes["Join"], rvNodes[key])
        tmpPoints, tmpEdges = resampleGeodesic(tmpPoints)
        tmpEdges = tmpEdges + points.shape[0] -1
        nsets[key] = [nodeIdx for nodeIdx in range(points.shape[0] , points.shape[0] + tmpPoints.shape[0] -1 )]
        tmpEdges[0,0] = rvJoinIdx
        edges = np.concatenate((edges, tmpEdges), axis=0)
        points = np.concatenate((points, tmpPoints[1:,:]), axis=0)
        nsets["{}_end".format(key.lower())] = [points.shape[0]-1]


# Get all together!, points is ready, generate cells and point_data for visualization in .vtk, nsets are ready

checkRepeatedPoints(points)

cells = [
    ("line", edges),
]

nsets["all_nodes"] = list(np.arange(points.shape[0]))

point_data={}
for key in nsets.keys():
    tmp = np.zeros(points.shape[0])
    tmp[nsets[key]] = 1
    point_data[key] = list(tmp)


meshOut = meshio.Mesh(points, cells, point_data=point_data)
meshOut.write(os.path.join(dataPath, "{}.vtk".format(outName)))
# meshio.vtk.write(os.path.join(dataPath, "{}.vtk".format(outName)), meshOut,  binary=False) #Debugging

meshOut = meshio.Mesh(points, cells, point_sets=nsets)
meshOut.write(os.path.join(dataPath, "{}.inp".format(outName)))


# Get the .obj as required for FractalTree Mesh loadOBJ
if genOBJ:
    cells = [
        ("triangle", meshRVFaces),
    ]


    meshOut = meshio.Mesh(meshRVPoints, cells)
    meshOut.write(os.path.join(dataPath, "rv_endo.obj"))

    cells = [
        ("triangle", meshLVFaces),
    ]

    meshOut = meshio.Mesh(meshLVPoints, cells)
    meshOut.write(os.path.join(dataPath, "lv_endo.obj"))