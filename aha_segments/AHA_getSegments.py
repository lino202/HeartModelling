# this code classifies an existing mesh into a RV and LV and the AHA segments for the LV from a segmentation of LV and RV
'''Standardized Myocardial Segmentation and Nomenclature for Tomographic Imaging of the Heart
A Statement for Healthcare Professionals From the Cardiac Imaging Committee
of the Council on Clinical Cardiology of the American Heart Association'''

import nrrd  
import argparse
import meshio
import numpy as np
import matplotlib.pyplot as plt
from utils import getBaseApexSA, getSAHeartContours, getMainAxisAHAByDistance, getMainAxisAHAByRVInsertions
import sys
import os
import copy
from scipy.spatial.transform import Rotation as R
from scipy.interpolate import griddata
from scipy.spatial.distance import cdist
import cv2 as cv
sys.path.append(os.path.join(os.path.dirname(sys.path[0])))
# from auxiliar.conductionSystem.lib.utils import isMemberIdxsRowWise

def isMemberIdxsRowWise(arr1, arr2, tol = 1E-6, showMem=False):
    if showMem: 
        print("Required Memory: {} GB".format(4 *(arr1.shape[0]) * (arr2.shape[0]) / 1e9))
    else:
        arr1 = np.reshape(arr1, (-1,3))
    idxs = np.min(cdist(arr2,arr1), axis=1) < tol
    return idxs.nonzero()[0]

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--segLVRV',type=str, required=True, help='path to data')
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
#change LV labels
segMask[segMask==args.labelRV] = 30
args.labelRV = 30
segMask[segMask==args.labelLV] = 31
args.labelLV = 31
axisSA = np.argmin(segMask.shape) # SA images axis

# first put the segmentation with the base up and the 
# axis 2 being the long axis of the heart, so change shape and orientation
if axisSA == 0:   segMask = np.moveaxis(segMask, [0,1,2], [-1,-3,-2])
elif axisSA == 1: segMask = np.moveaxis(segMask, [0,1,2], [-2,-1,-3])
else: pass
if args.flippedLA: segMask = np.rot90(segMask, k=2, axes=(0,2))

#Get base and apex slices
base, apex = getBaseApexSA(segMask)
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

# GET THREE MEDIAN SLICES -----------------------------------------------------------------
# First separate LV in 3 long axis according to mass percentages
volTot = np.count_nonzero(segMask==args.labelLV)
vol = 0
for s in range(apex, base+1):
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
print("SLICES:\n Apex {0}\n midApex {1}\n midBase {2}\n Base {3}\n".format(apex, midApexSlice, midBaseSlice, base))

#Get contours
countours = np.zeros(segMask.shape[2])
for i, s in enumerate(np.arange(apex, base+1)):
    #Contours, 0=no tissue, 1 = apex, 2 = mid, 3 = base
    countours[s] = len(getSAHeartContours(segMask[:,:,s], s)[0])

# We select the three median slices for the apical, mid-cavity and basal AHA segments
apexLVCavitySlice = np.min((countours==2).nonzero()[0]) # more apical slice with the LV cavity
apexRVCavitySlice = np.min((countours==3).nonzero()[0])-1
apexRVSlice       = np.min((segMask==args.labelRV).nonzero()[2])
ahaApicalSlice    = np.median(np.arange(apexLVCavitySlice, midApexSlice+1)).astype(int)
ahaMidSlice       = np.median(np.arange(midApexSlice+1, midBaseSlice+1)).astype(int)
ahaBaseSlice      = np.median(np.arange(midBaseSlice+1, base+1)).astype(int)
print("SLICES:\n apexLVCavitySlice {0}\n ahaApicalSlice {1}\n ahaMidSlice {2}\n ahaBaseSlice {3}\n".format(apexLVCavitySlice,  ahaApicalSlice, ahaMidSlice, ahaBaseSlice))

if args.show:
    fig, axs = plt.subplots(1,3)
    axs[0].imshow(segMask[:,:,ahaApicalSlice])
    axs[1].imshow(segMask[:,:,ahaMidSlice])
    axs[2].imshow(segMask[:,:,ahaBaseSlice])
    plt.show()  

# COMPUTE SEGMENTS FOR 3 MEDIAN SLICES-----------------------------------------------------------
# Get centroid of LV for the 3 slices
ahaSlices = [ahaBaseSlice, ahaMidSlice, ahaApicalSlice]
AHASegMask = copy.deepcopy(segMask).astype(float)
AHASegMask[AHASegMask==0] = np.nan; AHASegMask[AHASegMask==args.labelRV] = np.nan
cos60 = np.cos(np.pi/3)
cos120 = np.cos(2*np.pi/3)

for s in ahaSlices:
    # Get centroid of LV
    lvSlice = copy.deepcopy(segMask[:,:,s])
    lvSlice[(lvSlice==args.labelRV).nonzero()]=0
    cnts, hier = getSAHeartContours(lvSlice, s)
    if hier.shape[0]!=1 or hier.shape[1]!=2: raise ValueError("Wrong hierarchy: no one hier level or no two contours for LV, segmentation/patology?")
    lvBPcont = cnts[(hier[0,:,2]==-1).nonzero()[0][0]]
    M = cv.moments(lvBPcont); cX = int(M["m10"] / M["m00"]); cY = int(M["m01"] / M["m00"]); centroid = np.array([cY, cX])

    # Get main NORMALIZE axis 
    if countours[s]==2: #Get axis with distance
        mainAxis = getMainAxisAHAByDistance(centroid, segMask[:,:,s])
        #Check that is opossite to axisSeptum
        if np.dot(mainAxis, axisSeptum) > 0: mainAxis = -1 * mainAxis
    elif countours[s]==3: # Get axis wirh RV insertions
        mainAxis = getMainAxisAHAByRVInsertions(centroid, segMask[:,:,s])
        axisSeptum = copy.deepcopy(mainAxis)

    #Rotate for get the AHA boundaries per image
    if s == ahaApicalSlice: rotAngles = [-45,45] # 4 segments with only 2 directions
    else: rotAngles = [-30,30,90]     # 6 segments we need only 3 segments
    rotAnglesRad = np.expand_dims(np.radians(rotAngles), axis=1)
    normal = np.array([0, 0, 1])
    rotVectors = np.hstack((rotAnglesRad,rotAnglesRad,rotAnglesRad)) * normal
    rotations = R.from_rotvec(rotVectors)
    AHAboundaries = rotations.apply(np.array([mainAxis[0], mainAxis[1],0]))[:,:2]

    # See which pixel of the LV correspond to a segment
    lvPoints = np.where(lvSlice!=0)
    lvPoints = np.array(lvPoints).T
    dirs = lvPoints - centroid
    tmp = np.linalg.norm(dirs, axis=1)
    dirs =  dirs / np.hstack((tmp[:,np.newaxis],tmp[:,np.newaxis]))

    dots = np.dot(dirs, AHAboundaries.T)
    if dots.shape[1] == 2:

        idxsAHA16 = lvPoints[np.where((dots[:,0]>=0) & (dots[:,1]>0))[0],:]
        idxsAHA15 = lvPoints[np.where((dots[:,0]<=0) & (dots[:,1]>0))[0],:]
        idxsAHA14 = lvPoints[np.where((dots[:,0]<=0) & (dots[:,1]<0))[0],:]
        idxsAHA13 = lvPoints[np.where((dots[:,0]>=0) & (dots[:,1]<0))[0],:]
        idxsAHA16 = np.hstack((idxsAHA16, s*np.ones(idxsAHA16.shape[0])[:, np.newaxis]))
        idxsAHA15 = np.hstack((idxsAHA15, s*np.ones(idxsAHA15.shape[0])[:, np.newaxis]))
        idxsAHA14 = np.hstack((idxsAHA14, s*np.ones(idxsAHA14.shape[0])[:, np.newaxis]))
        idxsAHA13 = np.hstack((idxsAHA13, s*np.ones(idxsAHA13.shape[0])[:, np.newaxis]))
        AHASegMask[tuple(idxsAHA16.astype(int).T)] = 16
        AHASegMask[tuple(idxsAHA15.astype(int).T)] = 15
        AHASegMask[tuple(idxsAHA14.astype(int).T)] = 14
        AHASegMask[tuple(idxsAHA13.astype(int).T)] = 13

    elif dots.shape[1] == 3 and s == ahaMidSlice:  

        idxsAHA7  = lvPoints[np.where( (dots[:,1]>=cos60)  & (dots[:,2]>cos60)  )[0],:]
        idxsAHA8  = lvPoints[np.where( (dots[:,0]>=cos60)  & (dots[:,1]>cos60)  )[0],:]
        idxsAHA9  = lvPoints[np.where( (dots[:,2]<=cos120) & (dots[:,0]>cos60)  )[0],:]
        idxsAHA10 = lvPoints[np.where( (dots[:,1]<=cos120) & (dots[:,2]<cos120) )[0],:]
        idxsAHA11 = lvPoints[np.where( (dots[:,0]<=cos120) & (dots[:,1]<cos120) )[0],:]
        idxsAHA12 = lvPoints[np.where( (dots[:,2]>=cos60)  & (dots[:,0]<cos120) )[0],:]

        idxsAHA12 = np.hstack((idxsAHA12, s*np.ones(idxsAHA12.shape[0])[:, np.newaxis]))
        idxsAHA11 = np.hstack((idxsAHA11, s*np.ones(idxsAHA11.shape[0])[:, np.newaxis]))
        idxsAHA10 = np.hstack((idxsAHA10, s*np.ones(idxsAHA10.shape[0])[:, np.newaxis]))
        idxsAHA9  = np.hstack((idxsAHA9,  s*np.ones(idxsAHA9.shape[0] )[:, np.newaxis]))
        idxsAHA8  = np.hstack((idxsAHA8,  s*np.ones(idxsAHA8.shape[0] )[:, np.newaxis]))
        idxsAHA7 =  np.hstack((idxsAHA7,  s*np.ones(idxsAHA7.shape[0] )[:, np.newaxis]))
        
        AHASegMask[tuple(idxsAHA12.astype(int).T)] = 12
        AHASegMask[tuple(idxsAHA11.astype(int).T)] = 11
        AHASegMask[tuple(idxsAHA10.astype(int).T)] = 10
        AHASegMask[tuple(idxsAHA9.astype(int).T)]  = 9
        AHASegMask[tuple(idxsAHA8.astype(int).T)]  = 8
        AHASegMask[tuple(idxsAHA7.astype(int).T)]  = 7

    elif dots.shape[1] == 3 and s == ahaBaseSlice:

        idxsAHA6 = lvPoints[np.where( (dots[:,0]<=cos120) & (dots[:,1]<cos120) )[0],:]
        idxsAHA5 = lvPoints[np.where( (dots[:,1]<=cos120) & (dots[:,2]<cos120) )[0],:]
        idxsAHA4 = lvPoints[np.where( (dots[:,2]<=cos120) & (dots[:,0]>cos60)  )[0],:]
        idxsAHA3 = lvPoints[np.where( (dots[:,0]>=cos60)  & (dots[:,1]>cos60)  )[0],:]
        idxsAHA2 = lvPoints[np.where( (dots[:,1]>=cos60)  & (dots[:,2]>cos60)  )[0],:]
        idxsAHA1 = lvPoints[np.where( (dots[:,2]>=cos60)  & (dots[:,0]<cos120) )[0],:]

        idxsAHA6 = np.hstack((idxsAHA6, s*np.ones(idxsAHA6.shape[0])[:, np.newaxis]))
        idxsAHA5 = np.hstack((idxsAHA5, s*np.ones(idxsAHA5.shape[0])[:, np.newaxis]))
        idxsAHA4 = np.hstack((idxsAHA4, s*np.ones(idxsAHA4.shape[0])[:, np.newaxis]))
        idxsAHA3 = np.hstack((idxsAHA3, s*np.ones(idxsAHA3.shape[0])[:, np.newaxis]))
        idxsAHA2 = np.hstack((idxsAHA2, s*np.ones(idxsAHA2.shape[0])[:, np.newaxis]))
        idxsAHA1 = np.hstack((idxsAHA1, s*np.ones(idxsAHA1.shape[0])[:, np.newaxis]))
        
        AHASegMask[tuple(idxsAHA6.astype(int).T)] = 6
        AHASegMask[tuple(idxsAHA5.astype(int).T)] = 5
        AHASegMask[tuple(idxsAHA4.astype(int).T)] = 4
        AHASegMask[tuple(idxsAHA3.astype(int).T)] = 3
        AHASegMask[tuple(idxsAHA2.astype(int).T)] = 2
        AHASegMask[tuple(idxsAHA1.astype(int).T)] = 1

#Mark last segments: RV apex and ventricle and LV apex
AHASegMask[segMask==args.labelRV] = 19
for s in np.arange(apexRVSlice, apexRVCavitySlice+1):
    tmp = (segMask[:,:,s]==args.labelRV).nonzero()
    AHASegMask[:,:,s][tmp] = 18

for s in np.arange(apex, apexLVCavitySlice+1):
    tmp = (AHASegMask[:,:,s]==args.labelLV).nonzero()
    AHASegMask[:,:,s][tmp] = 17


if args.show:
    fig, axs = plt.subplots(1,3)
    axs[0].imshow(AHASegMask[:,:,ahaApicalSlice])
    axs[1].imshow(AHASegMask[:,:,ahaMidSlice])
    axs[2].imshow(AHASegMask[:,:,ahaBaseSlice])
    plt.show()  


# GET IJK-XYZ TRANSFORMATION-----------------------------------------------------------------
# Get initial shape and orientation
if args.flippedLA: 
    segMask    = np.rot90(segMask,    k=2, axes=(0,2))
    AHASegMask = np.rot90(AHASegMask, k=2, axes=(0,2))
if axisSA == 0:   
    segMask    = np.moveaxis(segMask,    [0,1,2], [-2,-1,-3])
    AHASegMask = np.moveaxis(AHASegMask, [0,1,2], [-2,-1,-3])
elif axisSA == 1: 
    segMask    = np.moveaxis(segMask,    [0,1,2], [-1,-3,-2])
    AHASegMask = np.moveaxis(AHASegMask, [0,1,2], [-1,-3,-2])
else: pass

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
ijkPixels = np.concatenate(( [ijkPixels[0]], [ijkPixels[1]], [ijkPixels[2]], [np.ones(ijkPixels[2].shape)] ))
points = np.matmul(ijk2Points, ijkPixels).T
points= points[:,:3]


#GET POINT_DATA ------------------------------------------------------------------------------------

# Get points differents regions in ijk segmentation domain
idxsLV = np.where(segMask==args.labelLV); idxsLV = np.array(idxsLV).T
for i in range(1,20):
    tmp  = np.where(AHASegMask==i)
    globals()["idxsAHA{}".format(i)] = np.array(tmp).T

#Get different regions idxs in xyz segmentation and add to point data
point_data = {}
ijkPixels = ijkPixels.T[:,:3]

#LVRV
idxsLV = isMemberIdxsRowWise(idxsLV, ijkPixels)
tmp = np.zeros(points.shape[0])
tmp[idxsLV] = 1
point_data["LVRV"] = tmp

#AHA segments
tmp = np.zeros(points.shape[0])
for i in range(1,20):
    tmpIdxs = globals()["idxsAHA{}".format(i)]
    tmpIdxs = isMemberIdxsRowWise(tmpIdxs,ijkPixels)
    tmp[tmpIdxs] = i
point_data["AHASegs"] = tmp

# Now that we have points in xyz and LVRV and AHASegs we can 
# interpolate (nearest neighbours) to complete the LV
idxsLV = (point_data["AHASegs"]==0).nonzero()
idxsAHA = np.where((point_data["AHASegs"]<=17) & (point_data["AHASegs"]!=0))
interAHA = griddata(points[idxsAHA], point_data["AHASegs"][idxsAHA], points[idxsLV], method='nearest')
point_data["AHASegs"][idxsLV] = interAHA

# SAVE VTK-----------------------------------------------------------------
cells = [
    ("line", [[0, 1]])    #this is just for being able to open with meshio afterwards
]

meshOut = meshio.Mesh(points, cells, point_data=point_data)
meshOut.write(args.outPath)