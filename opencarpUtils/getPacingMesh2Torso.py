'''Transform pacing sites from a heart mesh to a torso mesh. Get the vtx files for each.
I think by now, you should have the torso+heart meash with the elemTags and in micrometers (),
 so there is no need to transform to carp_txt.

'''


#Modify the files to be used in OpenCARP
import meshio
import argparse
import os
import numpy as np
import utils as ut
import time
from scipy.spatial import KDTree
import matplotlib.pyplot as plt
import seaborn as sns
# import nanomesh

def main():
    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument('--torso_mesh_path', type=str, required=True, help='Complete path to mesh torso+heart')
    parser.add_argument('--heart_mesh_path', type=str, required=True, help='Complete path to mesh of heart with stim points')
    parser.add_argument('--units_torso_mesh', type=str, default="um", help='Units of mesh heart+torso')
    parser.add_argument('--units_heart_mesh', type=str, default="um", help='Units of heart mesh')
    parser.add_argument('--add_2_mesh', action='store_true', help="If called, the stim points are added to the torso+heart mesh")
    parser.add_argument('--outFolder', type=str, required=True, help='Where to save the .vtx')

    # parser.add_argument('--file_path_fibers', type=str, required=True)
    # parser.add_argument('--unit',            type=str, required=True)
    # parser.add_argument('--cellType',        type=str, default="tetra")
    # parser.add_argument('--stimPointData',   type=str)
    # parser.add_argument('--fibersPointData', type=str)
    # parser.add_argument('--layersPointData', type=str)
    # parser.add_argument('--outFolder',       type=str, required=True)
    # parser.add_argument('--elemData',       type=str, required=False)
    # parser.add_argument('--groundPointData', action='store_true', help='To choose a ground point for bidomain simulations')
    
    # parser.add_argument('--save' ,action='store_true',  help='save histogram tags')
    
    args = parser.parse_args()

    '''INPUTS
    Heart mesh with pacing sites 
    torso mesh with heart mesh merged.

    At this point, you should already have the torso+heart mesh (after meshtool)

    '''

    #Open meshes
    meshTorso = meshio.read(args.torso_mesh_path)
    meshHeart = meshio.read(args.heart_mesh_path)

    
    ht=os.path.split(args.torso_mesh_path)
    fileName2Use=str(ht[1]).split(".")[0]
    

    
    #Change units of heart mesh in case they are not the same as in the torso
    if args.units_torso_mesh=="cm":
        if args.units_heart_mesh=="mm":
            meshHeart.points = meshHeart.points / 10

        elif args.units_heart_mesh=="um":
            meshHeart.points = meshHeart.points / 10000

            pass
        else: print("Coordinates units will not be modified")

    elif args.units_torso_mesh=="mm":
        if args.units_heart_mesh=="cm":
            meshHeart.points = meshHeart.points * 10

        elif args.units_heart_mesh=="um":
            meshHeart.points = meshHeart.points / 1000

            pass
        else: print("Coordinates units will not be modified")

    elif args.units_torso_mesh=="um":
        if args.units_heart_mesh=="mm":
            meshHeart.points = meshHeart.points * 1000

        elif args.units_heart_mesh=="cm":
            meshHeart.points = meshHeart.points * 10000

            pass
        else: print("Coordinates units will not be modified")

    else: print("Only units in cm, mm or um are supported")

    #Fix elem tag from openCARP
    fields = list(meshTorso.cell_data.keys())
    # for fd in fields:
    #     if 
    #     meshTorso.cell_data['elemTag']=np.squeeze(meshTorso.cell_data['elemTag'])
    #     meshTorso.cell_data['fiber']=np.squeeze(meshTorso.cell_data['fiber'])


    #KDT tree of mesh torso
    treeMesh = KDTree(meshTorso.points)
    


    #Find stim coordinates in heart mesh and save
    fields = list(meshHeart.point_data.keys())
    for fd in fields:
        if "stim" in fd: #Search for word stim and asume they are stimulus points
            #Get the coordonates of the stim point
            stimPointsAux=meshHeart.point_data[fd]

            stimCoordsAux=meshHeart.points[stimPointsAux.astype(bool),:]

            _ , idxs = treeMesh.query(stimCoordsAux, k=1) #Find closest point in mesh to the stim points
            # pacingCites = meshTorso.points[idxs,:] #Find coordinates of closest points in the mesh2use

            print("Getting stim nodes as vtx file -------------")
            ut.writeStimVtxFile(idxs, os.path.join(args.outFolder, "{}_{}.vtx".format(fd,fileName2Use)),"extra")

            if args.add_2_mesh:
     
                tm = np.zeros(meshTorso.points.shape[0])
                tm[idxs]=1
                tmp_fin=tm.astype(bool)*1
                meshTorso.point_data[fd]=tmp_fin.astype(np.int64)
                

    # tmp = np.zeros(meshUse.points.shape[0])
    # if args.store_together: #Save in the same field
    #     tmp_store = np.zeros(meshUse.points.shape[0])
    #     for i, pacingList in enumerate(pacingNodesLists):
    #         tmp_store[pacingList] = 1
    #     #Multiply by the layers
    #     tmp_store=tmp_store*points2use_num
    #     tmp_fin=tmp_store.astype(bool)*1
    #     meshUse.point_data["stim_Ext_{}".format(fieldName)] = tmp_fin#Original




    # meshTorso2 = meshio.Mesh(meshTorso.points,meshTorso.cells_dict['tetra'])
    # meshTorso2.write("/mnt/e/Jimena/HCULB/IHD/Segmentations/MI_MRI_32/Torso_3mm_micrometers_merged_2.vtk")
    if args.add_2_mesh:
        new_mesh_path=os.path.join(ht[0],fileName2Use+"_stimspts.vtk")
        # new_mesh_path= args.torso_mesh_path
        meshTorso.write(new_mesh_path)
    # meshTorso.write(args.torso_mesh_path, file_format="vtk", binary=False)

            

    #Find closest points from heart mesh to torso+heart mesh




if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))
