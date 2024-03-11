import os  
import argparse
import numpy as np
import meshio
import time

def main():

    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument('--dataPath',type=str, required=True,  help='path to data')
    parser.add_argument('--outName',type=str, required=True)
    parser.add_argument('--infAsHealthy', action='store_true', help='if especified, MI is not taken into account')
    args = parser.parse_args()

    validKeys = ["endo", "mid", "epi", "myo", "scar", "uncertain", "bz"]
    myo_flag = 1
    scar_flag = 8
    endo_flag = 3
    mid_flag = 4
    epi_flag = 5
    uncertain_flag = 6
    bz_flag = 7

    endo_per = 40; endo_per = endo_per /100
    epi_per = 25; epi_per = epi_per /100

    phi0 = -1
    phi1 = 1

    #Read Data
    meshLaplacians = meshio.read(os.path.join(args.dataPath, 'layers', "laplacians.vtk") )
    #Change data reference points for incorporating endo mid and epi
    if "layers_mi" in meshLaplacians.point_data.keys():
        all_points = meshLaplacians.point_data["layers_mi"]
    else:
        all_points = np.zeros((meshLaplacians.points.shape[0]))
    all_points[all_points==2] = uncertain_flag
    all_points[all_points==3] = bz_flag
    all_points[all_points==4] = scar_flag

    #Calculate layers
    phi_endo = (1-endo_per) * phi0 + endo_per * phi1    #thresholds
    phi_epi = epi_per * phi0 + (1-epi_per) * phi1

    transA_endo = np.zeros((meshLaplacians.points.shape[0]))
    transA_endo[meshLaplacians.point_data['xv']<phi_endo] = 1
    transA_endo = transA_endo.astype(bool)

    transA_epi = np.zeros((meshLaplacians.points.shape[0]))
    transA_epi[meshLaplacians.point_data['xv']>phi_epi] = 1
    transA_epi = transA_epi.astype(bool)

    transA_mid = np.zeros((meshLaplacians.points.shape[0]))
    transA_mid[(meshLaplacians.point_data['xv']<=phi_epi) & (meshLaplacians.point_data['xv']>=phi_endo)] = 1
    transA_mid = transA_mid.astype(bool)

    transB_endo = np.zeros((meshLaplacians.points.shape[0]))
    transB_endo[meshLaplacians.point_data['rv']<phi_endo] = 1
    transB_endo = transB_endo.astype(bool)

    transB_epi = np.zeros((meshLaplacians.points.shape[0]))
    transB_epi[meshLaplacians.point_data['rv']>phi_epi] = 1
    transB_epi = transB_epi.astype(bool)

    transB_mid = np.zeros((meshLaplacians.points.shape[0]))
    transB_mid[(meshLaplacians.point_data['rv']<=phi_epi) & (meshLaplacians.point_data['rv']>=phi_endo)] = 1
    transB_mid = transB_mid.astype(bool)

    transC_endo = np.zeros((meshLaplacians.points.shape[0])) 
    transC_endo[meshLaplacians.point_data['lv']<phi_endo] = 1
    transC_endo = transC_endo.astype(bool)

    transC_epi = np.zeros((meshLaplacians.points.shape[0]))
    transC_epi[meshLaplacians.point_data['lv']>phi_epi] = 1
    transC_epi = transC_epi.astype(bool)

    transC_mid = np.zeros((meshLaplacians.points.shape[0])) 
    transC_mid[(meshLaplacians.point_data['lv']<=phi_epi) & (meshLaplacians.point_data['lv']>=phi_endo)] = 1
    transC_mid = transC_mid.astype(bool)

    algo_points = np.zeros((meshLaplacians.points.shape[0])) 

    #We saw that algo 2 is more biomimetic
    #Algo 2 use A, B and C
    algo_points[transA_epi] = epi_flag
    algo_points[(transA_endo | transA_mid) & (transB_mid | transB_epi) & (transC_mid | transC_epi)] = mid_flag
    algo_points[(transA_endo | transA_mid) & (transB_endo | transC_endo)] = endo_flag

    if not args.infAsHealthy:
        endoBZ_points = np.zeros((meshLaplacians.points.shape[0])) 
        endoBZ_points[np.where((all_points==bz_flag) & (algo_points==endo_flag))] = 1
        midBZ_points = np.zeros((meshLaplacians.points.shape[0])) 
        midBZ_points[np.where((all_points==bz_flag) & (algo_points==mid_flag))] = 1
        epiBZ_points = np.zeros((meshLaplacians.points.shape[0])) 
        epiBZ_points[np.where((all_points==bz_flag) & (algo_points==epi_flag))] = 1
        algo_points[all_points==bz_flag] = bz_flag
        algo_points[all_points==scar_flag] = scar_flag

    # point_data = meshLaplacians.point_data # Maybe we need to save data already compute as the tissues for MI
    point_data = {}
    nsets = {}
    for tissueType in validKeys:
        point_data[tissueType] = np.zeros((meshLaplacians.points.shape[0]))
        point_data[tissueType][algo_points==locals()["{}_flag".format(tissueType)]] = 1
        nsets["{}_nodes".format(tissueType)] = np.where(point_data[tissueType] == 1)[0]
    point_data["layers"] = algo_points


    if not args.infAsHealthy:
        point_data["endoBZ"] = endoBZ_points
        point_data["midBZ"] = midBZ_points
        point_data["epiBZ"] = epiBZ_points
        nsets["endobz_nodes"] = np.where(endoBZ_points==1)[0]
        nsets["midbz_nodes"] = np.where(midBZ_points==1)[0]
        nsets["epibz_nodes"] = np.where(epiBZ_points==1)[0]

    #SaveData
    meshOutVtk = meshio.Mesh(meshLaplacians.points, meshLaplacians.cells, point_data=point_data)
    meshOutVtk.write(os.path.join(args.dataPath, "{}.vtk".format(args.outName)))

    meshOutInp = meshio.Mesh(meshLaplacians.points, meshLaplacians.cells, point_sets=nsets)
    meshOutInp.write(os.path.join(args.dataPath, "{}.inp".format(args.outName)))

if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))

