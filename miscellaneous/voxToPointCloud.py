'''We get a point cloud with some point-wise definitions/data from a voxelized data
This was serves majorly for dwi voxelized maps where we have myo healthy and scar, so we can have a point cloud
for interpolation in a real 3D tet mesh'''

import nrrd 
import os 
import argparse
import meshio
import numpy as np

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--dataPath',type=str, required=True, help='path to data')
parser.add_argument('--name'    ,type=str, required=True)
args = parser.parse_args()

myo_flag = 1
scar_flag = 2

bivArr, bivHeader = nrrd.read(os.path.join(args.dataPath, "{}.nrrd".format(args.name)))
space = bivHeader['space']
spaceOrigin = np.concatenate((bivHeader['space origin'],[1]))
ijk2Points = np.zeros((4,4))
ijk2Points[:3,:3] = bivHeader['space directions'].T
ijk2Points[:,3] =  spaceOrigin

#here it should not matter as we do not have dwi in a probable different space, but still checks
if space != "left-posterior-superior": raise ValueError("Wrong space?") 

# as s2_estimateDti we need to add points to the .vtk in xyz coordinates with the ijk2xyz matrix
ijkPixels = np.where(bivArr!=0)
tissueFlags = bivArr[ijkPixels]
ijkPixels = np.concatenate(( [ijkPixels[0]], [ijkPixels[1]], [ijkPixels[2]], [np.ones(ijkPixels[2].shape)] ))
points = np.matmul(ijk2Points, ijkPixels).T
points= points[:,:3]

tmp = np.zeros(tissueFlags.shape)
tmp[tissueFlags==scar_flag] = 1

meshOut = meshio.Mesh(points, [("line", [[0,1]])], point_data={"scar_nodes": tmp}) # we add a line just for being able to read back with meshio
meshOut.write(os.path.join(args.dataPath, "{}.vtk".format(args.name)))