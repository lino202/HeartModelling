#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plot the ECG and save the ECG and leads order and get min,max and range values of each lead.
Created on Fri Oct 18 11:01:57 2024

@author: Clara (basis) and Jimena (modification)
"""


import matplotlib.pyplot as plt
import numpy as np
import sys
import carputils.carpio.igb as carp
import argparse
import os
import scipy.io
from matplotlib.ticker import AutoMinorLocator, MultipleLocator


def create_file_name(simulation_path,simulation_name,simulation_ecg_format,file_name):

    if simulation_ecg_format=="igb":
        path_mesh_complete=os.path.join(simulation_path, simulation_name,file_name+".igb")
        
    elif simulation_ecg_format=="txt":
        path_mesh_complete=os.path.join(simulation_path, simulation_name,file_name+".txt")

    elif simulation_ecg_format=="mat":
        path_mesh_complete=os.path.join(simulation_path, simulation_name,file_name+".mat")
        

    return path_mesh_complete

def read_ecg_from_mat(filename):
    
    vm_values = scipy.io.loadmat(filename)
    
    # vm_values=np.transpose(vm_values)

    #If the electrodes are already there
    # vm_values['pECGLabels']
    


    return np.transpose(vm_values['pECG'])

def read_ecg_from_txt(filename):
    vm_values=np.loadtxt(filename)
    # vm_values=np.transpose(vm_values)


    # f = open(filename)
    # vm_values=f.readline()


    return vm_values

def read_ecg_from_igb(filename):
    """Translate the phie.igb file(s) to 10-lead, 12-trace ECG data

    Extracts the complete mesh data from the phie.igb file using CARPutils, which contains the data for the body
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

def compute_show_ECG(phie_recovery,electrodeFile, resultsLoc,file_name,header_phie,normalizeECG):
    
    electrodes = []
    namesElectrode = []
    
    with open(electrodeFile, 'r', encoding='utf-8') as file:
        i = 0
        for line in file:
            i = i+1
            electrode, nameElectrode = line.split()
            electrodes.append(int(electrode)) 
            namesElectrode.append(nameElectrode)
    
        
    # Index for each electrode
    idRA = namesElectrode.index('RA')
    idLA = namesElectrode.index('LA')
    idLL = namesElectrode.index('LL') 
    idV1 = namesElectrode.index('V1')
    idV2 = namesElectrode.index('V2')
    idV3 = namesElectrode.index('V3')
    idV4 = namesElectrode.index('V4')
    idV5 = namesElectrode.index('V5')
    idV6 = namesElectrode.index('V6')

    # WCT computation
    RA = phie_recovery[idRA,:]
    LA = phie_recovery[idLA,:]
    LL = phie_recovery[idLL,:]

    WCT = (RA+LA+LL)/3
    
    # Limb leads
    I   = LA - RA
    II  = LL - RA
    III = LL - LA

    # Augmented limb leads
    aVR = 3/2*(RA-WCT)
    aVL = 3/2*(LA-WCT)
    aVF = 3/2*(LL-WCT)

    # Precordial leads
    V1 = phie_recovery[idV1,:] - WCT
    V2 = phie_recovery[idV2,:] - WCT
    V3 = phie_recovery[idV3,:] - WCT
    V4 = phie_recovery[idV4,:] - WCT
    V5 = phie_recovery[idV5,:] - WCT
    V6 = phie_recovery[idV6,:] - WCT

    ecg_signal = [I, II, III, aVR, aVL, aVF, V1, V2, V3, V4, V5, V6]
    ecg_names  = ['I', 'II', 'III', 'aVR', 'aVL', 'aVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']  

    totmaxabs=np.max(np.abs(ecg_signal))

    totmax=np.max(ecg_signal)
    totmin=np.min(ecg_signal)
    print("totmax: ", totmax, "totmin: ", totmin, "totmaxabs: ", totmaxabs)

    l = np.arange(11, -1, -1)
    lds = np.arange(0,12)

    # t = np.linspace(0,phie_recovery.shape[1],1)

    t = np.arange(0.0, phie_recovery.shape[1], 1)

    num_samples = phie_recovery.shape[1]
    num_signals = 12

    range_values=np.zeros([num_signals,3])

    #Option1
    fig, ax = plt.subplots(num_signals, 1, figsize=(6, 6))

    for ld in range(num_signals):
        signal = ecg_signal[ld][0:num_samples]
        if normalizeECG=='ind':
            ax[ld].plot(t, signal/np.max(abs(signal)),color='black')
            ax[ld].set(ylim=(-1.01,1.01))
            # ax[ld].set(ylim=(0, 100), title='FFT')
            # .ylim([-1, 1])
        elif normalizeECG=='all':
            ax[ld].plot(t, signal/totmaxabs,color='black')
            ax[ld].set(ylim=(-1.01,1.01))
            # .ylim([-1, 1])
            # .set(ylim=(0, 100), title='FFT')
        else:
            ax[ld].plot(t, signal,color='black')
            # ax[ld].set(ylim=(totmin,totmax))

        ax[ld].set_ylabel(ecg_names[ld])
        # ax[ld].set_xlabel(t)
        range_values[ld,:]=[np.min(signal), np.max(signal),np.max(signal)-np.min(signal)]
        # l[ld]

    # l = 12:-1:1;
    # th = 40;

    # for ld = 1:12, plot(pECG(:,l(ld))+ld*th,'k'); end

    # plt.sca(ax[ld])
    # plt.xticks(range(3), t[range(4)], color='red')
    # ax[ld].xticks(t)
    # ax[ld].set_xlabel("Time (ms)")

    # ax[ld].xaxis.set_major_locator(MultipleLocator(20))
    # ax[ld].xaxis.set_major_formatter('{x:.0f}')

    # # For the minor ticks, use no labels; default NullFormatter.
    # ax[ld].xaxis.set_minor_locator(MultipleLocator(5))

    # fig.tight_layout()
    
   
    # if normalizeECG:
    #         plt.savefig(resultsLoc + '/ECG_phie_recovery_'+file_name+'_normalized.png')
    # else:
    #     plt.savefig(resultsLoc + '/ECG_phie_recovery_'+file_name+'.png')
    # # plt.savefig(resultsLoc + '/ECG_phie_recovery_'+file_name+'.png')  # Guarda la figura como archivo PNG

    if normalizeECG=='ind':
        plt.savefig(resultsLoc + '/ECG_phie_recovery_'+file_name+'_normalized_ind.png')
    elif normalizeECG=='all':
        plt.savefig(resultsLoc + '/ECG_phie_recovery_'+file_name+'_normalized_all.png')
    else:
        plt.savefig(resultsLoc + '/ECG_phie_recovery_'+file_name+'.png')  # Guarda la figura como archivo PNG
    
    ecg_signal = np.array(ecg_signal)
    np.savetxt(resultsLoc + '/ecg_phie_recovery_'+file_name+'.txt', ecg_signal, fmt='%.5f')  

    np.savetxt(resultsLoc + '/ecg_phie_recovery_'+file_name+'_ranges.txt', range_values, fmt='%.5f')  

    with open(resultsLoc + "/ecg_leads_phie_recovery_"+file_name+".txt", "w") as file:
        file.write(', '.join(ecg_names)) 

def show_ECG(phie_recovery, resultsLoc,file_name,normalizeECG):
    
    electrodes = []
    namesElectrode = []
    
    pECGLabels = [ "I" , "II" , "III" , "aVR" , "aVL" , "aVF" , "V1" , "V2" , "V3" , "V4" , "V5" , "V6" ]
    

    # Precordial leads
    I = phie_recovery[0,:] 
    II = phie_recovery[1,:] 
    III = phie_recovery[2,:]
    aVR = phie_recovery[3,:]
    aVL = phie_recovery[4,:]
    aVF = phie_recovery[5,:]
    V1 = phie_recovery[6,:]
    V2 = phie_recovery[7,:] 
    V3 = phie_recovery[8,:]
    V4 = phie_recovery[9,:]
    V5 = phie_recovery[10,:]
    V6 = phie_recovery[11,:]

    ecg_signal = [I, II, III, aVR, aVL, aVF, V1, V2, V3, V4, V5, V6]
    ecg_names  = [ "I" , "II" , "III" , "aVR" , "aVL" , "aVF" , "V1" , "V2" , "V3" , "V4" , "V5" , "V6" ]

    totmaxabs=np.max(np.abs(ecg_signal))

    l = np.arange(11, -1, -1)
    lds = np.arange(0,12)

    # t = np.linspace(0,phie_recovery.shape[1],1)

    t = np.arange(0.0, phie_recovery.shape[1], 1)

    num_samples = phie_recovery.shape[1]
    num_signals = 12

    range_values=np.zeros([num_signals,3])

    #Option1
    fig, ax = plt.subplots(num_signals, 1, figsize=(6, 6))

    for ld in range(num_signals):
        signal = ecg_signal[ld][:num_samples]
        if normalizeECG=='ind':
            ax[ld].plot(t, signal/np.max(np.abs(signal)),color='black')
            ax[ld].set(ylim=(-1.01,1.01))
        elif normalizeECG=='all':
            ax[ld].plot(t, signal/totmaxabs,color='black')
            ax[ld].set(ylim=(-1.01,1.01))
        else:
            ax[ld].plot(t, signal,color='black')
        ax[ld].set_ylabel(ecg_names[ld])
        # ax[ld].set_xlabel(t)
        range_values[ld,:]=[np.min(signal), np.max(signal),np.max(signal)-np.min(signal)]
        # l[ld]

        # l = 12:-1:1;
        # th = 40;

        # for ld = 1:12, plot(pECG(:,l(ld))+ld*th,'k'); end

        # plt.sca(ax[ld])
        # plt.xticks(range(3), t[range(4)], color='red')
        # ax[ld].xticks(t)
        # ax[ld].set_xlabel("Time (ms)")

        # ax[ld].xaxis.set_major_locator(MultipleLocator(20))
        # ax[ld].xaxis.set_major_formatter('{x:.0f}')

        # # For the minor ticks, use no labels; default NullFormatter.
        # ax[ld].xaxis.set_minor_locator(MultipleLocator(5))

        # fig.tight_layout()
        
        # #Option2
        # for ld in range(num_signals):
        #     signal = ecg_signal[l[ld]][:num_samples]
        #     plt.plot( t, signal/np.max(abs(signal)) + ld,color='black')
        #     # plt.plot( t, signal + ld * 0.2,color='black')
        
        # # plt.yticks( lds * 0.2, ecg_names[::-1])
        # plt.yticks( lds, ecg_names[::-1])
        # plt.xticks([0, 0.5, 1],[1, (phie_recovery.shape[1]-1)/2, phie_recovery.shape[1]-1])
        # plt.xlabel('ms')

    if normalizeECG=='ind':
        plt.savefig(resultsLoc + '/ECG_phie_recovery_'+file_name+'_normalized_ind.png')
    elif normalizeECG=='all':
        plt.savefig(resultsLoc + '/ECG_phie_recovery_'+file_name+'_normalized_all.png')
    else:
        plt.savefig(resultsLoc + '/ECG_phie_recovery_'+file_name+'.png')  # Guarda la figura como archivo PNG
    
    
        
    
    # ecg_signal = np.array(ecg_signal)
    np.savetxt(resultsLoc + '/ecg_phie_recovery_'+file_name+'.txt', ecg_signal, fmt='%.5f')  

    np.savetxt(resultsLoc + '/ecg_phie_recovery_'+file_name+'_ranges.txt', range_values, fmt='%.5f')  

    with open(resultsLoc + "/ecg_leads_phie_recovery_"+file_name+".txt", "w") as file:
        file.write(', '.join(ecg_names)) 

if __name__=="__main__":

    parser = argparse.ArgumentParser(description="Options")
    # parser.add_argument('--mesh_path',      type=str, required=True, help='path to mesh')
    # parser.add_argument('--mesh_name',      type=str, required=True, help='name of mesh with the end')
    parser.add_argument('--simulation_path',  type=str, required=True, help='simulation path')
    parser.add_argument('--simulation_name',  type=str, required=True, help='simulation number or name')
    parser.add_argument('--simulation_file_name',  type=str, required=True, help='results file to use')
    parser.add_argument('--simulation_ecg_format',  type=str, required=True, help='simulation format (igb, txt or mat)')
    # parser.add_argument('--simulation_ecg_type',  type=str, required=True, help='simulation type (phie_recovery or extracelullar from torso(extra) )')
    parser.add_argument('--electrode_file_path',  type=str, required=True, help='simulation number')
    parser.add_argument('--electrode_file_name',  type=str, required=True, help='simulation number')
    parser.add_argument('--pECG_computed',  action='store_true', help='If the pECG is already computed ')
    parser.add_argument('--normalizeECG', type=str,  help='If to normalize the ECG plot to the maximum value of each lead or of all leads (ind or all). ')
    # parser.add_argument('--normalizeECG_all',  action='store_true', help='If to normalize the ECG plot to the maximum value of all leads. ')

    args = parser.parse_args()

    # in_cluster=0;
    # patient_number=32;
    # simulation_name='3N_1EB_wo_scar';
    # pECG_format='mat';
    # ecg_type='Ana'; 

    

    resultsLoc       = os.path.join(args.simulation_path, args.simulation_name)
    # filename         = os.path.join(args.simulation_path, args.simulation_name ,"phie_recovery.igb")
    electrodeFile    = os.path.join(args.electrode_file_path, args.electrode_file_name)
    
    simFileName=create_file_name(args.simulation_path,args.simulation_name,args.simulation_ecg_format,args.simulation_file_name)
    # create_file_name(simulation_path,simulation_name,simulation_ecg_format)
    #Read phie_recovery files
    if args.simulation_ecg_format=="igb":
        header_phie,phie_recovery=read_ecg_from_igb(simFileName)
        
    elif args.simulation_ecg_format=="txt":
        phie_recovery=read_ecg_from_txt(simFileName)
        header_phie=[]

    elif args.simulation_ecg_format=="mat":
        phie_recovery=read_ecg_from_mat(simFileName)
        header_phie=[]



    # Show the computed ECG
    # phie_recovery = read_ecg_from_igb(filename)
    if args.pECG_computed:
        print("The pECG is already computed, so it will be plotted")
        show_ECG(phie_recovery, resultsLoc,args.simulation_file_name,args.normalizeECG)
    else:
        compute_show_ECG(phie_recovery,electrodeFile, resultsLoc,args.simulation_file_name,header_phie,args.normalizeECG)
        # compute_show_ECG(phie_recovery,electrodeFile, resultsLoc,file_name,header_phie)
    
