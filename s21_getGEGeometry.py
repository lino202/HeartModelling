# this code classifies Scar in segmentation as real scar and border zone and generates a point cloud for 
# using another algorithm to add fibers direction and the it should keep going with the 3D meshing and interpolation
# from this output .vtk to the 3D mesh


import nrrd 
import os 
import argparse
import meshio
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import seaborn as sns
from auxiliar.conductionSystem.lib.utils import isMemberIdxsRowWise

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--dataPath',type=str, required=True, help='path to data')
parser.add_argument('--outName',type=str, required=True, help='output name')
parser.add_argument('--healthyNumber',type=int, required=True)
parser.add_argument('--unhealthyNumber',type=int, required=True)
parser.add_argument('--remoteRoiNumber',type=int, required=True)
parser.add_argument('--save',action='store_true',  help='save histogram with thresholds')
args = parser.parse_args()

geVolData = nib.load(os.path.join(args.dataPath, "sa_ge.nii"))
geVolArr = geVolData.get_fdata()
segMask, segMaskHeader = nrrd.read(os.path.join(args.dataPath, "Segmentation.seg.nrrd"))
space = segMaskHeader['space']
spaceOrigin = np.concatenate((segMaskHeader['space origin'],[1]))
ijk2Points = np.zeros((4,4))
ijk2Points[:3,:3] = segMaskHeader['space directions'].T
ijk2Points[:,3] =  spaceOrigin

#here it should not matter as we do not have dwi in a probable different space, but still checks
if space != "left-posterior-superior": raise ValueError("Wrong space?") 

# as s2_estimateDti we need to add points to the .vtk in xyz coordinates with the ijk2xyz matrix
ijkPixels = np.where(segMask!=0)
tissueFlags = segMask[ijkPixels]
ijkPixels = np.concatenate(( [ijkPixels[0]], [ijkPixels[1]], [ijkPixels[2]], [np.ones(ijkPixels[2].shape)] ))
points = np.matmul(ijk2Points, ijkPixels).T
points= points[:,:3]

# apply method for thresholding border zone and scar from unhealthy mask by 
# Infarct Tissue Heterogeneity by Magnetic Resonance Imaging Identifies Enhanced Cardiac Arrhythmia
# Susceptibility in Patients With Left Ventricular Dysfunction, André Schmidt

unhealthyIJKIdxs = np.where(segMask==args.unhealthyNumber)
unhealthyGreyValues = geVolArr[unhealthyIJKIdxs]
remoteRoiIJKIdxs = np.where(segMask==args.remoteRoiNumber)
remoteRoiGreyValues = geVolArr[remoteRoiIJKIdxs]
scarThres = 0.5 * np.max(unhealthyGreyValues)
borderZoneThresBottom = np.max(remoteRoiGreyValues)
print("The scarThres is {}".format(scarThres))
print("The borderZoneThresBottom is {}".format(borderZoneThresBottom))

sns.set(style="ticks")
f, (ax_box, ax_hist) = plt.subplots(2, sharex=True, gridspec_kw={"height_ratios": (.15, .85)})
sns.boxplot(x=unhealthyGreyValues, ax=ax_box)
sns.histplot(x=unhealthyGreyValues, ax=ax_hist)
ax_box.set(yticks=[])
ax_hist.set_ylabel("Frequencies")
ax_hist.set_xlabel("Unhealthy Grey Values")
ax_hist.axvline(borderZoneThresBottom, color='g', linestyle='dashed', linewidth=2)
ax_hist.axvline(scarThres, color='r', linestyle='dashed', linewidth=2)
ax_box.axvline(borderZoneThresBottom, color='g', linestyle='dashed', linewidth=2)
ax_box.axvline(scarThres, color='r', linestyle='dashed', linewidth=2)
sns.despine(ax=ax_hist)
sns.despine(ax=ax_box, left=True)
plt.savefig(os.path.join(args.dataPath, "thresholds.png")) if args.save else plt.show(block=True)

# Get points for border zone and scar in unhealthy zone
mask = np.zeros(geVolArr.shape)
mask[unhealthyIJKIdxs] = 1
unhealthyArray = mask * geVolArr
idxsScar = np.where(unhealthyArray>scarThres)
idxsBZ = np.where((unhealthyArray>=borderZoneThresBottom)&(unhealthyArray<=scarThres))
idxsCorrectHealthy = np.where((unhealthyArray>0)&(unhealthyArray<borderZoneThresBottom))

#Pass ijk idxs of scar and BZ to idxs in xyz
ijkPixels = ijkPixels.T[:,:3]
idxsScar = np.concatenate(( [idxsScar[0]], [idxsScar[1]], [idxsScar[2]] )).T
idxsBZ = np.concatenate(( [idxsBZ[0]], [idxsBZ[1]], [idxsBZ[2]] )).T
idxsCorrectHealthy = np.concatenate(( [idxsCorrectHealthy[0]], [idxsCorrectHealthy[1]], [idxsCorrectHealthy[2]] )).T
idxsScar = isMemberIdxsRowWise(idxsScar, ijkPixels, showMem=True)
idxsBZ = isMemberIdxsRowWise(idxsBZ, ijkPixels, showMem=True)
idxsCorrectHealthy = isMemberIdxsRowWise(idxsCorrectHealthy, ijkPixels, showMem=True)

healthyIdxs = np.where((tissueFlags==args.healthyNumber) | (tissueFlags==args.remoteRoiNumber))
unhealthyIdxs = np.where(tissueFlags==args.unhealthyNumber)



nsets = {"healthy": healthyIdxs, "unhealthy": unhealthyIdxs, "scar": idxsScar, "bz": idxsBZ, "correctHealthy": idxsCorrectHealthy }
point_data={}
for key in nsets.keys():
    tmp = np.zeros(points.shape[0])
    tmp[nsets[key]] = 1
    point_data[key] = list(tmp)

point_data["all"] = np.zeros(points.shape[0])
point_data["all"][healthyIdxs] = 1
point_data["all"][idxsCorrectHealthy] = 2
point_data["all"][idxsBZ] = 3
point_data["all"][idxsScar] = 4


# There might be zeros in all as some pixels with zero value could be segmented
# into the unhealthy zone, we can decide what to do with them if they are healthy or border zone
point_data["all"][point_data["all"]==0] = 2

meshOut = meshio.Mesh(points, [], point_data=point_data)
meshOut.write(os.path.join(args.dataPath, "{}.vtk".format(args.outName)))