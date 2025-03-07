import os 
import numpy as np
import argparse
import meshio
from scipy.spatial import KDTree


import os
import sys
sys.path.append(os.path.join(os.path.dirname(sys.path[0])))
from auxiliar.rbm.utils import writeFibers4JSON

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--meshNoScar',type=str, required=True, help='path to data')
parser.add_argument('--meshFibers',type=str, required=True)
parser.add_argument('--outPath',type=str, required=True)
args = parser.parse_args()

meshNoScar = meshio.read(args.meshNoScar)
meshFibers = meshio.read(args.meshFibers)

#Compute normals from mesh heart for patch points
tree = KDTree(meshFibers.points)
_ , idxs = tree.query(meshNoScar.points, k=1)

fibers = meshFibers.point_data['fibers_rbmlongmyo_randompatch'][idxs,:]
meshNoScar.point_data['fibers_rbmlongmyo_randompatch'] = fibers

#Save
meshNoScar.write(args.meshNoScar)
writeFibers4JSON(os.path.join(args.outPath, "fibers_rbmlongmyo_randompatch.json"), fibers)