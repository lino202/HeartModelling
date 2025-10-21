# this takes a CS mesh with AT times for creating stim nodes point data
import argparse
import meshio
from scipy.spatial import KDTree
import numpy as np
import copy
import os

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--meshCS',type=str, required=True, help='CS mesh with the ATs')
parser.add_argument('--mesh',type=str, required=True, help='the mesh we will put stim on')
parser.add_argument('--avNodeATtime',type=int, help='in the simulation of CS usually the av node is stimulated at a certain time,'
                    ' as the AT in the resulting mesh can be normalized to init in zero, we can with this param get the original ATs values', default=10)
parser.add_argument('--radius',type=float, required=True, help='the radius of the pmj, take into account the units of the mesh')
args = parser.parse_args()

# Read data
meshCS = meshio.read(args.meshCS)
mesh = meshio.read(args.mesh)

# Get CS pmjs
csCells = meshCS.cells_dict['line']
pmjIdxs, count = np.unique(csCells.flatten(), return_counts=True)
pmjIdxs = pmjIdxs[np.where(count==1)[0]]
pmjIdxs = pmjIdxs[pmjIdxs!=0]   # 0 is the av_node

# Get stim nodes on mesh
tree = KDTree(mesh.points)
_ , idxs = tree.query(meshCS.points[pmjIdxs,:], k=1)

idxsBall = tree.query_ball_point(mesh.points[idxs,:], r=args.radius) 

stims = np.zeros(mesh.points.shape[0])
for i in range(idxsBall.shape[0]):
    stims[idxsBall[i]] = meshCS.point_data['ATs_(ms)'][pmjIdxs[i]] + args.avNodeATtime


# Save
mesh.point_data['stim_nodes'] = stims
mesh.write(args.mesh)



