'''
Here it is to plot the vm results of the APs
'''


import pyvista as pv
import numpy as np
import argparse
import os
import time
import utils as ut
import sys
import pandas as pd
import glob
import re
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument('--APs_paths',  type=str, nargs='*', required=True, help='Path to APs to compare, they need to be with the same timestep')
    parser.add_argument('--out_path',  type=str, required=True, help='Path to save img')
    
    
 

    # parser.add_argument('--mesh_name',      type=str, required=True, help='name of mesh with the end')
    # parser.add_argument('--vm_path_input',     type=str, required=True, help='path to vm, result of openCARP')
    # parser.add_argument('--simulation_number',     type=str, required=True, help='path to vm, result of openCARP')
    # parser.add_argument('--cellType',        type=str, default="tetra")
    # parser.add_argument('--time_steps',type=int,help='time steps to plot results')
    
    args = parser.parse_args()

    for file_path in args.APs_paths:

        try:
            # Assuming data is in a structured format like CSV or similar
            df = pd.read_csv(file_path[0], delimiter='\t')
            # Process the DataFrame
            print(df)

        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

        # dataaux = np.array(df._values[:,16], dtype='O')
        dataaux = np.array(df._values, dtype='O')
        data=dataaux[:,:-1]

        fig1, ax1 = plt.subplots()
        for colaux in np.arange(data.shape[1]):

            ax1.plot(data[:,colaux],label=str(colaux))
        ax1.legend(loc="upper left")
        fig1.show()

        fig1, ax1 = plt.subplots()
        ax1.plot(data[:,16],label="Vm")
        ax1.legend(loc="upper left")
        fig1.show()

    #

    # meshName=os.path.join(args.mesh_path, args.mesh_name)
    # mesh = pv.read(meshName)

    # vm_path=os.path.join(args.vm_path_input,args.simulation_number)
    # vmName=os.path.join(vm_path,"vm_"+ args.simulation_number + ".txt")

    # vm_values = np.loadtxt(vmName)

    # assert vm_values.shape[1] == mesh.n_points, "Mismatch in number of cells"

    # # connectivity = mesh.cell_connectivity

    # if args.cellType == 'tetra': 
    #     cell_type_id = 10 
    # else: 
    #     cell_type_id=3000
    #     print("Error in cell type: ", args.mesh_path) # VTK_TETRA = 10
    # # mesh.cells_dict[cell_type_id]

    # # vm_values[1,:]=25
    # max_vm=np.max(vm_values)
    # min_vm=np.min(vm_values)

    # outPath=os.path.join(vm_path,"Images")
    # if not os.path.exists(outPath): os.mkdir(outPath)

    

    # for time_id in range(0,vm_values.shape[0],args.time_steps):
    # # time_id=10
    #     layersCells=ut.points2Elements(mesh.cells_dict[cell_type_id], vm_values[time_id,:])
    #     # mesh.cell_data["layers_scar"]=layersCells

    #     pl = pv.Plotter(off_screen=True)
    #     actor = pl.add_mesh(mesh,scalars=layersCells,lighting=True,cmap="viridis",preference='cell',show_scalar_bar=False,clim=(-90,100))
    #     pl.add_scalar_bar('Vm',interactive=True,vertical=False,title_font_size=35,
    #     label_font_size=30, outline=True,fmt='%10.5f',mapper=actor.mapper)
    #     # pl.update_scalar_bar_range([min_vm, max_vm], name=None)
    #     namePlot="im_time_"+str(time_id)+".svg"
    #     pl.save_graphic(os.path.join(vm_path,"Images",namePlot))
    #     # pl.show()
    #     # mesh.plot(scalars=layersCells, show_edges=True, cmap="viridis", opacity=0.6)
    #     # mesh.plot(layersCells, show_edges=True, cmap="viridis", opacity=0.6)
    #     pl.close()
    #     print("Image: "+str(time_id)+", Patient:"+ args.mesh_path)


    # print("Finished: ", args.mesh_path)

    



if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))