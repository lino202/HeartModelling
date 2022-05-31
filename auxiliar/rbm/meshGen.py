'''Here we need to select the .obj files containing the surfaces of the apex rings and endo for XV and the superposition 
of all in the surfMesh gives epi. I prefer doing the manual selection in meshlab. The ring is contained in the endo counterpart'''

import os
import numpy as np
import argparse
import time 
import meshio
from utils import getHugeNearest

start = time.time()
parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--mesh3dPath',type=str, required=True, help='path to data')
parser.add_argument('--mesh2dPath',type=str, required=True, help='path to data')
parser.add_argument('--dataPath',type=str, required=True, help='path to data')
parser.add_argument('--outName',type=str, required=True, help='output name')
parser.add_argument('--endoLVName',type=str, required=True, help='endo surface of the LV')
parser.add_argument('--endoRVName',type=str, required=True, help='endo surface of the RV')
parser.add_argument('--ringLV',type=str, required=True, help='LV ring')
parser.add_argument('--ringRV',type=str, required=True, help='RV ring')
parser.add_argument('--apexLV' ,type=str, required=True, help='apex LV')
parser.add_argument('--apexRV' ,type=str, required=True, help='apex RV')
args = parser.parse_args()


# Get the endo and epi surfaces
nsets={}
endoLV = meshio.read(os.path.join(args.dataPath,  "{}.obj".format(args.endoLVName)))
endoRV = meshio.read(os.path.join(args.dataPath,  "{}.obj".format(args.endoRVName)))
ringLV = meshio.read(os.path.join(args.dataPath,  "{}.obj".format(args.ringLV)))
ringRV = meshio.read(os.path.join(args.dataPath,  "{}.obj".format(args.ringRV)))
apexLV = meshio.read(os.path.join(args.dataPath,  "{}.obj".format(args.apexLV)))
apexRV = meshio.read(os.path.join(args.dataPath,  "{}.obj".format(args.apexRV)))
meshSurf = meshio.read(os.path.join(args.mesh2dPath, "surfMesh.obj"))
mesh = meshio.read(os.path.join(args.mesh3dPath, "electra_tetmesh.vtk"))
points = mesh.points

idxsSurf2Vol = getHugeNearest(meshSurf.points, points,  maxNumPoints=1000)

idxsEndoRV = getHugeNearest(endoRV.points, meshSurf.points)
idxsRingRV = getHugeNearest(ringRV.points, meshSurf.points)
# idxsEndoRV = idxsEndoRV[np.in1d(idxsEndoRV, idxsRingRV, invert=True)]
nsets["rv_ring"] = idxsRingRV
nsets["rv_endo"] = idxsEndoRV

idxsEndoLV = getHugeNearest(endoLV.points, meshSurf.points)
idxsRingLV = getHugeNearest(ringLV.points, meshSurf.points)
# idxsEndoLV = idxsEndoLV[np.in1d(idxsEndoLV, idxsRingLV, invert=True)]
nsets["lv_ring"] = idxsRingLV
nsets["lv_endo"] = idxsEndoLV


idxsApexLV = getHugeNearest(apexLV.points, meshSurf.points)
nsets["lv_apex"] = idxsApexLV
idxsApexRV = getHugeNearest(apexRV.points, meshSurf.points)
nsets["rv_apex"] = idxsApexRV


allMinusEpi = np.array([])
idxsEpi = np.arange(meshSurf.points.shape[0])
for key in nsets.keys():
    if "endo" in key:
        allMinusEpi = np.concatenate((allMinusEpi, nsets[key])) if allMinusEpi.size else nsets[key]
idxsEpi = idxsEpi[np.in1d(idxsEpi, allMinusEpi, invert=True)]
nsets["epi"] = idxsEpi

point_data={}
for key in nsets.keys():
    tmp = np.zeros(points.shape[0])
    tmp[idxsSurf2Vol[nsets[key]]] = 1
    point_data[key] = list(tmp)

meshOut = meshio.Mesh(points, mesh.cells, point_data=point_data)
meshOut.write(os.path.join(args.dataPath, "{}.vtk".format(args.outName)))
meshOut = meshio.Mesh(points, mesh.cells, point_sets=nsets)
meshOut.write(os.path.join(args.dataPath, "{}.inp".format(args.outName)))

print("Ended in {} seconds\n".format(time.time()-start))