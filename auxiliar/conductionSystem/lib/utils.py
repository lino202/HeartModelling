import numpy as np
import pygeodesic.geodesic as geodesic


def getLinearPath(sourcePoint, targetPoint, step = 0.5):
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

