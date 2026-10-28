'''
Here it is to plot the VM results on the mesh surface
'''


import pyvista as pv
import numpy as np
import argparse
import os
import time
import utils as ut
import sys



def main():
    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument('--mesh_path',      type=str, required=True, help='path to mesh')
    parser.add_argument('--mesh_name',      type=str, required=True, help='name of mesh with the end')
    parser.add_argument('--vm_path_input',     type=str, required=True, help='path to vm, result of openCARP')
    parser.add_argument('--simulation_number',     type=str, required=True, help='simulation name, result of openCARP')
    parser.add_argument('--cellType',        type=str, default="tetra")
    parser.add_argument('--time_steps',type=int,help='time steps to plot results')
    parser.add_argument('--type_remove_label', type=str, default="cell", help="If the label to be used to compare is in the elem(cell)Data or the pointData. Options=cell or point")
    
    
    args = parser.parse_args()


    meshName=os.path.join(args.mesh_path, args.mesh_name)
    mesh = pv.read(meshName)

    vm_path=os.path.join(args.vm_path_input,args.simulation_number)
    vmName=os.path.join(vm_path,"vm_"+ args.simulation_number + ".txt")

    vm_values = np.loadtxt(vmName)

    assert vm_values.shape[1] == mesh.n_points, "Mismatch in number of cells"

    # connectivity = mesh.cell_connectivity

    if args.cellType == 'tetra': 
        cell_type_id = 10 
    else: 
        cell_type_id=3000
        print("Error in cell type: ", args.mesh_path) # VTK_TETRA = 10
    # mesh.cells_dict[cell_type_id]

    # vm_values[1,:]=25
    max_vm=np.max(vm_values)
    min_vm=np.min(vm_values)

    outPath=os.path.join(vm_path,"Images")
    if not os.path.exists(outPath): os.mkdir(outPath)

    

    for time_id in range(0,vm_values.shape[0],args.time_steps):
    # time_id=10
        layersCells=ut.points2Elements(mesh.cells_dict[cell_type_id], vm_values[time_id,:])
        # mesh.cell_data["layers_scar"]=layersCells

        pl = pv.Plotter(off_screen=True)
        actor = pl.add_mesh(mesh,scalars=layersCells,lighting=True,cmap="viridis",preference='cell',show_scalar_bar=False,clim=(-90,100))
        pl.add_scalar_bar('Vm',interactive=True,vertical=False,title_font_size=35,
        label_font_size=30, outline=True,fmt='%10.5f',mapper=actor.mapper)
        # pl.update_scalar_bar_range([min_vm, max_vm], name=None)
        namePlot="im_time_"+str(time_id)+".svg"
        pl.save_graphic(os.path.join(vm_path,"Images",namePlot))
        # pl.show()
        # mesh.plot(scalars=layersCells, show_edges=True, cmap="viridis", opacity=0.6)
        # mesh.plot(layersCells, show_edges=True, cmap="viridis", opacity=0.6)
        pl.close()
        print("Image: "+str(time_id)+", Patient:"+ args.mesh_path)


    print("Finished: ", args.mesh_path)

    



if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))