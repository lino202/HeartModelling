''' this gets the pacing nodes corresponding to the external file to add to the heart mesh. The external file contains the coordinates
The pacing sites can be limited to specific layer of the mesh if you want.

'''
import argparse
import meshio
import numpy as np
from scipy.spatial import KDTree
import time
import os

def main():
    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument('--mesh_path_layers',type=str, help='Mesh with layers if the mesh you want to add the coordinates does not have the labels. It should be the same mesh in elements although it might be in other units')
    parser.add_argument('--mesh_path_use',type=str, required=True, help='Mesh ')
    parser.add_argument('--unit_mesh',type=str,required=True, help="Units of mesh to add the coordinates (mesh_path_use) (um,mm or cm)")
    parser.add_argument('--layer_mesh_field',type=str, help='If added, the pacing sites are limited to this field of points')
    parser.add_argument('--layer_mesh_value',type=int, nargs='+', help='If added, the pacing sites are limited to these values of the field layer_mesh_field')
    # parser.add_argument('--outPath',type=str, required=True, help='output path of stim vtx file')
    parser.add_argument('--path_2_coordinates',type=str, required=True, help='path to file with coordinates of points')
    parser.add_argument('--unit_coordinates',type=str,required=True, help="Units of the coordinates (path_2_coordinates) (um,mm or cm)")
    # parser.add_argument('--add_to_mesh',action='store_true', help='If called,to add the pacing sites to the mesh to use')
    parser.add_argument('--stimRadious',type=float, default=1.5, help='Radius around the input points in mm')
    parser.add_argument('--store_together', action='store_true', help="If called, all the stim points are saved in the same field")
    
    # parser.add_argument('--endoLV',type=str, required=True, help='Complete path to mesh with Endo LV surface mesh')
    # parser.add_argument('--endoRV',type=str, required=True, help='Complete path to mesh with Endo RV surface mesh')
    # parser.add_argument('--rvPacingCite',type=float, nargs=3,default=np.nan, help="The unit is the same that the points of the mesh have")
    # parser.add_argument('--errasePointData', action='store_true', help="If called, the other fields of pointData are erased")
    args = parser.parse_args()

    meshUse = meshio.read(args.mesh_path_use) #Original, #Mesh in which to add the pacing sites
    # meshLayers = meshio.read(args.mesh_path_layers) #Mesh with layers


    #raise ValueError("Only units in cm, mm or um are supported")

    # Layer of mesh
    if args.layer_mesh_field: #if you want a specific layer
        tmp = np.zeros(meshUse.points.shape[0])
        if args.mesh_path_layers: # of the mesh with layers is not the same as the mesh in micrometers
            meshLayers = meshio.read(args.mesh_path_layers) #Mesh with layers
            field2use = meshLayers.point_data[args.layer_mesh_field]
            
            if args.layer_mesh_value:
                for lmv in args.layer_mesh_value:
                    points2use_bool=field2use==lmv
                    tmp[points2use_bool]=1
            else:
                print("No specific value was selected")

        else: # if the mesh with layers is the same as the mesh to use
            field2use = meshUse.point_data[args.layer_mesh_field]
            if args.layer_mesh_value:
                # points2use_bool=field2use==args.layer_mesh_value
                for lmv in args.layer_mesh_value:
                    points2use_bool=field2use==lmv
                    tmp[points2use_bool]=1
            else:
                print("No specific value was selected")
    else:
        print("No field was selected")
        points2use_bool=np.ones(meshUse.points.shape[0])
        tmp=np.ones(meshUse.points.shape[0])

    #Read pacing points. If there are more than one. Save as vtx, one for each point or together. The name is going to be as the input file
    
    # points2use_num=points2use_bool*1
    points2use_num=tmp

    

    coorStim = np.loadtxt(args.path_2_coordinates)
    
    #Change units of pacing points if necessary
    if args.unit_mesh=="cm":
        if args.unit_coordinates=="mm":
            coorStim = coorStim / 10

        elif args.unit_coordinates=="um":
            coorStim = coorStim / 10000
            pass
        else: print("Coordinates units will not be modified")

    elif args.unit_mesh=="mm":
        if args.unit_coordinates=="cm":
            coorStim = coorStim * 10

        elif args.unit_coordinates=="um":
            coorStim = coorStim / 1000

            pass
        else: print("Coordinates units will not be modified")

    elif args.unit_mesh=="um":
        if args.unit_coordinates=="mm":
            coorStim = coorStim * 1000

        elif args.unit_coordinates=="cm":
            coorStim = coorStim * 10000
            pass
        else: print("Coordinates units will not be modified")

    else: print("Only units in cm, mm or um are supported")

    # pacingCites     = np.zeros((np.shape(coorStim)[0],3))

    treeMesh = KDTree(meshUse.points)

    _ , idxs = treeMesh.query(coorStim, k=1) #Find closest point in mesh to the stim points
    pacingCites = meshUse.points[idxs,:] #Find coordinates of closest points in the mesh2use



    #Check that the stim radio units correspond to the mesh
    if args.unit_mesh=="cm":
        stimRadious = args.stimRadious / 10
    elif args.unit_mesh=="um":
        stimRadious = args.stimRadious * 1000

    else: stimRadious=args.stimRadious

    

    # Use radious for defining nodesets
    pacingNodesLists = treeMesh.query_ball_point(pacingCites, r=stimRadious)

    ht=os.path.split(args.path_2_coordinates)
    fieldName=ht[1].split(".")[0]
    

    # Get nodesets and point_data
    if args.store_together: #Save in the same field
        tmp_store = np.zeros(meshUse.points.shape[0])
        for i, pacingList in enumerate(pacingNodesLists):
            tmp_store[pacingList] = 1
        #Multiply by the layers
        tmp_store=tmp_store*points2use_num
        tmp_fin=tmp_store.astype(bool)*1
        meshUse.point_data["stim_Ext_{}_{}_mm".format(fieldName,args.stimRadious)] = tmp_fin#Original

    else: #Save in separate fields
        for i, pacingList in enumerate(pacingNodesLists):
            tmp_store = np.zeros(meshUse.points.shape[0])
            tmp_store[pacingList] = 1
            #Multiply by the layers
            tmp_store=tmp_store*points2use_num
            tmp_fin=tmp_store.astype(bool)*1
            meshUse.point_data["stim_Ext_{}_{}_{}_mm".format(fieldName,i+1,args.stimRadious)] = tmp_fin#Original


    #SAVE you can take to inp with mesh2inp
    meshUse.write(args.mesh_path_use)


    print("Finished:",args.mesh_path_use)


if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))
