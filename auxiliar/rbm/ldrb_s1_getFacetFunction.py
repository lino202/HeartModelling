import dolfin as df
import ldrb
import os
import argparse
import numpy as np
import meshio
from tqdm import tqdm
from utils import getHugeNearest, isMemberIdxsRowWise

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--dataPath',type=str, required=True, help='path to data')
args = parser.parse_args()

outPath = os.path.join(args.dataPath, "RBM_LDRB")

# Volume Mesh reading
mesh = df.Mesh()
f = df.XDMFFile(df.MPI.comm_world, os.path.join(args.dataPath, "tetmesh.xdmf"))
f.read(mesh)
df.info(mesh)
bmesh = df.BoundaryMesh(mesh, "exterior", True)
bmeshPoints = bmesh.coordinates()
endoLVMesh = meshio.read(os.path.join(args.dataPath, "RBM_LDRB", "lv_endo.obj"))
endoRVMesh = meshio.read(os.path.join(args.dataPath, "RBM_LDRB", "rv_endo.obj"))
epiMesh = meshio.read(os.path.join(args.dataPath, "RBM_LDRB", "epi.obj"))

endoRVPoints = endoRVMesh.points
endoLVPoints = endoLVMesh.points
epiPoints = epiMesh.points

markers = ldrb.utils.default_markers()
all_markers = np.zeros((mesh.coordinates().shape[0]))
idxs = getHugeNearest(endoRVPoints, mesh.coordinates(), showMem=True)
all_markers[idxs] = markers["rv"]

idxs = getHugeNearest(endoLVPoints, mesh.coordinates(), showMem=True)
all_markers[idxs] = markers["lv"]

idxs = getHugeNearest(epiPoints, mesh.coordinates(), showMem=True)
all_markers[idxs] = markers["epi"]

#Delete all from surf and get base
allMinusBase = np.concatenate((endoLVPoints, endoRVPoints, epiPoints), axis=0)
idxs = getHugeNearest(allMinusBase, bmeshPoints, showMem=True)
basePoints = np.delete(bmeshPoints, idxs, axis=0)
idxs = getHugeNearest(basePoints, mesh.coordinates(), showMem=True)
all_markers[idxs] = markers["base"]


ffun = df.MeshFunction("size_t", mesh , mesh.topology().dim()-1)
ffun.set_all(0)

mapping = bmesh.entity_map(mesh.topology().dim()-1)
boundary_facets = [ df.Facet(mesh, mapping[cell.index()]) for cell in df.cells(bmesh) ]

#map faster than for (not sure if map is really faster)
def getPoints(v):
    return v.point().array()

# def getVertexs(f):
#     vLs = df.vertices(f)
#     vertexsCoords = list(map(getPoints,vLs))
#     # idxs = isMemberIdxsRowWise(vertexsCoords, mesh.coordinates(), showMem=False)
#     # facetClass = np.median(all_markers[idxs]).astype(int)
#     return np.array(vertexsCoords)

# facetClass = list(map(getVertexs,boundary_facets))
# ffun[boundary_facets] = facetClass
# pass

for f in tqdm(boundary_facets):


    vertexLs = df.vertices(f)
    vertexsCoords = np.array(list(map(getPoints,vertexLs)))
    idxs = isMemberIdxsRowWise(vertexsCoords, mesh.coordinates(), showMem=False)
    ffun[f] = np.median(all_markers[idxs]).astype(int)

with df.XDMFFile(mesh.mpi_comm(), os.path.join(outPath, "mesh.xdmf")) as xdmf:
    xdmf.write(mesh)

with df.XDMFFile(mesh.mpi_comm(), os.path.join(outPath, "ffun.xdmf")) as xdmf:
    xdmf.write(ffun)

