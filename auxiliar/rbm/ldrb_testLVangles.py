import dolfin as df
import ldrb
import os
import argparse
import time
import numpy as np
from tqdm import tqdm
import meshio
import h5py
from scipy.spatial import KDTree
import matplotlib.pyplot as plt

start = time.time()
parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--dataPath',type=str, required=True, help='path to data')
parser.add_argument('--outName',type=str, required=True, help='path to data')
args = parser.parse_args()

# Volume Mesh, Mesh DTI fibers and FacetFunction reading
mesh = df.Mesh()
with df.XDMFFile(os.path.join(args.dataPath, "RBM_LDRB", "mesh.xdmf")) as xdmf:
    xdmf.read(mesh)
ffun = df.MeshFunction("size_t", mesh, 2)
with df.XDMFFile(os.path.join(args.dataPath, "RBM_LDRB", "ffun.xdmf")) as xdmf:
    xdmf.read(ffun)
dtiMesh = meshio.read(os.path.join(args.dataPath, "tetmesh_dtiFibers_rbf.vtk"))
dtiFibers = dtiMesh.point_data["dti_fibers"]
dtiPoints = dtiMesh.points
markers = ldrb.utils.default_markers()
markers.pop("rv", None)

# Choose space for the fiber fields
fiber_space = "Lagrange_1"
indexs = np.meshgrid(np.arange(-90, -88, 1), np.arange(-90, -88, 1))
indexs = np.array([indexs[0].flatten(), indexs[1].flatten()])

with open(os.path.join(args.dataPath, "RBM_LDRB", "{}.txt".format(args.outName)), 'w') as file:
    file.write("# Results for LV alpha angle determination\n")

thetaMeans = np.zeros(indexs.shape[1])
for i in tqdm(range(indexs.shape[1])):
        # Compute the microstructure
        endo = indexs[0,i]; epi = indexs[1,i]; print("Endo {}, Epi {}".format(endo, epi))
        fiber, _, _ = ldrb.dolfin_ldrb(mesh=mesh, fiber_space=fiber_space, ffun=ffun, markers=markers, log_level=30, alpha_endo_lv=endo, alpha_epi_lv=epi, beta_endo_lv=0, beta_epi_lv=0)

        ldrb.fiber_to_xdmf(fiber, os.path.join(args.dataPath, "RBM_LDRB", "fiberLong"))
        
        with h5py.File(os.path.join(args.dataPath, "RBM_LDRB", "fiberLong.h5"), "r") as f:
            # List all groups
            rbmPoints = np.array(f["fiber"]["coordinates"])
            rbmVersors = np.array(f["fiber"]["vector"])   #already normalized
            # angles = np.array(f["fiber"]["scalar"])

        tree = KDTree(rbmPoints)
        _ , idxs = tree.query(dtiPoints, k=1)
        rbmVersors = rbmVersors[idxs,:]
        
        dotProduct = np.sum(np.multiply(dtiFibers, rbmVersors), axis=1)
        normProduct = np.multiply(np.linalg.norm(dtiFibers, axis=1), np.linalg.norm(rbmVersors, axis=1))
        thetaMeans[i] = np.mean(np.rad2deg(np.arccos(np.abs(dotProduct / normProduct))))

        with open(os.path.join(args.dataPath, "RBM_LDRB", "{}.txt".format(args.outName)), 'a') as file:
            file.write("{0}: Endo {1}, Epi {2}, ThetaMean {3:.2f}\n".format(i, endo, epi, thetaMeans[i]))

plt.figure()
plt.plot(np.arange(0,indexs.shape[1]), thetaMeans)
plt.ylabel("Theta Mean in Degrees")
plt.savefig(os.path.join(args.dataPath, "RBM_LDRB", "{}.png".format(args.outName)))

# Get the minimum pair
idxMin = np.argmin(thetaMeans)
print("The min mean theta is {0:.2f}, for alpha_endo_lv {1} and alpha_epi_lv {2}".format(thetaMeans[idxMin], indexs[0,idxMin], indexs[1,idxMin]))

print("Time of entire operation: {} seconds".format(time.time()-start))
