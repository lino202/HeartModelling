# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 11:02:34 2015
@author: fsc
"""

from lib.FractalTree import *
from lib.parameters import Parameters
import numpy as np
import os 
import meshio
import argparse

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--data_path',type=str, required=True, help='path to data')
parser.add_argument('--endnode_name',type=str, required=True, help='endnode name in .inp file for Purk tree computation')
parser.add_argument('--length',type=float, required=True, help='length for tree calculation, see Paper')
parser.add_argument('--seglength',type=float, required=True, help='seglength for tree calculation, see Paper')
parser.add_argument('--angle',type=float, required=True, help='angle for tree calculation, see Paper')
parser.add_argument('--iterations',type=int, required=True, help='iterations for tree calculation, see Paper')
args = parser.parse_args()

dataPath = args.data_path
endnode_name = args.endnode_name

bb_infile    = os.path.join(dataPath, 'mainCSBundle.inp')
surf_file    = os.path.join(dataPath, '{}_endo.obj'.format('rv' if "rv" in endnode_name else 'lv'))
output_path  = os.path.join(dataPath, 'finalBundles')
if not os.path.isdir(output_path): os.mkdir(output_path)
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
param.setLength(args.length)
param.setSegLength(args.seglength)
param.setAngle(args.angle)
param.setIterations(args.iterations)

# Compute purkinje tree for RBB
param.setMeshfile(surf_file)
param.setFilename(output_file)
param.setInitNode(end_node)
param.setSecondNode(next_node)
print("Computing purkinje network")
branches, nodes = Fractal_Tree_3D(param)