import numpy as np
import argparse
import meshio
from scipy.interpolate import RBFInterpolator, griddata
import time
import sys
import os
sys.path.append(os.path.join(os.path.dirname(sys.path[0])))
from miscellaneous.regions import patch_flag

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--heartPatchMesh',type=str, required=True)
parser.add_argument('--layersMesh',type=str, required=True)
parser.add_argument('--fibsMesh',type=str, required=True)
parser.add_argument('--neighbours',type=str, default=1000)
parser.add_argument('--outPath',type=str, required=True)
args = parser.parse_args()

start = time.time()
fields2interpolate = ["layers",  "rbm_60_minus60_60_minus60"]
baseMesh   = meshio.read(args.heartPatchMesh)
layersMesh = meshio.read(args.layersMesh)
fibsMesh   = meshio.read(args.fibsMesh)

baseMeshCells = baseMesh.cells_dict["tetra"]
idxsCellsMyo = np.where(baseMesh.cell_data["cell_scalars"][0]==1)[0]
idxsPointsMyo = np.unique(baseMesh.cells_dict["tetra"][idxsCellsMyo].flatten())
idxsPointsPatch = np.isin(np.arange(baseMesh.points.shape[0]),idxsPointsMyo, invert=True).nonzero()[0]

#First interpolate myo layers and define patch nodes
point_data = {}
for field in fields2interpolate:
    if 'layers' in field:
        values1 = layersMesh.point_data[field]
    elif 'rbm' in field:
        values1 = fibsMesh.point_data[field]
    else:
        raise ValueError('Check the field names and things you are triying to interpolate')
    
    # here we use nearest neighbour interpolation rather than RBF as myocardial meshes should not be coarser or finer than the one used 
    # for the MI-only model, then this interp should be ok. Also and more importantly RBF gets nodes with a layers values intermediate for example 30 (see regions)
    values2 = griddata(layersMesh.points, values1, baseMesh.points[idxsPointsMyo], method='nearest')
    # values2 = RBFInterpolator(layersMesh.points, values1, neighbors=args.neighbours)(baseMesh.points[idxsPointsMyo])
    if "layers" in field: 
        finalValues2 = np.zeros(baseMesh.points.shape[0])
    elif "rbm" in field:
        finalValues2 = np.zeros((baseMesh.points.shape[0],values2.shape[1]))
    finalValues2[:] = np.nan 
    finalValues2[idxsPointsMyo] = values2

    #get round values for vtk and inp
    if "layers" in field:
        finalValues2[finalValues2<np.nanmin(values1)] = np.nanmin(values1)
        finalValues2[finalValues2>np.nanmax(values1)] = np.nanmax(values1)
        finalValues2 = np.round(finalValues2)
        finalValues2[idxsPointsPatch] = patch_flag
    elif "rbm" in field:
        fibersNorm = np.linalg.norm(finalValues2, axis=1)
        finalValues2 = finalValues2 /  np.array([fibersNorm, fibersNorm, fibersNorm]).T
    else: raise ValueError("Wrong valueName")

    point_data[field] = finalValues2

#SAVE--------------------------------------------------
#Use mesh2inp in miscellaneous for getting inp
meshOut = meshio.Mesh(baseMesh.points, baseMesh.cells, point_data=point_data)
meshOut.write(args.outPath)
print("Elapsed time: {0:.4f} s".format(time.time()-start))