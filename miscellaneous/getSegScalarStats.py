"""Here we get statistics for scalar maps obtained from dti with the segemetation of the myo and scar,
usually ADC and FA maps obtained with Slicer. The segmentation needs to be a label in order to save both
the scalar map and the label as .nii and the label should have 0 values as background, 1 as myo, 2 as scar
not used overlapped combination of both cause only one value will be saved"""

import numpy as np
import os
import argparse
import nibabel as nib
import matplotlib.pyplot as plt
from utils import calculateBoxPlotParams, printUsefulStats

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--scalarMapPath',type=str, required=True, help='path to file and file name')
parser.add_argument('--labelMapPath',type=str, required=True, help='path to file and file name')
parser.add_argument('--nameData1',type=str, required=True, help='name of data in label map with value 1')
parser.add_argument('--nameData2',type=str, required=True, help='name of data in label map with value 2')
parser.add_argument('--outPath',type=str, required=True, help='path to output folder')
parser.add_argument('--outType',type=str, required=True, help='png or pdf or any supported')
parser.add_argument('--histSteps',type=int, required=True, help='steps for creating hist bins')
args = parser.parse_args()

mapType = args.scalarMapPath.split("/")[-1].split(".nii")[0]
scalarMapData = nib.load(args.scalarMapPath)
scalarMapArray = scalarMapData.get_fdata()

labelMapData = nib.load(args.labelMapPath)
labelMapArray = labelMapData.get_fdata()

slices = np.linspace(0, scalarMapArray.shape[2]-1,30).astype(int)
zeros = np.zeros(scalarMapArray.shape)
zeros[np.where(labelMapArray>0)] = 1
tmp = scalarMapArray + zeros
f = plt.figure()
for i, s in enumerate(slices):
    ax = f.add_subplot(5,6,i+1)
    ax.imshow(tmp[:,:,s])
plt.show(block=True)


data1 = scalarMapArray[np.where(labelMapArray==1)]
data2 = scalarMapArray[np.where(labelMapArray==2)]
print(args.nameData1)
printUsefulStats(data1)
print(args.nameData2)
printUsefulStats(data2)

dataMin = np.min(np.array([np.min(data1), np.min(data2)]))
dataMax = np.max(np.array([np.max(data1), np.max(data2)]))
bins = np.linspace(dataMin, dataMax, args.histSteps)
fig, ax = plt.subplots()
ax.hist(data1, bins, alpha=0.5, label=args.nameData1, color = (0.2039,0.2039, 0.2039), ec = (0.2039,0.2039, 0.2039))
ax.hist(data2, bins, alpha=0.5, label=args.nameData2, color = (0.3334,0.6667, 1.0), ec = (0.3334,0.6667, 1.0))
ax.set_ylabel("Frequency")
ax.set_xlabel(mapType)
ax.legend(loc='upper right')
# ax.axis("off")
plt.savefig(os.path.join(args.outPath,'hist_{}.{}'.format(mapType, args.outType)), transparent=False)
plt.show()

data = [data1, data2]
fig, ax = plt.subplots()
ax.boxplot(data, labels=[args.nameData1, args.nameData2])
ax.set_ylabel(mapType)
plt.savefig(os.path.join(args.outPath,'boxplot_{}.{}'.format(mapType, args.outType)), transparent=False)
plt.show()


