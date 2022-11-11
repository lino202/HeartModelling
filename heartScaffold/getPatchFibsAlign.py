import os
import numpy as np
import argparse
import meshio
from numba import cuda
from distPoint2Tri import pointTriDistCuda, pointTriDistCPU, getPerPointParams
from tqdm import tqdm
import math
import time
import matplotlib.pyplot as plt
import sys
sys.path.append(os.path.join('/'.join(sys.path[0].split("/")[:-1])))
from auxiliar.rbm.utils import writeFibers4JSON
import copy

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--meshMIPatch',type=str, required=True)
parser.add_argument('--meshScaffold',type=str, required=True, help='path to data')
parser.add_argument('--outPath',type=str, required=True, help='path to data')
parser.add_argument('--distThreshold',type=float, required=True)
parser.add_argument('--forceCPU', action='store_true')
args = parser.parse_args()


meshScaffold = meshio.read(args.meshScaffold)
meshMIPatch = meshio.read(args.meshMIPatch)
idxsPatch = np.where(meshMIPatch.point_data["layers"]==9)[0]
mipatchPoints = meshMIPatch.points.astype(float)
scaffoldPoints = meshScaffold.points.astype(float)
scaffoldCells = meshScaffold.cells_dict["triangle"]
patchFibs = meshMIPatch.point_data["fibers-rbmlongmyo-randompatch"][idxsPatch]

# idxsPatch = idxsPatch[:10000]
times = np.zeros(idxsPatch.shape[0])
startTot = time.time()

#Get nearest triangle from scaffold
triangles = scaffoldPoints[scaffoldCells,:]
Bs = triangles[:,0,:]
E0s = triangles[:,1,:] - Bs
E1s = triangles[:,2,:] - Bs
aArr = np.sum(E0s*E0s, axis=1)
bArr= np.sum(E0s*E1s, axis=1)
cArr = np.sum(E1s*E1s, axis=1)

pointNearTriIdx = np.zeros((idxsPatch.shape[0],2))
pointNearTriIdx[:] = np.nan
if cuda.is_available() and not args.forceCPU:
    print("Using gpu --> numba cuda")
    aArr = cuda.to_device(aArr)
    bArr = cuda.to_device(bArr)
    cArr = cuda.to_device(cArr)
    threadsperblock = 16
    blockspergrid =  math.ceil(triangles.shape[0] / threadsperblock)
    
    for i, idx in enumerate(tqdm(idxsPatch)):
        start = time.time()
        dArr, eArr, fArr = getPerPointParams(mipatchPoints[idx,:], Bs, E0s, E1s) 
        dArr = cuda.to_device(dArr)
        eArr = cuda.to_device(eArr)
        fArr = cuda.to_device(fArr)
        dists = cuda.to_device(np.zeros(triangles.shape[0]))
        #Define cuda kernel and launch
        pointTriDistCuda[blockspergrid, threadsperblock](dists, aArr, bArr, cArr, dArr, eArr, fArr)
        # nearestTriIdx[i] = np.argmin(dists.copy_to_host())
        # if i == 0: print(dists.copy_to_host())
        times[i] = time.time() - start
else:
    print("Using cpu --> numba jit")
    for i, idx in enumerate(tqdm(idxsPatch)):
        start = time.time()
        dArr, eArr, fArr = getPerPointParams(mipatchPoints[idx,:], Bs, E0s, E1s) 
        dists = pointTriDistCPU(aArr, bArr, cArr, dArr, eArr, fArr)
        if (dists < args.distThreshold).nonzero()[0].size:
            pointNearTriIdx[i,:] = [idx, np.argmin(dists)]
        # if i == 0: print(dists)
        times[i] = time.time() - start
    
print("Total time {0:.4f} s".format(time.time()-startTot))
# plt.figure(),plt.plot(times),plt.show()
print("Per point times mean: {0:.4f} s min:{1:.4f} s max:{2:.4f} s".format(np.mean(times), np.min(times), np.max(times)))

pointNearTriIdx = np.delete(pointNearTriIdx, np.isnan(pointNearTriIdx[:,0]), axis=0).astype(int)
fibers = copy.deepcopy(meshMIPatch.point_data["fibers-rbmlongmyo-randompatch"])                                 #rbm-fibers-long should have the random fibers on patch
fibers[pointNearTriIdx[:,0],:] = meshScaffold.cell_data["fibs"][0][pointNearTriIdx[:,1],:]
fibersAlignedPointData = np.zeros(meshMIPatch.points.shape[0])
fibersAlignedPointData[pointNearTriIdx[:,0]] = 1

#SAVE
print("The percentage of alignment is {0:.4f} %".format(pointNearTriIdx.shape[0]/idxsPatch.shape[0] * 100))
meshMIPatch.point_data["fibers-aligned-vectors"] = fibers
meshMIPatch.point_data["fibers-aligned-scalar"] = fibersAlignedPointData
# meshMIPatch.point_data["fibers-rbmlongmyo-randompatch"] = meshMIPatch.point_data["rbm-fibers-long"]
# meshMIPatch.point_data.pop("rbm-fibers-long")
meshMIPatch.write(os.path.join(args.outPath, "heartPatch_tetmesh_layers_fibs.vtk"))

writeFibers4JSON(os.path.join(args.outPath, "fibers.txt"), fibers)