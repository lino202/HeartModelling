# this gets the tetmesh that usually has the complete mesh (with scar) for generating th inp
# fibers and layers must be present
 
import argparse
import meshio
import numpy as np
import os
import sys
sys.path.append(os.path.join(os.path.dirname(sys.path[0])))
from miscellaneous.regions import patch_flag, regions
from auxiliar.rbm.utils import writeFibers4JSON

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--dataFolder',type=str, required=True, help='path to data')
args = parser.parse_args()

meshVtk = meshio.read(os.path.join(args.dataFolder, 'tetmesh.vtk'))
layers = meshVtk.point_data['layers']

nsets = {}
for key in regions.keys():
    nsets[key.replace('flag', 'nodes')] = np.where(layers==regions[key])[0]
nsets['patch_nodes'] = np.where(layers==patch_flag)[0]

fibers = meshVtk.point_data['fibers_rbmlongmyo_randompatch']

#SAVE
meshInp = meshio.Mesh(meshVtk.points, meshVtk.cells, point_sets=nsets)
meshInp.write(os.path.join(args.dataFolder, 'tetmesh.inp'))
writeFibers4JSON(os.path.join(args.dataFolder, "fibers_rbmlongmyo_randompatch_tetmesh.json"), fibers)
