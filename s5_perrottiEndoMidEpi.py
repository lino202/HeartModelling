#Create the layers' tags endo, mid and epi within the mesh. 

# /mnt/e/Jimena/Programas/Simulations/Maxi/HeartModelling/auxiliar/rbm/ldrb_s1_getFacetFunction.py
# /mnt/e/Jimena/Programas/Simulations/Maxi/HeartModelling/s5_perrottiEndoMidEpi.py

import os  
import argparse
import numpy as np
import meshio
import time
import dolfin as df
from scipy.spatial import KDTree

import sys
# sys.path.append("/mnt/e/Jimena/Programas/Simulations/Maxi/HeartModelling/auxiliar/rbm")

import matplotlib.pyplot as plt
import seaborn as sns
# print(sys.executable)
# print(sys.path)



def main():

    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument('--data_path',type=str, required=True,  help='path to data')
    parser.add_argument('--outName',type=str, required=True)
    parser.add_argument('--infAsHealthy', action='store_true', help='if especified, MI is not taken into account')
    parser.add_argument('--mesh_name',     type=str, required=True, help='name of the mesh')
    parser.add_argument('--maxNumPoints',  type=int, help='Value for determining chunksize in Pool', default=1000)
    parser.add_argument('--inCluster', action='store_true', help='if especified, it is in the cluster') #JRDZC 01/08/2025
    parser.add_argument('--add_Apex2base', action='store_true', help='if especified, the sections apex to base are added')
    parser.add_argument('--add_FEC', action='store_true', help='if especified, the FEC layer is added') #JRDZC 01/07/2026
    # parser.add_argument('--thick_Fec', action='store_true', help='if especified, the FEC layer is 2 elements wide') #JRDZC 01/07/2026
    parser.add_argument('--type_FEC',     type=str, help='thicknes of FEC:super Thin(sTHin, only the elements in surface), Thin (1 element) and Thick (2 elements)')
    parser.add_argument('--domainType',    type=str, required=True, help='BiV (Biventricular) or LV')
    args = parser.parse_args()

    print("Started:",args.data_path)

    if not args.inCluster:
        sys.path.append("/mnt/e/Jimena/Programas/Simulations/Maxi/HeartModelling/auxiliar/rbm")
        print("In computer")
    else:
        sys.path.append("/home/bio/jimena.rodriguez/Programas/Maxi/HeartModelling/auxiliar/rbm")
        print("In cluster")

    from utils import getHugeNearest #, isMemberIdxsRowWise

    # --data_path    General path to all files. the outName mesh will be saved there
    # --outName'     Name of the result vtk mesh that will be stored in the general path
    # --infAsHealthy Flags to not join the transmurality and scar. If added, args.infAsHealthy is True.

    validKeys = ["endo", "mid", "epi", "myo", "scar", "bz", "FEC"]
    # validKeys = ["endo", "mid", "epi", "myo", "scar", "bz"]#JRDZC 10/03/2025
    
    myo_flag = 1

    FEC_flag = 2
    endo_flag = 3
    mid_flag = 4
    epi_flag = 5

    uncertain_flag = 6
    bz_flag = 7
    scar_flag = 8

    base_flag=1
    mida_flag=2
    apex_flag=3

    FEC_H_flag = 21
    FEC_BZ_flag = 22
    FEC_S_flag = 23

    endo_H_flag=31
    endo_BZ_flag=32
    endo_S_flag=33

    mid_H_flag=41
    mid_BZ_flag=42
    mid_S_flag=43

    epi_H_flag=51
    epi_BZ_flag=52
    epi_S_flag=53

    #With apex flags
    FEC_H_base_flag = 211 ; FEC_H_mida_flag = 212 ; FEC_H_apex_flag = 213
    FEC_BZ_base_flag = 221 ; FEC_BZ_mida_flag = 222 ; FEC_BZ_apex_flag = 223
    FEC_S_base_flag = 231 ;FEC_S_mida_flag = 232 ; FEC_S_apex_flag = 233

    endo_H_base_flag=311 ; endo_H_mida_flag=312 ; endo_H_apex_flag=313
    endo_BZ_base_flag=321 ; endo_BZ_mida_flag=322; endo_BZ_apex_flag=323
    endo_S_base_flag=331 ; endo_S_mida_flag=332 ; endo_S_apex_flag=333

    mid_H_base_flag=411 ; mid_H_mida_flag=412 ; mid_H_apex_flag=413
    mid_BZ_base_flag=421 ; mid_BZ_mida_flag=422 ; mid_BZ_apex_flag=423
    mid_S_base_flag=431 ; mid_S_mida_flag=432 ; mid_S_apex_flag=433

    epi_H_base_flag=511 ; epi_H_mida_flag=512 ; epi_H_apex_flag=513
    epi_BZ_base_flag=521 ; epi_BZ_mida_flag=522 ; epi_BZ_apex_flag=523
    epi_S_base_flag=531 ; epi_S_mida_flag=532 ; epi_S_apex_flag=533
    
   
    
    #From HeartModelling/ge_s1_getGEGeometry.py "tetmesh_interpolated.vtk"
    # myo_flag = 1
    # uncertain_flag = 2
    # bz_flag = 3
    # scar_flag = 4 

    endo_per = 40; endo_per = endo_per /100
    epi_per = 25; epi_per = epi_per /100
    # FEC_per=10; FEC_per=FEC_per/100

    phi0 = -1
    phi1 = 1

    #Read Data
    #Mesh
    # baseMesh       = meshio.read(os.path.join(args.data_path, 'mesh', "tetmesh.vtk") ) 
    baseMesh       = meshio.read(os.path.join(args.data_path, 'mesh', "{}.vtk".format(args.mesh_name)) ) #JRDZC 07/03/2025. I modified it to vtu because I have trouble reading .vtk.
    #Mesh with endo to epi tags
    meshLaplacians = meshio.read(os.path.join(args.data_path, 'layers', "laplacians_{}.vtk".format(args.mesh_name)) )
    #Mesh with scar tags. It comes from s4_interpolation.py #JRDZC 10/03/2025
    scarmesh = meshio.read(os.path.join(args.data_path, 'mesh', "{}_interpolated.vtk".format(args.mesh_name)) )

    if args.add_FEC:
        #FEC layer will be all the points of 2 element depth from endo
        #Read the mesh surfaces
        LVEndoName = args.mesh_name + "_lv_endo.vtu"
        endoLVMesh = meshio.read(os.path.join(args.data_path, "mesh", LVEndoName))# JRDZC
        endoLVPoints = endoLVMesh.points
        if args.domainType.lower() == "biv":
            RVEndoName = args.mesh_name + "_rv_endo.vtu"
            endoRVMesh = meshio.read(os.path.join(args.data_path, 'mesh', RVEndoName))# JRDZC
            endoRVPoints = endoRVMesh.points
        else:
            endoRVPoints = np.array([])

        #Find points within the surfaces mesh- Jimena 22/07/2026
        treeMesh = KDTree(baseMesh.points)
        _ , idxsLV = treeMesh.query(endoLVPoints, k=1)
        all_markers = np.zeros((baseMesh.points.shape[0]))
        all_markers[idxsLV] = FEC_flag

        if args.domainType.lower() == "biv":
            _ , idxsRV = treeMesh.query(endoRVPoints, k=1)
            all_markers[idxsRV] = FEC_flag
            idxs = [*idxsRV, *idxsLV]

        else:
            idxs = [*idxsLV]

        


        # #Find points within the surfaces mesh -- Maxis version
        # all_markers = np.zeros((baseMesh.points.shape[0]))
        # idxsRV = getHugeNearest(endoRVPoints, baseMesh.points, showMem=True, maxNumPoints=args.maxNumPoints)
        # all_markers[idxsRV] = FEC_flag
        # idxsLV = getHugeNearest(endoLVPoints, baseMesh.points, showMem=True, maxNumPoints=args.maxNumPoints)
        # all_markers[idxsLV] = FEC_flag
        # idxs = [*idxsRV, *idxsLV]
        

        
        if args.type_FEC.lower() == 'sthin':
            points2Choose=np.array(idxs)

        if args.type_FEC.lower() == 'thin' or args.type_FEC.lower() == 'thick':
            # idxs = [*idxsRV, *idxsLV]
            elementsSurface=baseMesh.cells_dict['tetra']
            elemS=np.isin(elementsSurface, idxs) #FInd elements with those points in the surface
            cell2Choose=np.sum(elemS,axis=1) #Sum , to find all elemets with at least1 point in the surface
            cell2Choose=cell2Choose!=0 #FInd elements that have at least one, sum>0
            #Choose the whole cell if at least a vertex is in the surface
            elem2Choose=elementsSurface[cell2Choose,:] #Choose the elems
            elem2Choose=np.reshape(elem2Choose, (-1,1)) 
            points2Choose=np.unique(elem2Choose) #These are the points, not the elems

            if args.type_FEC.lower() == 'thick':
                #Find a second layer of points that touch an element that has at least one point in the surface
                elemS=np.isin(elementsSurface, points2Choose)
                cell2Choose=np.sum(elemS,axis=1)
                cell2Choose=cell2Choose!=0
                #Choose the whole cell if at least a vertex is in the surface
                elem2Choose=elementsSurface[cell2Choose,:]
                elem2Choose=np.reshape(elem2Choose, (-1,1)) 
                points2Choose=np.unique(elem2Choose)

        #modify the array format for it to be compatible later
        points2ChooseBool=np.zeros(baseMesh.points.shape[0])
        points2ChooseBool[points2Choose]=1
        points2ChooseBool = points2ChooseBool.astype(bool) #This is the points to choose, not elems

        # idxs=[*idxs, *elementsSurface[elemS]]
        # idxs=np.array(idxs)
        # # all_markers[elementsSurface[elemS]]=FEC_flag
        # elemS*elementsSurface
        # np.sum((idxs==0)*1)
        # xy, x_ind, y_ind=np.intersect1d(elementsSurface,idxs,return_indices=True)
        # print("Geometric dimension:", ffun.geometry().dim())
        # print("Topological dimension:", ffun.topology().dim())
    else: #If FEC is not added
        points2ChooseBool=np.zeros(baseMesh.points.shape[0])
        points2ChooseBool = points2ChooseBool.astype(bool)

    
    #Change data reference points for incorporating endo mid and epi
    # if "layers_mi" in meshLaplacians.point_data.keys():
    #     all_points = meshLaplacians.point_data["layers_mi"]
    if "layers_mi" in scarmesh.point_data.keys():#Modified the file because in the laplacians.vtk there is no info on layers.JRDZC 10/03/2025
        all_points = scarmesh.point_data["layers_mi"]
    else: #It should never enter this becasue the scarmesh file has the layers_mi 
        all_points = np.zeros((meshLaplacians.points.shape[0]))
    
    #Modify the values of the tags to incorporate the scar all_points==1 is myo_flag
    all_points[all_points==2] = uncertain_flag
    all_points[all_points==3] = bz_flag
    all_points[all_points==4] = scar_flag

    #Calculate layers to correspond the values of -1 (endo) to 1 (epi)
    phi_endo = (1-endo_per) * phi0 + endo_per * phi1    #thresholds
    phi_epi = epi_per * phi0 + (1-epi_per) * phi1

    # phi_FEC = (1-FEC_per) * phi0 + FEC_per * phi1

    #Whole transmurality----------------
    #Find point which correspond to Endo
    transA_endo = np.zeros((meshLaplacians.points.shape[0]))
    transA_endo[meshLaplacians.point_data['xv']<phi_endo] = 1
    transA_endo = transA_endo.astype(bool)

    # transA_FEC = np.zeros((meshLaplacians.points.shape[0]))
    # transA_FEC[meshLaplacians.point_data['xv']<phi_FEC] = 1
    # transA_FEC = transA_FEC.astype(bool)

    #Find point which correspond to Epi
    transA_epi = np.zeros((meshLaplacians.points.shape[0]))
    transA_epi[meshLaplacians.point_data['xv']>phi_epi] = 1
    transA_epi = transA_epi.astype(bool)

    #Find point which correspond to Mid
    transA_mid = np.zeros((meshLaplacians.points.shape[0]))
    transA_mid[(meshLaplacians.point_data['xv']<=phi_epi) & (meshLaplacians.point_data['xv']>=phi_endo)] = 1
    transA_mid = transA_mid.astype(bool)

    #RV transmurality---------------------
    #Find point which correspond to Enddo RV
    transB_endo = np.zeros((meshLaplacians.points.shape[0]))
    transB_endo[meshLaplacians.point_data['rv']<phi_endo] = 1
    transB_endo = transB_endo.astype(bool)

    # transB_FEC = np.zeros((meshLaplacians.points.shape[0]))
    # transB_FEC[meshLaplacians.point_data['rv']<phi_FEC] = 1
    # transB_FEC = transB_FEC.astype(bool)

    #Find point which correspond to Epi RV
    transB_epi = np.zeros((meshLaplacians.points.shape[0]))
    transB_epi[meshLaplacians.point_data['rv']>phi_epi] = 1
    transB_epi = transB_epi.astype(bool)

    #Find point which correspond to Mid RV
    transB_mid = np.zeros((meshLaplacians.points.shape[0]))
    transB_mid[(meshLaplacians.point_data['rv']<=phi_epi) & (meshLaplacians.point_data['rv']>=phi_endo)] = 1
    transB_mid = transB_mid.astype(bool)

    #LV transmurality----------------------
    #Find point which correspond to Endo LV
    transC_endo = np.zeros((meshLaplacians.points.shape[0])) 
    transC_endo[meshLaplacians.point_data['lv']<phi_endo] = 1
    transC_endo = transC_endo.astype(bool)

    # transC_FEC = np.zeros((meshLaplacians.points.shape[0]))
    # transC_FEC[meshLaplacians.point_data['lv']<phi_FEC] = 1
    # transC_FEC = transC_FEC.astype(bool)

    #Find point which correspond to Epi LV
    transC_epi = np.zeros((meshLaplacians.points.shape[0]))
    transC_epi[meshLaplacians.point_data['lv']>phi_epi] = 1
    transC_epi = transC_epi.astype(bool)

    #Find point which correspond to Mid LV
    transC_mid = np.zeros((meshLaplacians.points.shape[0])) 
    transC_mid[(meshLaplacians.point_data['lv']<=phi_epi) & (meshLaplacians.point_data['lv']>=phi_endo)] = 1
    transC_mid = transC_mid.astype(bool)

    #Transmurality labels
    algo_points = np.zeros((meshLaplacians.points.shape[0])) 
    #We saw that algo 2 is more biomimetic
    #Algo 2 use A, B and C
    algo_points[transA_epi] = epi_flag
    algo_points[(transA_endo | transA_mid) & (transB_mid | transB_epi) & (transC_mid | transC_epi)] = mid_flag
    algo_points[(transA_endo | transA_mid) & (transB_endo | transC_endo)] = endo_flag

    #Create the FEC layers
    if args.add_FEC:
        algo_pointsFEC=algo_points.copy()
        algo_pointsFEC[points2ChooseBool]=FEC_flag
        # algo_points[(transA_FEC | transA_mid) & (transB_FEC | transC_FEC)] = FEC_flag
        # algo_points_mod=algo_points.copy() #To also add the scar tissue #JRDZC 18/03/2025

    #Check it there are zeros left in the array #JRDZC 10/03/2025
    t_0=sum(algo_points==0)
    if t_0:
        print("There are zeros in the array \n \n")

    #Apex to base flags
    apex2base_points = np.zeros((meshLaplacians.points.shape[0])) 
    apex2base_points[meshLaplacians.point_data['base_apex']<0.45] = base_flag
    apex2base_points[(meshLaplacians.point_data['base_apex']>=0.45) & (meshLaplacians.point_data['base_apex']<0.8)] = mida_flag #Base
    apex2base_points[meshLaplacians.point_data['base_apex']>=0.8] = apex_flag

    # if apex2baseID>=(-0.01) and apex2baseID<(0.33):
    #     elif apex2baseID>=(0.33) and apex2baseID<(0.66):
    #     elif apex2baseID>=(0.66) and apex2baseID<(1.01):
    # if args.add_Apex2base:
    #     result = int("".join(map(str, a)))
        
    # scarmesh
    if not args.infAsHealthy:#Join the transmurality with the scar
        endoBZ_points = np.zeros((meshLaplacians.points.shape[0])) 
        endoBZ_points[np.where((all_points==bz_flag) & (algo_points==endo_flag))] = 1
        midBZ_points = np.zeros((meshLaplacians.points.shape[0])) 
        midBZ_points[np.where((all_points==bz_flag) & (algo_points==mid_flag))] = 1
        epiBZ_points = np.zeros((meshLaplacians.points.shape[0])) 
        epiBZ_points[np.where((all_points==bz_flag) & (algo_points==epi_flag))] = 1


        #Add the scar flags to the transmurality in one filed
        algo_points_mod = np.zeros((meshLaplacians.points.shape[0])) 
        #Endo
        algo_points_mod[(algo_points==endo_flag)]=endo_H_flag
        algo_points_mod[(algo_points==endo_flag) & (all_points==bz_flag)] = endo_BZ_flag
        algo_points_mod[(algo_points==endo_flag) & (all_points==scar_flag)] = endo_S_flag

        algo_points_mod[(algo_points==epi_flag)]=epi_H_flag
        algo_points_mod[(algo_points==epi_flag) & (all_points==bz_flag)] = epi_BZ_flag
        algo_points_mod[(algo_points==epi_flag) & (all_points==scar_flag)] = epi_S_flag

        algo_points_mod[(algo_points==mid_flag)]=mid_H_flag
        algo_points_mod[(algo_points==mid_flag) & (all_points==bz_flag)] = mid_BZ_flag
        algo_points_mod[(algo_points==mid_flag) & (all_points==scar_flag)] = mid_S_flag

        if args.add_FEC:
            algo_points_modFEC=algo_points_mod.copy()
            algo_points_modFEC[(algo_pointsFEC==FEC_flag)]=FEC_H_flag
            algo_points_modFEC[(algo_pointsFEC==FEC_flag) & (all_points==bz_flag)] = FEC_BZ_flag
            algo_points_modFEC[(algo_pointsFEC==FEC_flag) & (all_points==scar_flag)] = FEC_S_flag

        if args.add_Apex2base: #Add the apex to base values
            algo_points_mod_apex = [int(f"{int(x)}{int(y)}") for x, y in zip(algo_points_mod, apex2base_points)]

            if args.add_FEC:
                algo_points_mod_apexFEC=[int(f"{int(x)}{int(y)}") for x, y in zip(algo_points_modFEC, apex2base_points)]


        # algo_points_mod[points2ChooseBool]=FEC_H_flag 
        # algo_points_mod[points2ChooseBool & (all_points==bz_flag)]=FEC_BZ_flag #Add FEC layer over the BZ
        # algo_points_mod[points2ChooseBool & (all_points==scar_flag)]=FEC_S_flag #Add FEC layer over the BZ
        #I remove this to not have overlapping segments #JRDZC 10/03/2025

    
    #For algo_points and all_points
    # myo_flag = 1
    # scar_flag = 8
    # endo_flag = 3
    # mid_flag = 4
    # epi_flag = 5
    # uncertain_flag = 6
    # bz_flag = 7


    # point_data = meshLaplacians.point_data # Maybe we need to save data already compute as the tissues for MI
    point_data = {}
    nsets = {}
    for tissueType in validKeys: #validKeys = ["endo", "mid", "epi", "myo", "scar", "bz"]
        point_data[tissueType] = np.zeros((meshLaplacians.points.shape[0]))
        if tissueType=="FEC" and args.add_FEC:
            point_data[tissueType][algo_pointsFEC==locals()["{}_flag".format(tissueType)]] = 1
            nsets["{}_nodes".format(tissueType)] = np.where(point_data[tissueType] == 1)[0]

        #Transmurality tags
        point_data[tissueType][algo_points==locals()["{}_flag".format(tissueType)]] = 1
        nsets["{}_nodes".format(tissueType)] = np.where(point_data[tissueType] == 1)[0]
        #Scar tags #JRDZC 10/03/2025
        point_data[tissueType][all_points==locals()["{}_flag".format(tissueType)]] = 1
        nsets["{}_nodes".format(tissueType)] = np.where(point_data[tissueType] == 1)[0]
        if sum(algo_points==locals()["{}_flag".format(tissueType)]) & sum(all_points==locals()["{}_flag".format(tissueType)]):
            print("Overlapping segments \n \n")

    point_data["layers"] = algo_points
    point_data["layers_scar"] = algo_points_mod #Filed with the transmurality and scar
    point_data["apex_base"] =apex2base_points

    if args.add_FEC:
        point_data["layers_FECini"] = algo_pointsFEC
        point_data["layers_scar_FECini"] = algo_points_modFEC #Filed with the transmurality and scar

    if args.add_Apex2base: #Add the apex to base values
            algo_points_apex = [int(f"{int(x)}{int(y)}") for x, y in zip(algo_points, apex2base_points)]
            point_data["layers_apex"] = algo_points_apex 
            point_data["layers_scar_apex"]=algo_points_mod_apex

            if args.add_FEC:
                algo_points_apexFEC = [int(f"{int(x)}{int(y)}") for x, y in zip(algo_pointsFEC, apex2base_points)]
                point_data["layers_apex_FECini"] = algo_points_apexFEC 
                point_data["layers_scar_apex_FECini"]=algo_points_mod_apexFEC

    f, (ax_box, ax_hist) = plt.subplots(2, sharex=True, gridspec_kw={"height_ratios": (.15, .85)})
    f.suptitle('Edge lengths') #JRDZC Add 14/01/2025
    sns.histplot(x=point_data["layers_scar_apex"], ax=ax_hist)

    


    if not args.infAsHealthy:
        point_data["endoBZ"] = endoBZ_points
        point_data["midBZ"] = midBZ_points
        point_data["epiBZ"] = epiBZ_points
        nsets["endobz_nodes"] = np.where(endoBZ_points==1)[0]
        nsets["midbz_nodes"] = np.where(midBZ_points==1)[0]
        nsets["epibz_nodes"] = np.where(epiBZ_points==1)[0]

    #Join data in one tag- for openCARP #JRDZC 18/03/2025


    


    #SaveData
    meshOutVtk = meshio.Mesh(baseMesh.points, baseMesh.cells, point_data=point_data)
    meshOutVtk.write(os.path.join(args.data_path, "{}.vtk".format(args.outName)))

    meshOutInp = meshio.Mesh(baseMesh.points, baseMesh.cells, point_sets=nsets)
    meshOutInp.write(os.path.join(args.data_path, "{}.inp".format(args.outName)))

    print("Finished:",args.data_path)

if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))


