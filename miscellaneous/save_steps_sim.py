'''Open the vm file and save it in steps to opne better in matlab
'''


import matplotlib.pyplot as plt
import numpy as np
import sys
import carputils.carpio.igb as carp
import argparse
import os
import scipy.io as scio
from matplotlib.ticker import AutoMinorLocator, MultipleLocator
import compute_pECG_utils as pECGut
import pyvista as pv
import h5py
import time


def save_steps_sim(vm, dt, startTime_ms,endTime_ms,step_ms):
    return

def main():

    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument('--mesh_path',      type=str, required=True, help='path to mesh')
    parser.add_argument('--mesh_format',      type=str, required=True, help='mesh format (.mat or .vtk)')
    parser.add_argument('--simulation_path',  type=str, required=True, help='simulation path')
    parser.add_argument('--simulation_name',  type=str, required=True, help='simulation number or name')
    parser.add_argument('--file_name',  type=str, required=True, help='results file to use')
    parser.add_argument('--simulation_ecg_format',  type=str, required=True, help='simulation format (igb, txt or mat)')
    # parser.add_argument('--simulation_ecg_type',  type=str, required=True, help='simulation type (phie_recovery or extracelullar from torso(extra) )')
    parser.add_argument('--dt',type=float, required=True, help='time step of the output of the simulation in miliseconds')
    parser.add_argument('--startTime_ms', type=int, required=True, help='start time in milliseconds')
    parser.add_argument('--endTime_ms', type=int, required=True, help='end time in milliseconds')
    parser.add_argument('--step_ms', type=int, required=True, help='step size for pecg in ms')

    args = parser.parse_args()

    #Read mesh from MATLAB file to have .Gop
    if args.mesh_format=="vtk":
        mesh = pv.read(args.mesh_path + ".vtk")
        print("Hello vtk mesh")
        
    elif args.mesh_format=="mat":
        try:
            H = scio.loadmat(args.mesh_path + ".mat")
            H['tri']=H['tri']-1 #Convert to 0-based indexing for Python
            mesh = pv.PolyData(H['xyz'], H['tri'])
    
            print("Hello mat mesh")
        except:
            H=dict()
            with h5py.File(args.mesh_path + ".mat", 'r') as f:
                auxfile=f['H']

                H['xyz'] = np.array(auxfile["xyz"][:]).transpose()
                H['tri'] = np.array(auxfile["tri"][:]).transpose()
                H['tri']=H['tri']-1

                mesh = pv.PolyData(H['xyz'], H['tri'])
                # ugrid.cell_data['my-data'] = simple_range

                # if "triCENTER" in auxfile.keys():
                #     H['triCENTER'] = np.array(auxfile["triCENTER"][:]).transpose()
                # else:
                #     H["triCENTER"] = pECGut.meshFacesCenter( H )

                # if "triVOL" in auxfile.keys():
                #     H['triVOL'] = np.array(auxfile["triVOL"][:]).transpose()
                # else:
                #     H["triVOL"] = pECGut.meshVolume( H )

                # H['Gop'] = np.array(auxfile["Gop"][:]).transpose()
                
                # # Example: if your MAT file contains a variable named 'H' or specific arrays:
                # # H = {key: f[key][()] for key in f.keys()}
            print("Something went wrong in  mat mesh")
        else:
            print("Nothing went wrong")
    else:
        print("Mesh format not supported. Use .vtk or .mat")
    

    #Read simulation file name
        
    simFileName=pECGut.create_file_name(args.simulation_path,args.simulation_name,args.simulation_ecg_format,args.file_name)

    #Read simulation
    if args.simulation_ecg_format=="igb":
        header_phie,phie_recovery=pECGut.read_sim_from_igb(simFileName)
            
    elif args.simulation_ecg_format=="txt":
        phie_recovery=pECGut.read_sim_from_txt(simFileName)
        header_phie=[]

    elif args.simulation_ecg_format=="mat":
        phie_recovery=pECGut.read_sim_from_mat(simFileName)
        header_phie=[]
    else:
        print("sim format not supported. Use .igb, .txt or .mat")
        sys.exit(1)


    start_idx = int(np.round(args.startTime_ms / args.dt))
    end_idx = int(np.round(args.endTime_ms / args.dt))

    # np.arange range is exclusive of stop, so add step_ms/2 to include end boundary safely
    samples = np.arange(start_idx, end_idx + args.step_ms / 2, args.step_ms, dtype=int)

    n_samples = len(samples)

    #Save
    for i in samples:
        
        filename_aux=args.file_name+"_step_"+str(i)
        phie_recovery_aux=phie_recovery[:,i]
        simFileNameout=pECGut.create_file_name(args.simulation_path,args.simulation_name,"txt",filename_aux)
        print("Sample %d / %d" % (i, n_samples))
        np.savetxt(simFileNameout, phie_recovery_aux, fmt='%0.3f', delimiter=' ', newline='\n', header='', footer='', comments='# ', encoding=None)
        

    



if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))