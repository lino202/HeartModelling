'''
Get labels of points with each label to create file for igbextract

'''


import pyvista as pv
import numpy as np
import argparse
import os
import time
import utils as ut
import sys
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument('--mesh_path',      type=str, required=True, help='path to mesh')
    parser.add_argument('--mesh_name',      type=str, required=True, help='name of mesh with the end')
    parser.add_argument('--vm_path_input',     type=str, required=True, help='path to vm, result of openCARP')
    parser.add_argument('--simulation_number',     type=str, required=True, help='path to vm, result of openCARP')
    parser.add_argument('--cellType',        type=str, default="tetra")
    # parser.add_argument('--time_steps',type=int,help='time steps to plot results')
    parser.add_argument('--data_label_compare',    type=str, required=True, help="Labels of where to get the zones")
    parser.add_argument('--labels_compare',   nargs='+',    type=int, required=True, help="Labels of zones to get the APs and compare")
    parser.add_argument('--type_remove_label', type=str, default="cell", help="If the remove label is in the elem(cell)Data or the pointData. Options=cell or point")
    parser.add_argument('--output_name', type=str, help="Name txt file")
    
    
    args = parser.parse_args()

    #Load mesh
    meshName=os.path.join(args.mesh_path, args.mesh_name)
    mesh = pv.read(meshName)

    meshName_use=args.mesh_name.split(".vtk")[0]

    #Get points

    if args.type_remove_label=="cell":
        layersPoints=np.asarray(mesh.cell_data[args.data_label_compare])

    elif args.type_remove_label=="point":

        #Convert to elems to see which elements to remove
        layersPoints=mesh.point_data[args.data_label_compare]

    else:
        print("Error in type_remove_label")

    outArray = np.empty((len(args.labels_compare), 2,)) * np.nan
   
    for index, labels_aux in enumerate(args.labels_compare):
        #Find Aps in that section

        indexLabel=np.where(layersPoints == labels_aux)
        indexLabel_aux=indexLabel[0][0]

        outArray[index,:]=[labels_aux, indexLabel_aux]

    

    # my_string = ','.join(map(str, map(int,outArray[:,1]))) 


    node_file_name = "nodes_" + args.output_name +"_" +meshName_use+".txt"
    node_file_name_comp=os.path.join(args.mesh_path, node_file_name)

    np.savetxt(node_file_name_comp, outArray[:,1], fmt='%d', delimiter=' ', newline='\n', header='', footer='', comments='# ', encoding=None)


    # #Save files
    # with open(node_file_name_comp, "w") as f:
    #     f.write("Woops! I have deleted the content!")

    node_file_name = "nodes_" + args.output_name + "_" +meshName_use+"_def.txt"
    node_file_name_comp=os.path.join(args.mesh_path, node_file_name)
    np.savetxt(node_file_name_comp, outArray, fmt='%d', delimiter=' ', newline='\n', header='', footer='', comments='# ', encoding=None)

    

    



if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))