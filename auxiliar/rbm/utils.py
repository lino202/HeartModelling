
import numpy as np
from scipy.spatial.distance import cdist
from tqdm import tqdm
# import psutil

def isMemberIdxsRowWise(arr1, arr2, tol = 1E-6, showMem=False):
    if showMem: 
        print("Required Memory: {} GB".format(4 *(arr1.shape[0]) * (arr2.shape[0]) / 1e9))
    else:
        arr1 = np.reshape(arr1, (-1,3))
    idxs = np.min(cdist(arr2,arr1), axis=1) < tol
    return idxs.nonzero()[0]

def getHugeNearest(arr1, arr2, showMem=False, maxNumPoints=100):
    '''Gets the nearest memory efficiently'''

    reqMem = 4 *(arr1.shape[0]) * (arr2.shape[0]) / 1e9
    if showMem: print("Required Memory: {} GB".format(reqMem))
    # avaiMem = (psutil.virtual_memory().available / 1e9) * 1/3
    # maxNumPoints = (avaiMem * 1e9) / (4*arr2.shape[0])
    # if maxNumPoints > arr1.shape[0]: 
    #     maxNumPoints = arr1.shape[0] 
    # else: 
    #     maxNumPoints = int(np.floor(maxNumPoints))
    steps = int(np.ceil(arr1.shape[0] / maxNumPoints))
    idxsTot = np.array([])
    for i in tqdm(range(steps)):
        if i == steps-1:
            dist = cdist(arr1[i*maxNumPoints:, :], arr2, 'euclidean')
        else:
            dist = cdist(arr1[i*maxNumPoints:(i+1)*maxNumPoints, :], arr2, 'euclidean')

        idxs = np.argmin(dist, axis=1)
        idxsTot = np.concatenate((idxsTot, idxs), axis=0) if idxsTot.size else idxs

    return idxsTot

def readFibersfromElectraPre(filePath):
    rbmVersors = np.array([])
    with open(filePath) as file:
        data = file.readlines()

    cleanLinefromTxt = lambda x: np.array(x.split("\n")[0].split(",")).astype(float)
    rbmVersors = np.array(list(map(cleanLinefromTxt, data[4:])))
    return rbmVersors

def writeFibers4JSON(filePath, rbmVersors):
    with open(filePath, "w") as file:
        file.write('"fibers":[[{0:.15f}, {1:.15f}, {2:.15f}],\n'.format(rbmVersors[0,0], rbmVersors[0,1], rbmVersors[0,2]))
        for i in range(1,rbmVersors.shape[0]-1):
            file.write("\t\t\t[{0:.15f}, {1:.15f}, {2:.15f}],\n".format(rbmVersors[i,0], rbmVersors[i,1], rbmVersors[i,2]))
        file.write("\t\t\t[{0:.15f}, {1:.15f}, {2:.15f}]]".format(rbmVersors[-1,0], rbmVersors[-1,1], rbmVersors[-1,2]))