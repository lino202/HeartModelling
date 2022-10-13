import meshio 
import numpy as np
import os
import argparse

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--inPath',type=str, required=True, help='path to file and file name')
parser.add_argument('--outPath',type=str, required=True, help='path to file and file name')
args = parser.parse_args()

validKeys = ["endo", "mid", "epi", "myo", "scar", "uncertain", "bz"]
myo_flag = 1
scar_flag = 8
endo_flag = 3
mid_flag = 4
epi_flag = 5
uncertain_flag = 6
bz_flag = 7

mesh = meshio.read(args.inPath)
pointData = mesh.point_data
pointDataKeys = pointData.keys()
nsets={}

if "layers" in pointDataKeys and ((not "endo" in pointDataKeys) and (not "mid" in pointDataKeys) and (not "epi" in pointDataKeys)):
    for key in pointDataKeys:
        if pointData[key].ndim == 1 and "layers" in key:
            for pointKey in validKeys:
                nsets["{}_nodes".format(pointKey)] = np.where(pointData["layers"] == globals()["{}_flag".format(pointKey)])[0]
        elif pointData[key].ndim == 1 and "cover" in key:
            nsets["cover_nodes"] = np.where(pointData[key]==1)[0]
else:
    for key in pointDataKeys:
        if key in validKeys:
            nsets["{}".format(key)] = np.where(pointData[key]==1)[0]

meshOut = meshio.Mesh(mesh.points, mesh.cells, point_sets=nsets)
meshOut.write(args.outPath)
