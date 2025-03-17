# After cleaning the mesh for dropping the scar we ended up having SOME nodes in the boundary as being of the patch
# here we fix this for the vtk and inp mesh_no_scar files


import argparse
import meshio
import numpy as np
import os
import sys
from scipy.spatial import KDTree
import time
import copy
from tqdm import tqdm
from multiprocessing import Pool
sys.path.append(os.path.join(os.path.dirname(sys.path[0])))
from miscellaneous.regions import patch_flag, regions


def getNewLayerValueInit(_cells, _layers, _patch_flag):
    global cells, layers, patch_flag
    cells        = _cells
    layers       = _layers
    patch_flag   = _patch_flag

def getNewLayerValue(idx):
    neighbour_nodes = cells[np.any(np.isin(cells, idx), axis=1),:].flatten()
    if np.any(layers[neighbour_nodes]!=patch_flag):
        neighbour_nodes = neighbour_nodes[layers[neighbour_nodes]!=patch_flag] #without patch nodes
        new_values, counts = np.unique(layers[neighbour_nodes], return_counts=True)
        return new_values[np.argmax(counts)]
    else:
        return layers[idx]


start = time.time()

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--dataFolder',type=str, required=True, help='path to data')
parser.add_argument('--nProcesses',type=int, default=8,  help='N of workers, if exceeds cpu_count() then cpu_count-1 is used')
parser.add_argument('--chunksize',type=int, default=0,  help='Numbers of nodes to be treated by worker, if 0 all nodes are divided in the number of workers')
args = parser.parse_args()


meshNoScarVtk = meshio.read(os.path.join(args.dataFolder, 'mesh_no_scar.vtk'))
meshNoScarInp = meshio.read(os.path.join(args.dataFolder, 'mesh_no_scar.inp'))
meshTetMesh   = meshio.read(os.path.join(args.dataFolder, 'tetmesh.vtk'))
layersNoSCar = copy.deepcopy(meshNoScarVtk.point_data['layers'])

# Nodes in no scar mesh which are patch nodes, some of this are ok and others are wrong
idxs_noscar_patch = np.where(layersNoSCar==patch_flag)[0]

tree = KDTree(meshTetMesh.points)
_ , idxs = tree.query(meshNoScarVtk.points[idxs_noscar_patch,:], k=1)

# the points of the no scar mesh that are patch and are not patch in the with scar mesh -> are the nodes that has changed from scar to
# patch. This is correct in the free patch region but in the nodes of the interface where there is a tet with at least one non patch node
# we need to make all nodes in that tet as non patch AS THE INTERFACE IS FOR THE HEART AND NO THE PATCH (this should not have that much impact in the
# overall results but we did previous simulation so we keep consistent)

idxs_noscar_patch_changed = idxs_noscar_patch[layersNoSCar[idxs_noscar_patch] != meshTetMesh.point_data['layers'][idxs]]
cells = meshNoScarVtk.cells_dict['tetra']



if args.nProcesses >= os.cpu_count(): args.nProcesses = os.cpu_count()-1
if args.chunksize == 0: args.chunksize = int(np.round(idxs_noscar_patch_changed.shape[0] / args.nProcesses))
with Pool(args.nProcesses, initializer=getNewLayerValueInit, initargs=(cells, layersNoSCar, patch_flag)) as p:
    res = list(tqdm(p.imap(getNewLayerValue, idxs_noscar_patch_changed, chunksize=args.chunksize), total=idxs_noscar_patch_changed.shape[0]))

meshNoScarVtk.point_data['layers'][idxs_noscar_patch_changed] = res

# nsets = {}
# for key in regions.keys():
#     nsets[key] = np.where(layers==regions[key])[0]
# nsets['patch_nodes'] = np.where(layers==patch_flag)[0]

# fibers = meshVtk.point_data['fibers_rbmlongmyo_randompatch']

#SAVE

meshNoScarVtk.write(os.path.join(args.dataFolder, 'mesh_no_scar2.vtk'))

print("Fix interface nodes completed in {0:.2f} s".format(time.time() -start))
