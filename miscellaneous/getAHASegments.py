# this code classifies an existing mesh into a RV and LV and the AHA segments for the LV from a segmentation of LV and RV
'''Standardized Myocardial Segmentation and Nomenclature for Tomographic Imaging of the Heart
A Statement for Healthcare Professionals From the Cardiac Imaging Committee
of the Council on Clinical Cardiology of the American Heart Association'''

import nrrd  
import argparse
import meshio
import numpy as np
import matplotlib.pyplot as plt
from utils import getBaseApexSA

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--segLVRV',type=str, required=True, help='path to data')
parser.add_argument('--meshIn',type=str, required=True, help='path to data')
parser.add_argument('--outPath',type=str, required=True, help='output path')
parser.add_argument('--basalPerc',type=int, default=35)
parser.add_argument('--midPerc',type=int, default=35)
parser.add_argument('--apicalPerc',type=int, default=30)
parser.add_argument('--labelLV',type=int, default=1)
parser.add_argument('--labelRV',type=int, default=2)
parser.add_argument('--flippedLA',action='store_true',  help='If base is down and apex high this should be true')
parser.add_argument('--show',action='store_true',  help='Show images for details')
args = parser.parse_args()

# GET INPUTS AND COMPUTE SKELETONS -----------------------------------------------------------------
segMask, segMaskHeader = nrrd.read(args.segLVRV)
axisSA = np.argmin(segMask.shape)
mesh = meshio.load(args.meshIn)

# first put the segmentation with the base up and the 
# axis 2 being the long axis of the heart, so change shape and orientation
if axisSA == 0:   segMask = np.moveaxis(segMask, [0,1,2], [-1,-3,-2])
elif axisSA == 1: segMask = np.moveaxis(segMask, [0,1,2], [-2,-1,-3])
else: pass
if args.flippedLA: segMask = np.rot90(segMask, k=2, axes=(0,2))

#Get base and apex slices
base, apex = getBaseApexSA(segMask)
print("The base and apex slices are: {} and {}".format(base, apex))
if args.show:
    fig, axs = plt.subplots(3,2)
    axs[0,0].imshow(segMask[:,:,base-1])
    axs[0,1].imshow(segMask[:,:,apex-1])
    axs[1,0].imshow(segMask[:,:,base])
    axs[1,1].imshow(segMask[:,:,apex])
    axs[2,0].imshow(segMask[:,:,base+1])
    axs[2,1].imshow(segMask[:,:,apex+1])
    fig.suptitle("This Should be:  Left=Base and Right=Apex, Bottom Base and Top Apex empty")
    plt.show(block=True)

#Get skeletons

# COMPUTE AHA SEGMENTS -----------------------------------------------------------------
# First separate LV in 3 long axis according to mass percentages
volTot = np.count_nonzero(segMask==args.labelLV)
vol = 0
for s in range(apex, base+1):
    print(s)
    vol += np.count_nonzero(segMask[:,:,s]==args.labelLV)
    if vol/volTot > ((args.midPerc + args.apicalPerc)/100):
        print("The apical + mid volume ratio is {0:.2f}".format(vol/volTot * 100))
        midBaseSlice = s
        break
    elif vol/volTot > (args.apicalPerc/100):
        if not "midApexSlice" in globals():
            print("The apical volume ratio is {0:.2f}".format(vol/volTot * 100))
            midApexSlice = s
    else: continue

#GET POINT_DATA ------------------------------------------------------------------------------------
point_data = mesh.point_data
# Get points differents regions

# idxsRV = np.where(segMask==args.labelRV)
# idxsLV = np.where(segMask==args.labelLV)


#Pass ijk idxs of scar and BZ to idxs in xyz
ijkPixels = ijkPixels.T[:,:3]
idxsScar = np.concatenate(( [idxsScar[0]], [idxsScar[1]], [idxsScar[2]] )).T
idxsBZ = np.concatenate(( [idxsBZ[0]], [idxsBZ[1]], [idxsBZ[2]] )).T
idxsCorrectHealthy = np.concatenate(( [idxsCorrectHealthy[0]], [idxsCorrectHealthy[1]], [idxsCorrectHealthy[2]] )).T
idxsScar = isMemberIdxsRowWise(idxsScar, ijkPixels, showMem=True)
idxsBZ = isMemberIdxsRowWise(idxsBZ, ijkPixels, showMem=True)
idxsCorrectHealthy = isMemberIdxsRowWise(idxsCorrectHealthy, ijkPixels, showMem=True)


# GET XYZ POINTS IN REAL ORIENTATION-----------------------------------------------------------------
# Get initial shape and orientation
if args.flippedLA: segMask = np.rot90(segMask, k=2, axes=(0,2))
if axisSA == 0:   segMask = np.moveaxis(segMask, [0,1,2], [-2,-1,-3])
elif axisSA == 1: segMask = np.moveaxis(segMask, [0,1,2], [-1,-3,-2])
else: pass

#Get different regions idxs
idxsRV = np.where(segMask==args.labelRV)
idxsLV = np.where(segMask==args.labelLV)

#Get xyz coordinates

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

# SAVE VTK-----------------------------------------------------------------
cells = [
    ("line", [[0, 1]])    #this is just for being able to open with meshio afterwards
]
# There might be zeros in layers_mi as some pixels with zero value could be segmented
# into the unhealthy zone, we can decide what to do with them if they are healthy or border zone
# point_data["layers_mi"][point_data["layers_mi"]==0] = uncertain_flag

meshOut = meshio.Mesh(points, cells)
meshOut.write(args.outPath)