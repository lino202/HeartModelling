

import numpy as np
import pygeodesic.geodesic as geodesic
from scipy.spatial.distance import cdist, pdist
from scipy.interpolate import interp1d
import itertools


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


def resampleGeodesic(points, thresholdDist=0.7):
    #Interpolate in every axis
    x = np.arange(0,points.shape[0]-1,thresholdDist/10)
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


def isMemberIdxsRowWise(arr1, arr2, tol = 1E-6, showMem=False):
    if showMem: 
        print("Required Memory: {} GB".format(4 *(arr1.shape[0]) * (arr2.shape[0]) / 1e9))
    else:
        arr1 = np.reshape(arr1, (-1,3))
    idxs = np.min(cdist(arr2,arr1), axis=1) < tol
    return idxs.nonzero()[0]


def getEdges(points):
    edges = np.array([])
    for nodeIdx in range(points.shape[0]-1):
        newEdge = np.array([[nodeIdx, nodeIdx+1]])
        edges = np.concatenate((edges, newEdge), axis=0) if edges.size else newEdge
    return edges

def getLineInfo(points):
    print("Line data ------------")
    res = np.zeros(points.shape[0]-1)
    for i in range(points.shape[0]-1):
        a = points[i,:]
        b = points[i+1,:]
        res[i] = np.linalg.norm(a-b)
    print("Mean distances {}".format(np.mean(res)))
    print("Length {}".format(np.sum(res)))
    print("-------------------")