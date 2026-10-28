#Modify the files to be used in OpenCARP
import meshio
import argparse
import os
import numpy as np
import utils as ut
import time
import matplotlib.pyplot as plt
import seaborn as sns
# import nanomesh

def main():
    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument('--mesh_path',        type=str, required=True)
    parser.add_argument('--unit',            type=str, required=True)
    parser.add_argument('--out_path',        type=str, required=True)
    parser.add_argument('--cellType',        type=str, default="tetra")

    # parser.add_argument('--cellType',        type=str, default="tetra")
    # parser.add_argument('--stimPointData',   type=str)
    # parser.add_argument('--fibersPointData', type=str)
    # parser.add_argument('--layersPointData', type=str)
    # parser.add_argument('--outFolder',       type=str, required=True)
    # parser.add_argument('--elemData',       type=str, required=False)
    # parser.add_argument('--groundPointData', action='store_true', help='To choose a ground point for bidomain simulations')

    
    # parser.add_argument('--save' ,action='store_true',  help='save histogram tags')
    
    args = parser.parse_args()

    # --mesh_path         #Complete path to the mesh with the fibers and pacing sites
    # --unit              #Units of the mesh.  cm, mm or um
    # --cellType          #Cell type. Default value is tetra 
    # --stimPointData     #Name of the field with the Points where the stimuli will start. Right now only add 1 stimulus
    # --fibersPointData   #Point data for fiber orientation
    # --layersPointData   #Maxi removed it
    # --outFolder         #Path for results
    #--elemData           #Data in points to be included as element tags in the .elem file
    

    #Open mesh
    mesh = meshio.read(args.mesh_path)
    if not os.path.isdir(args.out_path): 
        os.mkdir(args.out_path)
        print("Directory creates :",args.out_path)
    # fileName2Use = args.mesh_path.split(".")[0].split("/")[-1]

    ht=os.path.split(args.mesh_path)
    fileName2Use=str(ht[1]).split(".")[0]
    # fileName2Use = ht[1](".")[0].split("/")[-1]
    
    #Switch to um as opencarp only seems to support that
    if args.unit=="cm":
        mesh.points = mesh.points * 10000
    elif args.unit=="mm":
        mesh.points = mesh.points * 1000
    elif args.unit=="um":
        pass
    else: raise ValueError("Only units in cm, mm or um are supported")

    newNameMesh=os.path.join(args.out_path,fileName2Use+"_micrometers."+ht[1].split(".")[-1])
    mesh.write(newNameMesh)

    




if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))