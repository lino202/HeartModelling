import meshio
import argparse
import os
import numpy as np
import utils as ut
import time

def main():
    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument('--meshPath',        type=str, required=True)
    parser.add_argument('--spatialUnit',     type=str, required=True)
    parser.add_argument('--cellType',        type=str, default="tetra")
    parser.add_argument('--stimPointData',   type=str)
    parser.add_argument('--fibersPointData', type=str)
    parser.add_argument('--layersPointData', type=str)
    parser.add_argument('--tend',            type=int, default=100)
    parser.add_argument('--outFolder',       type=str, required=True)
    args = parser.parse_args()

    mesh = meshio.read(args.meshPath)
    if not os.path.isdir(args.outFolder): os.mkdir(args.outFolder)
    fileName = args.meshPath.split(".")[0].split("/")[-1]
    #Switch to um as opencarp only seems to support that
    if args.spatialUnit=="cm":
        mesh.points = mesh.points * 10000
    elif args.spatialUnit=="mm":
        mesh.points = mesh.points * 1000
    elif args.spatialUnit=="um":
        pass
    else: raise ValueError("Only spatialUnits in cm, mm or um are supported")

    #Save pts in carp format
    print("Getting points as .pts file-------------")
    ut.writePointsFile(mesh.points, os.path.join(args.outFolder, "{}.pts".format(fileName)))

    #Save cells in carp format
    print("Getting cells as .elem file-------------")
    ut.writeCellsFile(mesh.cells_dict[args.cellType], os.path.join(args.outFolder, "{}.elem".format(fileName)), cellType=ut.meshioOCCellsMap[args.cellType])

    #Add fibers to cell data
    # if fibers are already or you want just default fibers from meshtool just dont pass the argument
    if args.fibersPointData:
        print("Getting fibers for elem as .lon file-------------")
        fibsCells = np.mean(mesh.point_data[args.fibersPointData][mesh.cells_dict[args.cellType]], axis=1)
        fibsCells = ut.getArrNormalization(fibsCells)
        ut.writeFibsFile(fibsCells, os.path.join(args.outFolder, "{}.lon".format(fileName)))

    #Create .vtx files of point data of interest
    if args.stimPointData:
        print("Getting stim nodes as vtx files -------------")
        stimATs = mesh.point_data[args.stimPointData]
        stimATIdxs = (stimATs>0).nonzero()[0]
        uniqueATs = np.unique(stimATs[stimATIdxs])

        # For every unique AT we need a .vtx file and this should be added to the settings file as well
        for i, at in enumerate(uniqueATs):

            idxs = np.where(stimATs==at)[0]
            ut.writeStimVtxFile(idxs, os.path.join(args.outFolder, "stim_{0:d}.vtx".format(i)))


    # Make the .par file ---------------------------------------------------------------------------------------------------------
    # Ionic model
    
    string = '''
# Ionic Model Setup =======================================================
num_imp_regions       = 1

imp_region[0].im      = Gaur
imp_region[0].num_IDs = 1
imp_region[0].ID[0]   = 1\n'''


    # Stimulus
    string += '''
# Stimulus Setup =======================================================
num_stim               = {0:d}\n'''.format(uniqueATs.shape[0])

    for i, at in enumerate(uniqueATs): 
        string += '''

stim[{0:d}].crct.type      = 0      # stimulate using transmembrane current 
stim[{0:d}].pulse.strength = 250.0	# uA/cm^2
stim[{0:d}].ptcl.start     = {1:f}	# apply stimulus following the AT
stim[{0:d}].ptcl.duration  = 1.	    # stimulate for 1ms
stim[{0:d}].ptcl.npls = 3
stim[{0:d}].ptcl.bcl = 1000.
stim[{0:d}].elec.vtx_file  = {2:s}
'''.format(i, at, "./stim_{0:d}.vtx".format(i))
    
    # Integration and physics

    string += '''
# Simulation Setup =======================================================
bidomain    =   0       # run monodomain
spacedt     =   1.	# output every ms
timedt      =   10.	# update progess on commandline every ms
parab_solve =   1
dt          =   20  # dt for integration is 20us

# Region's Physics =======================================================
num_phys_regions          = 1
phys_region[0].name       = Intracellular domain
phys_region[0].ptype      = 0
phys_region[0].num_IDs    = 1
phys_region[0].ID[0]      = 1 

simID                                   = ./results
meshname                                = ./{0:s}
tend                                    = {1:d}
'''.format(fileName, args.tend)

    # Conductivity
    # Change this in case it is neccesary
    string += '''
#Conductivity =======================================================
num_gregions                            = 1

gregion[0].name                         = Myocardium
gregion[0].num_IDs                      = 1
gregion[0].ID[0]                        = 1
gregion[0].g_el                         = 0.5486
gregion[0].g_et                         = 0.1311
gregion[0].g_en                         = 0.1311
gregion[0].g_il                         = 0.1527
gregion[0].g_it                         = 0.0365
gregion[0].g_in                         = 0.0365
gregion[0].g_mult                       = 1.0'''


    with open(os.path.join(args.outFolder, 'settings.par'), 'w') as f:
        f.write(string)


if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))