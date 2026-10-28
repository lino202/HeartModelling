'''
Here it is to plot the VM results on the mesh
'''


# import pyvista as pv
import numpy as np
import argparse
import os
import time
import utils as ut
import sys
import meshio



def main():
    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument('--mesh_path',      type=str, required=True, help='path to mesh')
    parser.add_argument('--mesh_name',      type=str, required=True, help='name of mesh with the end')
    parser.add_argument('--vm_path_input',     type=str, required=True, help='path to vm, result of openCARP')
    parser.add_argument('--simulation_number',     type=str, required=True, help='path to vm, result of openCARP')
    parser.add_argument('--cellType',        type=str, default="tetra")
    parser.add_argument('--time_steps',type=int,help='time steps to plot results')
    parser.add_argument('--add2Elems', action='store_true', help="If called, the points are also added to the elements")
    parser.add_argument('--errasePointData', action='store_true', help="If called, the other fields of pointData are erased")
    
    args = parser.parse_args()


    meshName=os.path.join(args.mesh_path, args.mesh_name)
    mesh = meshio.read(meshName)

    vm_path=os.path.join(args.vm_path_input,args.simulation_number)
    vmName=os.path.join(vm_path,"vm_"+ args.simulation_number + ".txt")

    vm_values = np.loadtxt(vmName)

    assert vm_values.shape[1] == mesh.points.shape[0], "Mismatch in number of cells"

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

    if args.errasePointData: #If you want to errase the other pointData fields
        fields = list(mesh.point_data.keys())
        for f in fields:
            print("Erasing: ",f)
            mesh.point_data.pop(f, None)

        fields = list(mesh.cell_data.keys())
        for f in fields:
            print("Erasing: ",f)
            mesh.cell_data.pop(f, None)
    

    for time_id in range(0,vm_values.shape[0],args.time_steps):
    # time_id=10
        mesh.point_data[aux_time]=vm_values[time_id,:]

        if args.add2Elems:
            layersCells=ut.points2Elements(mesh.cells_dict[args.cellType], vm_values[time_id,:])
            # mesh.cell_data["layers_scar"]=layersCells
            aux_time="time_"+str(time_id)
            layersCells2=layersCells.reshape(layersCells.shape[0],1)
            mesh.cell_data[aux_time]=layersCells2
            # mesh.cell_data[aux_time]=layersCells.astype('')
        

        print("Image: "+str(time_id)+", Patient:"+ args.mesh_path)

    meshio.write(os.path.join(outPath,"mesh_"+args.simulation_number+".xdmf"),mesh)


    print("Finished: ", args.mesh_path)


# for name, value in mesh.cell_data.items():
#     print(f"Cell data key: {name}")
#     for i, v in enumerate(value):
#         if np.isscalar(v):
#             print(f"  -> Entry {i}: SCALAR {v} (type={type(v)}) ❌")
#         else:
#             print(f"  -> Entry {i}: array shape={np.shape(v)} dtype={getattr(v, 'dtype', type(v))} ✅")
#         print()



if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))