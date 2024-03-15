'''This code needs several improvements but it works,
It is slow for high resolution meshes 4 hour for 1.5M nodes and 9M tet cells for example
Also it distort the jacobian of a mesh as it saves the mesh cells differently'''


import dolfin as df
import ldrb
import os
import argparse
import numpy as np
import meshio
from tqdm import tqdm
from utils import getHugeNearest, isMemberIdxsRowWise
from multiprocessing import Pool
import time

def initGetFaceClass(_facets, _points, __all_markers):
    global facets, points, all_markers
    facets  = _facets
    points  = _points
    all_markers = __all_markers

def getPoints(v):
    return v.point().array()

def getFaceClass(idx):
    vertexLs = df.vertices(facets[idx])
    vertexsCoords = np.array(list(map(getPoints,vertexLs)))
    idxs = isMemberIdxsRowWise(vertexsCoords, points, showMem=False)
    return np.median(all_markers[idxs]).astype(int)

def main():
    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument('--dataPath',      type=str, required=True, help='path to data')
    parser.add_argument('--domainType',    type=str, required=True, help='BiV (Biventricular) or LV')
    parser.add_argument('--nProcesses',    type=int, help='number of processes to use', default=7)
    parser.add_argument('--chunksize',     type=int, help='Value for determining chunksize in Pool', default=1000)
    parser.add_argument('--maxNumPoints',  type=int, help='Value for determining chunksize in Pool', default=1000)
    args = parser.parse_args()


    outPath = os.path.join(args.dataPath, "RBM_LDRB")
    if not os.path.exists(outPath): os.mkdir(outPath)

    # Volume Mesh reading
    mesh = df.Mesh()
    f = df.XDMFFile(df.MPI.comm_world, os.path.join(args.dataPath, "mesh", "tetmesh.xdmf"))
    f.read(mesh)
    df.info(mesh)
    bmesh = df.BoundaryMesh(mesh, "exterior", True)
    bmeshPoints = bmesh.coordinates()
    endoLVMesh = meshio.read(os.path.join(args.dataPath, 'mesh', "lv_endo.obj"))
    endoLVPoints = endoLVMesh.points
    epiMesh = meshio.read(os.path.join(args.dataPath, 'mesh', "epi.obj"))
    epiPoints = epiMesh.points

    if args.domainType == "BiV": 
        endoRVMesh = meshio.read(os.path.join(args.dataPath, 'mesh', "rv_endo.obj"))
        endoRVPoints = endoRVMesh.points
    markers = ldrb.utils.default_markers()
    all_markers = np.zeros((mesh.coordinates().shape[0]))
    if args.domainType == "BiV": 
        idxs = getHugeNearest(endoRVPoints, mesh.coordinates(), showMem=True, maxNumPoints=args.maxNumPoints)
        all_markers[idxs] = markers["rv"]
    idxs = getHugeNearest(endoLVPoints, mesh.coordinates(), showMem=True, maxNumPoints=args.maxNumPoints)
    all_markers[idxs] = markers["lv"]
    idxs = getHugeNearest(epiPoints, mesh.coordinates(), showMem=True, maxNumPoints=args.maxNumPoints)
    all_markers[idxs] = markers["epi"]

    #Delete all from surf and get base
    if args.domainType == "BiV": 
        allMinusBase = np.concatenate((endoLVPoints, endoRVPoints, epiPoints), axis=0) 
    elif args.domainType == "LV": 
        allMinusBase = np.concatenate((endoLVPoints, epiPoints), axis=0) 
    else: raise ValueError("Wrong domainType parameter")

    idxs = getHugeNearest(allMinusBase, bmeshPoints, showMem=True, maxNumPoints=args.maxNumPoints)
    basePoints = np.delete(bmeshPoints, idxs, axis=0)
    idxs = getHugeNearest(basePoints, mesh.coordinates(), showMem=True, maxNumPoints=args.maxNumPoints)
    all_markers[idxs] = markers["base"]

    # Get the ffun with faces classes
    ffun = df.MeshFunction("size_t", mesh , mesh.topology().dim()-1)
    ffun.set_all(0)
    mapping = bmesh.entity_map(mesh.topology().dim()-1)
    boundary_facets = [ df.Facet(mesh, mapping[cell.index()]) for cell in df.cells(bmesh) ]
    boundary_idxs   = [ facet.index() for facet in boundary_facets ]

    nProcesses = args.nProcesses
    # chunksize = int((args.maxMem * 1e9) / (len(boundary_facets) * 4)) #maxMem in GB
    chunksize = args.chunksize
    idxs      = np.arange(len(boundary_facets))
    if nProcesses >= os.cpu_count(): nProcesses = os.cpu_count()-1
    with Pool(nProcesses, initializer=initGetFaceClass, initargs=(boundary_facets, mesh.coordinates(), all_markers)) as p:
        res = list(tqdm(p.imap(getFaceClass, idxs, chunksize=chunksize), total=len(boundary_facets)))
    
    ffun.array()[boundary_idxs] = res

    # for f in tqdm(boundary_facets):
    #     vertexLs = df.vertices(f)
    #     vertexsCoords = np.array(list(map(getPoints,vertexLs)))
    #     idxs = isMemberIdxsRowWise(vertexsCoords, mesh.coordinates(), showMem=False)
    #     ffun[f] = np.median(all_markers[idxs]).astype(int)

    # TODO here this mesh has wrong saving of cells as jacobian are changed drastically to have negative numbers,
    # now you can avoid this by using tetmesh.vtk from tetgen as final mesh and the point data definitions obtained from this
    # mesh as layers and fiber fields
    with df.XDMFFile(mesh.mpi_comm(), os.path.join(outPath, "mesh.xdmf")) as xdmf:
        xdmf.write(mesh)

    with df.XDMFFile(mesh.mpi_comm(), os.path.join(outPath, "ffun.xdmf")) as xdmf:
        xdmf.write(ffun)

if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))