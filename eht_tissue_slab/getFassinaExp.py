import os
import meshio
import argparse
import numpy as np
import pickle

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--dataPath',type=str, required=True, help='path to data')
parser.add_argument('--outName',type=str, required=True, help='path to data')
parser.add_argument('--patchFiberName',type=str, required=True, help='path to data')
parser.add_argument('--tissueThickness',type=float, required=True, help='thickness of the slab of tissue')
parser.add_argument('--epiAlphaAngle',type=int, required=True, help='angle alpha for the epi layer usually defined in RBMs, 90 is parallel to the patch in common setting')
parser.add_argument('--alphaAngleRange',type=int, required=True, help='angle alpha range')
parser.add_argument('--stimThickness',type=float, required=True, help='stimulation uniform band thickness')
parser.add_argument('--scarThickness',type=float, required=True, help='scar thickness')
parser.add_argument('--scarInit',type=float, required=True, help='scar init position in y if experiment setting is the common one see code otherwise')
args = parser.parse_args()

# Fixed markers and transmural heterogenity
# validKeys = ["endo", "mid", "epi", "myo", "scar", "uncertain", "bz"]

myo_flag = 1
scar_flag = 8
endo_flag = 3
mid_flag = 4
epi_flag = 5
uncertain_flag = 6
bz_flag = 7
patch_flag = 9

endo_per = 40; endo_per = endo_per /100
epi_per = 25; epi_per = epi_per /100

# Read mesh 
mesh = meshio.read(os.path.join(args.dataPath, "tetmesh.vtk"))
points = mesh.points

# TRANSMURAL HETEROGENITY ---------------------------------------------------------------------------------------------------------------
endoThres = args.tissueThickness * endo_per
epiThres = args.tissueThickness * (1-epi_per)

point_data = {}
layers = np.ones(points.shape[0]) * mid_flag
layers[points[:,2]<=endoThres] = endo_flag
layers[points[:,2]>epiThres] = epi_flag
layers[points[:,2]>args.tissueThickness] = patch_flag

point_data["tissueLayers"] = layers
tissues = {"endo": endo_flag, "mid": mid_flag, "epi": epi_flag, "patch": patch_flag}
for key in tissues.keys():
    tmp = np.zeros(points.shape[0])
    tmp[layers==tissues[key]] = 1
    point_data[key] = tmp

# FIBER DETERMINATION----------------------------------------------------------------------------------------------------
# We define the angle of the fibers from the epi layer (the one in contact with the patch)
# with respect to the axis perpendicular to the longitudinal axis of the mesh (x for the normal setting)
# The endo angle is going to be that value -120 degrees as common values of alpha in RBM go between -60 and 60
# I assume a linear variation transmurally with the distance as the experiment is a parallelepiped
fibers = np.zeros(points.shape)

#patch
idxs = (layers == patch_flag).nonzero()[0]
if args.patchFiberName != "0":
    with open(os.path.join(args.dataPath, '{}.pkl'.format(args.patchFiberName)), 'rb') as file:
        patchFibers = pickle.load(file)
    fibers[idxs,:] = patchFibers
else:
    angles = np.random.uniform(low=-90, high=90, size=idxs.shape)
    fibers[idxs,0] = np.cos(np.deg2rad(angles))
    fibers[idxs,1] = np.sin(np.deg2rad(angles))

#anything else
idxs = (layers != patch_flag).nonzero()[0]
dists = args.tissueThickness - points[idxs][:,2]
angles = args.epiAlphaAngle + (args.alphaAngleRange/args.tissueThickness) * dists
fibers[idxs,0] = np.cos(np.deg2rad(angles))
fibers[idxs,1] = np.sin(np.deg2rad(angles))

point_data["fibers"] = fibers


# STIM DEFINITION ---------------------------------------------------------------------------------------------------------
stim_nodes = np.zeros(points.shape[0])
stim_nodes[points[:,1]<= args.stimThickness] = 1
point_data["stim"] = stim_nodes

# SCAR DEFINITION ---------------------------------------------------------------------------------------------------------
scar_nodes = np.zeros(points.shape[0])
scar_nodes[np.where((points[:,1]>= args.scarInit) & (points[:,1]<= args.scarInit + args.scarThickness))[0]] = 1
scar_nodes[layers==patch_flag] = 0
point_data["scar"] = scar_nodes

# Point data correction
for key in tissues.keys():
    point_data[key][scar_nodes==1] = 0
point_data["tissueLayers"][scar_nodes==1] = scar_flag 

# SAVE DATA ----------------------------------------------------------------------------------------------------------
meshOutVtk = meshio.Mesh(mesh.points, mesh.cells, point_data=point_data)
meshOutVtk.write(os.path.join(args.dataPath, "{}.vtk".format(args.outName)))

# Get nsets for INP
nsets = {}
for key in point_data.keys():
    if key != "fibers" and key != "tissueLayers":
        nsets["{}_nodes".format(key)] = np.where(point_data[key]==1)[0]

meshOutInp = meshio.Mesh(mesh.points, mesh.cells, point_sets=nsets)
meshOutInp.write(os.path.join(args.dataPath, "{}.inp".format(args.outName)))



