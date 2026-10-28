''' Read the .elem, .pts and .lon files and remove elements with the tags in .elem
'''


#Modify the files to be used in OpenCARP
import meshio
import argparse
import os
import numpy as np
import utils as ut
import time
import matplotlib.pyplot as plt
import seaborn as sns
# import nanomesh
import fenics
import pyvista as pv
import carputils.carpio.igb as carp
import json
import csv

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

def main():
    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument('--mesh_name',    type=str, required=True)
    parser.add_argument('--mesh_path',    type=str, required=True)
    parser.add_argument('--label_remove',   nargs='+',  default=0,  type=int, required=True, help="Labels of elements to be removed")
    parser.add_argument('--field_remove',   nargs='+',  default="elemTag",  type=str, required=True, help="Labels of elements to be removed")
    # parser.add_argument('--label_keep',    nargs='+',  type=int, required=True, help="Labels of elements to be kept")
    parser.add_argument('--simulation_path',    type=str)
    parser.add_argument('--simulation_name',    type=str)
    parser.add_argument('--file_phie_name',    type=str)
    parser.add_argument('--simulation_ecg_format',  type=str,default="igb", help='simulation format (igb, txt or mat)')
    parser.add_argument('--cell_type',   type=str, default="tetra")
    parser.add_argument('--new_mesh_name',   type=str,required=True)
    parser.add_argument('--saveOpenCARP', action='store_true', help="If called, the carp_txt is saved")
    parser.add_argument('--extract_vm', action='store_true', help="If called, the vm from the mesh is also saved")

    

    # parser.add_argument('--fibersPointData', type=str)
    # parser.add_argument('--layersPointData', type=str)
    # parser.add_argument('--outFolder',       type=str, required=True)
    # parser.add_argument('--elemData',       type=str, required=False, help="Filed where the labels to be added to the elems are")
    # # parser.add_argument('--groundPointData', action='store_true', help='To choose a ground point for bidomain simulations')
    # # parser.add_argument('--save' ,action='store_true',  help='save histogram tags')
    
    args = parser.parse_args()

    # --file_path_fibers         #Complete path to the mesh with the fibers and pacing sites
    # --unit              #Units of the mesh.  cm, mm or um
    # --cell_type          #Cell type. Default value is tetra 
    # --stimPointData     #Name of the field with the Points where the stimuli will start. Right now only add 1 stimulus
    # --fibersPointData   #Point data for fiber orientation
    # --layersPointData   #Maxi removed it
    # --outFolder         #Path for results
    #--elemData           #Data in points to be included as element tags in the .elem file


    #Read mesh
    # mesh_file=os.path.join(args.mesh_path,args.mesh_name)
    # mesh = meshio.read(mesh_file)
    # tagMatrix=mesh.cell_data[args.field_remove]
    # elemMatrix=mesh.cells_dict[args.cellType]
    # pointMatrix = mesh.points
    # lonMatrix = mesh.cell_data['fiber']

    # Open the .elem
    elemFile=os.path.join(args.mesh_path,args.mesh_name+".elem")

    data = np.loadtxt(elemFile, skiprows=1, usecols=range(1,6), dtype=int)
    elemMatrix=data[:,:-1]
    tagMatrix=data[:,-1]

    # Open the .pts
    pointFile=os.path.join(args.mesh_path,args.mesh_name+".pts")
    pointMatrix = np.loadtxt(pointFile, skiprows=1, dtype=float)

    # Open the .lon
    lonFile=os.path.join(args.mesh_path,args.mesh_name+".lon")
    lonMatrix = np.loadtxt(lonFile, skiprows=1, dtype=float)

    #Read vm file
    
    

    
    #Remove tags
    cells2keep=np.ones(tagMatrix.shape)
    for tagaux in args.label_remove:
        aux = tagMatrix==np.array(tagaux)
        cells2keep[aux]=0 #Turn to 0 the cells to remove

    cells2keepBool=cells2keep.astype(bool)
    cells2keep=elemMatrix[cells2keepBool,:]
    pointss2keep=np.unique(cells2keep) #Get the points that are still left in the mesh

    newPoints=pointMatrix[pointss2keep,:]

    

    #Create new phile_file
    if args.extract_vm:
        if args.simulation_ecg_format=="igb":
            simulation_Name=os.path.join(args.simulation_path,args.simulation_name,args.file_phie_name+".igb")
            header_phie,phie_recovery=read_ecg_from_igb(simulation_Name)
        new_phie=phie_recovery[pointss2keep,:]
        new_header_phie=header_phie.copy()
        new_header_phie['x']=new_phie.shape[0]
        aux=carp.IGBFile(os.path.join(args.simulation_path,args.simulation_name,args.file_phie_name+"_"+ args.new_mesh_name +".igb"),mode = 'w')
        # carp.IGBFile.__init__(self,filename,mode = 'r' )	
        aux.write(new_phie,header = new_header_phie )
        aux.close()

    

    #Renumber cells in cell matrix to get new mesh
    #Add labels to points
    pointslables=np.arange(0, pointMatrix.shape[0], dtype=int)
    pointsNumbered=np.concatenate((pointslables[:, None],pointMatrix),axis=1)
    #Remove points that are eliminated
    pointsNumbered=pointsNumbered[pointss2keep]
    newpointslables=np.arange(0, pointsNumbered.shape[0], dtype=int)
    pointsNumbered=np.concatenate((pointsNumbered,newpointslables[:, None]),axis=1)

    mappings=dict(zip(pointsNumbered[:,0], pointsNumbered[:,-1]))
    
    replace_func = np.vectorize(lambda x: mappings.get(x, x))  # if not in dict, leave unchanged
    auxcells=replace_func(cells2keep)
    newCells={}
    newCells[args.cell_type] = auxcells.astype('int')

    
    cell_data_aux = {}
    cell_data_aux["fibers"]=[lonMatrix[cells2keepBool]]
    cell_data_aux["elemTag"]=[tagMatrix[cells2keepBool]]

    #Write new mesh
    newMesh=meshio.Mesh(newPoints,newCells,  cell_data=cell_data_aux)
    
    newMeshName= args.mesh_name+"_"+args.new_mesh_name
    newMesh.write(os.path.join(args.mesh_path,newMeshName+".vtk"))

    # if args.save_empty_mesh:
    #     newMeshEmpty=meshio.Mesh(newPoints,newCells)
    #     newMeshEmpty.write(os.path.join(args.mesh_path,args.new_mesh_name+"_empty.vtk"))

    #Get surface and surface points-----------
    #Read mesh again
    newMeshpv = pv.read(os.path.join(args.mesh_path,newMeshName+".vtk"))
    surf = newMeshpv.extract_surface() #Get surface
    surfIds=surf['vtkOriginalPointIds'] #Get Ids of surface
    surf.save(os.path.join(args.mesh_path,newMeshName+"_surface.vtk"))  #Save surface mesh

    #Get phie from surface
    if args.extract_vm:
        new_phie_surf=new_phie[surfIds,:]
        with open(os.path.join(args.simulation_path,args.simulation_name,args.file_phie_name+"_"+ args.new_mesh_name +"_surface.txt"),'w') as f:
            csv.writer(f,delimiter='\n').writerows(new_phie_surf)

        new_header_phie_surface=header_phie.copy()
        new_header_phie_surface['x']=new_header_phie_surface.shape[0]
        aux=carp.IGBFile(os.path.join(args.simulation_path,args.simulation_name,args.file_phie_name+"_"+ args.new_mesh_name +"_surface.igb"),mode = 'w')
        # carp.IGBFile.__init__(self,filename,mode = 'r' )	
        aux.write(new_phie_surf,header = new_header_phie_surface )
        aux.close()

    
# #----------------------------------------------------------------------------------------------------
    
    #Save new .elem , .pts and .lon
    if args.saveOpenCARP:

        
        #Save pts in carp format
        print("Getting points as .pts file-------------")
        ut.writePointsFile(newMesh.points, os.path.join(args.mesh_path, "{}.pts".format(newMeshName)))

        #Save cells in carp format
        print("Getting cells as .elem file-------------")
        # ut.writeCellsFile(mesh.cells_dict[args.cell_type], os.path.join(args.outFolder, "{}.elem".format(fileName2Use)), cell_type=ut.meshioOCCellsMap[args.cell_type],layers)
        ut.writeCellsFile(newMesh.cells_dict[args.cell_type], os.path.join(args.mesh_path, "{}.elem".format(newMeshName)),cell_data_aux["elemTag"][0], cellType=ut.meshioOCCellsMap[args.cell_type])#Add the tags to cells. #JRDZC 20/03/2025
        #writeCellsFile(arr, outName, cell_type="Tt", tags)

        
        # print("Getting fibers for elem as .lon file-------------")
        # fibsCells = np.mean(newMesh.point_data["fibers"][newMesh.cells_dict["tetra"]], axis=1)
        # fibsCells = ut.getArrNormalization(fibsCells)
        # ut.writeFibsFile(fibsCells, os.path.join(args.data_path, "{}.lon".format(newMeshName)))

        print("Getting fibers for elem as .lon file-------------")
        # fibsCells = np.mean(newMesh.point_data["fibers"][newMesh.cells_dict["tetra"]], axis=1)
        # fibsCells = ut.getArrNormalization(fibsCells)
        ut.writeFibsFile(cell_data_aux["fibers"][0], os.path.join(args.mesh_path, "{}.lon".format(newMeshName)))
        cell_data_aux['fibers']

   

    print("Finished:",args.mesh_path)

if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))