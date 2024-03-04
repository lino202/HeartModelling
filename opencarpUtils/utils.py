import numpy as np

meshioOCCellsMap = {"tetra": "Tt", "line": "Ln"}

def writeStimVtxFile(arr, outName, stimType="Intra"):
    with open(outName, 'w') as f:
        f.write("{0:d}\n".format(arr.shape[0]))
        f.write("{}\n".format(stimType))                         #For now it seems ok to only have Intra
        vtxs = list(map(lambda x: "{:d}\n".format(x),list(arr)))
        f.writelines(vtxs)

def getArrNormalization(arr):
    if arr.shape[1]!=3: raise ValueError("Only work with nx3 arrays, for 3D vecs normalization")
    arrMag = np.expand_dims(np.linalg.norm(arr, axis=1), axis=1)
    return arr / np.hstack((arrMag,arrMag,arrMag))

def writeFibsFile(arr, outName, nFibs=1):
        with open(outName, 'w') as f:
            f.write("{0:d}\n".format(nFibs))
            if nFibs==1:
                fibs = list(map(lambda x: "{0:f} {1:f} {2:f}\n".format(x[0], x[1], x[2]),list(arr)))
            else:
                raise ValueError("Wrong fibs direction number") 
            f.writelines(fibs)


def writePointsFile(arr, outName):
        with open(outName, 'w') as f:
            f.write("{0:d}\n".format(arr.shape[0]))
            pts = list(map(lambda x: "{0:f} {1:f} {2:f}\n".format(x[0], x[1], x[2]),list(arr)))
            f.writelines(pts)


def writeCellsFile(arr, outName, cellType="Tt", tags=1):
        with open(outName, 'w') as f:
            f.write("{0:d}\n".format(arr.shape[0]))
            if cellType=="Tt":
                cells = list(map(lambda x: "{0:s} {1:d} {2:d} {3:d} {4:d} {5:d}\n".format(cellType, x[0], x[1], x[2], x[3], tags),list(arr)))
            elif cellType=="Ln":
                cells = list(map(lambda x: "{0:s} {1:d} {2:d} {3:d}\n".format(cellType, x[0], x[1], tags),list(arr)))
            else: raise ValueError("Wrong cell type")
            f.writelines(cells)


