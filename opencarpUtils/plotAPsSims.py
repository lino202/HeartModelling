'''
Compare APs of the same patients but different simulations. The APs are plotted in the same figure for comparison.
Mesh needs to be the same
'''


import pyvista as pv
import numpy as np
import argparse
import os
import time
import utils as ut
import sys
import matplotlib.pyplot as plt
import meshio

import binascii

# import carputils as carp
import carputils.carpio.igb as carp
from scipy.signal import find_peaks

import scipy.io


def read_data_from_mat(filename):
    
    vm_values = scipy.io.loadmat(filename)
    
    # vm_values=np.transpose(vm_values)

    return vm_values

def read_data_from_txt(filename):
    vm_values=np.loadtxt(filename)
    vm_values=np.transpose(vm_values)


    # f = open(filename)
    # vm_values=f.readline()

    return vm_values

def read_data_from_igb(filename):
    """

    Extracts the complete mesh data from the phie.igb or vm.igb file using CARPutils, which contains the data for the body
    surface potential for an entire human torso.

    Parameters
    ----------
    filename : str
        Filename for the phie.igb data to extract

    References
    ----------
    https://carpentry.medunigraz.at/carputils/generated/carputils.carpio.igb.IGBFile.html#carputils.carpio.igb.IGBFile
    """
    inputfile=carp.read(filename)
    header=inputfile[1]
    vm_values=inputfile[0]
    # vm_values=np.transpose(vm_values)


    return header,vm_values

def main():
    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument('--mesh_path',      type=str, required=True, help='path to mesh')
    parser.add_argument('--mesh_name',      type=str, required=True, help='name of mesh with the end')
    parser.add_argument('--simulation_path',     type=str, nargs='+', required=True, help='path to vm. It can be one path for all simulations or different paths for each simulation')
    parser.add_argument('--vm_path_input',     type=str, nargs='+', required=True, help='path to vm, result of openCARP')
    # parser.add_argument('--vm_input_format',     type=str, required=True, help='format, result of openCARP')
    parser.add_argument('--simulation_number',     type=str, required=True, help='path to vm, result of openCARP')
    parser.add_argument('--points_2_see',   nargs='+',    type=int, required=True, help="Labels of zones to get the APs and compare")
    parser.add_argument('--cellType',        type=str, default="tetra")
    # parser.add_argument('--normalizeECG', type=str,  help='If to normalize the ECG plot to the maximum value of each lead or of all leads (ind or all). ')
        
    
    
    
    args = parser.parse_args()

    #Load mesh
    meshName=os.path.join(args.mesh_path, args.mesh_name)
    # mesh = pv.read(meshName)
    mesh = meshio.read(meshName)

    #Save the vm values for each simulation in a dictionary
    vm_values_all=dict()    

    
    for auxpath,i in enumerate(args.simulation_path):
        auxpath_name='simulation_'+str(i)
        sim_number=os.path.split(auxpath)[-1]
        vm_values_all[auxpath_name]=[]
        for lns in args.points_2_see: 
            vm_values_all[auxpath_name][str(lns)]=[]

        #Create path to sim
        # vaux = args.vm_path_input
        # vm_path=os.path.join(auxpath,vaux)
        
        vm_path=os.path.join(auxpath)
        if args.vm_input_format=="igb":
            vmPathName=os.path.join(vm_path,"vm.igb")
            header_phie,vm_values=read_data_from_igb(vmPathName)
            
        elif args.vm_input_format=="txt":
            vmPathName=os.path.join(vm_path,"vm_"+ sim_number + ".txt")
            # vmPathName=os.path.join(vm_path,"vm_nodes_healthy.txt")
            vm_values=read_data_from_txt(vmPathName)
            header_phie=[]

        elif args.vm_input_format=="mat":
            # vmPathName=os.path.join(vm_path,"vm_nodes_healthy.txt")
            vmPathName=os.path.join(vm_path,"vm_"+ sim_number + ".mat")
            vm_values=read_data_from_mat(vmPathName)
            header_phie=[]

        for lns in args.points_2_see: 
            vm_values_all[auxpath_name][str(lns)]=vm_values[:,lns]
            # vm_values_all.append(vm_values[:,lns])
            # print("Sample %d / %d" % (i, n_samples))
            # np.savetxt(simFileNameout, phie_recovery_aux, fmt='%0.3f', delimiter=' ', newline='\n', header='', footer='', comments='# ', encoding=None)


        assert vm_values.shape[1] == mesh.n_points, "Mismatch in number of cells"


    #Find tags
    fieldsPoints = list(mesh.point_data.keys())
    fieldsCells = list(mesh.cell_data.keys())

    # #tags in data
    # if args.data_label_compare in fieldsPoints:
    #     pointTags=mesh.point_data[args.data_label_compare]

    # elif args.data_label_compare in fieldsCells:
    #     tags2use=mesh.cell_data[args.data_label_compare]
    #     pointTags=ut.elements2points(mesh.cells_dict[args.cellType], tags2use)
    # else: raise ValueError("Error in label")

    #Plot data
    num_pts=len(args.points_2_see)
    fig, ax = plt.subplots(num_pts, 1, figsize=(6, 6))
    
    for auxpath,i in enumerate(args.simulation_path):
        auxpath_name='simulation_'+str(i)
        sim_number=os.path.split(auxpath)[-1]

        for lns in args.points_2_see: 
            # vm_values_all[auxpath_name][str(lns)]=[]
            signal=vm_values_all[auxpath_name][str(lns)]
            t = np.arange(0.0, signal.shape[1], 1)
            # =vm_values[:,lns]
            
            ax[lns].plot(t, signal/np.max(abs(signal)))
            ax[lns].set_ylabel("Point : "+str(lns))
            # ax[ld].set_xlabel(t)


    
    
    for ld in range(num_pts):
        signal = ecg_signal[ld][0:num_samples]
        if normalizeECG=='ind':
            ax[ld].plot(t, signal/np.max(abs(signal)),color='black')
        elif normalizeECG=='all':
            ax[ld].plot(t, signal/totmax,color='black')
        else:
            ax[ld].plot(t, signal,color='black')
        ax[ld].set_ylabel(ecg_names[ld])
        # ax[ld].set_xlabel(t)
        range_values[ld,:]=[np.min(signal), np.max(signal),np.max(signal)-np.min(signal)]


    #Plot
    fig1, ax1 = plt.subplots()

    fig2, ax2 = plt.subplots() 

    x = np.arange(vm_values.shape[0])

    lns=1
    APaux=vm_values[:,lns]
    diffs = [APaux[i] - APaux[i-3] for i in range(3, len(APaux))]

    dvdt=np.diff(APaux)
    # indexdvdt, valdvdt = np.max(dvdt)
    np.argmax(dvdt)
    peaks, _ = find_peaks(dvdt, distance=150)
    peaks2, _ = find_peaks(dvdt, prominence=10)

    peaks3, _ = find_peaks(diffs, prominence=10)

    ax1.plot(x,APaux,'r')
    # ax1.plot(x[inflection_indices], APaux[inflection_indices], 'o', label='Inflection Points'+str(labels_aux))
    aux_x=np.array(range(3, len(APaux)))
    ax1.plot(aux_x,diffs,'g')
    ax1.plot(aux_x[peaks3],diffs[peaks3],'xg')

    ax1.plot(x[peaks2],APaux[peaks2],'rx')

    ax1.plot(dvdt,'b')

    ax1.plot(peaks2,dvdt[peaks2],'xb')


    

    

    # connectivity = mesh.cell_connectivity

    if args.cellType == 'tetra': 
        cell_type_id = 10 
    else: 
        cell_type_id=3000
        print("Error in cell type: ", args.mesh_path) # VTK_TETRA = 10
    # mesh.cells_dict[cell_type_id]

    # vm_values[1,:]=25
    max_vm=np.max(vm_values)
    min_vm=np.min(vm_values)

    outPath=os.path.join(vm_path,"Images")
    if not os.path.exists(outPath): os.mkdir(outPath)


    if args.type_remove_label=="cell":
        layersCells=np.asarray(mesh.cell_data[args.data_label_compare])

    elif args.type_remove_label=="point":

        #Convert to elems to see which elements to remove
        layersCells=mesh.point_data[args.data_label_compare]

    else:
        print("Error in type_remove_label")

    
    # plAPs = plt.figure()
    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots() 

    x = np.arange(vm_values.shape[0])
   
    for labels_aux in args.labels_compare:
        #Find Aps in that section

        indexLabel=np.where(layersCells == labels_aux)
        indexLabel_aux=indexLabel[0][0]

        APaux=vm_values[:,indexLabel_aux]

        diffs = [APaux[i] - APaux[i-3] for i in range(3, len(APaux))]

        dvdt=np.diff(APaux)
        diffAPaux2=np.diff(dvdt)

        signs = np.sign(diffAPaux2)
        # inflection_indices = np.where(signs == 0)
        inflection_indices = np.where(np.diff(diffAPaux2) > 0)[0]

        ax1.plot(x,APaux, label=str(labels_aux))
        # ax1.plot(x[inflection_indices], APaux[inflection_indices], 'o', label='Inflection Points'+str(labels_aux))

        ax2.plot(range(3, len(APaux)),diffs, label=str(labels_aux))
        # ax2.plot(diffAPaux2, label=str(labels_aux))

    ax1.legend(loc="upper left")
    ax2.legend(loc="upper left")

    namePlot="APs_{}_{}_{}.svg".format(args.mesh_name,args.simulation_number,args.data_label_compare)
    fig1.savefig(os.path.join(vm_path,"Images",namePlot))
    # fig1.close()

    namePlot="APs_{}_{}_{}_der.svg".format(args.mesh_name,args.simulation_number,args.data_label_compare)
    fig2.savefig(os.path.join(vm_path,"Images",namePlot))
    # fig2.close()

    print("Image: "+ args.mesh_name+ args.simulation_number + args.data_label_compare +", Patient:"+ args.mesh_path)


    print("Finished: ", args.mesh_path)

    



if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))