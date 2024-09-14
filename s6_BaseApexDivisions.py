import os  
import argparse
import numpy as np
import meshio
import time

def main():

    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument('--dataPath',type=str, required=True,  help='path to data')
    parser.add_argument('--meshName',type=str, required=True,  help='Name of the .vtk mesh to use')
    parser.add_argument('--mid_base_perc',type=float, default=48, help="the percentage of the maximum value in the gradient for the mid_base threshold")
    parser.add_argument('--mid_apex_perc',type=float, default=83, help="the percentage of the maximum value in the gradient for the mid_apex threshold")
    args = parser.parse_args()

    validKeys = ["endo", "mid", "epi", "myo", "scar", "bz"]
    myo_flag = 1
    scar_flag = 8
    endo_flag = 3; base_endo_flag = 11; mid_endo_flag = 12; apex_endo_flag = 13
    mid_flag = 4;  base_mid_flag = 14; mid_mid_flag = 15; apex_mid_flag = 16
    epi_flag = 5;  base_epi_flag = 17; mid_epi_flag = 18; apex_epi_flag = 19
    uncertain_flag = 6
    bz_flag = 7

    
    #Read Data
    mesh       = meshio.read(os.path.join(args.dataPath, "{}.vtk".format(args.meshName)) )  #Mesh with layers point_data
    meshLaplacians = meshio.read(os.path.join(args.dataPath, 'layers', "laplacians.vtk") )
    
    base_apex = meshLaplacians.point_data['base_apex']
    layers    = mesh.point_data['layers']

    mid_base_th = base_apex.max()*args.mid_base_perc/100
    mid_apex_th = base_apex.max()*args.mid_apex_perc/100

    # Apex
    idxs = np.where(base_apex>=mid_apex_th)[0]
    layers[idxs[np.where(layers[idxs]==endo_flag)[0]]] = apex_endo_flag 
    layers[idxs[np.where(layers[idxs]==mid_flag)[0]]]  = apex_mid_flag
    layers[idxs[np.where(layers[idxs]==epi_flag)[0]]]  = apex_epi_flag

    # Base
    idxs = np.where(base_apex<=mid_base_th)[0]
    layers[idxs[np.where(layers[idxs]==endo_flag)[0]]] = base_endo_flag 
    layers[idxs[np.where(layers[idxs]==mid_flag)[0]]]  = base_mid_flag
    layers[idxs[np.where(layers[idxs]==epi_flag)[0]]]  = base_epi_flag


    # Mid
    layers[layers==endo_flag] = mid_endo_flag 
    layers[layers==mid_flag]  = mid_mid_flag
    layers[layers==epi_flag]  = mid_epi_flag


    #SaveData
    mesh.point_data['layers'] = layers
    mesh.write(os.path.join(args.dataPath, "{}.vtk".format(args.meshName)))

if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))

