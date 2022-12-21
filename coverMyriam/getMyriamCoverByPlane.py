import os 
import numpy as np
import argparse
import meshio

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--dataPath',type=str, required=True, help='path to data')
parser.add_argument('--outPath',type=str, required=True, help='path to data')
parser.add_argument('--planeOrigin',type=float, nargs=3, required=True)
parser.add_argument('--planeNormal',type=float, nargs=3, required=True)
args = parser.parse_args()

mesh = meshio.read(args.dataPath)
points = mesh.points
planeOrigin = args.planeOrigin
planeNormal = args.planeNormal

pointsFromPlane = points - planeOrigin
dots = np.dot(pointsFromPlane, planeNormal)

idxsCover = np.where(dots > 0)[0]

cover = np.zeros(points.shape[0])
cover[idxsCover] = 1


point_data = {"cover" : cover}
mesh.point_data = point_data
mesh.write(args.outPath)