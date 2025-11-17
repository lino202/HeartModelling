""""Create the rotational gradient for both LV and RV to be later used to obtain the AHA segments
"""

import dolfin as df
import ldrb
import os
import argparse
import time
import meshio
from mpi4py import MPI
# import statistics
# from scipy.spatial import ConvexHull, convex_hull_plot_2d
from scipy.spatial.distance import cdist,pdist
import numpy as np
import matplotlib.pyplot as plt
import pyvista as pv #To get the edge loops
import sys
import multiprocessing as mp #For parallel computation
 

# Vector of a point with the LVCentroid
def rotationalGradient(normBasePlane,longAxisVector, pointCentroid, point2Use, point2Comp, indexPoint):
    # normBasePlane   Plane from which to compute the angle a,b,c and d of plane equation
    # longAxisVector  The long avis vector that will be used to get the plane from the point of interest
    # pointCentroid   Point in the center of the edge. To get the vector to create the plane to get the angle. Is lV
    #                 Centroid or RV centroid
    # point2Use       Point to get the rotational value
    # point2Comp      Point to compare the front. I usually asume the LVapex as front and the RV apex as back
    #                 When getting LV rotational, you use put as input -RVapex

    # #Try in one point
    # normBasePlane=equationLV
    # longAxisVector=v1LV
    # pointCentroid=LVCentroid
    # point2Use=filledMeshPoint[0,:]
    # point2Comp=apexRVCoor

    # normBasePlane=normBasePlane[0:3]

    # normBasePlane=equationRV 
    # longAxisVector=v1RV
    # pointCentroid=RVCentroid
    # point2Use=filledMeshPoint[x,:]
    # point2Comp=apexLVCoor
    # indexPoint=x

    vectPoint=point2Use-pointCentroid
    # Perpendicular vector to and Midapex
    vectNormPoint=np.cross(longAxisVector,vectPoint)
    #Get d value for plane with point 2 use
    d_onePoint=-1*np.sum(vectNormPoint*point2Use)
    d_twoPoint=-1*np.sum(vectNormPoint*pointCentroid)
    d_totalPoint=np.array([d_onePoint, d_twoPoint])

    #Difference againt the other values
    YLV = cdist(np.reshape(d_totalPoint, (2, -1)),np.reshape(d_totalPoint, (2, -1)), 'euclidean')

    if not(np.sum((abs(YLV)>(0.001*abs(np.mean(d_totalPoint))))*1)): #If all the same
        d2usePoint=np.mean(d_totalPoint)
    elif np.sum((abs(YLV)>(0.001*abs(np.mean(d_totalPoint))))*1)==2: #Just one is different from the rest
        sys.exit("Age less than 18 for 4")

    elif np.sum((abs(YLV)>(0.001*abs(np.mean(d_totalPoint))))*1)==4: #They are all very different between them
        sys.exit("Age less than 18 for all")

    # vectNormPoint=np.append(vectNormPoint,d2usePoint)


    # Angle between plane with point and base plane using their normal vectors
    # Dot product between both vectors
    dotP=np.dot(vectNormPoint,normBasePlane[0:3])
    
    # Magnitude of both vectors
    magnNormPoint=np.sqrt(np.matmul(vectNormPoint,np.transpose(vectNormPoint)))
    magnNormCentr=np.sqrt(np.matmul(normBasePlane[0:3],np.transpose(normBasePlane[0:3])))

    if magnNormPoint==0: #This would mean that the vector is at origin. But technically this would not happen
        magnNormPoint=np.array([[0.000001]])

    
    # Angle between both normal vectors(plane towards the chosen point and plane towars the LV centroid)
    ang_aux=np.arccos(dotP/(magnNormPoint*magnNormCentr)) 
    ang_aux_deg=ang_aux*180/np.pi  #Value in degrees

    # Have the values of the coefficient for the planes to see direction 
    #Value for point 2 compare
    plane2Comp=np.sum(normBasePlane[0:3]*point2Comp)+normBasePlane[3]
    #Value for Chosen point
    planePoint=np.sum(normBasePlane[0:3]*point2Use)+normBasePlane[3]
    
    if np.sign(planePoint)>0:
        rotationValue=ang_aux
        rotationAngle=ang_aux_deg

    elif np.sign(planePoint)<0:
        rotationValue=-ang_aux
        rotationAngle=-ang_aux_deg
        
    # # elif np.sign(planePoint)==0:

    else:
        print('Error Rotational_LV:',indexPoint)
        rotationValue=np.array([[0]])
        rotationAngle=np.array([[0]])

    # if np.sign(plane2Comp)==np.sign(planePoint): #It is anterior
    #     rotationValue=ang_aux
    #     rotationAngle=ang_aux_deg

    # elif -np.sign(plane2Comp)==np.sign(planePoint):#It is posterior
    #     rotationValue=-ang_aux
    #     rotationAngle=-ang_aux_deg
    
    # else: #If the angle is cero
    #     print('Error Rotational_LV:',point2Comp)
    #     # rotationValue=0 
    #     # rotationAngle=0



    # if dotP==0: #Just in case. This would mean that the vector is at origin. But technically this would not happen
        
    #     print('Eror, dot product equals zero:',point2Comp)
    #     rotationValue=0
    #     rotationAngle=0

    # elif np.sign(plane2Comp)==np.sign(planePoint): #It is anterior
    #     rotationValue=ang_aux
    #     rotationAngle=ang_aux_deg

    # elif -np.sign(plane2Comp)==np.sign(planePoint):#It is posterior
    #     rotationValue=-ang_aux
    #     rotationAngle=-ang_aux_deg
    
    # else: #If the angle is cero
    #     print('Error Rotational_LV:',point2Comp)
    #     rotationValue=0 
    #     rotationAngle=0

    if not(isinstance(rotationValue, np.ndarray)):
        print('Not array:',indexPoint)
    if not(rotationValue.shape==(1,1)):
        print('wrong size:',indexPoint)



    return np.array(rotationValue)
    # return plane2Comp



def main():
    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument('--data_path',type=str, required=True, help='path to data')
    parser.add_argument('--mesh_name',type=str, required=True, help='Mesh to use. With surfaces') 
    parser.add_argument('--domainType',    type=str, required=True, help='BiV (Biventricular) or LV')
    parser.add_argument('--insert2Laplacians', action='store_true', help='If called the layers/laplacians.vtk mesh is searched and the apex_base grad is added')
    # parser.add_argument('--radius',type=float, default=6, help='Radius for defining the apex subdomain for the BC')
    args = parser.parse_args()

    # --data_path Path with the lv endo and rv endo surfaces
    # --insert2Laplacians


    filledMesh=meshio.read(os.path.join(args.data_path, "mesh", "mesh.xdmf"))
    filledMeshPoint=filledMesh.points

    LVEndoName = args.mesh_name + "_lv_endo.vtu"

    # endoLVMesh = meshio.read(os.path.join(args.data_path, "mesh", LVEndoName))# JRDZC
    # endoLVMeshPoints = endoLVMesh.points
    # centerLV=endoLVMeshPoints.mean(0)

    # Load your VTU mesh
    meshLV = pv.read(os.path.join(args.data_path, "mesh", LVEndoName))
    meshLVPoints=meshLV.points

    # Extract boundary edges
    boundary_edgesLV = meshLV.extract_feature_edges(
        boundary_edges=True,
        non_manifold_edges=False,
        feature_edges=False,
        manifold_edges=False
    )

    # Extract points that form the boundary
    boundary_pointsLV = boundary_edgesLV.points
    #Center of the boundary
    LVCentroid=boundary_pointsLV.mean(0)
    LVCentroid = np.reshape(LVCentroid, (-1, 3))
    #Apex as the farthest point of the center
    disT2MeshLV = cdist(meshLVPoints, LVCentroid, 'euclidean') #Distances of the LVedno to the center
    apexLVIndex = np.argmax(disT2MeshLV) #Index of the point with maximum distance
    apexLVCoor=meshLVPoints[apexLVIndex,:] #Coordinates of point with maximum distance



    # #If you wanted to save the edge
    # boundary_edges.save(os.path.join(args.data_path, "mesh", "EdgeLoop.obj"))


    #Read the RV endo if the mesh is BIV
    if args.domainType == "BiV": 
        # if not(os.path.isfile(os.path.join(args.data_path, 'mesh', "rv_endo.obj"))):
        #     getObjFile(os.path.join(args.data_path, 'mesh', "rv_endo.vtk"))
        #endoRVMesh = meshio.read(os.path.join(args.data_path, 'mesh', "rv_endo.obj"))# Original
        RVEndoName = args.mesh_name + "_rv_endo.vtu"

        # endoRVMesh = meshio.read(os.path.join(args.data_path, 'mesh', RVEndoName))# JRDZC
        # endoRVMeshPoints = endoRVMesh.points
        # centerRV=endoRVMeshPoints.mean(0)

        # Load your VTU mesh
        meshRV = pv.read(os.path.join(args.data_path, "mesh", RVEndoName))
        meshRVPoints=meshRV.points

        # Extract boundary edges
        boundary_edgesRV = meshRV.extract_feature_edges(
            boundary_edges=True,
            non_manifold_edges=False,
            feature_edges=False,
            manifold_edges=False
        )
        # Extract points that form the boundary
        boundary_pointsRV = boundary_edgesRV.points 
        #Center of the boundary
        RVCentroid=boundary_pointsRV.mean(0)
        RVCentroid = np.reshape(RVCentroid, (-1, 3))
        #Apex as the farthest point of the center
        disT2MeshRV = cdist(meshRVPoints, RVCentroid, 'euclidean') #Distances of the LVedno to the center
        apexRVIndex = np.argmax(disT2MeshRV) #Index of the point with maximum distance
        apexRVCoor=meshRVPoints[apexRVIndex,:] #Coordinates of point with maximum distance

    else: #If the mesh does not have an RV
        apexRVCoor=meshLVPoints[0,:]#Choose a random point in the LV to use as a second point. Ideally it should be a point of the septum but right now I dont have the labels
        #Later it could be an input


    #Vectors to compute the plane for LV gradient
    v1LV=apexLVCoor-LVCentroid
    v2LV=RVCentroid-LVCentroid


    # Perpendicular vector to free wall and LV apex plane
    vectNormCentrLV=np.cross(v1LV,v2LV) #The results are the a, b and c of the plane equation
    # %ax + by + cz + d = 0
    # %a, b and c are from the normal vector of the plane
    d_one=-1*np.sum(vectNormCentrLV*RVCentroid)
    d_two=-1*np.sum(vectNormCentrLV*apexLVCoor)
    d_three=-1*np.sum(vectNormCentrLV*LVCentroid)
    d_total=np.array([d_one, d_two, d_three])

    #Difference againt the other values
    YLV = cdist(np.reshape(d_total, (3, -1)),np.reshape(d_total, (3, -1)), 'euclidean')

    if not(np.sum((abs(YLV)>(0.001*abs(np.mean(d_total))))*1)): #If all the same
        d2useLV=np.mean(d_total)
    elif np.sum((abs(YLV)>(0.001*abs(np.mean(d_total))))*1)==4: #Just one is different from the rest
        sys.exit("Age less than 18 for 4")

    elif np.sum((abs(YLV)>(0.001*abs(np.mean(d_total))))*1)==6: #They are all very different between them
        sys.exit("Age less than 18 for all")

    #The equation is made by vectNormCentrLV and d2useLV

    equationLV=np.append(np.array(vectNormCentrLV),np.array(d2useLV))
    # equationLV=vectNormCentrLV



    #LV Rotation
    nProcesses=15
    if nProcesses >= os.cpu_count(): nProcesses = os.cpu_count()-1
    pool = mp.Pool(processes=nProcesses)
    resultsLV = [pool.apply(rotationalGradient, args=(equationLV, v1LV,LVCentroid, filledMeshPoint[x,:], -apexRVCoor,x)) for x in range(0,filledMeshPoint.shape[0])]
    resultsLV=np.array(resultsLV)
    resultsLV=resultsLV+np.array(abs(np.min(resultsLV)))
    # print(results)
    print([np.max(resultsLV), np.min(resultsLV)])

    # filledMesh.point_data["LVrotational"]=np.array(resultsLV)


    #Vectors to compute the plane for RV gradient
    if args.domainType == "BiV": 
        v1RV=apexRVCoor-RVCentroid
        v2RV=LVCentroid-RVCentroid

        # Perpendicular vector to free wall and LV apex plane
        vectNormCentrRV=np.cross(v1RV,-v2RV) #I use the negative V2RV because the vector is on the opposite direction of V2LV
        #The results are the a, b and c of the plane equation
        # %ax + by + cz + d = 0
        # %a, b and c are from the normal vector of the plane
        d_one=-1*np.sum(vectNormCentrRV*RVCentroid)
        d_two=-1*np.sum(vectNormCentrRV*apexRVCoor)
        d_three=-1*np.sum(vectNormCentrRV*RVCentroid)
        d_total=np.array([d_one, d_two, d_three])

        #Difference againt the other values
        YRV = cdist(np.reshape(d_total, (3, -1)),np.reshape(d_total, (3, -1)), 'euclidean')

        if not(np.sum((abs(YRV)>(0.001*abs(np.mean(d_total))))*1)): #If all the same
            d2useRV=np.mean(d_total) #The mean of the d value
        elif np.sum((abs(YRV)>(0.001*abs(np.mean(d_total))))*1)==4: #Just one is different from the rest
            sys.exit("Age less than 18 for 4")

        elif np.sum((abs(YRV)>(0.001*abs(np.mean(d_total))))*1)==6: #They are all very different between them
            sys.exit("Age less than 18 for all")


        equationRV=np.append(np.array(vectNormCentrRV),np.array(d2useRV))
        # equationRV=vectNormCentrRV



        pool = mp.Pool(processes=nProcesses)
        resultsRV = [pool.apply(rotationalGradient, args=(equationRV, v1RV,RVCentroid, filledMeshPoint[x,:], apexLVCoor,x)) for x in range(0,filledMeshPoint.shape[0])]
        # resultsRV = [pool.apply(rotationalGradient, args=(equationRV, v1RV,RVCentroid, filledMeshPoint[x,:], apexLVCoor,x)) for x in range(0,1000)]
        
        # for x in range(0,filledMeshPoint.shape[0]):
        #     auxRV=resultsRV[x].shape
        #     if isinstance(auxRV, np.ndarray):
        #         for ll in auxRV:
        #             if ll>1:
        #                 print("Index",x)

        
        resultsRV=np.array(resultsRV)
        resultsRV=resultsRV+np.array(abs(np.min(resultsRV)))
        # print(results)
        print([np.max(resultsRV), np.min(resultsRV)])

        filledMesh.point_data["RVrotational"]=np.array(resultsRV)

        #The equation is made by vectNormCentrRV and d2useRV



    #Save the result mesh
    # filledMesh.write(os.path.join(args.data_path, "layers", "rotational.vtk"))  

    if args.insert2Laplacians:
        mesh_laplacians = meshio.read(os.path.join(args.data_path,"layers", "laplacians.vtk"))
        mesh_laplacians.point_data['LVrotational'] = np.array(resultsLV)
        if args.domainType == "BiV":
            mesh_laplacians.point_data['RVrotational'] = np.array(resultsRV)
            
        mesh_laplacians.write(os.path.join(args.data_path,"layers", "laplacians.vtk"))
    else:
        filledMesh.write(os.path.join(args.data_path, "layers", "rotational.vtk")) 

    





if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))




    # #Try in one point-----------------------------------------------------------------------------------
    # normBasePlane=equationLV
    # longAxisVector=v1LV
    # pointCentroid=LVCentroid
    # point2Use=filledMeshPoint[0,:]
    # point2Comp=-apexRVCoor


    # vectPoint=point2Use-pointCentroid
    # # Perpendicular vector to and Midapex
    # vectNormPoint=np.cross(longAxisVector,vectPoint)
    # #Get d value for plane with point 2 use
    # d_onePoint=-1*np.sum(vectNormPoint*point2Use)
    # d_twoPoint=-1*np.sum(vectNormPoint*pointCentroid)
    # d_totalPoint=np.array([d_onePoint, d_twoPoint])

    # #Difference againt the other values
    # YLV = cdist(np.reshape(d_totalPoint, (2, -1)),np.reshape(d_totalPoint, (2, -1)), 'euclidean')

    # if not(np.sum((abs(YLV)>(0.001*abs(np.mean(d_totalPoint))))*1)): #If all the same
    #     d2usePoint=np.mean(d_totalPoint)
    # elif np.sum((abs(YLV)>(0.001*abs(np.mean(d_totalPoint))))*1)==2: #Just one is different from the rest
    #     sys.exit("Age less than 18 for 4")

    # elif np.sum((abs(YLV)>(0.001*abs(np.mean(d_totalPoint))))*1)==4: #They are all very different between them
    #     sys.exit("Age less than 18 for all")

    # vectNormPoint=np.append(vectNormPoint,d2usePoint)



    # # Angle between plane with point and base plane using their normal vectors
    # # Dot product between both vectors
    # dotP=np.dot(vectNormPoint,normBasePlane)
    
    # # Magnitude of both vectors
    # magnNormPoint=np.sqrt(np.matmul(vectNormPoint,np.transpose(vectNormPoint)))
    # magnNormCentr=np.sqrt(np.matmul(normBasePlane,np.transpose(normBasePlane)))

    # if magnNormPoint==0: #This would mean that the vector is at origin. But technically this would not happen
    #     magnNormPoint=0.000001

    
    # # Angle between both normal vectors(plane towards the chosen point and plane towars the LV centroid)
    # ang_aux=np.arccos(dotP/(magnNormPoint*magnNormCentr)) 
    # ang_aux_deg=ang_aux*180/np.pi  #Value in degrees

    # # Have the values of the coefficient for the planes to see direction 
    # #Value for point 2 compare
    # plane2Comp=np.sum(normBasePlane[0:3]*point2Comp)+normBasePlane[3]
    # #Value for Chosen point
    # planePoint=np.sum(normBasePlane[0:3]*point2Use)+normBasePlane[3]
    
    # # if dotP==0: #Just in case. This would mean that the vector is at origin. But technically this would not happen
        
    # #     print('Eror, dot product equals zero:',point2Comp)
    # #     rotationValue=0
    # #     rotationAngle=0

    # # elif np.sign(plane2Comp)==np.sign(planePoint): #It is anterior
    # #     rotationValue=ang_aux
    # #     rotationAngle=ang_aux_deg

    # # elif -np.sign(plane2Comp)==np.sign(planePoint):#It is posterior
    # #     rotationValue=-ang_aux
    # #     rotationAngle=-ang_aux_deg
    
    # # else: #If the angle is cero
    # #     print('Error Rotational_LV:',point2Comp)
    # #     rotationValue=0 
    # #     rotationAngle=0

    # if np.sign(plane2Comp)==np.sign(planePoint): #It is anterior
    #     rotationValue=ang_aux
    #     rotationAngle=ang_aux_deg

    # elif -np.sign(plane2Comp)==np.sign(planePoint):#It is posterior
    #     rotationValue=-ang_aux
    #     rotationAngle=-ang_aux_deg
    
    # else: #If the angle is cero
    #     print('Error Rotational_LV:',point2Comp)
    #     # rotationValue=0 
    #     # rotationAngle=0

    # rotationalGradient(normBasePlane,longAxisVector, pointCentroid, point2Use, point2Comp):
    