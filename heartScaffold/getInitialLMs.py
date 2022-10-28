import os 
import numpy as np
import argparse
import meshio
from scipy.spatial.distance import cdist
import sys
sys.path.append(os.path.join(os.path.dirname(sys.path[0])))
from auxiliar.conductionSystem.lib.Mesh import Mesh
from auxiliar.conductionSystem.lib.utils import getEdges

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--meshHeart',type=str, required=True, help='path to data mesh in obj')
parser.add_argument('--meshScaffold',type=str, required=True, help='path to data')
# parser.add_argument('--transformation',type=str, help='Transformation for the Scaffold if neccesary')
parser.add_argument('--radious',type=float, required=True, help='percentage of LMs on scaffold')
parser.add_argument('--outPath',type=str, required=True, help='path to data')
args = parser.parse_args()

meshHeart = Mesh(args.meshHeart)
heartPoints = meshHeart.verts
meshScaffold = meshio.read(args.meshScaffold)
scaffoldPoints = meshScaffold.points
scaffoldName = args.meshScaffold.split("/")[-1].split(".")[0]
heartName = args.meshHeart.split("/")[-1].split(".")[0]

# GET LANDMARKS FOR SCAFFOLD-----------------------------------------------------------------------------------------------------
#Get uniformly distributed LMs on Scaffold and contact set
idxsContact = np.where(meshScaffold.point_data["set_contact"]==1)[0]
contactPoints = scaffoldPoints[idxsContact]

nearPoints = np.array([]).astype(int)
idxsLMs = np.array([]).astype(int)   #This is equal because nodes in the contact are the first nodes to be added so idexes correspond
for i, point in enumerate(contactPoints):
    if not i in nearPoints:
        idxsLMs = np.append(idxsLMs, i)
        distances = cdist(np.expand_dims(point, axis=0), contactPoints).flatten()
        localNearPoints = np.where((distances>0) & (distances<args.radious))[0]
        nearPoints = np.concatenate((nearPoints, localNearPoints))
        nearPoints = np.unique(nearPoints)

if "set_lm_corner_1" in meshScaffold.point_data.keys():
    for key in meshScaffold.point_data.keys():
        if "set_lm_corner" in key:
            idxsLMs = np.append(idxsLMs, np.where(meshScaffold.point_data[key]==1)[0])
    idxsLMs = np.unique(idxsLMs)

nsetsScaffold = {}
nsetsScaffold["set_contact"] = idxsContact
nsetsScaffold["set_all_lms"] = idxsLMs

for i, lm in enumerate(idxsLMs):
    nsetsScaffold["set_lm_{}".format(i)] = lm

# #ROTATE ------------------------------------------------------
# if args.transformation:
#     transform = np.loadtxt(args.transformation) 
#     scaffoldPoints = np.concatenate((scaffoldPoints, np.ones((scaffoldPoints.shape[0],1))), axis=1)
#     scaffoldPoints = np.matmul(scaffoldPoints, transform) 
#     meshScaffold.points = scaffoldPoints[:,:3]


# GET LANDMARKS FOR HEART-----------------------------------------------------------------------------------------------------

# # Get the most neart point in heart for LMs
# dists = cdist(scaffoldPoints[idxsLMs,:], heartPoints)
# heartLMs = np.argmin(dists, axis=1)
# if np.count_nonzero(np.unique(heartLMs, return_counts=True)[1]-1) > 0:
#     print("There are repeated LMs in the heart associated with one in the scaffold")
# else:
#     print("No repeated LMs in the heart")
# nsetsHeart = {}
# nsetsHeart["set_all_lms"] = heartLMs
# for i, lm in enumerate(heartLMs):
#     nsetsHeart["set_lm_{}".format(i)] = lm

#Get projection into heartMesh of points in contact
heartPoints = np.array([])
nsetsHeart = {}
for i, pointIdx in enumerate(nsetsScaffold["set_all_lms"]):
    projectedPoint, _ = meshHeart.project_new_point(scaffoldPoints[pointIdx])
    nsetsHeart["set_lm_{}".format(i)] = i
    projectedPoint = np.expand_dims(projectedPoint,axis=0)
    heartPoints = np.concatenate((heartPoints, projectedPoint), axis=0) if heartPoints.size else projectedPoint


#SAVE-----------------------------------------------------------------------------------------------------
#Heart
point_data_Heart={}
for key in nsetsHeart.keys():
    tmp = np.zeros(heartPoints.shape[0])
    tmp[nsetsHeart[key]] = 1
    point_data_Heart[key] = tmp

edges = getEdges(heartPoints)
heartCells = [("line", edges)]
meshHeartOut = meshio.Mesh(heartPoints, heartCells, point_data = point_data_Heart)
meshHeartOut.write(os.path.join(args.outPath, "{}_lms.vtk".format(heartName)))

#Scaffold
point_data_Scaffold={}
for key in nsetsScaffold.keys():
    tmp = np.zeros(scaffoldPoints.shape[0])
    tmp[nsetsScaffold[key]] = 1
    point_data_Scaffold[key] = tmp

meshScaffold.point_data = point_data_Scaffold
meshScaffold.write(os.path.join(args.outPath, "scaffolds", "{}_lms.vtk".format(scaffoldName)))

# #Write Landmarks for tweking in Slicer
# with open(os.path.join(args.outPath, "scaffold_lms.fcsv"), 'w') as f:
#     f.write("# Markups fiducial file version = 5.0\n")
#     f.write("# CoordinateSystem = LPS\n")
#     f.write("# columns = id,x,y,z,ow,ox,oy,oz,vis,sel,lock,label,desc,associatedNodeID\n")

#     for i, lm in enumerate(idxsLMs):
#         f.write("{0},{1},{2},{3},".format(i, scaffoldPoints[lm,0], scaffoldPoints[lm,1], scaffoldPoints[lm,2]))
#         f.write("0,0,0,1,1,1,0,")
#         f.write("{0},,,2,0\n".format("set_lm_{}".format(i)))

# with open(os.path.join(args.outPath, "heart_lms.fcsv"), 'w') as f:
#     f.write("# Markups fiducial file version = 5.0\n")
#     f.write("# CoordinateSystem = LPS\n")
#     f.write("# columns = id,x,y,z,ow,ox,oy,oz,vis,sel,lock,label,desc,associatedNodeID\n")

#     for i, lm in enumerate(heartLMs):
#         f.write("{0},{1},{2},{3},".format(i, heartPoints[lm,0], heartPoints[lm,1], heartPoints[lm,2]))
#         f.write("0,0,0,1,1,1,0,")
#         f.write("{0},,,2,0\n".format("set_lm_{}".format(i)))


# meshOut = meshio.Mesh(points, mesh.cells, point_sets=nsets)
# meshOut.write(os.path.join(path, "{}_lms.inp".format(name)))