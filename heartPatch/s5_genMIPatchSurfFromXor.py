'''Once you have the xor and previously or not of the cleanning of the triangles of the interface we erase the tris in the inner of the heart
that were part of the patch.

For this we need a surf_xor.ply mesh where the faces of the patch were added with a color in meshlab previous the xor 
So we add both meshes in meshlab and add to the mesh scaffold a color with Filters -> Color Creation -> Per Face Color Function and select a RED patch,
Then we apply the xor an set the transfer face color to true and save this xor mesh as .ply

Also there when saving the .ply we need to uncheck byte encoding (and check color of course!) as it gives an error when reading with meshio.

Moreover, the meshHeart and meshPatch should be the exact mesh of the xor without the patch or the heart, respectively. You can obtain this from the xor mesh
using  on meshlab Filters -> Selection -> Conditional Face Selection and putting fr == 255 for the patch and deleting all vertexs and faces. Then you can recompute the normals
with Filters -> Normals .. -> Recompute normals coherently and when the shades of the heart/patch meshes are correct you export them and it is done :P'''


import os 
import numpy as np
import argparse
import meshio
from utils import getPointsEnclosedByMesh, delElemsFromMesh

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--meshXor',type=str, required=True, help='path to data mesh in ply with color red on the patch faces')
parser.add_argument('--meshHeart',type=str, required=True, help='this is the EXACT SAME epi mesh of the xor WITHOUT the patch (normals must be ok)')
parser.add_argument('--meshPatch',type=str, required=True, help='this is the EXACT SAME patch mesh of the xor WITHOUT the heart/epi (normals must be ok)')
parser.add_argument('--outPath',type=str, required=True, help='path to output file')
args = parser.parse_args()

flags = {"innerPatch": 0, "outerPatch": 1, "innerHeart": 2, "outerHeart": 3}

meshXor = meshio.read(args.meshXor)
meshHeart = meshio.read(args.meshHeart)
meshPatch = meshio.read(args.meshPatch)

xorCellCentroids = np.mean(meshXor.points[meshXor.cells_dict["triangle"]], axis=1)
idxFacePatch = np.where(meshXor.cell_data["red"][0]==255)[0]
idxFaceHeart = np.where(meshXor.cell_data["red"][0]!=255)[0]
xorHeartCentroids = xorCellCentroids[idxFaceHeart,:]
xorPatchCentroids = xorCellCentroids[idxFacePatch,:]

#Get innerPatch and get innerHeart
idxs = getPointsEnclosedByMesh(xorPatchCentroids, meshHeart)
innerPatch = idxFacePatch[idxs]
outerPatch = idxFacePatch[(~np.isin(idxFacePatch, innerPatch)).nonzero()[0]]
idxs = getPointsEnclosedByMesh(xorHeartCentroids, meshPatch)
innerHeart = idxFaceHeart[idxs]
outerHeart = idxFaceHeart[(~np.isin(idxFaceHeart, innerHeart)).nonzero()[0]]

if innerPatch.shape[0] + outerPatch.shape[0] + innerHeart.shape[0] + outerHeart.shape[0] != xorCellCentroids.shape[0]:
    raise ValueError("Wrong cell clustering in Xor ")
cellsXorFamily = np.zeros(xorCellCentroids.shape[0])
cellsXorFamily[outerPatch] = flags["outerPatch"]
cellsXorFamily[innerHeart] = flags["innerHeart"]
cellsXorFamily[outerHeart] = flags["outerHeart"]
meshXor.cell_data = {"cellsXor": [cellsXorFamily]}
meshXor.write(os.path.join(args.outPath, "controlXorClustering.vtk"))

#del inner Patch from mesh
meshWithoutInnerPatch = delElemsFromMesh(meshXor, innerPatch)
meshWithoutInnerPatch.write(os.path.join(args.outPath, "final_mipatch_surfmesh.obj"))
# meshWithoutInnerPatch.write(os.path.join(args.outPath, "final_mipatch_surfmesh.vtk"))

#Create a new scaffold mesh to use surfseeds in Matlab
outerHeart = (meshWithoutInnerPatch.cell_data["cellsXor"][0]==flags["outerHeart"]).nonzero()[0]
meshFinalScaffold = delElemsFromMesh(meshWithoutInnerPatch, outerHeart)
meshFinalScaffold.write(os.path.join(args.outPath, "final_shell.obj"))
# meshFinalScaffold.write(os.path.join(args.outPath, "final_shell.vtk"))
