import meshio 
import numpy as np
import os
import argparse

validKeys = ["endo", "mid", "epi", "myo", "scar"]

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--filePath',type=str, required=True, help='path to file and file name')
args = parser.parse_args()

mesh = meshio.read(args.filePath)
pointData = mesh.point_data
nsets={}
for key in pointData.keys():
    # if key in validKeys:
    nsets["{}".format(key)] = np.where(pointData[key]==1)[0]

meshOut = meshio.Mesh(mesh.points, mesh.cells, point_sets=nsets)
meshOut.write("{}.inp".format(args.filePath.split(".")[0]))
