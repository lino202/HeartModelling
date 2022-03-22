import copy
import os
import random
import meshio
import numpy as np 
import argparse
from scipy.spatial.distance import cdist, pdist
from lib.utils import getEdges, getLinearPath, getProjectionDir, getProjectionMag, saveVtkInpMesh1D, updatePointsEdgesBranches


parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--data_path',type=str, required=True, help='path to data')
parser.add_argument('--out_name',type=str, required=True, help='output file name')
parser.add_argument('--mesh_name',type=str, required=True, help='mesh with scar name')
parser.add_argument('--endo_per',type=int, required=True, help='endo percentage')
parser.add_argument('--epi_per',type=int, required=True, help='epi percentage')
parser.add_argument('--meanMag',type=int, required=True, help='number of nodes to average for magnitud of the projection')
parser.add_argument('--meanNor',type=int, required=True, help='number of nodes to average for normal direction of the projection')
parser.add_argument('--intramyo_window',type=int, required=True, help='intramyo window is the middle width transmural wall in which purk endnodes are going to be projected')
parser.add_argument('--intramyo_percentage',type=int, help='percentage of endpoints to project to intramyo')
# parser.add_argument('--epi_window',type=int, required=True, help='epi window is the proximal width transmural wall in which purk endnodes are going to be projected')
parser.add_argument('--epi_percentage',type=int, help='percentage of endpoints to project to epi')
parser.add_argument('--proj_linear', action='store_true', help='if especified, linear projection into intramid otherwise folows the already curved branch')
args = parser.parse_args()

#Inputs
lvSurfMesh = meshio.read(os.path.join(args.data_path, "stim", "stim_cs", "lv_endo.obj"))  #normals corrected
rvSurfMesh = meshio.read(os.path.join(args.data_path, "stim", "stim_cs", "rv_endo.obj"))
csSubEndoMesh = meshio.read(os.path.join(args.data_path, "stim", "stim_cs", "cs_subendo.inp"))
csSubEndoIntraMesh = meshio.read(os.path.join(args.data_path, "stim", "stim_cs", "cs_subendo_intramyo.inp"))
mesh = meshio.read(os.path.join(args.data_path, "layers", "{}.inp".format(args.mesh_name)))
transDistRV = meshio.read(os.path.join(args.data_path, "layers", "transmural_distRV000000.vtu"))
transDistLV = meshio.read(os.path.join(args.data_path, "layers", "transmural_distLV000000.vtu"))
outPath = os.path.join(args.data_path, "stim", "stim_cs")
outName = args.out_name


points = csSubEndoIntraMesh.points
edges = csSubEndoIntraMesh.cells[0][1]
nsets = copy.deepcopy(csSubEndoIntraMesh.point_sets)

#Perrotti definitions, must be consistent with the ones used
endoPer = args.endo_per / 100
epiPer = args.epi_per / 100
phi0 = -1
phi1 = 1
phiEndo = (1-endoPer) * phi0 + endoPer * phi1    # thresholds
phiEpi = epiPer * phi0 + (1-epiPer) * phi1
intramyoWindow = [phiEndo + (abs(phiEndo - phiEpi) / args.intramyo_window)  , phiEndo + 2*(abs(phiEndo - phiEpi) / args.intramyo_window)]
# epiWindow = [phiEpi , phiEpi + (abs(phi1 - phiEpi) / args.epi_window)]
epiWindow = [phiEpi , phi1]

# ------------------------- Project EndBranches in Scar as SubEndo again -------------------------------------------------
endNodes = nsets["purk_endnodes"]
dists = cdist(points[endNodes,:], mesh.points, 'euclidean')
nearEndNodesIdxs = np.argmin(dists, axis=1)
scarNodes = mesh.point_sets["scar_nodes"]
scarEndNodes = np.array([])
for i,idx in enumerate(nearEndNodesIdxs):
    if idx in scarNodes:
        scarEndNodes = np.concatenate((scarEndNodes, np.array([endNodes[i]]))) if scarEndNodes.size else np.array([endNodes[i]])

scarEndBranches = []
endBranches = [key for key in nsets.keys() if "endBranch" in key]

for endIdx in scarEndNodes:
    for endBranch in endBranches:
        if endIdx in csSubEndoIntraMesh.point_sets[endBranch]:
            if "intramyo" in endBranch:
                subEndoPointsIdxs = csSubEndoMesh.point_sets[endBranch.split("_intramyo")[0]]
                tmpIdxs= nsets[endBranch]
                del nsets[endBranch]
                nsets[endBranch.split("_intramyo")[0]] = tmpIdxs
                scarEndBranches.append(endBranch.split("_intramyo")[0])
                points[tmpIdxs,:] = csSubEndoMesh.points[np.sort(subEndoPointsIdxs),:]
            else:
                scarEndBranches.append(endBranch)



# ---------------------------------------Project Intramyo--------------------------------------------

print("-----------Making projection into mid-myocardium of End Branches------------")
tmpPurkBranches = {}  
totBranches = len(scarEndBranches)
scarEndBranches2Mid = random.sample(scarEndBranches, int(totBranches*(args.intramyo_percentage/100)))

for branchName in scarEndBranches2Mid:


    branchPoints = sorted(list(nsets[branchName]))
    endNodePoint = np.expand_dims(points[max(branchPoints),:], axis=0)

    dirs = getProjectionDir(endNodePoint, lvSurfMesh if "lv" in branchName else rvSurfMesh, k=args.meanNor)
    mags = getProjectionMag(endNodePoint, transDistLV if "lv" in branchName else transDistRV, intramyoWindow, k=args.meanMag)
    
    #Reference de joint, create projection and update Points and Edges
    jointNodeIdx = min(branchPoints)
    #Linear
    if args.proj_linear:
        newBranchPoints, newBranchEdges = getLinearPath(points[jointNodeIdx,:], np.squeeze(endNodePoint + dirs * mags), step=0.6)
    else:
        mags = np.linspace(0,mags, len(branchPoints))
        mags = np.repeat(mags, repeats=3, axis=1)
        newBranchPoints = points[branchPoints,:] + dirs * mags
        newBranchEdges = getEdges(newBranchPoints)

    branchPoints.remove(jointNodeIdx)
    points, edges, nsets, _ = updatePointsEdgesBranches(points, edges, nsets, {}, branchPoints)
    
    #Add new edges and points
    newBranchEdges = newBranchEdges + points.shape[0] - 1
    newBranchEdges[np.where(newBranchEdges == points.shape[0] - 1)] = jointNodeIdx
    
    newBranchIndex = sorted(list(np.unique(newBranchEdges.flatten())))

    del nsets[branchName]
    nsets[branchName+ "_intramyo"] = newBranchIndex
    nsets["{}_purk".format(branchName.split("_")[0])] = np.concatenate((nsets["{}_purk".format(branchName.split("_")[0])] , newBranchIndex[1:]))

    edges = np.concatenate((edges, newBranchEdges), axis=0)
    points = np.concatenate((points, newBranchPoints[1:]), axis=0)
        
uniqueEdges, count = np.unique(edges, return_counts=True)   
uniqueEdges = uniqueEdges[count==1]
#TODO calculate branch specific endpoints using the dict branches and the enpoints values
nsets["purk_endnodes"] = uniqueEdges[uniqueEdges!=nsets["av_node"]] 


# ---------------------------------------Project Epi--------------------------------------------

print("-----------Making projection into epicardium of End Branches------------")

scarEndBranches = [endBranch for endBranch in scarEndBranches if not endBranch in scarEndBranches2Mid]
scarEndBranches2Epi = random.sample(scarEndBranches, int(totBranches*(args.epi_percentage/100)))

for branchName in scarEndBranches2Epi:


    branchPoints = sorted(list(nsets[branchName]))
    endNodePoint = np.expand_dims(points[max(branchPoints),:], axis=0)

    dirs = getProjectionDir(endNodePoint, lvSurfMesh if "lv" in branchName else rvSurfMesh, k=args.meanNor)
    mags = getProjectionMag(endNodePoint, transDistLV if "lv" in branchName else transDistRV, epiWindow, k=args.meanMag)
    
    #Reference de joint, create projection and update Points and Edges
    jointNodeIdx = min(branchPoints)
    #Linear
    if args.proj_linear:
        newBranchPoints, newBranchEdges = getLinearPath(points[jointNodeIdx,:], np.squeeze(endNodePoint + dirs * mags), step=0.6)
    else:
        mags = np.linspace(0,mags, len(branchPoints))
        mags = np.repeat(mags, repeats=3, axis=1)
        newBranchPoints = points[branchPoints,:] + dirs * mags
        newBranchEdges = getEdges(newBranchPoints)

    branchPoints.remove(jointNodeIdx)
    points, edges, nsets, _ = updatePointsEdgesBranches(points, edges, nsets, {}, branchPoints)
    
    #Add new edges and points
    newBranchEdges = newBranchEdges + points.shape[0] - 1
    newBranchEdges[np.where(newBranchEdges == points.shape[0] - 1)] = jointNodeIdx
    
    newBranchIndex = sorted(list(np.unique(newBranchEdges.flatten())))

    del nsets[branchName]
    nsets[branchName+ "_epi"] = newBranchIndex
    nsets["{}_purk".format(branchName.split("_")[0])] = np.concatenate((nsets["{}_purk".format(branchName.split("_")[0])] , newBranchIndex[1:]))

    edges = np.concatenate((edges, newBranchEdges), axis=0)
    points = np.concatenate((points, newBranchPoints[1:]), axis=0)
        
uniqueEdges, count = np.unique(edges, return_counts=True)   
uniqueEdges = uniqueEdges[count==1]
#TODO calculate branch specific endpoints using the dict branches and the enpoints values
nsets["purk_endnodes"] = uniqueEdges[uniqueEdges!=nsets["av_node"]] 


# Save
print("-----------Saving------------")
saveVtkInpMesh1D(points, edges, nsets, outPath, outName)
