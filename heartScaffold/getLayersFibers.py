import numpy as np
import argparse
import meshio
from scipy.interpolate import RBFInterpolator
import time

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--heartPatchMesh',type=str, required=True)
parser.add_argument('--layersFibsMesh',type=str, required=True)
parser.add_argument('--outPath',type=str, required=True)
args = parser.parse_args()

start = time.time()
fields2interpolate = ["layers",  "rbm-fibers-long"]
baseMesh = meshio.read(args.heartPatchMesh)
layersMesh = meshio.read(args.layersFibsMesh)

baseMeshCells = baseMesh.cells_dict["tetra"]
idxsCellsMyo = np.where((baseMesh.cell_data["myo_cells"][0]==3) | (baseMesh.cell_data["myo_cells"][0]==0))[0]
idxsPointsMyo = np.unique(baseMesh.cells_dict["tetra"][idxsCellsMyo].flatten())
# idxsCellsPatch = np.isin(np.arange(baseMeshCells.shape[0]),idxsCellsMyo, invert=True).nonzero()[0]
# idxsPointsPatch = np.unique(baseMesh.cells_dict["tetra"][idxsCellsPatch].flatten())
idxsPointsPatch = np.isin(np.arange(baseMesh.points.shape[0]),idxsPointsMyo, invert=True).nonzero()[0]

#First interpolate myo layers and define patch nodes
point_data = {}
for field in fields2interpolate:
    values1 = layersMesh.point_data[field]
    values2 = RBFInterpolator(layersMesh.points, values1, neighbors=10)(baseMesh.points[idxsPointsMyo])
    if "layers" in field: 
        finalValues2 = np.zeros(baseMesh.points.shape[0])
    elif "fib" in field:
        finalValues2 = np.zeros((baseMesh.points.shape[0],values2.shape[1]))
    finalValues2[:] = np.nan 
    finalValues2[idxsPointsMyo] = values2

    #get round values for vtk and inp
    if "layers" in field:
        finalValues2[finalValues2<np.nanmin(values1)] = np.nanmin(values1)
        finalValues2[finalValues2>np.nanmax(values1)] = np.nanmax(values1)
        finalValues2 = np.round(finalValues2)
        finalValues2[idxsPointsPatch] = 9
    elif "fib" in field:
        fibersNorm = np.linalg.norm(finalValues2, axis=1)
        finalValues2 = finalValues2 /  np.array([fibersNorm, fibersNorm, fibersNorm]).T
    else: raise ValueError("Wrong valueName")

    point_data[field] = finalValues2

#SAVE--------------------------------------------------
#Use mesh2inp in miscellaneous for getting inp
meshOut = meshio.Mesh(baseMesh.points, baseMesh.cells, point_data=point_data)
meshOut.write(args.outPath)
print("Elapsed time: {0:.4f} s".format(time.time()-start))