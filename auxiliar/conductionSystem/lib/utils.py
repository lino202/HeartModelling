import math
import numpy as np
import pygeodesic.geodesic as geodesic
from scipy.spatial.distance import cdist, pdist
from scipy.interpolate import interp1d
import itertools
import copy
import meshio
import os
import pandas as pd

def getLinearPath(sourcePoint, targetPoint, step = 1):
    if type(sourcePoint) != np.ndarray: sourcePoint = np.array(sourcePoint)
    if type(targetPoint) != np.ndarray: targetPoint = np.array(targetPoint)

    normPoints = np.linalg.norm(sourcePoint-targetPoint)
    points = np.linspace(sourcePoint, targetPoint, int(np.round(normPoints/step)))
    edges = getEdges(points)

    return points, edges


def getGeodesicPath(meshPoints, meshFaces, sourcePoint, targetPoint):
    
    if type(sourcePoint) != np.ndarray:
        sourcePoint = np.array([sourcePoint])
    if type(targetPoint) != np.ndarray:
        targetPoint = np.array([targetPoint])
    
    geoalg = geodesic.PyGeodesicAlgorithmExact(meshPoints, meshFaces)
    sourceIndex = isMemberIdxsRowWise(sourcePoint, meshPoints, tol=0.001)
    targetIndex = isMemberIdxsRowWise(targetPoint, meshPoints, tol=0.001)
    if sourceIndex.size != 1 or targetIndex.size != 1: raise ValueError("More than one point indentified, tweak tol") 

    _, points = geoalg.geodesicDistance(targetIndex, sourceIndex)
    edges =  getEdges(points)
    return points, edges


def getEdges(points):
    edges = np.array([])
    for nodeIdx in range(points.shape[0]-1):
        newEdge = np.array([[nodeIdx, nodeIdx+1]])
        edges = np.concatenate((edges, newEdge), axis=0) if edges.size else newEdge
    return edges


def isMemberIdxsRowWise(arr1, arr2, tol = 1E-6):
    idxs = np.where((abs(arr1-arr2[:,None]) <= tol).all(2))
    return idxs[0]

            
def getPointsInSphere(points, center, radius=2):
    center = np.tile(center, (points.shape[0], 1))
    dist = np.linalg.norm(center-points, axis=1)
    return np.where(dist<radius)[0]


def getProjectionDir(nodes, mesh, k=5):
    dist = cdist(nodes, mesh.points, 'euclidean')
    normals = mesh.point_data['obj:vn']
    if k>1:
        sortedIdxs = np.argsort(dist, axis=1)
        sortedIdxs = sortedIdxs[:,:k]
        meanNormals = np.array([])
        for i in range(sortedIdxs.shape[0]):
            currentNormal = np.mean(normals[sortedIdxs[i,:]], axis=0)
            # currentNormal = currentNormal/np.linalg.norm(currentNormal)
            meanNormals = np.concatenate((meanNormals, np.expand_dims(currentNormal, axis=0)), axis=0) if meanNormals.size else np.expand_dims(currentNormal, axis=0)
        return -1 * meanNormals
    else:
        nearSurfaceNodes = np.argmin(dist, axis=1)
        return -1 * normals[nearSurfaceNodes,:]


def getProjectionMag(nodes, mesh, subendoWindow, k=1):
    subendoNodesIdxs = np.where((mesh.point_data['f_20']>subendoWindow[0]) & (mesh.point_data['f_20']<subendoWindow[1]))[0]
    dist = cdist(nodes, mesh.points[subendoNodesIdxs,:], 'euclidean')
    if k>1:
        sortedIdxs = np.argsort(dist, axis=1)
        sortedIdxs = sortedIdxs[:,:k]
        meanMag = np.array([])
        for i in range(sortedIdxs.shape[0]):
            currentMag = np.mean(dist[i,sortedIdxs[i,:]], axis=0)
            meanMag = np.concatenate((meanMag, np.expand_dims(currentMag, axis=0)), axis=0) if meanMag.size else np.expand_dims(currentMag, axis=0)
        return meanMag
    else:
        return np.min(dist, axis=1)


def checkRepeatedPoints(points):
    _, counts = np.unique(points, axis=0, return_counts=True)
    if np.any(counts!=1): raise ValueError("Repeated points in mesh points")

def resampleGeodesic(points, thresholdDist=0.7):
    #Interpolate in every axis
    x = np.arange(0,points.shape[0]-1,thresholdDist)
    newPoints = np.array([])
    for i in range(points.shape[1]):
        lin = interp1d(np.arange(0,points.shape[0]), points[:,i])
        y = lin(x)
        y = np.expand_dims(y, axis=1)
        newPoints = np.concatenate((newPoints, y), axis=1) if newPoints.size else y 

    #resample with thresholdDist
    dist = pdist(newPoints)
    idxsThDist = np.where(dist>thresholdDist)
    resampledPoints = np.array([newPoints[0,:]])
    mapDistIdxs = np.array(list(itertools.combinations(range(newPoints.shape[0]),2)))
    relations = mapDistIdxs[idxsThDist]
    pointAIdx=0
    while True:
        idxArrPointA = np.where(relations[:,0]==pointAIdx)[0]
        if idxArrPointA.size <= 0: break
        pointBIdx = relations[idxArrPointA[0],1]
        resampledPoints = np.concatenate((resampledPoints, np.expand_dims(newPoints[pointBIdx,:], axis=0)), axis=0)
        pointAIdx = pointBIdx
    edges = getEdges(resampledPoints)
    return resampledPoints, edges


def smoothProjection(points,edges, angleTheshold=10):
    
    # Get idxs of edges that correspond to nodes connected 2 or 3 times (exclude extremes)
    idxs2Evaluate, count = np.unique(edges.flatten(), return_counts=True)
    idxs2Evaluate = idxs2Evaluate[count!=1]
    if np.any(count>3): raise ValueError("A node cannot have other than 2 or 3 connections")

    #Avoid the first one as it is part of the other branch
    for i in range(1,idxs2Evaluate.shape[0]):
        edges2Evaluate = np.where(edges==idxs2Evaluate[i])[0]
        if edges2Evaluate.shape[0] == 2:
            uEdges = edges[edges2Evaluate[0],:]
            vEdges = edges[edges2Evaluate[1],:]
            nodes2Evaluate = np.concatenate((uEdges,vEdges))
            nodeIdx = np.max(nodes2Evaluate)
            points[nodeIdx,:] = smoothCurve3Points(points, nodeIdx, uEdges, vEdges, angleTheshold)
        elif edges2Evaluate.shape[0] == 3:
            #first curve
            uEdges = edges[edges2Evaluate[0],:]
            vEdges = edges[edges2Evaluate[1],:]
            nodes2Evaluate = np.concatenate((uEdges,vEdges))
            nodeIdx = np.max(nodes2Evaluate)
            points[nodeIdx,:] = smoothCurve3Points(points, nodeIdx, uEdges, vEdges, angleTheshold)
            #second curve
            uEdges = edges[edges2Evaluate[0],:]
            vEdges = edges[edges2Evaluate[2],:]
            nodes2Evaluate = np.concatenate((uEdges,vEdges))
            nodeIdx = np.max(nodes2Evaluate)
            points[nodeIdx,:] = smoothCurve3Points(points, nodeIdx, uEdges, vEdges, angleTheshold)
        else: raise ValueError("This should never happen")

    return points
        

def smoothCurve3Points(points, nodeIdx, uEdges, vEdges, angleThreshold):
    u = points[uEdges[1],:] - points[uEdges[0],:]
    v = points[vEdges[1],:] - points[vEdges[0],:]
    theta = math.degrees(math.acos(np.dot(u,v)/(np.linalg.norm(u)*np.linalg.norm(v))))

    if theta > angleThreshold and theta < 90:
        # We need to define a vector projection, direction must be perpedicular to u for moving v towards u
        uxv = np.cross(u,v)
        direction = np.cross(u,uxv)
        direction = direction / np.linalg.norm(direction)
        #magnitude
        mag = np.linalg.norm(v) * math.sin(np.radians(theta-angleThreshold))
        return  points[nodeIdx,:] + direction * mag
    elif theta > 90:
        # We need to define a vector projection, direction must be perpedicular to u for moving v towards u
        points[nodeIdx,:] = points[nodeIdx,:] - 2*v 
        uxv = np.cross(u,-v)
        direction = np.cross(u,uxv)
        direction = direction / np.linalg.norm(direction)
        #magnitude
        mag = np.linalg.norm(v) * math.sin(np.radians(180 - theta))
        return  points[nodeIdx,:] + direction * mag
    else:
        return points[nodeIdx,:]


def removeNearNodesPurk(points, edges, thresholdDist=0.3):
    newPoints = np.array([points[0,:]])
    newEdges = np.array([])
    #TODO better separate in branches
    return newPoints, newEdges


def getBranches(edges, endpointRef, purkBranch):
    #We have triple, double joints and the endpoints
    #the first node, idx=0, should be the init point of the purk tree
    edgesUnique, count = np.unique(edges, return_counts=True)
    assert((np.max(count)==3 and np.min(count)==1))
    assert(np.any(edgesUnique[count==2]==endpointRef))
    edgesOri = copy.deepcopy(edges)
    nBranches = 0 
    branches = {}
    flag = True
    while edges.size != 0:
        edgesUnique, count = np.unique(edges, return_counts=True)
        endIdxs = edgesUnique[count==1]
        edgesUnique, count = np.unique(edgesOri, return_counts=True)
        tripleJoint = edgesUnique[count==3]

        #we need to forget originalTriplejoints that now are ends
        forgetIdxs = np.in1d(tripleJoint, endIdxs)
        tripleJoint = tripleJoint[forgetIdxs==False]
        
        for pointIdx in endIdxs:
            nodesInBranch = [pointIdx]
            while not pointIdx in tripleJoint and pointIdx != endpointRef:
                edgeIdx = np.where(edges==pointIdx)[0]
                assert(edgeIdx.size==1) 
                pointIdx = edges[edgeIdx,0]
                edges = np.delete(edges, edgeIdx, axis=0)
                nodesInBranch.extend(pointIdx)

            if flag: 
                branches["{}_endBranch_{}".format(purkBranch,nBranches)] = nodesInBranch
            else:
                branches["{}_branch_{}".format(purkBranch,nBranches)] = nodesInBranch
            nBranches += 1
    
        flag = False

    return branches

def reorderPurkMesh(points, edges):
    newPoints = np.array([])
    newEdges = np.array([]).astype(int)
    unique, count = np.unique(edges, return_counts=True)
    endpoints = unique[count==1]
    joints = unique[count==3]
    mapJoints = np.expand_dims(np.array([0,0]), axis=0)
    idxPointA = 0 #firs not in purk must be the one initiating the purk fractal algo
    newPoints = np.expand_dims(points[idxPointA,:], axis=0)
    while edges.size:   
        connectionIdx = np.where(edges[:,0]==idxPointA)[0]
        if not connectionIdx.size: 
            unique, count = np.unique(edges, return_counts=True)
            updatedEndpoints = unique[count==1]
            idx = np.logical_not(np.isin(updatedEndpoints, endpoints)).nonzero()[0][0]
            idxPointA = updatedEndpoints[idx]
            connectionIdx = np.where(edges[:,0]==idxPointA)[0]


        assert(connectionIdx[0].size==1)
        idxPointB = edges[connectionIdx[0], 1]  #first connection
        newPoint = np.expand_dims(points[idxPointB,:], axis=0)
        newPoints = np.concatenate((newPoints, newPoint), axis=0)


        if np.any(np.isin(idxPointB, joints)): 
            newMapJoint = np.expand_dims(np.array([idxPointB, newPoints.shape[0]-1]), axis=0)
            mapJoints = np.concatenate((mapJoints, newMapJoint),axis=0) if mapJoints.size else newMapJoint
        
        if np.where(mapJoints[:,0]==idxPointA)[0].size:
            row = np.where(mapJoints[:,0]==idxPointA)[0]
            assert(row.size==1)
            newEdge = np.expand_dims(np.array([mapJoints[row,1][0], newPoints.shape[0]-1]), axis=0) 
        else:
            newEdge = np.expand_dims(np.array([newPoints.shape[0]-2, newPoints.shape[0]-1]), axis=0)
        newEdges = np.concatenate((newEdges, newEdge), axis=0) if newEdges.size else newEdge
        edges = np.delete(edges, connectionIdx[0], axis=0)
        

        idxPointA = idxPointB
        

    assert(points.shape==newPoints.shape)
    return newPoints, newEdges


    
def updatePointsEdgesBranches(points, edges,   purkSimple, purkBranches, nodes2Erase):
    points = np.delete(points, nodes2Erase, axis=0)
    edges2Erase = np.unique(np.isin(edges, nodes2Erase).nonzero()[0])
    edges = np.delete(edges, edges2Erase, axis=0)
    edgesIdx2Update = np.where(edges>=min(nodes2Erase))
    edges[edgesIdx2Update] = edges[edgesIdx2Update] - len(nodes2Erase)

    for branchType in purkBranches.keys():
        for branch in purkBranches[branchType].keys():
            data = np.array(purkBranches[branchType][branch])
            data[data>=min(nodes2Erase)] = data[data>=min(nodes2Erase)] - len(nodes2Erase)
            purkBranches[branchType][branch] = list(data)


    for branch in purkSimple.keys():
        data = np.array(purkSimple[branch])
        data[data>=min(nodes2Erase)] = data[data>=min(nodes2Erase)] - len(nodes2Erase)
        purkSimple[branch] = list(data)

    return points, edges, purkSimple, purkBranches

def saveVtkInpMesh1D(points, edges, nsets, outPath, outName, debug=False):
    cells = [
        ("line", edges),
    ]
    point_data={}
    for key in nsets.keys():
        tmp = np.zeros(points.shape[0])
        tmp[nsets[key]] = 1
        point_data[key] = list(tmp)

    meshOut = meshio.Mesh(points, cells, point_data=point_data)
    if not debug:
        meshOut.write(os.path.join(outPath, "{}.vtk".format(outName)))
    else:
        meshio.vtk.write(os.path.join(outPath, "{}.vtk".format(outName)), meshOut,  binary=False) #Debugging

    meshOut = meshio.Mesh(points, cells, point_sets=nsets)
    meshOut.write(os.path.join(outPath, "{}.inp".format(outName)))


def checkEndBranchesOrder(endBranchesDict, branchType):
    idxsEndBad = []
    idxs = [branch.split("_")[-1] for branch in endBranchesDict.keys() if "end" in branch]
    for idx in idxs:
        branch = np.array(endBranchesDict["{}_endBranch_{}".format(branchType, idx)])
        if np.any(np.abs(np.diff(branch[:-1]))!=1):
            print("Wrong branch, branch {}: {}".format(idx, branch))
            idxsEndBad.extend(idx)

    if len(idxsEndBad) !=0: raise ValueError("Wrong branch percentage: {}".format(100*len(idxsEndBad)/len(idxs)))
    return idxs


def getOutliersTh(data):
    df = pd.DataFrame(data)
    q25 = df.quantile(0.25)
    q75 = df.quantile(0.75)
    IQR = q75-q25
    th = q75 + 1.5 * IQR
    return th[0]