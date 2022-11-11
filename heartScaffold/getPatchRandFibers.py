import os 
import numpy as np
import argparse
import meshio
from scipy.spatial import KDTree
from scipy.spatial.transform import Rotation as R


parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--meshHeart',type=str, required=True, help='path to data')
parser.add_argument('--meshMIPatch',type=str, required=True)
parser.add_argument('--outPath',type=str, required=True, help='path to data')
args = parser.parse_args()

q1 = np.array([1,0,0])
q2 = np.array([0,1,0]) 
meshHeart = meshio.read(args.meshHeart)
meshMIPatch = meshio.read(args.meshMIPatch)
idxsPatch = np.where(meshMIPatch.point_data["layers"]==9)
patchPoints = meshMIPatch.points[idxsPatch]

#Compute normals from mesh heart for patch points
tree = KDTree(meshHeart.points)
_ , idxs = tree.query(patchPoints, k=1)
n = meshHeart.point_data["obj:vn"][idxs,:]

nq1 = np.abs(np.dot(n,q1))
nq2 = np.abs(np.dot(n,q2))
q = np.zeros(n.shape)
qidxs = nq1<=nq2
q[qidxs] = q1
q[np.invert(qidxs)]= q2

patchFibs = np.cross(n, q)

rotAnglesRad = np.expand_dims(np.radians(np.random.randint(-90,90,patchFibs.shape[0])), axis=1)
rotVectors = np.hstack((rotAnglesRad,rotAnglesRad,rotAnglesRad)) * n
rotations = R.from_rotvec(rotVectors)
patchFibs = rotations.apply(patchFibs)

#Normalize and check for nans in final fiber field
patchFibsMag = np.expand_dims(np.linalg.norm(patchFibs, axis=1), axis=1)
patchFibs = patchFibs / np.hstack((patchFibsMag,patchFibsMag,patchFibsMag))
meshMIPatch.point_data["rbm-fibers-long"][idxsPatch] = patchFibs
meshMIPatch.point_data["fibers-rbmlongmyo-randompatch"] = meshMIPatch.point_data.pop("rbm-fibers-long")
if np.isnan(meshMIPatch.point_data["fibers-rbmlongmyo-randompatch"]).nonzero()[0].size:
    raise ValueError("Nan in fiber field!")

#SAVE
meshMIPatch.write(args.outPath)