#transform stim points to vtx file for opencarp

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
    parser.add_argument('--mesh_data_path',        type=str, required=True)
    parser.add_argument('--outFolder',       type=str, required=True)
   
    args = parser.parse_args()

    # --mesh_data_path         #Complete path to the mesh with the fibers and pacing sites
    # --unit              #Units of the mesh.  cm, mm or um
    # --cellType          #Cell type. Default value is tetra 
    # --stimPointData     #Name of the field with the Points where the stimuli will start. Right now only add 1 stimulus
    # --fibersPointData   #Point data for fiber orientation
    # --layersPointData   #Maxi removed it
    # --outFolder         #Path for results
    #--elemData           #Data in points to be included as element tags in the .elem file

    ht=os.path.split(args.mesh_data_path)
    

    #Open mesh
    mesh = meshio.read(args.mesh_data_path)
    if not os.path.isdir(args.outFolder): os.mkdir(args.outFolder)
    # fileName2Use = args.mesh_data_path.split(".")[0].split("/")[-1]
    fileName2Use=str(ht[1]).split(".")[0]
    # fileName2Use = ht[1](".")[0].split("/")[-1]
    
    
    fields = list(mesh.point_data.keys())
    for fd in fields:
        if "stim" in fd: #Search for word stim and asume they are stimulus points
            print("Getting stim nodes as vtx file -------------")
            tmp = mesh.point_data[fd]
            tmp = (tmp==1).nonzero()[0]
            # ut.writeStimVtxFile(tmp, os.path.join(args.outFolder, "{}.vtx".format(fd)))
            ut.writeStimVtxFile(tmp, os.path.join(args.outFolder, "{}_{}.vtx".format(fd,fileName2Use)),"extra")

                


    print("Finished:",args.mesh_data_path)

 

if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))