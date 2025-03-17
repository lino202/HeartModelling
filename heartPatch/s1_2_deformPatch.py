"This code project a volumetical or superficial mesh into a surface"
"ATTENTION it was thought to project the patch of an engineered heart tissue so me assume a thin volumetical/superficial mesh where all nodes that are projected"
"need to be selected in a property of the mesh as set_contact and its counterpart non contacting nodes (in the non contacting face) will we projected in the same way"
"high resolution of meshes (in both heart and scaffold) help to make this projection better and obviously it works better when the curvature of the mesh we want "
"to project in, is no so sharp. If this now work you can try to use s1 and s2 codes to use abaqus to perform impose deformation"


import os 
import numpy as np
import argparse
import meshio
from scipy.spatial import KDTree
import sys
sys.path.append(os.path.join(os.path.dirname(sys.path[0])))
from auxiliar.conductionSystem.lib.Mesh import Mesh

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--meshHeart',type=str, required=True, help='path to data mesh in obj')
parser.add_argument('--meshScaffold',type=str, required=True, help='path to data')
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
idxsNoContact = np.where(np.logical_not(np.isin(np.arange(meshScaffold.points.shape[0]), idxsContact)))[0]

tree = KDTree(meshScaffold.points[idxsNoContact])
_ , idxsContact2NoContact = tree.query(meshScaffold.points[idxsContact], k=1)

# Make projection of all points
newPoints = np.zeros(meshScaffold.points.shape)
for i, pointIdx in enumerate(idxsContact):
    projectedPoint, _ = meshHeart.project_new_point(scaffoldPoints[pointIdx])
    newPoints[pointIdx,:] = projectedPoint

    # Now project in the same way the non contact point for this contact point
    vec = projectedPoint - scaffoldPoints[pointIdx]
    pointIdxNonContact = idxsNoContact[idxsContact2NoContact][pointIdx]
    newPoints[pointIdxNonContact,:] = scaffoldPoints[pointIdxNonContact,:] + vec


#SAVE-----------------------------------------------------------------------------------------------------
meshScaffold.points = newPoints
meshScaffold.write(os.path.join(args.outPath, "deformed_scaffold_mesh.vtk"))

