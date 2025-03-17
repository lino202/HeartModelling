import os 
import numpy as np
import argparse
import meshio
from scipy.spatial import KDTree


parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--meshPath',type=str, required=True, help='path to data mesh')
parser.add_argument('--myoTag',type=int, required=True, help='tag you desire to change to 1')

args = parser.parse_args()

mesh = meshio.read(args.meshPath)
cell_scalars = mesh.cell_data["cell_scalars"]
idxs = np.where(cell_scalars[0] == args.myoTag)

cell_scalars[0][idxs] = 1
cell_scalars[0] = cell_scalars[0].astype(int)
mesh.cell_data["cell_scalars"] = cell_scalars

mesh.write(args.meshPath)



