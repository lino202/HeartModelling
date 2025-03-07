# this gets the patch nodes into the inp, as the cleanScar script does not take this into account
 
import argparse
import meshio
import numpy as np
import os
import sys
sys.path.append(os.path.join(os.path.dirname(sys.path[0])))
from miscellaneous.regions import patch_flag

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--meshNoScarVtk',type=str, required=True, help='path to data')
parser.add_argument('--meshNoScarInp',type=str, required=True, help='path to data')
args = parser.parse_args()

meshNoScarVtk = meshio.read(args.meshNoScarVtk)
meshNoScarInp = meshio.read(args.meshNoScarInp)

meshNoScarInp.point_sets['patch_nodes'] = np.where(meshNoScarVtk.point_data['layers'] == patch_flag)[0]

#SAVE
meshNoScarInp.write(args.meshNoScarInp)
