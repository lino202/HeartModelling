import os
import json 



dataPath = "/home/maxi/Documents/PhD/Data/DTI_hearts/Data_Electra_DWI/sampleLE_Control2"
purkInitNodes =  os.path.join(dataPath, 'stim', 'stim_cs', "purkInitNodes.json")

Nodes = {
    "Common_Nodes" : {
        "AV_Node" : [-20.745,-51.8293,23.3676],
        "HIS_Node" : [-20.745,-51.8293,18.3676], 
    },

    "RV_Nodes": {
        "Init": [-25.5579,-49.9371,15.1669],
        "Join": [-25.8922, -49.3078, 13.5586],
        "RV_AS": [-26.6508, -60.1452, 2.50581],
        "RV_SMA": [-26.3031, -48.5599, 8.67955],
    },

    "LV_Nodes": {
        "Init": [-15.3299,-52.1873,15.3401],
        "Join": [-14.14,-51.3193,12.8821],
        "LV_ALS": [-13.066,-58.4558,9.47285],
        "LV_MS": [-7.74579,-50.3277,3.29272],
        "LV_PI": [-3.35402,-37.6051,5.49655],
    }
}

# Select all the points for generating the bundle - Import nodes info
with open(purkInitNodes, 'w') as json_file:
  json.dump(Nodes, json_file, indent = 4, sort_keys=True)


