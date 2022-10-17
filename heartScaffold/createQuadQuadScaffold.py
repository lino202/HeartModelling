import os 
import numpy as np
import argparse
import meshio
import pandas as pd
from utils import getGeodesicPath, resampleGeodesic, getLineInfo
from scipy.spatial import KDTree

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--meshHeart',type=str, required=True, help='path to data')
parser.add_argument('--pointLocs',type=str, required=True, help='Points taken following a clockwise order if seen in the front')
parser.add_argument('--thickness',type=float, required=True)
parser.add_argument('--poreSide',type=float, required=True)
parser.add_argument('--outPath',type=str, required=True, help='path to data')
args = parser.parse_args()

meshHeart = meshio.read(args.meshHeart)
meshHeartPoints = meshHeart.points
meshHeartCells = meshHeart.cells_dict['triangle']
tree = KDTree(meshHeartPoints)
df= pd.read_csv(args.pointLocs, usecols=[0,1,2,3])
extremePoints = {}
for i, point in enumerate(df["Point ID"]):
    extremePoints["point_{}".format(point)] = np.array([df["Points_0"][i], df["Points_1"][i], df["Points_2"][i]])


# Get first line and features of spacing
extremePointsKeys = list(extremePoints.keys())
line1Points, _ =  getGeodesicPath(meshHeartPoints, meshHeartCells, extremePoints[extremePointsKeys[0]], extremePoints[extremePointsKeys[1]])
line1Points, line1Edges = resampleGeodesic(line1Points, thresholdDist=args.poreSide)
_ , idx = tree.query(line1Points[-1,:], k=1)
line1Points[-1,:] = meshHeartPoints[idx,:]
getLineInfo(line1Points)

# Get the rest of the lines and features of spacing
line2Points, _ =  getGeodesicPath(meshHeartPoints, meshHeartCells, line1Points[-1,:], extremePoints[extremePointsKeys[2]])
line2Points, line2Edges = resampleGeodesic(line2Points, thresholdDist=args.poreSide)
_ , idx = tree.query(line2Points[-1,:], k=1)
line2Points[-1,:] = meshHeartPoints[idx,:]
getLineInfo(line2Points)

line3Points, _ =  getGeodesicPath(meshHeartPoints, meshHeartCells, line2Points[-1,:], extremePoints[extremePointsKeys[3]])
line3Points, line3Edges = resampleGeodesic(line3Points, thresholdDist=args.poreSide)
_ , idx = tree.query(line3Points[-1,:], k=1)
line3Points[-1,:] = meshHeartPoints[idx,:]
getLineInfo(line3Points)


line4Points, _ =  getGeodesicPath(meshHeartPoints, meshHeartCells, line3Points[-1,:], extremePoints[extremePointsKeys[0]])
line4Points, line4Edges = resampleGeodesic(line4Points, thresholdDist=args.poreSide)
_ , idx = tree.query(line4Points[-1,:], k=1)
line4Points[-1,:] = meshHeartPoints[idx,:]
getLineInfo(line4Points)




scaffoldPoints = line1Points
scaffoldEdges = line1Edges
scaffoldEdges = np.concatenate((scaffoldEdges, line2Edges+scaffoldPoints.shape[0]-1), axis=0)
scaffoldPoints = np.concatenate((scaffoldPoints, line2Points[1:,:]), axis=0)

scaffoldEdges = np.concatenate((scaffoldEdges, line3Edges+scaffoldPoints.shape[0]-1), axis=0)
scaffoldPoints = np.concatenate((scaffoldPoints, line3Points[1:,:]), axis=0)

scaffoldEdges = np.concatenate((scaffoldEdges, line4Edges+scaffoldPoints.shape[0]-1), axis=0)
scaffoldEdges[-1,1] = 0
scaffoldPoints = np.concatenate((scaffoldPoints, line4Points[1:-1,:]), axis=0)

print("line1: {}, line2: {}, line3: {}, line4: {}".format(line1Points.shape[0], line2Points.shape[0], line3Points.shape[0], line4Points.shape[0]))


for i in range(1,8): #line1Points.shape[0]-1
    idxLine1 = i
    idxLine3 = line1Points.shape[0]-1-i
    _ , idx1 = tree.query(line1Points[idxLine1,:], k=1)
    _ , idx3 = tree.query(line3Points[idxLine3,:], k=1)
    innerLinePoints, _ =  getGeodesicPath(meshHeartPoints, meshHeartCells, meshHeartPoints[idx1,:], meshHeartPoints[idx3,:])
    innerLinePoints, innerLineEdges = resampleGeodesic(innerLinePoints, thresholdDist=args.poreSide)
    scaffoldPoints = np.concatenate((scaffoldPoints, innerLinePoints[1:-1,:]), axis=0)
    print("innerLine: {}".format(innerLinePoints.shape[0]))
    # break







patchCells = [
    ("line", scaffoldEdges),
]

meshScaffold = meshio.Mesh(scaffoldPoints, patchCells)
meshScaffold.write(args.outPath)