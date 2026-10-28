''' Read the vtx file to get stim points and add 2 mesh
'''


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
import fenics
import pyvista as pv
import carputils.carpio.igb as carp
import json
import csv



def main():
    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument('--mesh_name',    type=str, required=True)
    parser.add_argument('--mesh_path',    type=str, required=True)
    parser.add_argument('--vtx_name',    type=str, nargs='+', required=True)
    parser.add_argument('--add_2_mesh', action='store_true', help="If called, the vpts are saved in mesh")
    parser.add_argument('--store_together', action='store_true', help="If called, the vtx are saved in together")
    parser.add_argument('--vtx_out_name',  type=str, help="If stored together, the vtx name tags")
    
    # parser.add_argument('--unit_mesh',type=str,required=True, help="Units of mesh to add the coordinates (mesh_path_use) (um,mm or cm)")
    

    


    # parser.add_argument('--label_remove',   nargs='+',  default=0,  type=int, required=True, help="Labels of elements to be removed")
    # parser.add_argument('--field_remove',   nargs='+',  default="elemTag",  type=str, required=True, help="Labels of elements to be removed")
    # # parser.add_argument('--label_keep',    nargs='+',  type=int, required=True, help="Labels of elements to be kept")
    # parser.add_argument('--simulation_path',    type=str)
    # parser.add_argument('--simulation_name',    type=str)
    # parser.add_argument('--file_phie_name',    type=str)
    # parser.add_argument('--simulation_ecg_format',  type=str,default="igb", help='simulation format (igb, txt or mat)')
    # parser.add_argument('--cell_type',   type=str, default="tetra")
    # parser.add_argument('--new_mesh_name',   type=str,required=True)
    # parser.add_argument('--saveOpenCARP', action='store_true', help="If called, the carp_txt is saved")
    # parser.add_argument('--extract_vm', action='store_true', help="If called, the vm from the mesh is also saved")

    

    args = parser.parse_args()

    # --file_path_fibers         #Complete path to the mesh with the fibers and pacing sites
    # --unit              #Units of the mesh.  cm, mm or um
    # --cell_type          #Cell type. Default value is tetra 
    # --stimPointData     #Name of the field with the Points where the stimuli will start. Right now only add 1 stimulus
    # --fibersPointData   #Point data for fiber orientation
    # --layersPointData   #Maxi removed it
    # --outFolder         #Path for results
    #--elemData           #Data in points to be included as element tags in the .elem file


    #Read mesh
    mesh_file=os.path.join(args.mesh_path,args.mesh_name+".vtk")
    mesh = meshio.read(mesh_file)
    # tagMatrix=mesh.cell_data[args.field_remove]
    # elemMatrix=mesh.cells_dict[args.cellType]
    # pointMatrix = mesh.points
    # lonMatrix = mesh.cell_data['fiber']

    # Open the .vtx
    # vtxFile=os.path.join(args.mesh_path,args.vtx_name+".vtx")
    # vtxData = np.loadtxt(vtxFile, skiprows=2, dtype=int)

    vtxaux=dict()
    for i, nameaux in enumerate(args.vtx_name):
        vtxFile=os.path.join(args.mesh_path,nameaux+".vtx")
        vtxData = np.loadtxt(vtxFile, skiprows=2, dtype=int)
        vtxaux[nameaux]=vtxData



    # for key in list(mesh.point_data.keys()):
    #     # If an array is modern int32 or int64, cast it to standard C-integer
    #     if mesh.point_data[key].dtype in [np.int32, np.int64]:
    #         mesh.point_data[key] = mesh.point_data[key].astype(np.intc)

    # # Clean cell data arrays (meshio stores cell arrays inside lists)
    # for key in list(mesh.cell_data.keys()):
    #     for idx in range(len(mesh.cell_data[key])):
    #         if mesh.cell_data[key][idx].dtype in [np.int32, np.int64]:
    #             mesh.cell_data[key][idx] = mesh.cell_data[key][idx].astype(np.intc)


    if args.add_2_mesh:
        # tm = np.zeros(mesh.points.shape[0])
        # tm[vtxData]=1
        # tmp_fin=tm.astype(bool)*1
        # mesh.point_data["stim_vtx_{}".format(args.vtx_name)]=tmp_fin

        # new_mesh_path=os.path.join(args.mesh_path,args.mesh_name+"_2.vtk")
        # # new_mesh_path= args.torso_mesh_path
        # mesh.write(new_mesh_path)

        if args.store_together:

            tm = np.zeros(mesh.points.shape[0], dtype=np.int32)
            for i, nameaux in enumerate(args.vtx_name):
                vtxDataaux=vtxaux[nameaux]
                # 2. Assign your mask
                tm[vtxDataaux] = 1

            # 3. Explicitly force a standard, VTK-friendly data type
            # np.int32 maps to "int" in VTK. 
            # Alternatively, use np.uint8 (maps to "unsigned_char") to save disk space.
            tmp_fin = tm.astype(np.float32)
            tmp_fin = (tmp_fin > 0).astype(np.float32)
            mesh.point_data["stim_vtx_{}".format(args.vtx_out_name)]=tmp_fin


        else:

            for i, nameaux in enumerate(args.vtx_name):
                tm = np.zeros(mesh.points.shape[0], dtype=np.int32)
                vtxDataaux=vtxaux[nameaux]
                # 2. Assign your mask
                tm[vtxDataaux] = 1

                # 3. Explicitly force a standard, VTK-friendly data type
                # np.int32 maps to "int" in VTK. 
                # Alternatively, use np.uint8 (maps to "unsigned_char") to save disk space.
                tmp_fin = tm.astype(np.float32)
                tmp_fin = (tmp_fin > 0).astype(np.float32)
                mesh.point_data["stim_vtx_{}".format(nameaux)]=tmp_fin
            


        new_mesh_path=os.path.join(args.mesh_path,args.mesh_name+"_2.vtk")
        # new_mesh_path= args.torso_mesh_path
        mesh.write(new_mesh_path)




    print("Finished:",args.mesh_path)

if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))