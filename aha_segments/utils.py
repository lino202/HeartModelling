import numpy as np
import warnings
import cv2 as cv
from scipy.spatial.distance import cdist
from skimage.morphology import skeletonize
from skan import Skeleton, summarize
from scipy.spatial.transform import Rotation as R

def getBaseApexSA(arr):
    assert (np.nanmax(arr) > 0 and np.nanmin(arr)==0 and arr.ndim==3)
    axisSA = np.argmin(arr.shape)
    if axisSA !=2: warnings.warn("SA images are not in the third array axis")
    saIdxs = np.where(arr!=0)[axisSA]
    return np.max(saIdxs), np.min(saIdxs)


def getSAHeartContours(img, s):
    rgb = cv.cvtColor(img.astype(np.uint8), cv.COLOR_GRAY2RGB)
    tmp = cv.cvtColor(rgb, cv.COLOR_BGR2GRAY)
    conts, hier = cv.findContours(tmp, cv.RETR_TREE, cv.CHAIN_APPROX_TC89_KCOS)
    if len(conts) >3: 
        raise ValueError("wrong contours, Segmentation is correct or is there a patology? in slice {}".format(s))
    return conts, hier


def getMainAxisAHAByDistance(centroid, img):
    skel = skeletonize(img, method="lee")
    idxsSkel = np.where(skel!=0)
    skelPoints = np.concatenate(( [idxsSkel[0]], [idxsSkel[1]])).T
    distantPoint = skelPoints[np.argmax(cdist(centroid[np.newaxis,:], skelPoints)),:]
    axis = distantPoint - centroid
    axisMag = np.linalg.norm(axis)
    return axis / np.hstack((axisMag,axisMag))

def getMainAxisAHAByRVInsertions(centroid, img):
    skel = skeletonize(img, method="lee")
    branch_data = summarize(Skeleton(skel))
    if np.any(branch_data["branch-type"].to_numpy() != np.array([2,2,2])):
        raise ValueError("Seems that skeleton is not correct as branches are not only joint-to-joint, please check")
    joint1 = np.array([branch_data["image-coord-src-0"].to_numpy()[0], branch_data["image-coord-src-1"].to_numpy()[0]]).astype(int)
    joint2 = np.array([branch_data["image-coord-dst-0"].to_numpy()[0], branch_data["image-coord-dst-1"].to_numpy()[0]]).astype(int)

    axis1 = joint1 - centroid; axis1 = axis1 / np.linalg.norm(axis1)
    axis2 = joint2 - centroid; axis2 = axis2 / np.linalg.norm(axis2)
    angle = np.arccos(np.dot(axis1, axis2))/2
    
    normal = np.array([0, 0, 1])
    rotations = R.from_rotvec(angle * normal)
    return rotations.apply(np.array([axis2[0], axis2[1],0]))[:2]
