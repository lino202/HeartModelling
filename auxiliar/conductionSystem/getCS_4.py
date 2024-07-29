import os
import meshio
import numpy as np 
import argparse
from lib.utils import checkRepeatedPoints, reorderPurkMesh, saveVtkInpMesh1D

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--data_path',type=str, required=True, help='path to data')
parser.add_argument('--domainType',type=str, required=True, help='BiV (Biventricular) or LV')
# parser.add_argument('--cs_name',type=str, required=True, help='Name of the cs subfolder withe final data for cs construction')
parser.add_argument('--outName',   type=str, default='cs_endo')
args = parser.parse_args()

#Inputs

csBundle = meshio.read(os.path.join(args.data_path, "mainCSBundle.vtk"))
outPath = args.data_path
outName = args.outName

points = csBundle.points
edges = csBundle.cells_dict['line']
nsets = {}
for key in csBundle.point_data.keys():
    idxs = np.where(csBundle.point_data[key]!=0)[0]
    nsets[key] = idxs

# Unify all
if args.domainType == "BiV":
    purkTrees = ["lva", "lvp", "rvb"] 
elif args.domainType == "LV":
    purkTrees = ["lva", "lvp"]
else: raise ValueError("Domain type should be BiV or LV") 

for key in purkTrees:
    meshPurk = meshio.read(os.path.join(args.data_path, "{}.vtu".format(key)))
    meshPurkPoints = meshPurk.points
    meshPurkEdges = meshPurk.cells_dict['line']

    meshPurkPoints, meshPurkEdges = reorderPurkMesh(meshPurkPoints, meshPurkEdges)

    #add points, edges and nsets
    meshPurkEdges = meshPurkEdges + points.shape[0] - 1
 
    idxs = np.where(meshPurkEdges == (points.shape[0] -1 ))
    meshPurkEdges[idxs] = nsets["{}_end".format(key)]
    
    nsets[key + "_purk"] = [nodeIdx for nodeIdx in range(points.shape[0] , points.shape[0] + meshPurkEdges.shape[0])]
    endnodesPurk, count = np.unique(meshPurkEdges.flatten(), return_counts=True)
    nsets[key + "_purk_endnodes"] = endnodesPurk[count==1]
    try:
        nsets["purk_endnodes"] = np.concatenate((nsets["purk_endnodes"],endnodesPurk[count==1]))
    except KeyError:
        nsets["purk_endnodes"] = endnodesPurk[count==1]
    edges = np.concatenate((edges, meshPurkEdges), axis=0)
    points = np.concatenate((points, meshPurkPoints[1:]), axis=0)



checkRepeatedPoints(points)

saveVtkInpMesh1D(points, edges, nsets, outPath, outName)