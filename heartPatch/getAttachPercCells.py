import os 
import numpy as np
import argparse
import meshio
import random
import copy
import matplotlib.pyplot as plt


parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--meshPath',    type=str, required=True, help='path to data')
parser.add_argument('--name',        type=str, required=True, help='name of mesh data')
parser.add_argument('--unattPercents', type=int, required=True, help='name of mesh data', nargs='+')
parser.add_argument('--patchID',     type=int, required=True, help='int that identifies the patch')
args = parser.parse_args()

mesh                     = meshio.read(os.path.join(args.meshPath, "{}.vtk".format(args.name)))
cells                    = mesh.cells_dict["tetra"]
patchIdxs                = (mesh.point_data["layers"]==args.patchID).nonzero()[0]
cellsInBorder            = np.sum(np.isin(cells, patchIdxs), 1)
cellsInBorderIdxs        = np.where((cellsInBorder>0) & (cellsInBorder<4))[0]
CellsInBorderTotal       = cellsInBorderIdxs.shape[0]
unattachedPointIdxsTotal = np.unique(cells[cellsInBorderIdxs,:].flatten())
# unattachedIdxs = (mesh.point_data["layers"][unattachedPointIdxs]==args.patchID).nonzero()[0]
# unattachedIdxs = unattachedPointIdxs[unattachedIdxs]   #100 percent of patch nodes in the border

steps = np.arange(100,0,-1)
percentages = []
for i, unAttPercent in enumerate(steps):
    nUnatt     = int(np.round(CellsInBorderTotal * (unAttPercent / 100) ))
    currentUnattachedIdxs = random.sample(range(cellsInBorderIdxs.shape[0]), nUnatt)
    currentUnattachedIdxs = cellsInBorderIdxs[currentUnattachedIdxs]
    unattachedPointIdxs = np.unique(cells[currentUnattachedIdxs,:].flatten())
    
    percentages.append(unattachedPointIdxs.shape[0] * 100 / unattachedPointIdxsTotal.shape[0])
    cellsInBorderIdxs = currentUnattachedIdxs

plt.figure()
plt.plot(steps, percentages)
plt.ylabel("Interface Nodes Percentage")
plt.xlabel("Interface Cells Percentage")
plt.savefig(os.path.join(args.meshPath, "nodes_vs_cells_percents.png"))

percentages = np.array(percentages)
finalUnattPercentsIdxs = np.zeros(len(args.unattPercents))
for i, unAttPercent in enumerate(args.unattPercents):
    finalUnattPercentsIdxs[i] = np.argmin(np.abs(percentages-unAttPercent))

finalUnattPercents = steps[finalUnattPercentsIdxs.astype(int)]
print("Percentage steps for cells: {}".format(finalUnattPercents))
print("Percentage of nodes obtained: {}".format(percentages[finalUnattPercentsIdxs.astype(int)]))
#One more time compute the unattached interface with new percentages based in nodes
cellsInBorderIdxs  = np.where((cellsInBorder>0) & (cellsInBorder<4))[0]
percentages
for i, unAttPercent in enumerate(finalUnattPercents):
    nUnatt     = int(np.round(CellsInBorderTotal * (unAttPercent / 100) ))
    currentUnattachedIdxs = random.sample(range(cellsInBorderIdxs.shape[0]), nUnatt)
    currentUnattachedIdxs = cellsInBorderIdxs[currentUnattachedIdxs]
    unattachedPointIdxs = np.unique(cells[currentUnattachedIdxs,:].flatten())
    
    currentPercentUnattNodes = unattachedPointIdxs.shape[0] * 100 / unattachedPointIdxsTotal.shape[0]
    cellsInBorderIdxs = currentUnattachedIdxs
    
    #Update mesh and save
    meshOut             = copy.deepcopy(mesh)
    meshOut.point_data["layers"][unattachedPointIdxs] = 10 #unattached indexes
    tmp = np.zeros(mesh.points.shape[0])
    tmp[unattachedPointIdxs] = 1
    meshOut.point_data["unattached"] = tmp
    outPath = os.path.join(args.meshPath, "{0}_unattach_{1:.2f}.vtk".format(args.name, currentPercentUnattNodes))
    meshOut.write(outPath)