import numpy as np
import pygeodesic.geodesic as geodesic
import meshio
import os
import json
from lib.utils import getLinearPath, getLinearPath, getGeodesicPath

#XDMF from paraview has time attribute which does not work with meshio
#and .vtk legacy has a KeyError: 'vtkidtype' which seemed to be solved but it is not
# that is the reason why I am using .vtu

dataPath = "/home/maxi/Documents/PhD/Code/purkinje/data/sampleMA_Control2/"
rvEndoSurf = os.path.join(dataPath, "rv_endo.vtu")
lvEndoSurf = os.path.join(dataPath, "lv_endo.vtu")
outName = "mainCSBundle"
purkInitNodes =  os.path.join(dataPath, "purkInitNodes.json")
stepsNonGeodesic = 3
genOBJ = True
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
nsets["AV_HIS"] = [nodeIdx for nodeIdx in range(points.shape[0])]


tmpPoints, tmpEdges =  getLinearPath(commonNodes["HIS_Node"], rvNodes["Init"])
tmpEdges = tmpEdges + points.shape[0] -1
tmpEdges[0, 0] = hisIdx
edges = np.concatenate((edges, tmpEdges), axis=0)
points = np.concatenate((points, tmpPoints[1:,:]), axis=0)
rvInitIdx = points.shape[0] -1

tmpPoints, tmpEdges =  getLinearPath(commonNodes["HIS_Node"], lvNodes["Init"])
tmpEdges = tmpEdges + points.shape[0] -1 
tmpEdges[0,0] = hisIdx
edges = np.concatenate((edges, tmpEdges), axis=0)
points = np.concatenate((points, tmpPoints[1:,:]), axis=0)
lvInitIdx = points.shape[0] -1



# Geodesic o non linear paths-------------------------------------------------------------------------

tmpPoints, tmpEdges =  getGeodesicPath(meshRVPoints, meshRVFaces, rvNodes["Init"], rvNodes["Join"])
tmpEdges = tmpEdges + points.shape[0] -1
tmpEdges[0,0] = rvInitIdx
edges = np.concatenate((edges, tmpEdges), axis=0)
points = np.concatenate((points, tmpPoints[1:,:]), axis=0)
rvJoinIdx = points.shape[0] -1

tmpPoints, tmpEdges =  getGeodesicPath(meshLVPoints, meshLVFaces, lvNodes["Init"], lvNodes["Join"])
tmpEdges = tmpEdges + points.shape[0] -1
tmpEdges[0,0] = lvInitIdx
edges = np.concatenate((edges, tmpEdges), axis=0)
points = np.concatenate((points, tmpPoints[1:,:]), axis=0)
lvJoinIdx = points.shape[0] -1

nsets["HIS_LV_RV"] = [nodeIdx for nodeIdx in range(hisIdx + 1 ,points.shape[0])]

#Geodesic endpoints-----------------------------------------------------------------------------------------
for key in lvNodes.keys():
    if "LV" in key:
        tmpPoints, tmpEdges =  getGeodesicPath(meshLVPoints, meshLVFaces, lvNodes["Join"], lvNodes[key])
        tmpEdges = tmpEdges + points.shape[0] -1
        nsets[key] = [nodeIdx for nodeIdx in range(points.shape[0] , points.shape[0] + tmpPoints.shape[0] -1 )]
        tmpEdges[0,0] = lvJoinIdx
        edges = np.concatenate((edges, tmpEdges), axis=0)
        points = np.concatenate((points, tmpPoints[1:,:]), axis=0)
        nsets["{}_end".format(key)] = [points.shape[0]-1]
        


for key in rvNodes.keys():
    if "RV" in key:
        tmpPoints, tmpEdges =  getGeodesicPath(meshRVPoints, meshRVFaces, rvNodes["Join"], rvNodes[key])
        tmpEdges = tmpEdges + points.shape[0] -1
        nsets[key] = [nodeIdx for nodeIdx in range(points.shape[0] , points.shape[0] + tmpPoints.shape[0] -1 )]
        tmpEdges[0,0] = rvJoinIdx
        edges = np.concatenate((edges, tmpEdges), axis=0)
        points = np.concatenate((points, tmpPoints[1:,:]), axis=0)
        nsets["{}_end".format(key)] = [points.shape[0]-1]

cells = [
    ("line", edges),
]


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