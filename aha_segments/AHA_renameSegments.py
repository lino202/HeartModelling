# this gets change the naming in the .vtk and .inp mesh files of the AHA segments according to an excel info and save a copy 
# it is useful if you have an error or simply want to rename the segments
import argparse
import meshio
import numpy as np
import os
import copy 

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--meshFolder',type=str, required=True, help='path to data')
parser.add_argument('--meshInName',type=str, required=True)
parser.add_argument('--meshOutName',type=str, required=True)
parser.add_argument('--inSegmentNumbers',type=int, nargs='+', required=True)
parser.add_argument('--outSegmentNumbers',type=int, nargs='+', required=True)
args = parser.parse_args()

# Read meshes
meshVtk = meshio.read(os.path.join(args.meshFolder, '{}.vtk'.format(args.meshInName)))
meshInp = meshio.read(os.path.join(args.meshFolder, '{}.inp'.format(args.meshInName)))

new_point_data = copy.deepcopy(meshVtk.point_data)
new_point_sets = copy.deepcopy(meshInp.point_sets)

# delete old keys
for inSeg in args.inSegmentNumbers:
    key_in = 'stim_nodes_aha{}'.format(inSeg)
    new_point_data.pop(key_in)
    new_point_sets.pop(key_in)

# add new ones
for inSeg, outSeg in zip(args.inSegmentNumbers, args.outSegmentNumbers):
    key_in = 'stim_nodes_aha{}'.format(inSeg)
    key_out = 'stim_nodes_aha{}'.format(outSeg)
    if key_in in meshVtk.point_data.keys():
        new_point_data[key_out] = meshVtk.point_data[key_in]
    if key_in in meshInp.point_sets.keys():
        new_point_sets[key_out] = meshInp.point_sets[key_in]


# Write meshes
meshVtk.point_data = new_point_data
meshInp.point_sets = new_point_sets
meshVtk.write(os.path.join(args.meshFolder, '{}.vtk'.format(args.meshOutName)))
meshInp.write(os.path.join(args.meshFolder, '{}.inp'.format(args.meshOutName)))