import os 
import numpy as np
import argparse
import meshio
from scipy.spatial import KDTree


parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--meshHeart',type=str, required=True, help='path to data')
parser.add_argument('--meshScaffold',type=str, required=True)
parser.add_argument('--outPath',type=str, required=True, help='path to data')
args = parser.parse_args()

meshHeart = meshio.read(args.meshHeart)
meshScaffold = meshio.read(args.meshScaffold)
scaffoldCells = meshScaffold.cells_dict["triangle"]

#Compute face normals
pointsPerCell = meshScaffold.points[scaffoldCells]
u = pointsPerCell[:,2,:] - pointsPerCell[:,1,:]
v = pointsPerCell[:,2,:] - pointsPerCell[:,0,:]
normals = np.cross(u,v)
# normals = np.abs(normals)

#Get normal from mesh heart nearer to scaffold cell centroids
scaffoldCellsCent = np.mean(pointsPerCell, axis=1)
tree = KDTree(meshHeart.points)
_ , idxs = tree.query(scaffoldCellsCent, k=1)
normals2 = meshHeart.point_data["obj:vn"][idxs,:]

#Get final direction
fibs = np.cross(normals, normals2)
fibsMag = np.expand_dims(np.linalg.norm(fibs, axis=1), axis=1)
fibs = fibs / np.hstack((fibsMag,fibsMag,fibsMag))
# fibs = np.abs(fibs)

#SAVE
# points = np.concatenate((meshScaffold.points, scaffoldCellsCent), axis=0)
cell_data = {"fibs": [fibs], "normals": [normals], "normals2": [normals2]}

meshOut = meshio.Mesh(meshScaffold.points, meshScaffold.cells, cell_data=cell_data)
meshOut.write(args.outPath)