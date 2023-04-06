#This is conceptually wrong as tets will not have all their nodes as unattached
#then the complete unattachment is not a realistic one


import os 
import numpy as np
import argparse
import meshio
import random
import copy


parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--meshPath',    type=str, required=True, help='path to data')
parser.add_argument('--name',        type=str, required=True, help='name of mesh data')
parser.add_argument('--unattPercents', type=int, required=True, help='name of mesh data', nargs='+')
parser.add_argument('--patchID',     type=int, required=True, help='int that identifies the patch')
args = parser.parse_args()

mesh = meshio.read(os.path.join(args.meshPath, "{}.vtk".format(args.name)))
cells = mesh.cells_dict["tetra"]
patchIdxs = (mesh.point_data["layers"]==args.patchID).nonzero()[0]
cellsInBorder = np.sum(np.isin(cells, patchIdxs), 1)
cellsInBorderIdxs = np.where((cellsInBorder>0) & (cellsInBorder<4))[0]
unattachedPointIdxs = np.unique(cells[cellsInBorderIdxs,:].flatten())
unattachedPointPatchIdxs = (mesh.point_data["layers"][unattachedPointIdxs]==args.patchID).nonzero()[0]
unattachedPointPatchIdxs = unattachedPointIdxs[unattachedPointPatchIdxs]   #100 percent of patch nodes in the border


for i, unAttPercent in enumerate(args.unattPercents):
    nUnattPoints     = int(np.round(unattachedPointPatchIdxs.shape[0] * (unAttPercent / 100) ))
    
    currentUnattachedIdxs = random.sample(range(unattachedPointPatchIdxs.shape[0]), nUnattPoints)
    currentUnattachedIdxs = unattachedPointPatchIdxs[currentUnattachedIdxs]
    
    #Update mesh and save
    meshOut             = copy.deepcopy(mesh)
    meshOut.point_data["layers"][currentUnattachedIdxs] = 10 #unattached indexes
    tmp = np.zeros(mesh.points.shape[0])
    tmp[currentUnattachedIdxs] = 1
    meshOut.point_data["unattached"] = tmp
    outPath = os.path.join(args.meshPath, "{}_unattach{}.vtk".format(args.name, unAttPercent))
    meshOut.write(outPath)
    
    unattachedPointPatchIdxs = currentUnattachedIdxs
    