# this gets the pacing nodes corresponding to the endocardium of the AHA segments
 
import argparse
import meshio
import numpy as np
from scipy.spatial import KDTree
import time


def main():
    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument('--meshIn',type=str, required=True, help='Complete path to mesh to add the pacing sites')
    parser.add_argument('--meshAHA',type=str, required=True, help='Complete path to mesh with AHA segments')
    parser.add_argument('--outPath',type=str, required=True, help='Complete output path of mesh with the stim')
    parser.add_argument('--endoLV',type=str, required=True, help='Complete path to mesh with Endo LV surface mesh')
    parser.add_argument('--endoRV',type=str, required=True, help='Complete path to mesh with Endo RV surface mesh')
    parser.add_argument('--stimRadious',type=float, default=1.5)
    parser.add_argument('--rvPacingCite',type=float, nargs=3,default=np.nan, help="The unit is the same that the points of the mesh have")
    parser.add_argument('--errasePointData', action='store_true', help="If called, the other fields of pointData are erased")
    parser.add_argument('--mesh_path_layers',type=str, help='Mesh with layers to limit the stims place ')
    parser.add_argument('--layer_mesh_field',type=str, help='If added, the pacing sites are limited to this field')
    parser.add_argument('--layer_mesh_value',type=int, help='If added, the pacing sites are limited to this value of the field layer_mesh_field')
    
    args = parser.parse_args()

    # mesh = meshio.read(args.meshIn) #Original
    mesh = meshio.read(args.meshAHA)#JRDZC 06/06/2025. Modified because I had the AHA segments in other mesh
    meshAdd = meshio.read(args.meshIn) #Mesh in which to add the pacing sites

    try:
        ahaSegs = mesh.point_data["AHASegs"]

    except Exception as e:
        print("Caught an error:",args.meshAHA, e)

    endoLV = meshio.read(args.endoLV)
    endoRV = meshio.read(args.endoRV)

    treeMesh = KDTree(mesh.points)
    treeLV = KDTree(endoLV.points)
    treeRV = KDTree(endoRV.points)

    nSegs = int(np.max(ahaSegs))
    centroids = np.zeros((nSegs,3))
    if not(np.isnan(args.rvPacingCite)): #If you have as input the RV pacing site
        for i in range(nSegs-1): #Minus one as we do not compute for RV
            centroids[i,:] = np.mean(mesh.points[(ahaSegs==i+1).nonzero()], axis=0)
        centroids[-1,:] = args.rvPacingCite 
    else:
        for i in range(nSegs): #Minus one as we do not compute for RV
            centroids[i,:] = np.mean(mesh.points[(ahaSegs==i+1).nonzero()], axis=0)


    #If the stim points are to be limited to a layer of the mesh
    if args.layer_mesh_field: #if you want a specific layer
        if args.mesh_path_layers: # of the mesh with layers is not the same as the mesh in micrometers
            meshLayers = meshio.read(args.mesh_path_layers) #Mesh with layers
            field2use = meshLayers.point_data[args.layer_mesh_field]
            if args.layer_mesh_value:
                points2use_bool=field2use==args.layer_mesh_value
            else:
                print("No specific value was selected")

        else:
            field2use = meshAdd.point_data[args.layer_mesh_field]
            if args.layer_mesh_value:
                points2use_bool=field2use==args.layer_mesh_value
            else:
                print("No specific value was selected")
    else:
        print("No field was selected")
        points2use_bool=np.ones(meshAdd.points.shape[0])

    #Read pacing points. If there are more than one. Save as vtx, one for each point or together. The name is going to be as the input file
    
    points2use_num=points2use_bool*1
    

    # Pacing cites on endo surfs and on mesh
    pacingCites     = np.zeros((nSegs,3))

    _ , idxs = treeRV.query(centroids[-2:,:], k=1)
    _ , idxs = treeMesh.query(endoRV.points[idxs,:], k=1) #Pacing cites on tetmesh
    pacingCites[-2:,:] = mesh.points[idxs,:]

    _ , idxs = treeLV.query(centroids[:-2,:], k=1)
    _ , idxs = treeMesh.query(endoLV.points[idxs,:], k=1) #Pacing cites on tetmesh
    pacingCites[:-2,:] = mesh.points[idxs,:]

    # Use radious for defining nodesets
    pacingNodesLists = treeMesh.query_ball_point(pacingCites, r=args.stimRadious)

    if args.errasePointData: #If you want to errase the other pointData fields
        fields = list(mesh.point_data.keys())
        for f in fields:
            print("Erasing: ",f)
            mesh.point_data.pop(f, None)

    # Get nodesets and point_data
    for i, pacingList in enumerate(pacingNodesLists):
        tmp = np.zeros(mesh.points.shape[0])
        tmp[pacingList] = 1
        tmp=tmp*points2use_num
        mesh.point_data["stim_AHA{}".format(i+1)] = tmp#Original
        meshAdd.point_data["stim_AHA{}".format(i+1)] = tmp #JRDZC 06/06/2025. Modified to add the pacing sites to another mesh

    #SAVE you can take to inp with mesh2inp
    mesh.write(args.outPath)
    meshAdd.write(args.meshIn)

    print("Finished:",args.meshAHA)


if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))
