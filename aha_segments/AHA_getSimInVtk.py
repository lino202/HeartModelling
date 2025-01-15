# this gets the pacing nodes corresponding to the endocardium of the AHA segments
import argparse
import meshio
import numpy as np
# import os

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--meshIn',type=str, required=True, help='path to data')
parser.add_argument('--outPath',type=str, required=True, help='path to data')
args = parser.parse_args()

mesh = meshio.read(args.meshIn)

stim_all_AHA = np.zeros(mesh.points.shape[0])
for key in mesh.point_data.keys():
    if 'stim_AHA' in key:
        idxs = np.where(mesh.point_data[key]==1)[0]
        stim_all_AHA[idxs] = int(key.split('stim_AHA')[-1])

mesh.point_data['stim_all_AHA'] = stim_all_AHA
mesh.write(args.outPath)