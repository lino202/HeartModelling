from multiprocessing.sharedctypes import Value
import os
import meshio
import numpy as np 
import argparse
from lib.utils import checkRepeatedPoints, reorderPurkMesh, saveVtkInpMesh1D

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--data_path',type=str, required=True, help='path to data')
args = parser.parse_args()

#Inputs

csBundle = meshio.read(os.path.join(args.data_path, "stim", "stim_cs", "mainCSBundle.inp"))
outPath = os.path.join(args.data_path, "stim", "stim_cs")
outName = "cs_endo"

points = csBundle.points
edges = csBundle.cells[0][1]
nsets = csBundle.point_sets


# Unify all
purkTrees = ["lva", "lvp", "rvb"] 
for key in purkTrees:
    meshPurk = meshio.read(os.path.join(args.data_path, "stim", "stim_cs", "finalBundles", "{}.vtu".format(key)))
    meshPurkPoints = meshPurk.points
    meshPurkEdges = meshPurk.cells[0][1]

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