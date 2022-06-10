'''Doste code need labels and geometry in vtk. The labels are in points but can be easilly change
to cell data in paraview with filter point to cell'''
#FOR NOW THIS DOES WORK BUT THERE WAS A PROBLEM IN GENERATING THE CODE IN DOSTE

import os
import numpy as np
import argparse
import meshio
from scipy.spatial.distance import cdist


parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--dataPath',type=str, required=True, help='path to data')
args = parser.parse_args()

surfMesh = meshio.read(os.path.join(args.dataPath, "surfMesh.obj"))
lvRing = meshio.read(os.path.join(args.dataPath, "lv_ring.obj"))
rvRing = meshio.read(os.path.join(args.dataPath, "rv_ring.obj"))
lvApex = meshio.read(os.path.join(args.dataPath, "lv_apex.obj"))
rvApex = meshio.read(os.path.join(args.dataPath, "rv_apex.obj"))

surfMeshPoints = surfMesh.points

lvRingFlag = 13 #Mitral valve
rvRingFlag = 14 #Tricuspid valve
lvApexFlag = 12 
rvApexFlag = 18 

def isMemberIdxsRowWise(arr1, arr2, tol = 1E-6, showMem=False):
    if showMem: 
        print("Required Memory: {} GB".format(4 *(arr1.shape[0]) * (arr2.shape[0]) / 1e9))
    else:
        arr1 = np.reshape(arr1, (-1,3))
    idxs = np.min(cdist(arr2,arr1), axis=1) < tol
    return idxs.nonzero()[0]

labels = np.zeros(surfMeshPoints.shape[0])
idxs = isMemberIdxsRowWise(lvRing.points, surfMeshPoints, showMem=True)
labels[idxs] = lvRingFlag

idxs = isMemberIdxsRowWise(rvRing.points, surfMeshPoints, showMem=True)
labels[idxs] = rvRingFlag

idxs = isMemberIdxsRowWise(lvApex.points, surfMeshPoints, showMem=True)
labels[idxs] = lvApexFlag

idxs = isMemberIdxsRowWise(rvApex.points, surfMeshPoints, showMem=True)
labels[idxs] = rvApexFlag

point_data = {}
point_data["angle"] = labels   #Leo called this point data angle I do not think is compulsory
meshOut = meshio.Mesh(surfMeshPoints, surfMesh.cells, point_data=point_data)
meshOut.write(os.path.join(args.dataPath, "labels_point.vtk"))
# meshio.vtk.write(os.path.join(args.dataPath, "labels_point.vtk"), meshOut,  binary=False)