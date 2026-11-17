'''this gets the pacing nodes corresponding to the endocardium of the AHA segments 
or of a specific tag in a layer of the mesh
'''
 
import argparse
import meshio
import numpy as np
from scipy.spatial import KDTree
import time
import os

def openVTX (filename):
        #Read the coordinates values from the pts file
    # vm_values=np.loadtxt(filename)

    with open(filename, 'r', encoding='utf-8') as file:
        i = 0
        m=0
        for line in file:
            i = i+1
            if i==1:
                aux=line.strip()
                positions=np.zeros((int(aux)))
                positions=positions*np.nan

            elif i==2:

                placePts=line.strip()

            else:
                a=3
            
                aux=line.strip()
                aux1=aux.split(" ")
                # positions[m]=[int(x) for x in aux1]
                positions[m]=int(aux1[0])
                m=m+1
    return positions
    

def main():
    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument('--meshIn',type=str, required=True, help='Complete path to mesh to add the pacing sites')
    parser.add_argument('--pacingAHA', action='store_true', help="If called, the pacing locations are obtained from AHA")
    parser.add_argument('--pacingTag', action='store_true', help="If called, the pacing locations are obtained from a specific tag")
    parser.add_argument('--unit_mesh',type=str,required=True, help="Units of mesh to add the coordinates (mesh_path_use) (um,mm or cm)")
    # parser.add_argument('--unit_coordinates',type=str, help="Units of coordinates to create (um,mm or cm)")
    
    #If coordinates, get from aha
    parser.add_argument('--meshAHA',type=str, help='Complete path to mesh with AHA segments, has to be the same units as mesh in')
    parser.add_argument('--endoLV',type=str, help='Complete path to mesh with Endo LV surface mesh')
    parser.add_argument('--endoRV',type=str, help='Complete path to mesh with Endo RV surface mesh')

    #If coordinates come from tags
    parser.add_argument('--layer_mesh_field',type=str, help='If added, the pacing sites are limited to this field')
    parser.add_argument('--layer_mesh_value',type=int,nargs='+', help='If added, the pacing sites are limited to this value of the field layer_mesh_field')
    parser.add_argument('--mesh_path_layers',type=str, help='Mesh with layers to limit the stims place, same units as mesh ')

    parser.add_argument('--outName',type=str, required=True, help='Name for coordiantes. If more than one, numbers at the end will be added')
    parser.add_argument('--outPath',type=str, required=True, help='Output path for coordinates')

    # parser.add_argument('--stimRadious',type=float, default=1.5)
    parser.add_argument('--rvPacingCite',type=float, nargs=3,default=np.nan, help="The unit is the same that the points of the mesh have")
    parser.add_argument('--errasePointData', action='store_true', help="If called, the other fields of pointData are erased")
    

    #If coordinates, get from vtx of another mesh
    parser.add_argument('--vtxPath',type=str, help='Complete path to vtx files')

    
    args = parser.parse_args()

    
    
    meshAdd = meshio.read(args.meshIn) #Mesh in which to add the pacing sites and with the tags

    outName_complete=args.outName+"_"+args.unit_mesh

    
    #If you want to get the pacing location from the AHA segments
    if args.pacingAHA:
        mesh = meshio.read(args.meshAHA)#JRDZC 06/06/2025. Modified because I had the AHA segments in other mesh

        try:
            ahaSegs = mesh.point_data["AHASegs"]

        except Exception as e:
            print("Caught an error:",args.meshAHA, e)

        #Get endo surfaces to place the pacing sites there.
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


        # Pacing cites on endo surfs and on mesh
        pacingCites     = np.zeros((nSegs,3))

        _ , idxs = treeRV.query(centroids[-2:,:], k=1)
        _ , idxs = treeMesh.query(endoRV.points[idxs,:], k=1) #Pacing cites on tetmesh
        pacingCites[-2:,:] = mesh.points[idxs,:]

        _ , idxs = treeLV.query(centroids[:-2,:], k=1)
        _ , idxs = treeMesh.query(endoLV.points[idxs,:], k=1) #Pacing cites on tetmesh
        pacingCites[:-2,:] = mesh.points[idxs,:]

        pacingIds=idxs


        

        # # Use radious for defining nodesets
        # pacingNodesLists = treeMesh.query_ball_point(pacingCites, r=args.stimRadious)

    #If pacing is to be looked for in a specific layer o tag
    if args.pacingTag:
        pacingIds=np.array([])
        #If the stim points are to be limited to a layer of the mesh
        if args.layer_mesh_field: #if you want a specific layer
            if args.mesh_path_layers: # of the mesh with layers is not the same as the mesh in micrometers
                print("<<<Other mesh opened>>>>")
                meshLayers = meshio.read(args.mesh_path_layers) #Mesh with layers
                field2use = meshLayers.point_data[args.layer_mesh_field]
                if args.layer_mesh_value:
                    points2use_bool=np.zeros(field2use.shape[0])
                    for nm in range(np.size(args.layer_mesh_value)):
                        auxpoints=np.where(field2use==args.layer_mesh_value[nm])
                        points2use_bool[auxpoints[0][0]]=1
                        pacingIds=np.append(pacingIds, int(auxpoints[0][0]))
                        
                else:
                    print("No specific value was selected")

            else:
                field2use = meshAdd.point_data[args.layer_mesh_field]
                print("<<<Same mesh opened>>>")
                if args.layer_mesh_value:
                    # points2use_bool=field2use==args.layer_mesh_value
                    points2use_bool=np.zeros(field2use.shape[0])
                    for nm in range(np.size(args.layer_mesh_value)):
                        auxpoints=np.where(field2use==args.layer_mesh_value[nm])
                        points2use_bool[auxpoints[0][0]]=1
                        pacingIds=np.append(pacingIds, int(auxpoints[0][0]))
                else:
                    print("No specific value was selected")
        else:
            print("No field was selected")
            points2use_bool=np.ones(meshAdd.points.shape[0])
        pacingCites=meshAdd.points[points2use_bool.astype(bool)]

    if args.vtxPath:
        elemsVTX=openVTX(args.vtxPath)

        # meshAdd.points[elemsVTX,:]
        points=meshAdd.points
 

        pointsVTX=points[elemsVTX.astype(int),:]

        pacingIds=elemsVTX.astype(int)

        pacingCites=[np.mean(pointsVTX, axis=0)]


        #Find coordinates of these points



    outPath_complete=os.path.join(args.outPath,outName_complete+".txt")
    np.savetxt(outPath_complete, pacingCites, delimiter=" ", fmt="%f")

    outPath_complete=os.path.join(args.outPath,outName_complete+"_Ids.txt")
    np.savetxt(outPath_complete, pacingIds, delimiter=" ", fmt="%d")

    #Save coordinates

    #Read pacing points. If there are more than one. Save as vtx, one for each point or together. The name is going to be as the input file
    
    
    print("Finished:",outPath_complete)


if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))
