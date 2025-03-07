import os 
import numpy as np
import argparse
import meshio
import copy
from scipy.spatial import KDTree
from scipy.spatial.transform import Rotation as R
import sys
sys.path.append(os.path.join('/'.join(sys.path[0].split("/")[:-1])))
from auxiliar.rbm.utils import writeFibers4JSON


parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--mesh',type=str, required=True, help='path to data')
parser.add_argument('--meshSurf',type=str, required=True, help='path to data')
parser.add_argument('--outPath',type=str, required=True, help='path to data')
args = parser.parse_args()

mesh        = meshio.read(args.mesh)
meshSurf    = meshio.read(args.meshSurf)
idxsPatch   = np.where(mesh.point_data["layers"]==9)[0]
patchPoints = mesh.points[idxsPatch]
idxsMyo     = np.where(mesh.point_data["layers"]!=9)[0]
myoPoints   = mesh.points[idxsMyo]

#Get Parallel and Perpendicular fibers direction to the Epi layer
tree = KDTree(myoPoints)
_ , idxs = tree.query(patchPoints, k=1)
parallelFibers = mesh.point_data["fibers-rbmlongmyo-randompatch"][idxsMyo[idxs.astype(int)]]

tree     = KDTree(meshSurf.points)
_ , idxs = tree.query(patchPoints, k=1)
normals  = meshSurf.point_data["obj:vn"][idxs,:]

rotVectors          = np.radians(90) * normals
rotations           = R.from_rotvec(rotVectors)
perpendicularFibers = rotations.apply(parallelFibers)

#Normalize and check for nans in final fiber field
mesh.point_data["fibers-patchparallel"] = copy.deepcopy(mesh.point_data["fibers-rbmlongmyo-randompatch"])
mesh.point_data["fibers-patchparallel"][idxsPatch] = parallelFibers

mesh.point_data["fibers-patchperpendicular"] = copy.deepcopy(mesh.point_data["fibers-rbmlongmyo-randompatch"])
mesh.point_data["fibers-patchperpendicular"][idxsPatch] = perpendicularFibers



#SAVE mesh and fibers
meshName = args.mesh.split("/")[-1].split(".")[0]
mesh.write(os.path.join(args.outPath, "{}_para_per_deli2022.vtk".format(meshName)))
writeFibers4JSON(os.path.join(args.outPath, "fibers_patchrandom.txt"), mesh.point_data["fibers-rbmlongmyo-randompatch"])
writeFibers4JSON(os.path.join(args.outPath, "fibers_patchparallel.txt"), mesh.point_data["fibers-patchparallel"])
writeFibers4JSON(os.path.join(args.outPath, "fibers_patchperpendicular.txt"), mesh.point_data["fibers-patchperpendicular"])