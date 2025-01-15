# this gets the pacing nodes corresponding to the endocardium of the AHA segments
 
import argparse
import meshio
import numpy as np
from scipy.spatial import KDTree

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--meshIn',type=str, required=True, help='path to data')
parser.add_argument('--outPath',type=str, required=True, help='output path')
parser.add_argument('--endoLV',type=str, required=True)
parser.add_argument('--endoRV',type=str, required=True)
parser.add_argument('--stimRadious',type=float, default=1.)
parser.add_argument('--rvPacingCite',type=float, nargs=3, help="The unit is the same that the points of the mesh have")
args = parser.parse_args()

mesh = meshio.read(args.meshIn)
ahaSegs = mesh.point_data["AHASegs"]
endoLV = meshio.read(args.endoLV)
endoRV = meshio.read(args.endoRV)

treeMesh = KDTree(mesh.points)
treeLV = KDTree(endoLV.points)
treeRV = KDTree(endoRV.points)

nSegs = int(np.max(ahaSegs))
centroids = np.zeros((nSegs,3))
for i in range(nSegs-1): #Minus one as we do not compute for RV
    centroids[i,:] = np.mean(mesh.points[(ahaSegs==i+1).nonzero()], axis=0)
centroids[-1,:] = args.rvPacingCite       

# Pacing cites on endo surfs and on mesh
pacingCites     = np.zeros((nSegs,3))

_ , idxs = treeRV.query(centroids[-2:,:], k=1)
_ , idxs = treeMesh.query(endoRV.points[idxs,:], k=1) #Pacing cites on tetmesh
pacingCites[-2:,:] = mesh.points[idxs,:]

_ , idxs = treeLV.query(centroids[:-2,:], k=1)
_ , idxs = treeMesh.query(endoLV.points[idxs,:], k=1) #Pacing cites on tetmesh
pacingCites[:-2,:] = mesh.points[idxs,:]

# Use radious for defining nodesets
pacingNodesLists = treeMesh.query_ball_point(pacingCites, r=args.stimRadious)

# Get nodesets and point_data
for i, pacingList in enumerate(pacingNodesLists):
    tmp = np.zeros(mesh.points.shape[0])
    tmp[pacingList] = 1
    mesh.point_data["stim_AHA{}".format(i+1)] = tmp

#SAVE you can take to inp with mesh2inp
mesh.write(args.outPath)
