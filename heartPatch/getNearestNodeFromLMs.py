import os 
import numpy as np
import argparse
import meshio
from scipy.spatial.distance import cdist

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--mesh',type=str, required=True, help='path to data')
parser.add_argument('--landMarks',type=str, required=True, help='path to data')
args = parser.parse_args()

mesh = meshio.read(args.mesh)
name = args.mesh.split("/")[-1].split(".")[0]
path = args.mesh.split(name)[0]
points = mesh.points
point_data = mesh.point_data
nsets = {}
for key in point_data.keys():
    if "contact" in key:      #Exclude corner as it should already be in .fscv but the contact must be added
        nsets[key] = np.where(point_data[key]==1)[0]

with open(args.landMarks, 'r') as f:
    data = f.readlines()
if not "version = 5.0" in data[0]: raise ValueError("Version mismatch check fields correctness")
data = data[3:]
labels = []
coords = np.array([])
for row in data:
    rowSplit = row.split(",")
    labels.append(rowSplit[11])
    coords = np.concatenate((coords, np.array([rowSplit[1:4]]).astype(float)), axis=0) if coords.size else  np.array([rowSplit[1:4]]).astype(float)
dists = cdist(coords, points)
idxs = np.argmin(dists, axis=1)

nsets["all_LMs"] = []
for i, idx in enumerate(idxs):
    nsets[labels[i]] = [idx]
    nsets["all_LMs"].append(idx)
nsets["all"] = np.arange(0, mesh.points.shape[0])

point_data={}
for key in nsets.keys():
    tmp = np.zeros(points.shape[0])
    tmp[nsets[key]] = 1
    point_data[key] = list(tmp)

meshOut = meshio.Mesh(points, mesh.cells, point_data=point_data)
meshOut.write(os.path.join(path, "{}_lms.vtk".format(name)))
meshOut = meshio.Mesh(points, mesh.cells, point_sets=nsets)
meshOut.write(os.path.join(path, "{}_lms.inp".format(name)))