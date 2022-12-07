import numpy as np
from scipy.spatial import KDTree
from tqdm import tqdm
import meshio

def getPointsEnclosedByMesh(points, outerMesh):
    #Please check meshes if bad operatoin of the function happens
    outerMeshCellCentroids =  np.mean(outerMesh.points[outerMesh.cells_dict["triangle"]], axis=1)
    u = outerMesh.points[outerMesh.cells_dict["triangle"]][:,1] - outerMesh.points[outerMesh.cells_dict["triangle"]][:,0]
    v = outerMesh.points[outerMesh.cells_dict["triangle"]][:,2] - outerMesh.points[outerMesh.cells_dict["triangle"]][:,0]
    outerMeshNormals = np.cross(u,v)
    outerMeshNormals = outerMeshNormals / np.expand_dims(np.linalg.norm(outerMeshNormals, axis=1), axis=1)
    tree = KDTree(outerMeshCellCentroids)
    _ , idxs = tree.query(points, k=1)
    vecInner2Outer =  points - outerMeshCellCentroids[idxs]
    vecInner2Outer = vecInner2Outer / np.expand_dims(np.linalg.norm(vecInner2Outer, axis=1), axis=1)
    dots = np.sum(vecInner2Outer * outerMeshNormals[idxs,:], axis=1)
    return (dots<=0).nonzero()[0]


def delElemsFromMesh(mesh, elems):
    cells = mesh.cells_dict["triangle"]
    cellsRemaining = (~np.isin(np.arange(cells.shape[0]), elems)).nonzero()[0]
    pointsRemaining = np.unique(cells[cellsRemaining])
    newPoints = mesh.points[pointsRemaining]
    newCells = cells[cellsRemaining]

    for idx in tqdm(np.unique(newCells.flatten())):
        newIdx = (pointsRemaining==idx).nonzero()[0]
        newCells[np.where(newCells==idx)] = newIdx

    elems = [("triangle", newCells)]
    meshOut = meshio.Mesh(newPoints, elems)

    if mesh.cell_data.keys():
        newCellData = {}
        for key in mesh.cell_data.keys():
            newCellData[key] = [mesh.cell_data[key][0][cellsRemaining]]

        meshOut.cell_data = newCellData

    return meshOut