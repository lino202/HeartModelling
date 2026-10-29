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



parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--dataPath',type=str, required=True, help='path to data')
parser.add_argument('--save',action='store_true',  help='save histogram with thresholds')
args = parser.parse_args()

sns.set(style="ticks", font_scale=3, font="Times New Roman", rc={'figure.figsize':(12,9)})
# font = {'family' : "Times New Roman",
#         'weight' : 'normal',
#         'size'   : 20}
# plt.rc('font', **font)

myo_flag = 1
uncertain_flag = 2
bz_flag = 3
scar_flag = 4

#Load the images. Check that there are not repeated images in the file.
geVolData = nib.load(os.path.join(args.dataPath, "init", "img.nii"))
geVolArr = geVolData.get_fdata()
#Load the labels
segMask, segMaskHeader = nrrd.read(os.path.join(args.dataPath, "init", "label_he_rehe_mi.nrrd"))
space = segMaskHeader['space']
spaceOrigin = np.concatenate((segMaskHeader['space origin'],[1]))
ijk2Points = np.zeros((4,4))
ijk2Points[:3,:3] = segMaskHeader['space directions'].T
ijk2Points[:,3] =  spaceOrigin
#ijk2Points is a matrix 4x4  with the space directions at the beginning and then the space origin

#here it should not matter as we do not have dwi in a probable different space, but still checks
if space != "left-posterior-superior": raise ValueError("Wrong space?") 

# We need to add points to the .vtk in xyz coordinates with the ijk2xyz matrix
ijkPixels = np.where(segMask!=0) #Find the labels of the segmentations. Returns a tuple of arrays (3), each corresponding to a dimension of the original matrix
#Each array in here has the samen length since it corresponds to the 3 axis to create a coordinate to find non zedro elements
tissueFlags = segMask[ijkPixels] #The labels in the mask matrix (where all the labels are)
ijkPixels = np.concatenate(( [ijkPixels[0]], [ijkPixels[1]], [ijkPixels[2]], [np.ones(ijkPixels[2].shape)] )) #Concatenate the places where there are labels plus an array of ones
points = np.matmul(ijk2Points, ijkPixels).T #Matrix product of two arrays. Between the matrix with the space data (direction and origin) and
#
points= points[:,:3]

# Get the healthy, remote healthy and unhealthy numbers in the segMask
numbers, counts = np.unique(segMask, return_counts=True)
idxsHeReheMi    = np.argsort(counts) #Returns the indices that would sort an array. 
#The array is ordered depending on the amount of pixels in each label.
#The smallest number of pixels is for the ReHe, the second to the scar and the largest to the rest of the Healthy tissue
# reHeNumber      = numbers[idxsHeReheMi[0]] #ReHe tissue label (integrer)
# unHeNumber      = numbers[idxsHeReheMi[1]] #Scar tissue label (integrer)
# heNumber        = numbers[idxsHeReheMi[2]] #Healthy tissue label (integrer)
reHeNumber      = 2 #ReHe tissue label (integrer)
unHeNumber      = 3 #Scar tissue label (integrer)
heNumber        = 1

# apply method for thresholding border zone and scar from unhealthy mask by 
# Infarct Tissue Heterogeneity by Magnetic Resonance Imaging Identifies Enhanced Cardiac Arrhythmia
# Susceptibility in Patients With Left Ventricular Dysfunction, André Schmidt

maxSIValues=np.max(geVolArr)
unhealthyIJKIdxs = np.where(segMask==unHeNumber)# The location of the pixels for scar tissue in x,y,z
unhealthyGreyValues = geVolArr[unhealthyIJKIdxs] #Get intensity values in areas with scar labels
remoteRoiIJKIdxs = np.where(segMask==reHeNumber)# The location of the pixels for ReHe tissue
remoteRoiGreyValues = geVolArr[remoteRoiIJKIdxs]#Get intensity values in areas with ReHe labels
scarThres = 0.5 * np.max(unhealthyGreyValues) #Lower Threshold for the scar tissue
#scarThres = 4000 
#scarThres = 0.5 * maxSIValues #JRDZC Add 13/01/2025
borderZoneThresBottom = np.max(remoteRoiGreyValues) #Lower Threshold for the BZ tissue
#borderZoneThresBottom = 3000 
print("The lower scarThres is {}".format(scarThres))
print("The lower borderZoneThresBottom is {}".format(borderZoneThresBottom))

#Plot the histogram for the area wihtin the mask Scar
f, (ax_box, ax_hist) = plt.subplots(2, sharex=True, gridspec_kw={"height_ratios": (.15, .85)})
f.suptitle('Signal intensity within the scar region') #JRDZC Add 14/01/2025
sns.boxplot(x=unhealthyGreyValues, ax=ax_box)
sns.histplot(x=unhealthyGreyValues, ax=ax_hist)
ax_box.set(yticks=[])
ax_hist.set_ylabel("Count", fontdict=dict(weight='bold'))
ax_hist.set_xlabel("Affected Zone Voxel Intensities Count", fontdict=dict(weight='bold'))
ax_hist.axvline(borderZoneThresBottom, color='g', linestyle='dashed', linewidth=2)
ax_hist.axvline(scarThres, color='r', linestyle='dashed', linewidth=2)
ax_box.axvline(borderZoneThresBottom, color='g', linestyle='dashed', linewidth=2)
ax_box.axvline(scarThres, color='r', linestyle='dashed', linewidth=2)
sns.despine(ax=ax_hist)
sns.despine(ax=ax_box, left=True)
#Save plot
plt.savefig(os.path.join(args.dataPath, "mesh", "ge_thresholding.png"), dpi=400) if args.save else plt.show(block=True)

#Plot of the signal intensity of the complete volume #JRDZC Add 14/01/2025
geVolArr_arr=np.reshape(geVolArr,(geVolArr.size,))
f_2, (ax_box_2, ax_hist_2) = plt.subplots(2, sharex=True, gridspec_kw={"height_ratios": (.15, .85)})
f_2.suptitle('Signal intensity within the whole volume') #JRDZC Add 14/01/2025
sns.boxplot(x=geVolArr_arr, ax=ax_box_2)
sns.histplot(x=geVolArr_arr, ax=ax_hist_2)
ax_box_2.set(yticks=[])
ax_hist_2.set_ylabel("Count", fontdict=dict(weight='bold'))
ax_hist_2.set_xlabel("Affected Zone Voxel Intensities Count", fontdict=dict(weight='bold'))
ax_hist_2.axvline(borderZoneThresBottom, color='g', linestyle='dashed', linewidth=2)
ax_hist_2.axvline(scarThres, color='r', linestyle='dashed', linewidth=2)
ax_box_2.axvline(borderZoneThresBottom, color='g', linestyle='dashed', linewidth=2)
ax_box_2.axvline(scarThres, color='r', linestyle='dashed', linewidth=2)
sns.despine(ax=ax_hist_2)
sns.despine(ax=ax_box_2, left=True)
#Save plot
plt.savefig(os.path.join(args.dataPath, "mesh", "ge_thresholding_complete.png"), dpi=400) if args.save else plt.show(block=True)


# Get points for border zone and scar in unhealthy zone
mask = np.zeros(geVolArr.shape) #Matrix the same size as the original image
mask[unhealthyIJKIdxs] = 1 # The location of the pixels for scar tissue, changed to 1
unhealthyArray = mask * geVolArr #A mask for the pixels labeled as scar. Signal intensity in the area labeled as scar
idxsScar = np.where(unhealthyArray>scarThres) #Find the Ids of the pixels that have SI values higher than the threshold, to find the scar core
idxsBZ = np.where((unhealthyArray>=borderZoneThresBottom)&(unhealthyArray<=scarThres))#Find the Ids of the pixels that have SI values higher than the BZthreshold and lower to the scar threshold, to find the BZ core
idxsCorrectHealthy = np.where((unhealthyArray>0)&(unhealthyArray<borderZoneThresBottom)) #Find the Ids of the pixels that have SI values lower than the BZthreshold, to find the healthy tissue within the scar zone we selected

#Pass ijk idxs of scar and BZ to idxs in xyz
from auxiliar.conductionSystem.lib.utils import isMemberIdxsRowWise
ijkPixels = ijkPixels.T[:,:3]
#Change from tuples of arrays to a matrix
idxsScar = np.concatenate(( [idxsScar[0]], [idxsScar[1]], [idxsScar[2]] )).T
idxsBZ = np.concatenate(( [idxsBZ[0]], [idxsBZ[1]], [idxsBZ[2]] )).T
idxsCorrectHealthy = np.concatenate(( [idxsCorrectHealthy[0]], [idxsCorrectHealthy[1]], [idxsCorrectHealthy[2]] )).T
#
idxsScar = isMemberIdxsRowWise(idxsScar, ijkPixels, showMem=True)
idxsBZ = isMemberIdxsRowWise(idxsBZ, ijkPixels, showMem=True)
idxsCorrectHealthy = isMemberIdxsRowWise(idxsCorrectHealthy, ijkPixels, showMem=True)

healthyIdxs = np.where((tissueFlags==heNumber) | (tissueFlags==reHeNumber)) #Find positions of the healthy tissue within #The labels in the mask matrix (where all the labels are)
unhealthyIdxs = np.where(tissueFlags==unHeNumber)#Find positions of the Scar tissue within #The labels in the mask matrix (where all the labels are)

nsets = {"healthy": healthyIdxs, "unhealthy": unhealthyIdxs, "scar": idxsScar, "bz": idxsBZ}
point_data={}
for key in nsets.keys():
    tmp = np.zeros(points.shape[0])
    tmp[nsets[key]] = 1
    point_data[key] = list(tmp)

point_data["layers_mi"] = np.zeros(points.shape[0])
point_data["layers_mi"][healthyIdxs] = myo_flag
point_data["layers_mi"][idxsCorrectHealthy] = uncertain_flag
point_data["layers_mi"][idxsBZ] = bz_flag
point_data["layers_mi"][idxsScar] = scar_flag

#myo_flag = 1
#uncertain_flag = 2
#bz_flag = 3
#scar_flag = 4

cells = [
    ("line", [[0, 1]])    #this is just for being able to open with meshio afterwards
]
# There might be zeros in layers_mi as some pixels with zero value could be segmented
# into the unhealthy zone, we can decide what to do with them if they are healthy or border zone
point_data["layers_mi"][point_data["layers_mi"]==0] = uncertain_flag

meshOut = meshio.Mesh(points, cells, point_data=point_data)
meshOut.write(os.path.join(args.dataPath, "mesh", "mi_pointcloud.vtk"))