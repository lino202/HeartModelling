#Patch region is fill with patch elems, but the nodes at the interface are 
#defined as myocardium (scar, bz or epi) which seems the most logical choice

import os 
import numpy as np
import argparse
import meshio
import random
import copy
import matplotlib.pyplot as plt
from tqdm import tqdm
import sys
sys.path.append(os.path.join('/'.join(sys.path[0].split("/")[:-1])))
from auxiliar.rbm.utils import writeFibers4JSON

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--meshPath',      type=str, required=True, help='path to data')
parser.add_argument('--name',          type=str, required=True, help='name of mesh data')
parser.add_argument('--fibersKey',     type=str, required=True, help='name of fibers as duplicate nodes will need more fibers definitions')
parser.add_argument('--unattPercents', type=int, required=True, help='name of mesh data', nargs='+')
parser.add_argument('--patchID',       type=int, required=True, help='int that identifies the patch')
args = parser.parse_args()

def dupliAttachMeshPoints(mesh, unattPoints, cellsInBorderIdxs):
    #Duplicate Points
    cells             = mesh.cells_dict["tetra"]
    newPoints         = mesh.points
    newPoints         = np.concatenate((newPoints, mesh.points[unattPoints,:]), axis=0)
    newInterfaceCells = copy.deepcopy(cells[cellsInBorderIdxs])
    newCellsIdxs      = np.isin(newInterfaceCells, unattPoints) #Idxs of the points in the interface cells that will be duplicate

    cellMap = np.ones(unattPoints.max()+1) * np.nan
    cellMap[unattPoints] = np.arange(0,unattPoints.shape[0])
    cellMap = cellMap + mesh.points.shape[0]
    newInterfaceCells[newCellsIdxs] = cellMap[newInterfaceCells[newCellsIdxs]]

    # Update mesh and save
    newCells = cells
    newCells[cellsInBorderIdxs] = newInterfaceCells
    newCells = [("tetra", newCells)]
    meshOut = meshio.Mesh(newPoints, newCells)

    for key in mesh.point_data.keys():
        if mesh.point_data[key].ndim == 1:
            tmp = np.zeros(meshOut.points.shape[0])
        elif mesh.point_data[key].ndim == 2:
            tmp = np.zeros((meshOut.points.shape[0], mesh.point_data[key].shape[1]))
        
        tmp[:mesh.points.shape[0]] = mesh.point_data[key]
        if "layers" in key:
            tmp[mesh.points.shape[0]:] = 10
        else:
            tmp[mesh.points.shape[0]:] = mesh.point_data[key][unattPoints]
        meshOut.point_data[key] = tmp

    tmp = np.zeros(meshOut.points.shape[0])
    tmp[mesh.points.shape[0]:] = 1
    meshOut.point_data["unattached"] = tmp
    
    return meshOut


def main():

    mesh                     = meshio.read(os.path.join(args.meshPath, "{}.vtk".format(args.name)))
    cells                    = mesh.cells_dict["tetra"]
    patchIdxs                = (mesh.point_data["layers"]==args.patchID).nonzero()[0]
    cellsInBorder            = np.sum(np.isin(cells, patchIdxs), 1)
    cellsInBorderIdxs        = np.where((cellsInBorder>0) & (cellsInBorder<4))[0]
    cellsInBorderTotal       = cellsInBorderIdxs.shape[0]
    unattachedPointIdxsTotal = np.unique(cells[cellsInBorderIdxs,:].flatten())
    myoInterfacePointsIdxs   = (mesh.point_data["layers"][unattachedPointIdxsTotal]!=args.patchID).nonzero()[0]
    unattPoints              = unattachedPointIdxsTotal[myoInterfacePointsIdxs]  #These are the nodes at the interface
    nUnattPointsTotal        = unattPoints.shape[0]

    for i, unAttPercent in enumerate(args.unattPercents):
        nUnattPoints     = int(np.round(nUnattPointsTotal * (unAttPercent / 100) ))
        
        currentUnattachedIdxs = random.sample(range(unattPoints.shape[0]), nUnattPoints)
        currentUnattachedIdxs = unattPoints[currentUnattachedIdxs]
        
        meshOut = dupliAttachMeshPoints(mesh, currentUnattachedIdxs, cellsInBorderIdxs)
        
        #Save
        outPath = os.path.join(args.meshPath, "{}_unattach{}".format(args.name, unAttPercent))
        meshOut.write("{}.vtk".format(outPath))
        writeFibers4JSON("{}_{}.txt".format(outPath, args.fibersKey), meshOut.point_data[args.fibersKey])
        
        #Update unattached points
        unattPoints = currentUnattachedIdxs
    

if __name__ == '__main__':
    main()
