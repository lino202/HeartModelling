''''' Put coordinates as input and get the pts values (not the coordinates) in the mesh
Gets output as file with nodes_ and if want, add to mesh....
'''''


import argparse
import meshio
import numpy as np
from scipy.spatial import KDTree
import time
import utils as ut
import os
from scipy.io import savemat


def writePointsFile(arr, outName):
        with open(outName, 'w') as f:
            f.write("{0:d}\n".format(arr.shape[0]))
            pts = list(map(lambda x: "{0:f} {1:f} {2:f}\n".format(x[0], x[1], x[2]),list(arr)))
            f.writelines(pts)

def read_pts(filename):
    #Read the coordinates values from the pts file
    # vm_values=np.loadtxt(filename)

    with open(filename, 'r', encoding='utf-8') as file:
        i = 0
        m=0
        for line in file:
            i = i+1
            if i==1:
                aux=line.strip()
                positions=np.zeros((int(aux),3))
                positions=positions*np.nan

            else:
                a=3
            
                aux=line.strip()
                aux1=aux.split(" ")
                positions[m,:]=[float(x) for x in aux1]
                m=m+1
    return positions

def read_pts_names(filename, numpoints):
    #Read the coordinates values from the pts file
  
    namesout = [None] * numpoints
    i = 0
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            aux=line.strip()
            aux1=aux.split(" ")
            namesout[i]=aux1[1]
            i = i+1
        # i = 0
        # m=0
        # for line in file:
        #     i = i+1
        #     if i==1:
        #         aux=line.strip()
        #         positions=np.zeros((int(aux),3))
        #         positions=positions*np.nan

        #     else:
        #         a=3
            
                
        #         positions[m,:]=[float(x) for x in aux1]
        #         m=m+1
    return namesout

    # f = open(filename, "r")
    # print(f.readlines(33))

    # with open(filename, "r") as file:
    #     line = file.readline()
    #     print(line)

def main():
    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument('--points_path',type=str, help=' path to points')
    parser.add_argument('--points_name',type=str, help=' name of  points file')
    parser.add_argument('--points_file_names',type=str, help=' name of  file with points names (RA, V1-V2, etc)')
    parser.add_argument('--unit_points',type=str,required=True, help="Units of pointsccoordinates to search (um,mm or cm)")
    parser.add_argument('--mesh_path',type=str, required=True, help='path to Mesh ')
    parser.add_argument('--mesh_name',type=str, required=True, help='mesh name')
    # parser.add_argument('--output_name',type=str, required=True, help='name of output file')
    parser.add_argument('--store_together', action='store_true', help="If called, all the points are saved in the mesh")
    parser.add_argument('--unit_mesh',type=str,required=True, help="Units of mesh to add the coordinates (mesh_path_use) (um,mm or cm)")
    

    
    # parser.add_argument('--mesh_path_layers',type=str, help='Mesh with layers if the mesh you want to add the coordinates does not have the labels. It should be the same mesh in elements although it might be in other units')
    # parser.add_argument('--mesh_path_use',type=str, required=True, help='Mesh ')
    # parser.add_argument('--unit_mesh',type=str,required=True, help="Units of mesh to add the coordinates (mesh_path_use) (um,mm or cm)")
    # parser.add_argument('--layer_mesh_field',type=str, help='If added, the pacing sites are limited to this field')
    # parser.add_argument('--layer_mesh_value',type=int, help='If added, the pacing sites are limited to this value of the field layer_mesh_field')
    # # parser.add_argument('--outPath',type=str, required=True, help='output path of stim vtx file')
    # parser.add_argument('--path_2_coordinates',type=str, required=True, help='path to file with coordinates of points')
    # parser.add_argument('--unit_points',type=str,required=True, help="Units of the coordinates (path_2_coordinates) (um,mm or cm)")
    # # parser.add_argument('--add_to_mesh',action='store_true', help='If called,to add the pacing sites to the mesh to use')
    # parser.add_argument('--stimRadious',type=float, default=3, help='Radius around the input points in mm')
    # parser.add_argument('--store_together', action='store_true', help="If called, all the stim points are saved in the same field")
    
    args = parser.parse_args()

    if os.path.exists(os.path.join(args.mesh_path, "torso_electrodes_"+args.mesh_name)):
        meshUse=meshio.read(os.path.join(args.mesh_path, "torso_electrodes_"+args.mesh_name))
    else:
        meshUse = meshio.read(os.path.join(args.mesh_path, args.mesh_name)) #Original, #Mesh in which to add the pacing sites

    # ht=os.path.split(args.mesh_path_volumes)
    meshName=args.mesh_name.split(".vtk")[0]

    coorStimNameorig=args.points_name.split(".pts")[0]
   
    coorStim=read_pts(os.path.join(args.points_path,args.points_name))
    coorStimNames=read_pts_names(os.path.join(args.points_path,args.points_file_names),np.size(coorStim,0))

     

    
    #Change units of pacing points if necessary
    if args.unit_mesh=="cm":
        if args.unit_points=="mm":
            coorStim = coorStim / 10

        elif args.unit_points=="um":
            coorStim = coorStim / 10000
            pass
        else: print("Coordinates units will not be modified")

    elif args.unit_mesh=="mm":
        if args.unit_points=="cm":
            coorStim = coorStim * 10

        elif args.unit_points=="um":
            coorStim = coorStim / 1000

            pass
        else: print("Coordinates units will not be modified")

    elif args.unit_mesh=="um":
        if args.unit_points=="mm":
            coorStim = coorStim * 1000

        elif args.unit_points=="cm":
            coorStim = coorStim * 10000
            pass
        else: print("Coordinates units will not be modified")

    else: print("Only units in cm, mm or um are supported")

    # pacingCites     = np.zeros((np.shape(coorStim)[0],3))

    treeMesh = KDTree(meshUse.points)

    _ , idxs = treeMesh.query(coorStim, k=1) #Find closest point in mesh to the stim points
    pacingCites = meshUse.points[idxs,:] #Find coordinates of closest points in the mesh2use

    #Save coordinated
    columnsCoorNames = []
    dictCoorNames=dict()
    for i in range(np.size(pacingCites,0)):
        columnsCoorNames.append(str(pacingCites[i,:]) + " " + coorStimNames[i])
        dictCoorNames[coorStimNames[i]]=pacingCites[i,:]    
    np.savetxt(os.path.join(args.points_path,"ECGCoorsNames_"+coorStimNameorig+"_"+meshName+".txt"), columnsCoorNames, fmt='%s') 

    #Save as MATLAB
    savemat(os.path.join(args.points_path,"ECG_Nodes_"+coorStimNameorig+"_"+meshName+".mat"),dictCoorNames)
    #Save only the pts for torso
    np.savetxt(os.path.join(args.points_path,"ECG_Nodes_"+coorStimNameorig+"_"+meshName+".txt"), idxs, fmt='%s')


    #Save the idx with its corresponding name
    columnsPtsNames = []
    for i in range(np.size(coorStim,0)):
        columnsPtsNames.append(str(idxs[i]) + " " + coorStimNames[i] )
        if coorStimNames[i]=="RL": #Save stim_ref
            #Vhange to extra
             ut.writeStimVtxFile(np.array([idxs[i]]), os.path.join(args.points_path, "{}_{}_{}.vtx".format("stim_Ref", coorStimNameorig , meshName)),"extra")


    np.savetxt(os.path.join(args.points_path,"ECGPtsNames_"+coorStimNameorig+"_"+meshName+".txt"), columnsPtsNames, fmt='%s') 



    #Save file of coordinates as .pts
    fileName="electrodes_positions_"+coorStimNameorig+"_"+meshName
    writePointsFile(pacingCites, os.path.join(args.mesh_path, "{}.pts".format(fileName)))




    # Get nodesets and point_data
    if args.store_together: #Save in the same field
        tmp = np.zeros(meshUse.points.shape[0])
        tmp[idxs] = 1
        tmp_fin=tmp.astype(bool)*1
        meshUse.point_data["electrodes_pts"+"_"+coorStimNameorig] = tmp_fin.astype(np.int64) #Original



    #SAVE you can take to inp with mesh2inp
    meshUse.write(os.path.join(args.mesh_path, "torso_electrodes_"+args.mesh_name))


    print("Finished:",args.mesh_path)


if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))
