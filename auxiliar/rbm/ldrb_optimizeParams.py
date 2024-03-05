'''In this code, we use a biventricular mesh and generate diverses fiber fields that we compare with
the dti estimation obtained from dwi data. Specifically we compare the main eigenvector (longitudinal
fiber direction) against the F direction from Bayer et al. using the ldrb package.
We vary the 4 parameters: first the range +/-90 degrees with steps of 10 degrees is tested for the alfha endo and epi of LV (324 combinations)
the RV params are leave constant. Then the same is done for the RV. We also reduce the resolution to 1 degree for +/-20 degrees with
this range centered for the best value found before for both LV and RV'''


import dolfin as df
import ldrb
import os
import argparse
import time
import numpy as np
from tqdm import tqdm
import meshio
from scipy.spatial import KDTree
import matplotlib.pyplot as plt
import pickle


parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--dataPath',type=str, required=True, help='path to data')
args = parser.parse_args()

# Volume Mesh, Mesh DTI fibers and FacetFunction reading
mesh = df.Mesh()
with df.XDMFFile(os.path.join(args.dataPath, "mesh.xdmf")) as xdmf:
    xdmf.read(mesh)
ffun = df.MeshFunction("size_t", mesh, 2)
with df.XDMFFile(os.path.join(args.dataPath, "ffun.xdmf")) as xdmf:
    xdmf.read(ffun)
dtiMesh = meshio.read(os.path.join(args.dataPath, "tetmesh_dtifibs.vtk"))
dtiFibers = dtiMesh.point_data["dti_fibers"]
dtiPoints = dtiMesh.points

# Settings 
markers = ldrb.utils.default_markers() 
# if we want to use the LV only
# markers.pop("rv", None)
fiber_space = "Lagrange_1"
big_step = 10
small_step = 1
big_range_width = 90
small_range_width = 10

# Get RV Endo and Epi BIG Steps in Degrees--------------------------------------------------------------
print("------------+/-90 RV Optimization -------------------")
indexs = np.meshgrid(np.arange(-big_range_width, big_range_width+big_step, big_step), np.arange(-big_range_width, big_range_width+big_step, big_step))
indexs = np.array([indexs[0].flatten(), indexs[1].flatten()])

thetaMeans = np.zeros(indexs.shape[1])
start = time.time()
for i in tqdm(range(indexs.shape[1])):

        # Compute the microstructure
        endo = indexs[0,i]; epi = indexs[1,i]
        angles = dict(
            alpha_endo_lv=60,      # Fiber angle on the LV endocardium
            alpha_epi_lv=-60,        # Fiber angle on the LV epicardium
            beta_endo_lv=0,          # Sheet angle on the LV endocardium
            beta_epi_lv=0,           # Sheet angle on the LV epicardium
            # beta_endo_sept=0,      # Sheet angle on the Septum endocardium
            # beta_epi_sept=0,       # Sheet angle on the Septum epicardium
            alpha_endo_rv=endo,        # Fiber angle on the RV endocardium
            alpha_epi_rv=epi,        # Fiber angle on the RV epicardium
            beta_endo_rv=0,          # Sheet angle on the RV endocardium
            beta_epi_rv=0
        )
        fiber, _, _ = ldrb.dolfin_ldrb(mesh=mesh, fiber_space=fiber_space, ffun=ffun, markers=markers, log_level=30, **angles)

        # Get versors without saving as the ldrb package does it
        V = fiber.function_space()
        gs = fiber.split(deepcopy=True)
        W = V.sub(0).collapse()
        dim = V.mesh().geometry().dim()
        coords_tmp = W.tabulate_dof_coordinates()
        rbmPoints = coords_tmp.reshape((-1, dim))
        us = [g.vector().get_local() for g in gs]
        rbmVersors = np.array(us).T

        # Compute the difference as in Bayer et al, we need to match the nodes from the dti mesh and with the rbm results
        tree = KDTree(rbmPoints)
        _ , idxs = tree.query(dtiPoints, k=1)
        rbmVersors = rbmVersors[idxs,:]
        if "scar_nodes" in dtiMesh.point_data.keys():
            healthyIdxs = np.where(dtiMesh.point_data["scar_nodes"]==0)[0]
            dtiFibers = dtiFibers[healthyIdxs,:]
            rbmVersors = rbmVersors[healthyIdxs,:]

        
        dotProduct = np.sum(np.multiply(dtiFibers, rbmVersors), axis=1)
        normProduct = np.multiply(np.linalg.norm(dtiFibers, axis=1), np.linalg.norm(rbmVersors, axis=1))
        thetaMeans[i] = np.mean(np.rad2deg(np.arccos(np.abs(dotProduct / normProduct))))

        print("Endo {0}, Epi {1}, thetaMean {2:.2f}".format(endo, epi, thetaMeans[i]))


# Get the minimum pair
idxMin  = np.argmin(thetaMeans)
RV_ENDO = indexs[0,idxMin]
RV_EPI  = indexs[1,idxMin]
print("The min mean theta is {0:.2f}, for alpha_endo_rv {1} and alpha_epi_rv {2}".format(thetaMeans[idxMin], RV_ENDO, RV_EPI))
print("Time of entire operation: {} seconds".format(time.time()-start))


# Save a figure and the thetas
plt.figure()
plt.plot(np.arange(0,indexs.shape[1]), thetaMeans)
plt.ylabel("Theta Mean in Degrees")
plt.savefig(os.path.join(args.dataPath, "rv_bigReso.png"))

results = {"indexs": indexs, "thetaMeans": thetaMeans}
with open(os.path.join(args.dataPath, "rv_bigReso.pickle"), 'wb') as handle:
    pickle.dump(results, handle)
        

# Get RV Endo and Epi SMALL Steps in Degrees--------------------------------------------------------------
print("------------+/-10 from previous min RV Optimization -------------------")
indexs = np.meshgrid(np.arange(RV_ENDO-small_range_width, RV_ENDO+small_range_width+small_step, small_step), np.arange(RV_EPI-small_range_width, RV_EPI+small_range_width+small_step, small_step))
indexs = np.array([indexs[0].flatten(), indexs[1].flatten()])

thetaMeans = np.zeros(indexs.shape[1])
start = time.time()
for i in tqdm(range(indexs.shape[1])):

        # Compute the microstructure
        endo = indexs[0,i]; epi = indexs[1,i]
        angles = dict(
            alpha_endo_lv=60,      # Fiber angle on the LV endocardium
            alpha_epi_lv=-60,        # Fiber angle on the LV epicardium
            beta_endo_lv=0,          # Sheet angle on the LV endocardium
            beta_epi_lv=0,           # Sheet angle on the LV epicardium
            # beta_endo_sept=0,      # Sheet angle on the Septum endocardium
            # beta_epi_sept=0,       # Sheet angle on the Septum epicardium
            alpha_endo_rv=endo,        # Fiber angle on the RV endocardium
            alpha_epi_rv=epi,        # Fiber angle on the RV epicardium
            beta_endo_rv=0,          # Sheet angle on the RV endocardium
            beta_epi_rv=0
        )
        fiber, _, _ = ldrb.dolfin_ldrb(mesh=mesh, fiber_space=fiber_space, ffun=ffun, markers=markers, log_level=30, **angles)

        # Get versors without saving as the ldrb package does it
        V = fiber.function_space()
        gs = fiber.split(deepcopy=True)
        W = V.sub(0).collapse()
        dim = V.mesh().geometry().dim()
        coords_tmp = W.tabulate_dof_coordinates()
        rbmPoints = coords_tmp.reshape((-1, dim))
        us = [g.vector().get_local() for g in gs]
        rbmVersors = np.array(us).T

        # Compute the difference as in Bayer et al
        tree = KDTree(rbmPoints)
        _ , idxs = tree.query(dtiPoints, k=1)
        rbmVersors = rbmVersors[idxs,:]
        if "scar_nodes" in dtiMesh.point_data.keys():
            healthyIdxs = np.where(dtiMesh.point_data["scar_nodes"]==0)[0]
            dtiFibers = dtiFibers[healthyIdxs,:]
            rbmVersors = rbmVersors[healthyIdxs,:]
        
        dotProduct = np.sum(np.multiply(dtiFibers, rbmVersors), axis=1)
        normProduct = np.multiply(np.linalg.norm(dtiFibers, axis=1), np.linalg.norm(rbmVersors, axis=1))
        thetaMeans[i] = np.mean(np.rad2deg(np.arccos(np.abs(dotProduct / normProduct))))

        print("Endo {0}, Epi {1}, thetaMean {2:.2f}".format(endo, epi, thetaMeans[i]))


# Get the minimum pair
idxMin  = np.argmin(thetaMeans)
RV_ENDO = indexs[0,idxMin]
RV_EPI  = indexs[1,idxMin]
print("The min mean theta is {0:.2f}, for alpha_endo_rv {1} and alpha_epi_rv {2}".format(thetaMeans[idxMin], RV_ENDO, RV_EPI))
print("Time of entire operation: {} seconds".format(time.time()-start))


# Save a figure and the thetas
plt.figure()
plt.plot(np.arange(0,indexs.shape[1]), thetaMeans)
plt.ylabel("Theta Mean in Degrees")
plt.savefig(os.path.join(args.dataPath, "rv_smallReso.png"))

results = {"indexs": indexs, "thetaMeans": thetaMeans}
with open(os.path.join(args.dataPath, "rv_smallReso.pickle"), 'wb') as handle:
    pickle.dump(results, handle)




# Get LV Endo and Epi BIG Steps in Degrees--------------------------------------------------------------
print("------------+/-90 LV Optimization -------------------")
indexs = np.meshgrid(np.arange(-big_range_width, big_range_width+big_step, big_step), np.arange(-big_range_width, big_range_width+big_step, big_step))
indexs = np.array([indexs[0].flatten(), indexs[1].flatten()])

thetaMeans = np.zeros(indexs.shape[1])
start = time.time()
for i in tqdm(range(indexs.shape[1])):

        # Compute the microstructure
        endo = indexs[0,i]; epi = indexs[1,i]
        angles = dict(
            alpha_endo_lv=endo,      # Fiber angle on the LV endocardium
            alpha_epi_lv=epi,        # Fiber angle on the LV epicardium
            beta_endo_lv=0,          # Sheet angle on the LV endocardium
            beta_epi_lv=0,           # Sheet angle on the LV epicardium
            # beta_endo_sept=0,      # Sheet angle on the Septum endocardium
            # beta_epi_sept=0,       # Sheet angle on the Septum epicardium
            alpha_endo_rv=RV_ENDO,        # Fiber angle on the RV endocardium
            alpha_epi_rv=RV_EPI,        # Fiber angle on the RV epicardium
            beta_endo_rv=0,          # Sheet angle on the RV endocardium
            beta_epi_rv=0
        )
        fiber, _, _ = ldrb.dolfin_ldrb(mesh=mesh, fiber_space=fiber_space, ffun=ffun, markers=markers, log_level=30, **angles)

        # Get versors without saving as the ldrb package does it
        V = fiber.function_space()
        gs = fiber.split(deepcopy=True)
        W = V.sub(0).collapse()
        dim = V.mesh().geometry().dim()
        coords_tmp = W.tabulate_dof_coordinates()
        rbmPoints = coords_tmp.reshape((-1, dim))
        us = [g.vector().get_local() for g in gs]
        rbmVersors = np.array(us).T

        # Compute the difference as in Bayer et al
        tree = KDTree(rbmPoints)
        _ , idxs = tree.query(dtiPoints, k=1)
        rbmVersors = rbmVersors[idxs,:]
        if "scar_nodes" in dtiMesh.point_data.keys():
            healthyIdxs = np.where(dtiMesh.point_data["scar_nodes"]==0)[0]
            dtiFibers = dtiFibers[healthyIdxs,:]
            rbmVersors = rbmVersors[healthyIdxs,:]
        
        dotProduct = np.sum(np.multiply(dtiFibers, rbmVersors), axis=1)
        normProduct = np.multiply(np.linalg.norm(dtiFibers, axis=1), np.linalg.norm(rbmVersors, axis=1))
        thetaMeans[i] = np.mean(np.rad2deg(np.arccos(np.abs(dotProduct / normProduct))))

        print("Endo {0}, Epi {1}, thetaMean {2:.2f}".format(endo, epi, thetaMeans[i]))


# Get the minimum pair
idxMin  = np.argmin(thetaMeans)
LV_ENDO = indexs[0,idxMin]
LV_EPI  = indexs[1,idxMin]
print("The min mean theta is {0:.2f}, for alpha_endo_lv {1} and alpha_epi_lv {2}".format(thetaMeans[idxMin], LV_ENDO, LV_EPI))
print("Time of entire operation: {} seconds".format(time.time()-start))


# Save a figure and the thetas
plt.figure()
plt.plot(np.arange(0,indexs.shape[1]), thetaMeans)
plt.ylabel("Theta Mean in Degrees")
plt.savefig(os.path.join(args.dataPath, "lv_bigReso.png"))

results = {"indexs": indexs, "thetaMeans": thetaMeans}
with open(os.path.join(args.dataPath, "lv_bigReso.pickle"), 'wb') as handle:
    pickle.dump(results, handle)
        

# Get LV Endo and Epi SMALL Steps in Degrees--------------------------------------------------------------
print("------------+/-10 from previous min LV Optimization -------------------")
indexs = np.meshgrid(np.arange(LV_ENDO-small_range_width, LV_ENDO+small_range_width+small_step, small_step), np.arange(LV_EPI-small_range_width, LV_EPI+small_range_width+small_step, small_step))
indexs = np.array([indexs[0].flatten(), indexs[1].flatten()])

thetaMeans = np.zeros(indexs.shape[1])
start = time.time()
for i in tqdm(range(indexs.shape[1])):

        # Compute the microstructure
        endo = indexs[0,i]; epi = indexs[1,i]
        angles = dict(
            alpha_endo_lv=endo,      # Fiber angle on the LV endocardium
            alpha_epi_lv=epi,        # Fiber angle on the LV epicardium
            beta_endo_lv=0,          # Sheet angle on the LV endocardium
            beta_epi_lv=0,           # Sheet angle on the LV epicardium
            # beta_endo_sept=0,      # Sheet angle on the Septum endocardium
            # beta_epi_sept=0,       # Sheet angle on the Septum epicardium
            alpha_endo_rv=RV_ENDO,        # Fiber angle on the RV endocardium
            alpha_epi_rv=RV_EPI,        # Fiber angle on the RV epicardium
            beta_endo_rv=0,          # Sheet angle on the RV endocardium
            beta_epi_rv=0
        )
        fiber, _, _ = ldrb.dolfin_ldrb(mesh=mesh, fiber_space=fiber_space, ffun=ffun, markers=markers, log_level=30, **angles)

        # Get versors without saving as the ldrb package does it
        V = fiber.function_space()
        gs = fiber.split(deepcopy=True)
        W = V.sub(0).collapse()
        dim = V.mesh().geometry().dim()
        coords_tmp = W.tabulate_dof_coordinates()
        rbmPoints = coords_tmp.reshape((-1, dim))
        us = [g.vector().get_local() for g in gs]
        rbmVersors = np.array(us).T

        # Compute the difference as in Bayer et al
        tree = KDTree(rbmPoints)
        _ , idxs = tree.query(dtiPoints, k=1)
        rbmVersors = rbmVersors[idxs,:]
        if "scar_nodes" in dtiMesh.point_data.keys():
            healthyIdxs = np.where(dtiMesh.point_data["scar_nodes"]==0)[0]
            dtiFibers = dtiFibers[healthyIdxs,:]
            rbmVersors = rbmVersors[healthyIdxs,:]
        
        dotProduct = np.sum(np.multiply(dtiFibers, rbmVersors), axis=1)
        normProduct = np.multiply(np.linalg.norm(dtiFibers, axis=1), np.linalg.norm(rbmVersors, axis=1))
        thetaMeans[i] = np.mean(np.rad2deg(np.arccos(np.abs(dotProduct / normProduct))))

        print("Endo {0}, Epi {1}, thetaMean {2:.2f}".format(endo, epi, thetaMeans[i]))


# Get the minimum pair
idxMin  = np.argmin(thetaMeans)
LV_ENDO = indexs[0,idxMin]
LV_EPI  = indexs[1,idxMin]
print("The min mean theta is {0:.2f}, for alpha_endo_lv {1} and alpha_epi_lv {2}".format(thetaMeans[idxMin], LV_ENDO, LV_EPI))
print("Time of entire operation: {} seconds".format(time.time()-start))


# Save a figure and the thetas
plt.figure()
plt.plot(np.arange(0,indexs.shape[1]), thetaMeans)
plt.ylabel("Theta Mean in Degrees")
plt.savefig(os.path.join(args.dataPath, "lv_smallReso.png"))

results = {"indexs": indexs, "thetaMeans": thetaMeans}
with open(os.path.join(args.dataPath, "lv_smallReso.pickle"), 'wb') as handle:
    pickle.dump(results, handle)


res_string = "The final angles should be LV_ENDO {0}, LV_EPI {1}, RV_ENDO {2}, RV_EPI {3}".format(LV_ENDO, LV_EPI, RV_ENDO, RV_EPI)
print(res_string)
with open(os.path.join(args.dataPath, "final_results.txt"), 'w') as file:
    file.write(res_string)

