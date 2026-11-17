#Get elem and node quantity
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
    parser.add_argument('--mesh_name',        type=str, required=True)
    parser.add_argument('--mesh_format',        type=str, default="vtk")
    parser.add_argument('--cell_type',        type=str, default="tetra")
    # parser.add_argument('--save' ,action='store_true',  help='save histogram tags')
    
    args = parser.parse_args()

    # --mesh_path         #Complete path to the mesh with the fibers and pacing sites
    # --unit              #Units of the mesh.  cm, mm or um
    # --cell_type          #Cell type. Default value is tetra 
    # --stimPointData     #Name of the field with the Points where the stimuli will start. Right now only add 1 stimulus
    # --fibersPointData   #Point data for fiber orientation
    # --layersPointData   #Maxi removed it
    # --outFolder         #Path for results
    #--elemData           #Data in points to be included as element tags in the .elem file

    ht=os.path.split(args.mesh_path)
    

    #Open mesh
    if args.mesh_format=='vtk':
        elemFile=os.path.join(args.mesh_path,args.mesh_name+".vtk")
        mesh = meshio.read(elemFile)
        elems=mesh.cells_dict[args.cell_type]
        elemQuantity=elems.shape[0]

        points=mesh.points
        pointsQuantity=points.shape[0]
        
    elif args.mesh_format=='carp_txt':

        elemFile=os.path.join(args.mesh_path,args.mesh_name+".elem")

        data = np.loadtxt(elemFile, skiprows=1, usecols=range(1,6), dtype=int)
        elemMatrix=data[:,:-1]
        tagMatrix=data[:,-1]

        # Open the .pts
        pointFile=os.path.join(args.mesh_path,args.mesh_name+".pts")
        pointMatrix = np.loadtxt(pointFile, skiprows=1, dtype=float)

        elemQuantity=elemMatrix.shape[0]

        pointsQuantity=pointMatrix.shape[0]
    else:
        print("Format not found-------------")



    #Save cells in carp format
    print("Getting quantities-------------")
    outName=os.path.join(args.mesh_path,args.mesh_name+"_size.txt")
    with open(outName, 'w') as f:
        f.write("{}\n".format(args.mesh_path))   
        f.write("{}\n".format(args.mesh_name))   
        f.write("Number of elements: {}\n".format(elemQuantity))
        f.write("Number of points: {}\n".format(pointsQuantity))
        # f.write("{}\n".format(stimType))                         #For now it seems ok to only have Intra
        # vtxs = list(map(lambda x: "{:d}\n".format(x),list(arr)))
        # f.writelines(vtxs)


if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))