'''Here we get the patch nodes for passing to tetgen with the edge length, we do not do this in s5_genMIPatchSurfFromXor
because if the code have errors by getting the correct patch elems in the final_scaffold_shell.obj you can correct it

So this code must be done BEFORE correcting the interface manually in meshlab and blender'''

import numpy as np
import argparse
import meshio
from scipy.spatial import KDTree

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--meshHeartPatch',type=str, required=True, help='path to data mesh in ply with color red on the patch faces')
parser.add_argument('--meshPatch',type=str, required=True, help='this is the final_shell output in s5, the EXACT mesh not cleaned! ')
args = parser.parse_args()

meshHeartPatch = meshio.read(args.meshHeartPatch)
meshPatch = meshio.read(args.meshPatch)

tree = KDTree(meshHeartPatch.points)
_ , idxs = tree.query(meshPatch.points, k=1)

tmp = np.zeros(meshHeartPatch.points.shape[0]).astype(np.uint8)
tmp[idxs] = 255

# We need to add all colors otherwise you will not see them in meshlab or blender
point_data = { 'red': tmp, 'green': np.zeros(meshHeartPatch.points.shape[0]).astype(np.uint8), 
              'blue': np.zeros(meshHeartPatch.points.shape[0]).astype(np.uint8), 'alpha': np.zeros(meshHeartPatch.points.shape[0]).astype(np.uint8)}

outMesh = meshio.Mesh(meshHeartPatch.points, meshHeartPatch.cells, point_data=point_data)
args.meshHeartPatch = args.meshHeartPatch.replace('.obj', '.ply')
outMesh.write(args.meshHeartPatch)

