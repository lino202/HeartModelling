import os
import json 



dataPath = "/home/maxi/Documents/PhD/Code/purkinje/data/sampleMA_Control2/"
purkInitNodes =  os.path.join(dataPath, "purkInitNodes.json")

Nodes = {
    "Common_Nodes" : {
        "AV_Node" : [-8.47794,64.1918,26.9299],
        "HIS_Node" : [-8.47794,64.1918,21.9299], 
    },

    "RV_Nodes": {
        "Init": [-2.60798,59.3895,17.4008],
        "Join": [-1.68912,59.2179,15.8364],
        "RV_AS": [3.04967, 64.2201, 10.5169],
        "RV_SMA": [-0.765638, 58.1464, 10.0796],
    },

    "LV_Nodes": {
        "Init": [-15.5315,66.4473,16.8701],
        "Join": [-15.3283,66.4713,14.3907],
        "LV_ALS": [-12.3372,70.7359,12.7523],
        "LV_MS": [-10.9346,66.7419,4.87713],
        "LV_PI": [-20.3543,57.9508,-7.20526],
    }
}

# Select all the points for generating the bundle - Import nodes info
with open(purkInitNodes, 'w') as json_file:
  json.dump(Nodes, json_file, indent = 4, sort_keys=True)


