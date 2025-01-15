"""This code takes a point cloud (pc) of the measured bipolar and unipolar activation and voltages from Rhythmia and the BiV and the LV (for now) surface meshes 
where the activation found in Rhytmia is going to be projected onto the mesh for activation. The Rhythmia's point cloud should be already aligned
with the other meshes and only points near the mesh should exist. The point cloud should not be neccesarily clean in terms of activation or voltage
as we try somethings here for cleaning it"""


import meshio
import os
import argparse
import time
import numpy as np
import vtk 
from vtk.util import numpy_support # type: ignore
from scipy.interpolate import RBFInterpolator, griddata
from scipy.spatial import KDTree
import sys
sys.path.append(os.path.join('/'.join(sys.path[0].split("/")[:-1])))
from miscellaneous.regions import scar_flag
from auxiliar.conductionSystem.lib.utils import getProjectionDir, getProjectionMag, getProjectionMagLowMemory

cellsMeshio  = [("triangle", [[0,1,2]])] # just to make meshio work

def eraseFromPC(pc_mesh, label, threshold_min, threshold_max):
    idxs = np.where((pc_mesh.point_data[label]>threshold_min) & (pc_mesh.point_data[label]<threshold_max))[0]
    point_data = {}
    for key in pc_mesh.point_data.keys():
        point_data[key] = pc_mesh.point_data[key][idxs]
    pc_mesh = meshio.Mesh(pc_mesh.points[idxs], cellsMeshio, point_data=point_data)
    return pc_mesh

def main():

    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument('--dataPath',             type=str, required=True, help='path to data')
    parser.add_argument('--meshBiVvtk',             type=str, required=True, help='path to data')
    parser.add_argument('--meshBiVinp',             type=str, required=True, help='path to data')
    parser.add_argument('--pointCloudPath',       type=str, required=True, help='path to data')
    parser.add_argument('--LVendoPath',           type=str, required=True, help='path to data')
    parser.add_argument('--outPath',             type=str, required=True, help='path to data')
    parser.add_argument('--biActivationMin',     type=int, required=False)
    parser.add_argument('--biActivationMax',     type=int, required=False)
    parser.add_argument('--pmjRadious',           type=float, default=0.5, help='Pmj radious default is 0.5 which is good for tetgen created meshes of mean edge length 0.39 mm')
    parser.add_argument('--initial_stim_time',    type=float, default=0.0, help='This is the time of start the stim of the nodes activating first in th electro-anatomical mapping')
    
    # Projection into the intramyocardium
    parser.add_argument('--project_intramyo',     action='store_true', help='Porject or no the pmj into the intramyo ')
    parser.add_argument('--meanMag',type=int, required=True, help='number of nodes to average for magnitud of the projection')
    parser.add_argument('--meanNor',type=int, required=True, help='number of nodes to average for normal direction of the projection')
    parser.add_argument('--endo_per',type=int, required=True, help='endo percentage')
    parser.add_argument('--epi_per',type=int, required=True, help='epi percentage')
    parser.add_argument('--intramyo_window',type=int, required=True, help='intramyo window is the middle width transmural wall')
    
    args = parser.parse_args()

    # Get meshes and pc data
    # We generally use the _noscar mesh but the general MI can also be use
    # meshBiVMI       = meshio.read(os.path.join(args.dataPath, 'mesh_mi.vtk'))
    meshBiV     = meshio.read(args.meshBiVvtk)
    meshLVendo  = meshio.read(args.LVendoPath) # Only works for the LV
    if not os.path.isdir(args.outPath): os.mkdir(args.outPath)

    #  Make the pc a mesh so we can use meshio
    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName(args.pointCloudPath)
    reader.Update()
    pc    = reader.GetOutput()
    
    point_data = {}
    points  = numpy_support.vtk_to_numpy(pc.GetPoints().GetData())
    point_data["activation_bipolar"] = numpy_support.vtk_to_numpy(pc.GetPointData().GetArray("activation_bipolar"))
    point_data["activation_unipolar"] = numpy_support.vtk_to_numpy(pc.GetPointData().GetArray("activation_unipolar"))
    point_data["se_projected_dist"] = numpy_support.vtk_to_numpy(pc.GetPointData().GetArray("se_projected_dist"))
    point_data["voltage_bipolar"] = numpy_support.vtk_to_numpy(pc.GetPointData().GetArray("voltage_bipolar"))
    point_data["voltage_unipolar"] = numpy_support.vtk_to_numpy(pc.GetPointData().GetArray("voltage_unipolar"))
    
    pc_mesh      = meshio.Mesh(points, cellsMeshio, point_data=point_data)
    # pc_mesh.write(os.path.join(args.dataPath, "cleanPC.vtk"))
    del pc

    # First we clean the pc, we erase the low voltage arrays (bad contact or dense scar) using the bipolar voltage for avoiding the far-field effect on the 
    # unipolar electrodes, also rhythmia's good interelectrode distance (2.6 mm) helps with other bipolar related errors 
    # doi: 10.1111/pace.12581 and doi: 10.1111/pace.12581

    # Erase <1mV in bipolar voltage
    pc_mesh = eraseFromPC(pc_mesh, 'voltage_bipolar', 1, pc_mesh.point_data['voltage_bipolar'].max()+1)
    # pc_mesh.write(os.path.join(args.dataPath, "cleanPC.vtk"))

    # Delete points regarding min and max values of bipolar activation
    if args.biActivationMin and args.biActivationMax == None:
        percentile = (pc_mesh.point_data['activation_bipolar']<args.biActivationMin).nonzero()[0].size / pc_mesh.point_data['activation_bipolar'].shape[0] * 100
        print("Dropping points with bipolar activation lower than {} which is percentile {}".format(args.biActivationMin, percentile))
        pc_mesh = eraseFromPC(pc_mesh, 'activation_bipolar', args.biActivationMin, pc_mesh.point_data['activation_bipolar'].max()+1)

    if args.biActivationMax and args.biActivationMin == None:
        percentile = 100 - ((pc_mesh.point_data['activation_bipolar']>args.biActivationMax).nonzero()[0].size / pc_mesh.point_data['activation_bipolar'].shape[0] * 100)
        print("Dropping points with bipolar activation greater than {} which is percentile {}".format(args.biActivationMax, percentile))
        pc_mesh = eraseFromPC(pc_mesh, 'activation_bipolar', pc_mesh.point_data['activation_bipolar'].min()-1, args.biActivationMax)

    if args.biActivationMax and args.biActivationMin:
        percentilemin = (pc_mesh.point_data['activation_bipolar']<args.biActivationMin).nonzero()[0].size / pc_mesh.point_data['activation_bipolar'].shape[0] * 100
        percentilemax = 100 - ((pc_mesh.point_data['activation_bipolar']>args.biActivationMax).nonzero()[0].size / pc_mesh.point_data['activation_bipolar'].shape[0] * 100)
        print("Dropping points with bipolar activation lower than {} which is percentile {}".format(args.biActivationMin, percentilemin))
        print("Dropping points with bipolar activation greater than {} which is percentile {}".format(args.biActivationMax, percentilemax))
        pc_mesh = eraseFromPC(pc_mesh, 'activation_bipolar', args.biActivationMin, args.biActivationMax)

    # We now take the cleaned bipolar activation and select the nearest nodes in the mesh, then make an inteprolation of the activation bipolar from pc_mesh to
    # the nearest nodes in the LV endo
    tree = KDTree(meshLVendo.points)
    _ , activation_idxs = tree.query(pc_mesh.points, k=1)
    activation_idxs = np.unique(activation_idxs)
    # No Idxs in scar
    activation_idxs = activation_idxs[meshLVendo.point_data['layers'][activation_idxs]!=scar_flag]

    # If we use the nearest neighbour
    # activation_values = griddata(pc_mesh.points, pc_mesh.point_data['activation_bipolar'], meshLVendo.points[activation_idxs,:], method='nearest')
    
    # If we use the RBF
    # with RBF we need to normalize the range to the one found in the experimental EAM
    activation_values = RBFInterpolator(pc_mesh.points, pc_mesh.point_data['activation_bipolar'], neighbors=None)(meshLVendo.points[activation_idxs,:]) # this makes things smooth but last depolarization happens in another place
    activation_values = (activation_values - np.min(activation_values)) / (np.max(activation_values) - np.min(activation_values))
    activation_values = activation_values * (pc_mesh.point_data['activation_bipolar'].max() - pc_mesh.point_data['activation_bipolar'].min() )
    

    activation_values = activation_values - np.min(activation_values) + args.initial_stim_time # Make zero and put to the initial start time desired


    # For Debugging 
    # tmp = np.ones(meshLVendo.points.shape[0]) * -1
    # tmp[activation_idxs] = activation_values
    # meshOut = meshio.Mesh(meshLVendo.points, meshLVendo.cells, point_data={'interp_bipolar_activation': tmp})
    # meshOut.write(os.path.join(args.outPath, "test.vtk"))

    stim_points = meshLVendo.points[activation_idxs]

    # PROJECTION ------------------------------------------------
    # Up to here stim_points are the coordinates of the points where the center of stimulation will be and activation values hast the activation time from zero
    # of this points, now we need to project or not
    if args.project_intramyo:
        # Get useful data
        meshLVendoNormals = meshio.read(os.path.join(args.dataPath, 'mesh', 'lv_endo.obj'))
        laplaciansMesh = meshio.read(os.path.join(args.dataPath, "layers", "laplacians.vtk"))
        
        #Perrotti definitions, must be consistent with the ones used
        endoPer        = args.endo_per / 100
        epiPer         = args.epi_per / 100
        intramyoWindow = args.intramyo_window
        phi0 = -1
        phi1 = 1
        phiEndo = (1-endoPer) * phi0 + endoPer * phi1    # thresholds
        phiEpi = epiPer * phi0 + (1-epiPer) * phi1
        intramyoWindow = [phiEndo , phiEpi] # we use the whole mid-myocardium as intramyocardium due to taking only the mid-myocardium middle third could give few points and bad projection if mesh resolution is too poor

        dirs = getProjectionDir(meshLVendo.points[activation_idxs], meshLVendoNormals, k=args.meanNor)
        # if args.lowMemoryDivisions:
        #     mags = getProjectionMagLowMemory(csBundleNodes[branchIdxs,:], laplaciansMesh, subendoWindow, "lv" if "lv" in key else "rv", k=args.meanMag, divisions=args.lowMemoryDivisions)
        # else:
        mags = getProjectionMag(meshLVendo.points[activation_idxs], laplaciansMesh, intramyoWindow, "lv", k=args.meanMag)
        
        mags = np.expand_dims(mags, axis=1)
        mags = np.repeat(mags, repeats=3, axis=1)
        stim_points = meshLVendo.points[activation_idxs] + dirs * mags
        del laplaciansMesh, meshLVendoNormals, intramyoWindow
    del meshLVendo

    # Get indexes of Biventricular mesh to stim at a certain time
    tree = KDTree(meshBiV.points)
    stim_idxs = tree.query_ball_point(stim_points, r=args.pmjRadious)
    activation_on_biv_mesh = np.ones(meshBiV.points.shape[0]) * -1 # non stimulated nodes are depicted as -1
    for i, stim_arr in enumerate(stim_idxs):
        activation_on_biv_mesh[stim_arr] = activation_values[i]
    if args.project_intramyo:
        meshBiV.point_data['stim_from_EAM_intramyo'] = activation_on_biv_mesh
    else:
        meshBiV.point_data['stim_from_EAM_endo'] = activation_on_biv_mesh


    # SAVE -----------------------------------------------------------------------
    # We have in mesh BiV the idxs and the values for the activation, we need to put it .inp for ELECTRA and make the part of the .json file as several AT values
    # can be present. activation_on_biv_mesh has -1 for not stimulates nodes and the value of activation for the nodes activated from 0 to the end
    
    #  Save the .vtk for visualization and the final EAM point cloud used
    pc_mesh.write(os.path.join(args.outPath, 'EAM_used.vtk'))
    meshBiV.write(os.path.join(args.outPath, 'mesh_mi_noscar_lv_eam_stim.vtk'))
    
    # Save the .inp for ELECTRA
    unique_activation_values = np.unique(activation_values)
    stim_nodesets = {}
    if args.project_intramyo:
        nset_prefix = 'stim_nodes_intra'
    else:
        nset_prefix = 'stim_nodes_endo'
    for i, act_value in enumerate(unique_activation_values):
        stim_nodesets['{0}_{1}'.format(nset_prefix,str(i))] = np.where(activation_on_biv_mesh==act_value)[0] 

    meshBiVInp = meshio.read(args.meshBiVinp)
    meshBiVInp.point_sets = {**meshBiVInp.point_sets, **stim_nodesets}
    meshBiVInp.write(os.path.join(args.outPath, 'mesh_mi_noscar_lv_eam_stim.inp'))

    # Make the .json for the Stimuli
    tot_unique_act_values = unique_activation_values.shape[0]
    with open(os.path.join(args.outPath, 'stim_electra_{:s}.json'.format('intramyo' if args.project_intramyo else 'endo')), "w") as file:
        file.write('"stimuli" : {\n')
        file.write('\t"stimuli number" : {:d},\n'.format(tot_unique_act_values))
        for i, act_value in enumerate(unique_activation_values):
            file.write('\t"stimulus-{:d}" : '.format(i+1)) #stimulus start from 1
            file.write('{\n') # This { disturbs when .format {} are used
            
            file.write('\t\t"id" : {:d},\n'.format(i))
            file.write('\t\t"nodeset" : "{:s}",\n'.format('{0}_{1}'.format(nset_prefix,str(i))))
            file.write('\t\t"start" : {:.2f},\n'.format(act_value))
            file.write('\t\t"duration" : {:.1f},\n'.format(1))
            file.write('\t\t"cycle length" : {:.1f},\n'.format(1000))
            file.write('\t\t"amplitude" : {:.1f},\n'.format(80))
            file.write('\t\t"time unit" : {:s},\n'.format('"ms"'))
            file.write('\t\t"current unit" : {:s}\n'.format('"mA"'))
            
            file.write('\t}')

            if i == tot_unique_act_values-1:
                file.write('\n')
            else:
                file.write(',\n')

        file.write('},\n')

if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))