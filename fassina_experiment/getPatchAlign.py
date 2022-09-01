import os
import meshio
import argparse
import numpy as np
from scipy.spatial.distance import cdist
from tqdm import tqdm
from scipy.spatial import KDTree

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--tissuePath',type=str, required=True, help='path to data')
parser.add_argument('--scaffoldPath',type=str, required=True, help='path to data')
parser.add_argument('--outPath',type=str, required=True, help='path to data')
parser.add_argument('--patchCenter',type=float, nargs=3, required=True, help='center of mass of the scaffold')
parser.add_argument('--distThreshold',type=float, required=True, help='dist threshold for alignment')
args = parser.parse_args()

def writeFibers4JSON(filePath, rbmVersors):
    with open(filePath, "w") as file:
        file.write('"fibers":[[{0:.15f}, {1:.15f}, {2:.15f}],\n'.format(rbmVersors[0,0], rbmVersors[0,1], rbmVersors[0,2]))
        for i in tqdm(range(1,rbmVersors.shape[0]-1)):
            file.write("\t\t\t[{0:.15f}, {1:.15f}, {2:.15f}],\n".format(rbmVersors[i,0], rbmVersors[i,1], rbmVersors[i,2]))
        file.write("\t\t\t[{0:.15f}, {1:.15f}, {2:.15f}]]".format(rbmVersors[-1,0], rbmVersors[-1,1], rbmVersors[-1,2]))

# Read mesh 
tissueMesh = meshio.read(args.tissuePath)
tissuePoints = tissueMesh.points
tissueFibers = tissueMesh.point_data["fibers"]

scaffoldMesh = meshio.read(args.scaffoldPath)
scaffoldPoints = scaffoldMesh.points
scaffoldFibers = scaffoldMesh.point_data["Fibers"]

# Firstly, get scaffold to start in the origin
scaffoldPoints[:,0] =  scaffoldPoints[:,0] - np.min(scaffoldPoints[:,0])
scaffoldPoints[:,1] =  scaffoldPoints[:,1] - np.min(scaffoldPoints[:,1])
scaffoldPoints[:,2] =  scaffoldPoints[:,2] - np.min(scaffoldPoints[:,2])

#Secondly we sum to center the scaffold in the origin
scaffoldPoints[:,0] =  scaffoldPoints[:,0] - np.max(scaffoldPoints[:,0])/2
scaffoldPoints[:,1] =  scaffoldPoints[:,1] - np.max(scaffoldPoints[:,1])/2
scaffoldPoints[:,2] =  scaffoldPoints[:,2] - np.max(scaffoldPoints[:,2])/2

# Thirdly we move the scaffold to the patch tissue
scaffoldPoints[:,0] =  scaffoldPoints[:,0] + args.patchCenter[0]
scaffoldPoints[:,1] =  scaffoldPoints[:,1] + args.patchCenter[1]
scaffoldPoints[:,2] =  scaffoldPoints[:,2] + args.patchCenter[2]

#Get patch points and idxs
patchIdxs = (tissueMesh.point_data["patch"]==1).nonzero()[0]
patchPoints = tissuePoints[patchIdxs,:]
patchFibers = tissueFibers[patchIdxs]


#Orient
tree = KDTree(scaffoldPoints)
neighbours = tree.query_ball_point(patchPoints, args.distThreshold)
cellsAligned = 0
for j in tqdm(range(neighbours.shape[0])):
    if neighbours[j]: 
        cellsAligned += 1
        tmpFibers = scaffoldFibers[neighbours[j]]
        patchFibers[j,:] = np.mean(tmpFibers, axis=0)

tissueFibers[patchIdxs,:] = patchFibers

# GET ALIGNMENT VALUES-----------------------------------------------------------------------------------------------
longAlignDirection = np.array([[0 , 1, 0]]).T
longAlignRange = 45
A = (patchFibers @ longAlignDirection) / np.expand_dims(np.linalg.norm(patchFibers, axis=1) * np.linalg.norm(longAlignDirection), axis=1) 
auxMat = np.ones((patchFibers.shape[0],1))
cosTheta = np.maximum(np.minimum(A,auxMat),-1*auxMat)
thetaDegrees = np.degrees(np.arccos(cosTheta))
nInRange = np.where((thetaDegrees <= longAlignRange) | (thetaDegrees >= 180-longAlignRange))[0].shape[0]

print("Percentage of patch cellular alignment {}".format(cellsAligned / patchPoints.shape[0] * 100))
print("Longitudinal aligned nodes: {0:d}/{1:d}, percent: {2:.2f}".format(nInRange, patchPoints.shape[0], 100*(nInRange/patchPoints.shape[0])))



# SAVE DATA ----------------------------------------------------------------------------------------------------------
scaffoldMesh.points = scaffoldPoints
tissueMesh.point_data["fibers"] = tissueFibers

scaffoldMesh.write(os.path.join(args.outPath, "scaffold.vtk"))
tissueMesh.write(os.path.join(args.outPath, "tissue.vtk"))

# Get nsets for INP
point_data = tissueMesh.point_data
nsets = {}
for key in point_data.keys():
    if key != "fibers" and key != "tissueLayers":
        nsets["{}_nodes".format(key)] = np.where(point_data[key]==1)[0]

meshOutInp = meshio.Mesh(tissueMesh.points, tissueMesh.cells, point_sets=nsets)
meshOutInp.write(os.path.join(args.outPath, "tissue.inp"))
writeFibers4JSON(os.path.join(args.outPath, "fibers.txt"), tissueFibers)



