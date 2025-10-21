import os
import meshio
import argparse
import numpy as np
import pickle

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--dataPath',type=str, required=True, help='path to data')
parser.add_argument('--outName',type=str, required=True, help='path to data')
parser.add_argument('--tissueThickness',type=float, required=True, help='thickness of the slab of tissue')
args = parser.parse_args()

# Read mesh 
mesh = meshio.read(os.path.join(args.dataPath, "tetmesh.vtk"))
points = mesh.points


nNodesPatch = (points[:,2]>args.tissueThickness).nonzero()[0].shape[0]
fibers = np.zeros([nNodesPatch, 3])
angles = np.random.uniform(low=-90, high=90, size=nNodesPatch)
fibers[:,0] = np.cos(np.deg2rad(angles))
fibers[:,1] = np.sin(np.deg2rad(angles))

# Save
with open(os.path.join(args.dataPath, '{}.pkl'.format(args.outName)), 'wb') as file:
    pickle.dump(fibers, file)


