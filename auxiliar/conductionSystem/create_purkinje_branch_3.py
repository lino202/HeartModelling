# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 11:02:34 2015
@author: fsc
"""

from lib.FractalTree import *
from lib.parameters import Parameters
# from lib.utils import loadInp
import numpy as np
import os 
import meshio

dataPath = "/home/maxi/Documents/PhD/Data/DTI_hearts/Data_Electra_DWI/sampleLE_Control2/stim/stim_cs"
bb_infile    = os.path.join(dataPath, 'mainCSBundle.inp')
surf_file    = os.path.join(dataPath, 'rv_endo.obj')
output_path  = os.path.join(dataPath, 'finalBundles')
if not os.path.isdir(output_path): os.mkdir(output_path)
endnode_name = "RV_SMA_end"
output_file  = os.path.join(output_path, endnode_name.split('_end')[0])

if not os.path.isdir(output_path):
    os.mkdir(output_path)


# Load bundle tree
mesh = meshio.read(bb_infile)
vertexs = mesh.points
connectivity = mesh.cells[0][1]
nsets = mesh.point_sets
# vertexs, connectivity, nsets = loadInp(bb_infile)

# Get branch end node
end_node = vertexs[nsets[endnode_name][0]]

# Find previous node to end_node
prev_node = []
for el in connectivity:
    if (el[1] == nsets[endnode_name][0]):
        prev_node = vertexs[el[0]]

# Get tree growing direction
grow_dir = (prev_node-end_node) / np.linalg.norm(end_node-prev_node)
next_node = end_node - grow_dir

# Create Fractal tree parameters
param = Parameters()
param.setLength(2.7)
param.setSegLength(0.3)
param.setAngle(0.15)
param.setIterations(10)

# Compute purkinje tree for RBB
param.setMeshfile(surf_file)
param.setFilename(output_file)
param.setInitNode(end_node)
param.setSecondNode(next_node)
print("Computing purkinje network")
branches, nodes = Fractal_Tree_3D(param)



pass
