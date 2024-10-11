"""This code follows the projection on MI (affected zone) as described in Garcia-Bustos et al.
Remember to use debug_vtk in cs_projectSubendo_5.py for getting subendo and subendo_intramyo projection with the list of the endbranches projected
in this way this algorhitm can reproject back to subendocardium and re project to intra(mid)myocardium and to epicardium"""

import copy
import os
import random
import meshio
import numpy as np 
import argparse
import time
from scipy.spatial.distance import cdist
from lib.utils import getEdges, getLinearPath, getProjectionDir, getProjectionMag, saveVtkInpMesh1D, updatePointsEdgesBranches, checkRepeatedPoints

def main():
    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument('--data_path',type=str, required=True, help='path to data')
    parser.add_argument('--out_name',type=str, required=True, help='output file name')
    parser.add_argument('--cs_name',type=str, required=True, help='Name of the cs subfolder withe final data for cs construction')
    parser.add_argument('--endo_per',type=int, required=True, help='endo percentage')
    parser.add_argument('--epi_per',type=int, required=True, help='epi percentage')
    parser.add_argument('--meanMag',type=int, required=True, help='number of nodes to average for magnitud of the projection')
    parser.add_argument('--meanNor',type=int, required=True, help='number of nodes to average for normal direction of the projection')
    parser.add_argument('--intramyo_percentage',type=int, help='percentage of endpoints to project to intramyo')
    parser.add_argument('--epi_percentage',type=int, help='percentage of endpoints to project to epi')
    parser.add_argument('--pmjs_reduction_percentage',type=int, help='percentage of PMJs reduction')
    parser.add_argument('--proj_linear', action='store_true', help='if especified, linear projection into intramid otherwise folows the already curved branch')
    args = parser.parse_args()

    #Inputs
    lvSurfMesh         = meshio.read(os.path.join(args.data_path, "mesh", "lv_endo.obj"))  #normals corrected
    rvSurfMesh         = meshio.read(os.path.join(args.data_path, "mesh", "rv_endo.obj"))
    csSubEndoMesh      = meshio.read(os.path.join(args.data_path, "stim", "cs", args.cs_name, "cs_subendo.inp"))
    csSubEndoIntraMesh = meshio.read(os.path.join(args.data_path, "stim", "cs", args.cs_name, "cs_subendo_intramyo.inp"))
    mesh               = meshio.read(os.path.join(args.data_path, "mesh_mi.vtk"))
    laplaciansMesh     = meshio.read(os.path.join(args.data_path, "layers", "laplacians.vtk"))
    outPath            = os.path.join(args.data_path, "stim", "cs", args.cs_name)
    outName            = args.out_name


    points = csSubEndoIntraMesh.points
    edges = csSubEndoIntraMesh.cells_dict["line"]
    nsets = copy.deepcopy(csSubEndoIntraMesh.point_sets)

    #Perrotti definitions, must be consistent with the ones used
    endoPer = args.endo_per / 100
    epiPer = args.epi_per / 100
    phi0 = -1
    phi1 = 1
    phiEndo = (1-endoPer) * phi0 + endoPer * phi1    # thresholds
    phiEpi = epiPer * phi0 + (1-epiPer) * phi1
    #Windows
    intramyoWindow = [phiEndo , phiEpi] # we use the whole mid-myocardium as intramyocardium due to taking only the mid-myocardium middle third could give few points and bad projection if mesh resolution is too poor
    epiWindow = [phiEpi , phi1]

    # Tissue flags
    scar_flag = 8
    bz_flag = 7

    # ------------------------- Project EndBranches in Affected Zone as SubEndo again -------------------------------------------------
    endNodes = nsets["purk_endnodes"]
    dists = cdist(points[endNodes,:], mesh.points, 'euclidean')
    nearEndNodesIdxs = np.argmin(dists, axis=1)
    del dists
    # Get the scar and bz, so affected zone nodes
    scarNodes = np.where((mesh.point_data["layers"]==bz_flag) | (mesh.point_data["layers"]==scar_flag))[0]
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
        mags = getProjectionMag(endNodePoint, laplaciansMesh, intramyoWindow, "lv" if "lv" in branchName else "rv", k=args.meanMag)
        
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
    scarEndBranches2Endo = [endBranch for endBranch in scarEndBranches if not endBranch in scarEndBranches2Epi] 

    for branchName in scarEndBranches2Epi:


        branchPoints = sorted(list(nsets[branchName]))
        endNodePoint = np.expand_dims(points[max(branchPoints),:], axis=0)

        dirs = getProjectionDir(endNodePoint, lvSurfMesh if "lv" in branchName else rvSurfMesh, k=args.meanNor)
        mags = getProjectionMag(endNodePoint, laplaciansMesh, epiWindow, "lv" if "lv" in branchName else "rv", k=args.meanMag)
        
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

    # # ----------------------Reduce PMJs in affected Zone--------------------------------------------
    # We know the branches that are in the affected zone and in which region they are projected and the nodes indexes from them
    # this info can be recovered from scarEndBranches2Epi, scarEndBranches2Mid, scarEndBranches2Endo and nsets.
    # Then we basically delete from nsets["purk_endnodes"] the 50% of endo, mid and epi branches endpoint indexes
    # Note deleting the endbranches is not that easy as two enbranches deletion might lead to a new endbranch that we need to furterly delete
    print("-----------Reduce PMJs in affected Zone------------")
    nsets["purk_endnodes_old"] = copy.deepcopy(nsets["purk_endnodes"])
    purk_endpoints = copy.deepcopy(nsets["purk_endnodes"])
    scarEpiEndBranchesToDelete = random.sample(scarEndBranches2Epi, int(len(scarEndBranches2Epi)*(args.pmjs_reduction_percentage/100)))
    for endBranch in scarEpiEndBranchesToDelete:
        nodeIdxs = nsets[endBranch+"_epi"]
        idxToDelete = np.isin(purk_endpoints, nodeIdxs).nonzero()[0]
        if idxToDelete.size!=1: raise ValueError("You should not see this error")
        purk_endpoints = np.delete(purk_endpoints, idxToDelete)

    scarMidEndBranchesToDelete = random.sample(scarEndBranches2Mid, int(len(scarEndBranches2Mid)*(args.pmjs_reduction_percentage/100)))
    for endBranch in scarMidEndBranchesToDelete:
        nodeIdxs = nsets[endBranch+"_intramyo"]
        idxToDelete = np.isin(purk_endpoints, nodeIdxs).nonzero()[0]
        if idxToDelete.size!=1: raise ValueError("You should not see this error")
        purk_endpoints = np.delete(purk_endpoints, idxToDelete)

    scarEndoEndBranchesToDelete = random.sample(scarEndBranches2Endo, int(len(scarEndBranches2Endo)*(args.pmjs_reduction_percentage/100)))
    for endBranch in scarEndoEndBranchesToDelete:
        nodeIdxs = nsets[endBranch]
        idxToDelete = np.isin(purk_endpoints, nodeIdxs).nonzero()[0]
        if idxToDelete.size!=1: raise ValueError("You should not see this error")
        purk_endpoints = np.delete(purk_endpoints, idxToDelete)

    nsets["purk_endnodes"] = purk_endpoints
    checkRepeatedPoints(points)

    # Save
    print("-----------Saving------------")
    saveVtkInpMesh1D(points, edges, nsets, outPath, outName)



if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))