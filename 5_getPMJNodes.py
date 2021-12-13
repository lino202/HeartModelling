import os
import numpy as np
import meshio
from pathlib import PurePath
from auxiliar.conductionSystem.lib.utils import getPointsInSphere

dataPath = "../data/sampleMA_Control2/stim/stim_cs"
finalBundlesPath = os.path.join(dataPath, 'finalBundles')
meshPath = os.path.join(dataPath, "mesh.vtk")
outName = 'stim_mesh'

# Get mesh points and arrays from files
mesh = meshio.read(meshPath)
nodes = mesh.points

endpointsFiles = [os.path.join(finalBundlesPath,file) for file in os.listdir(finalBundlesPath) if 'xyz' in file or 'ien' in file]
endpointsFiles.sort()

for file in endpointsFiles:
    with open(file, 'r') as f:
        data = f.read()

        # if 'xyz' in file:
        dataArr = np.array([])
        data = data.split('\n')[:-1]
        for i in range(len(data)):
            newRow = np.array([data[i].split(' ')])
            dataArr = np.concatenate( (dataArr, newRow), axis=0) if dataArr.size else newRow

    if 'xyz' in file:
        dataArr = dataArr.astype(float)
    elif 'ien' in file:
        dataArr = dataArr.astype(int)
    name = PurePath(file).parts[-1].split('.')[0]
    locals()[name] = dataArr


#Get bundles and PMJ stim nodes for each of them
bundlesNames = [ PurePath(file).parts[-1].split('_xyz')[0] for file in endpointsFiles if 'xyz' in file] 

stimSets = {}
for bundle in bundlesNames:

    #Get PMJ xyz Centers
    flat = locals()['{}_ien'.format(bundle)].flatten()
    flatUnique, counts = np.unique(flat, return_counts=True)
    xyzPMJCenters = locals()['{}_xyz'.format(bundle)]
    xyzPMJCenters = xyzPMJCenters[flatUnique[counts == 1]]

    stimIdxs = np.array([])
    for row in range(xyzPMJCenters.shape[0]):
        idxs = getPointsInSphere(nodes, xyzPMJCenters[row,:])
        stimIdxs = np.concatenate((stimIdxs, idxs)) if stimIdxs.size else idxs

    stimSets[bundle] = stimIdxs


point_data = mesh.point_data

stimPointData={}
for key in stimSets.keys():
    tmp = np.zeros(nodes.shape[0])
    tmp[stimSets[key]] = 1
    stimPointData[key] = tmp

nsets={}
for key in point_data:
    if key != 'layers' and key != 'dti-fibers':
        tmp = np.where(point_data[key]==1.)[0]
        nsets[key+'_nodes'] = tmp 

new_point_data = {**point_data, **stimPointData}
meshOut = meshio.Mesh(nodes, mesh.cells, point_data=new_point_data)
meshOut.write(os.path.join(dataPath, "{}.vtk".format(outName)))
# meshio.vtk.write(os.path.join(dataPath, "{}.vtk".format(outName)), meshOut,  binary=False) #Debugging

new_nsets = {**nsets, **stimSets}
meshOut = meshio.Mesh(nodes, mesh.cells, point_sets=new_nsets)
meshOut.write(os.path.join(dataPath, "{}.inp".format(outName)))