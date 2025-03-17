import os 
import numpy as np
import argparse
import meshio
from scipy.spatial import KDTree


parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--meshHeart',type=str, required=True, help='path to data mesh in obj')
parser.add_argument('--meshScaffold',type=str, required=True, help='path to data')
parser.add_argument('--magnitude',type=float, default=0.6, help='magnitude to move')
args = parser.parse_args()

meshHeart = meshio.read(args.meshHeart)
meshScaffold = meshio.read(args.meshScaffold)

# Get the normal nearest to the scaffold centre
scaffoldMassCentrePoint = np.mean(meshScaffold.points, axis=0)

tree = KDTree(meshHeart.points)
_ , idxs = tree.query(scaffoldMassCentrePoint, k=1)

normal = meshHeart.point_data['obj:vn'][idxs,:]
normal = normal / np.linalg.norm(normal)

# Get the projection of the scaffold INTO the heart
meshScaffold.points = meshScaffold.points - args.magnitude * normal

meshScaffold.write(args.meshScaffold)



