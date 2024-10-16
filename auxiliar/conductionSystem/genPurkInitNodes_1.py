import os
import json 
import argparse

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--data_path',type=str, required=True, help='path to data')
parser.add_argument("--av_node", type=float, required=True, nargs=3, help="av node coords 3D")
parser.add_argument("--his_node", type=float, required=True, nargs=3, help="his node coords 3D")
parser.add_argument("--rv_init_node", type=float, required=True, nargs=3, help="first rv node coords 3D in the endo surface")
parser.add_argument("--rv_join_node", type=float, required=True, nargs=3, help="rv bifurcation node coords 3D in the endo")
parser.add_argument("--rvb", type=float, required=True, nargs=3, help="rvb endpoint")
parser.add_argument("--lv_init_node", type=float, required=True, nargs=3, help="first lv node coords 3D in the endo surface")
parser.add_argument("--lv_join_node", type=float, required=True, nargs=3, help="lv bifurcation node coords 3D in the endo")
parser.add_argument("--lva", type=float, required=True, nargs=3, help="lva endpoint")
parser.add_argument("--lvp", type=float, required=True, nargs=3, help="lvp endpoint")
# parser.add_argument("--lvs", type=float, required=True, nargs=3, help="lv septum endpoint")
args = parser.parse_args()

purkInitNodes =  os.path.join(args.data_path, "purkInitNodes.json")

Nodes = {
    "Common_Nodes" : {
        "AV_Node" : args.av_node,
        "HIS_Node" : args.his_node, 
    },

    "RV_Nodes": {
        "Init": args.rv_init_node,
        "Join": args.rv_join_node,
        "rvb": args.rvb,
    },

    "LV_Nodes": {
        "Init": args.lv_init_node,
        "Join": args.lv_join_node,
        "lva": args.lva,
        "lvp": args.lvp,
        # "lvs": args.lvs,
    }
}

# Select all the points for generating the bundle - Import nodes info
with open(purkInitNodes, 'w') as json_file:
  json.dump(Nodes, json_file, indent = 4, sort_keys=True)


