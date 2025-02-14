# We generate the new settings files for simulations of S2 from S1 in Electra

import os 
import argparse
import json
import copy


parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--filePath',type=str, required=True, help='path to data')
parser.add_argument('--outPath',type=str, required=True, help='path to data')
parser.add_argument('--S2_time',type=int, required=True, help='this might be sum to stim.start')
args = parser.parse_args()


with open(args.filePath, 'r') as file:
    data = json.load(file)

# Add load cell state
data['simulation']['load cells state'] = data['output']['cells state']


# Add new stimulus
data['tissue']['stimuli']['stimuli number'] = 2
data['tissue']['stimuli']['stimulus-2'] = copy.deepcopy(data['tissue']['stimuli']['stimulus-1'])
data['tissue']['stimuli']['stimulus-2']['id'] = 1
data['tissue']['stimuli']['stimulus-2']['start'] = args.S2_time + data['tissue']['stimuli']['stimulus-1']['start']
data['tissue']['stimuli']['stimulus-2']['cycle length'] = 100000
data['tissue']['stimuli']['stimulus-1']['cycle length'] = 100000

# Change simulation time 
data['physics']['reaction-diffusion']['simulation time'] = args.S2_time + data['tissue']['stimuli']['stimulus-1']['start'] + 1000

# Change savings
results_folder = args.outPath.split('/')[-1].split('.')[0].split('_')
results_folder[0] = 'results'
results_folder = '_'.join(results_folder)

for key in data['output']['ensight'].keys():
    for key2 in data['output']['ensight'][key].keys():
        tmp = data['output']['ensight'][key][key2]
        tmp = tmp.split('/')
        tmp[-3] = results_folder
        tmp.insert(10, 'S2_{0}'.format(args.S2_time))
        tmp = '/'.join(tmp)
        data['output']['ensight'][key][key2] = tmp

tmp = data['output']['cells state']
tmp = tmp.split('/')
tmp[-2] = results_folder
tmp.insert(10, 'S2_{0}'.format(args.S2_time))
tmp = '/'.join(tmp)
data['output']['cells state'] = tmp

# Write the updated JSON back to the file
with open(args.outPath, 'w') as file:
    json.dump(data, file, indent=4)



