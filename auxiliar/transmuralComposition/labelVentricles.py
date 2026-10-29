""""Create the Ids for LV, RV and septum 
You need the surface meshes of the LV endo, RV endo and epi.
It is based on the distance between the desired point to ID and the surfaces it is closest ot.
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
# import sys
import multiprocessing as mp #For parallel computation
from scipy.spatial import KDTree
 
def meshID(LVendoPoints,RVendoPoints, EpiPoints, Point2Use):
    # def meshID(LVendoPoints,RVendoPoints, EpiPoints, Point2Use):
    # LVendoPoints=meshLVPoints
    # RVendoPoints=meshRVPoints
    # EpiPoints=meshEpiPoints
    # Point2Use=filledMeshPoint[10,:]

    #Closes point to LVendo
    dist2LVEndo=cdist(np.reshape(Point2Use, (1, 3)), LVendoPoints, 'euclidean')
    minDist2LVendo=np.min(dist2LVEndo)
    closeLVEndoPoint=LVendoPoints[np.argmin(dist2LVEndo),:]
    farLVEndoPoint=LVendoPoints[np.argmax(dist2LVEndo),:]

    #Closes point to RVendo
    dist2RVEndo=cdist(np.reshape(Point2Use, (1, 3)), RVendoPoints, 'euclidean')
    minDist2RVendo=np.min(dist2RVEndo)
    closeRVEndoPoint=RVendoPoints[np.argmin(dist2RVEndo),:]
    farRVEndoPoint=RVendoPoints[np.argmax(dist2RVEndo),:]

    #Closes point to LVendo
    dist2Epi=cdist(np.reshape(Point2Use, (1, 3)), EpiPoints, 'euclidean')
    minDist2Epi=np.min(dist2Epi)
    closeEpiPoint=EpiPoints[np.argmin(dist2Epi),:]
    farEpiPoint=EpiPoints[np.argmax(dist2Epi),:]

    distArray=np.array([minDist2LVendo,minDist2RVendo,minDist2Epi])
    distArraySorted = sorted(enumerate(distArray), key=lambda i: i[1])
    LVLabel=0
    RVlabel=1
    SeptumLabel=2
    #LV endo=0, RV endo =1, Epi = 2
    #LV Endo & Epi #LV endo=0, Epi = 2
    if (distArraySorted[0][0]==0 and distArraySorted[1][0]==2) or (distArraySorted[0][0]==2 and distArraySorted[1][0]==0):
        PointID=LVLabel
    #RV Endo & Epi #RV endo =1, Epi = 2
    elif (distArraySorted[0][0]==1 and distArraySorted[1][0]==2) or (distArraySorted[0][0]==2 and distArraySorted[1][0]==1):
        PointID=RVlabel
    #LV Endo & RV Endo #LV endo=0, RV endo =1,
    elif(distArraySorted[0][0]==0 and distArraySorted[1][0]==1) or  (distArraySorted[0][0]==1 and distArraySorted[1][0]==0):
        PointID=SeptumLabel
    else:
        print("Error in labels")
        PointID=np.nan

    return PointID

def meshID_aux(distLV,distRV, distEpi):
    # x=10
    # point2Use=filledMeshPoint[x,:]
    # distLV=distancesLV[x]
    # distRV=distancesRV[x]
    # distEpi=distancesEpi[x]

    distArray=np.array([distLV,distRV,distEpi])
    distArraySorted = sorted(enumerate(distArray), key=lambda i: i[1])
    LVLabel=0
    RVlabel=1
    SeptumLabel=2
    #LV endo=0, RV endo =1, Epi = 2
    #LV Endo & Epi #LV endo=0, Epi = 2
    if (distArraySorted[0][0]==0 and distArraySorted[1][0]==2) or (distArraySorted[0][0]==2 and distArraySorted[1][0]==0):
        PointID=LVLabel
    #RV Endo & Epi #RV endo =1, Epi = 2
    elif (distArraySorted[0][0]==1 and distArraySorted[1][0]==2) or (distArraySorted[0][0]==2 and distArraySorted[1][0]==1):
        PointID=RVlabel
    #LV Endo & RV Endo #LV endo=0, RV endo =1,
    elif(distArraySorted[0][0]==0 and distArraySorted[1][0]==1) or  (distArraySorted[0][0]==1 and distArraySorted[1][0]==0):
        PointID=SeptumLabel
    else:
        print("Error in labels")
        PointID=np.nan

    return PointID


def main():
    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument('--data_path',type=str, required=True, help='path to data')
    parser.add_argument('--mesh_name',type=str, required=True, help='Mesh to use. With surfaces') 
    # parser.add_argument('--domainType',    type=str, required=True, help='BiV (Biventricular) or LV')
    # parser.add_argument('--filesInLapacians', action='store_true', help='If called the layers/laplacians.vtk mesh is searched for the labels needed')
    parser.add_argument('--insert2Laplacians', action='store_true', help='If called the layers/laplacians.vtk mesh is searched and the apex_base grad is added')
    
    
    # parser.add_argument('--radius',type=float, default=6, help='Radius for defining the apex subdomain for the BC')
    args = parser.parse_args()

    filledMesh=meshio.read(os.path.join(args.data_path, "mesh", "mesh_{}.xdmf".format(args.mesh_name)))
    filledMeshPoint=filledMesh.points


    # Load your LV endo VTU mesh
    LVEndoName = args.mesh_name + "_lv_endo.vtu"
    meshLV = pv.read(os.path.join(args.data_path, "mesh", LVEndoName))
    meshLVPoints=meshLV.points

    # Load your RV endo VTU mesh
    RVEndoName = args.mesh_name + "_rv_endo.vtu"
    meshRV = pv.read(os.path.join(args.data_path, "mesh", RVEndoName))
    meshRVPoints=meshRV.points

    # Load your Epi VTU mesh
    EpiName = args.mesh_name + "_epi.vtu"
    meshEpi = pv.read(os.path.join(args.data_path, "mesh", EpiName))
    meshEpiPoints=meshEpi.points

    treeLV = KDTree(meshLVPoints)
    distancesLV, indicesLV = treeLV.query(filledMeshPoint) 

    treeRV = KDTree(meshRVPoints)
    distancesRV, indicesRV = treeRV.query(filledMeshPoint) 

    treeEpi = KDTree(meshEpiPoints)
    distancesEpi, indicesEpi = treeEpi.query(filledMeshPoint) 
    
    # dists = np.linalg.norm(filledMeshPoint[:, np.newaxis, :] - meshLVPoints[np.newaxis, :, :], axis=2)

    


    nProcesses=20
    if nProcesses >= os.cpu_count(): nProcesses = os.cpu_count()-1
    pool = mp.Pool(processes=nProcesses)
    LabelsID = [pool.apply(meshID_aux, args=(distancesLV[x], distancesRV[x],distancesEpi[x])) for x in range(0,filledMeshPoint.shape[0])]
    




    # nProcesses=20
    # if nProcesses >= os.cpu_count(): nProcesses = os.cpu_count()-1
    # pool = mp.Pool(processes=nProcesses)
    # LabelsID = [pool.apply(meshID, args=(meshLVPoints, meshRVPoints,meshEpiPoints, filledMeshPoint[x,:])) for x in range(0,filledMeshPoint.shape[0])]
    

    if args.insert2Laplacians:
        mesh_laplacians = meshio.read(os.path.join(args.data_path,"layers", "laplacians_{}.vtk".format(args.mesh_name)))
        mesh_laplacians.point_data['LabelsID'] = np.array(LabelsID)
        mesh_laplacians.write(os.path.join(args.data_path,"layers", "laplacians_{}.vtk".format(args.mesh_name)))
    else:
        filledMesh.point_data["LabelsID"]=np.array(LabelsID)
        filledMesh.write(os.path.join(args.data_path, "layers", "IDs_{}.vtk".format(args.mesh_name)))  




if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))

# # def meshID(LVendoPoints,RVendoPoints, EpiPoints, Point2Use):
    # LVendoPoints=meshLVPoints
    # RVendoPoints=meshRVPoints
    # EpiPoints=meshEpiPoints
    # Point2Use=filledMeshPoint[10,:]

    # #Closes point to LVendo
    # dist2LVEndo=cdist(np.reshape(Point2Use, (1, 3)), LVendoPoints, 'euclidean')
    # minDist2LVendo=np.min(dist2LVEndo)
    # closeLVEndoPoint=LVendoPoints[np.argmin(dist2LVEndo),:]
    # farLVEndoPoint=LVendoPoints[np.argmax(dist2LVEndo),:]

    # #Closes point to RVendo
    # dist2RVEndo=cdist(np.reshape(Point2Use, (1, 3)), RVendoPoints, 'euclidean')
    # minDist2RVendo=np.min(dist2RVEndo)
    # closeRVEndoPoint=RVendoPoints[np.argmin(dist2RVEndo),:]
    # farRVEndoPoint=RVendoPoints[np.argmax(dist2RVEndo),:]

    # #Closes point to LVendo
    # dist2Epi=cdist(np.reshape(Point2Use, (1, 3)), EpiPoints, 'euclidean')
    # minDist2Epi=np.min(dist2Epi)
    # closeEpiPoint=EpiPoints[np.argmin(dist2Epi),:]
    # farEpiPoint=EpiPoints[np.argmax(dist2Epi),:]

    # distArray=np.array([minDist2LVendo,minDist2RVendo,minDist2Epi])
    # distArraySorted = sorted(enumerate(distArray), key=lambda i: i[1])
    # LVLabel=0
    # RVlabel=1
    # SeptumLabel=2
    # #LV endo=0, RV endo =1, Epi = 2
    # #LV Endo & Epi #LV endo=0, Epi = 2
    # if (distArraySorted[0][0]==0 and distArraySorted[1][0]==2) or (distArraySorted[0][0]==2 and distArraySorted[1][0]==0):
    #     PointID=LVLabel
    # #RV Endo & Epi #RV endo =1, Epi = 2
    # elif (distArraySorted[0][0]==1 and distArraySorted[1][0]==2) or (distArraySorted[0][0]==2 and distArraySorted[1][0]==1):
    #     PointID=RVlabel
    # #LV Endo & RV Endo #LV endo=0, RV endo =1,
    # elif(distArraySorted[0][0]==0 and distArraySorted[1][0]==1) or  (distArraySorted[0][0]==1 and distArraySorted[1][0]==0):
    #     PointID=SeptumLabel
    # else:
    #     print("Error in labels")
    #     PointID=np.nan