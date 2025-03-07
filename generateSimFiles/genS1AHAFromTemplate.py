# We generate the new settings files for simulations of S1 but using a template settings where we only change the stimAHA

import argparse
import json
import copy


parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--templatePath',type=str, required=True, help='path to data')
parser.add_argument('--stimAHA',type=int, required=True, help='path to data')
args = parser.parse_args()


with open(args.templatePath, 'r') as file:
    data = json.load(file)

# Change stimulus
data['tissue']['stimuli']['stimulus-1']['nodeset'] = "stim_nodes_aha{}".format(args.stimAHA)



# Change savings
results_folder = args.templatePath.split('/')[-1].split('.')[0].split('_')
results_folder[4] = 'stimAHA{}'.format(args.stimAHA)
settingsName = copy.deepcopy(results_folder)
settingsPath = args.templatePath.split('/')[:-1]

results_folder[0] = 'results'

results_folder = '_'.join(results_folder)
settingsName = '_'.join(settingsName)
settingsPath.append(settingsName)
settingsPath = '/'.join(settingsPath) + '.json'

for key in data['output']['ensight'].keys():
    for key2 in data['output']['ensight'][key].keys():
        tmp = data['output']['ensight'][key][key2]
        tmp = tmp.split('/')
        tmp[-3] = results_folder
        tmp = '/'.join(tmp)
        data['output']['ensight'][key][key2] = tmp

tmp = data['output']['cells state']
tmp = tmp.split('/')
tmp[-2] = results_folder
tmp = '/'.join(tmp)
data['output']['cells state'] = tmp

# Write the updated JSON back to the file
with open(settingsPath, 'w') as file:
    json.dump(data, file, indent=4)



