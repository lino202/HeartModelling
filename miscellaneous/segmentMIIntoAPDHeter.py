# Take the BZ and scar and separate them into apex-base and transmural
 
import argparse
import meshio
import numpy as np
import copy
import os
from regions import regions, bz_flag, scar_flag

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--meshHE',type=str, required=True, help='path to data')
parser.add_argument('--meshMI',type=str, required=True, help='path to data')
parser.add_argument('--outPath',type=str, required=True, help='output path')
args = parser.parse_args()


meshHE = meshio.read(args.meshHE)
meshMI = meshio.read(args.meshMI)

layersHE = meshHE.point_data["layers"]
layersMI = meshMI.point_data["layers"]

# Delete in case there is 
point_data = {"layers": copy.deepcopy(layersMI)}
nsets      = {}
for key, value in regions.items():
    nset_name = key.replace("flag", "nodes")

    if ("bz" in key) or ("scar" in key):
        mi_region = key.split("_")[0]
        he_region = key.split(mi_region + "_")[-1]

        idxs = np.where((layersMI==globals()["{}_flag".format(mi_region)]) & (layersHE==regions[he_region]))[0]
        if idxs.size == 0: print("Warning!! The region {} does not have any node".format(key))
        point_data["layers"][idxs] = value
        nsets[nset_name] = idxs

    else:
        nsets[nset_name] = np.where(layersMI==value)[0]


# SAVE
mesh_full_segmented = meshio.Mesh(meshMI.points, meshMI.cells, point_data=point_data)
mesh_full_segmented.write(os.path.join(args.outPath, "mesh_full_segmented.vtk"))

mesh_full_segmented_inp = meshio.Mesh(meshMI.points, meshMI.cells, point_sets=nsets)
mesh_full_segmented_inp.write(os.path.join(args.outPath, "mesh_full_segmented.inp"))