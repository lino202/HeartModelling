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

def main():
    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument('--data_path',    type=str, required=True)
    parser.add_argument('--mesh_name',    type=str, required=True)
    parser.add_argument('--label_remove',   nargs='+',    type=int, required=True, help="Labels of elements to be removed")
    parser.add_argument('--label_keep',    nargs='+',    type=int, required=True, help="Labels of elements to be kept")
    parser.add_argument('--new_mesh_name',    type=str, required=True)
    parser.add_argument('--cell_type',   type=str, default="tetra")
    parser.add_argument('--saveOpenCARP', action='store_true', help="If called, the carp_txt is saved")
    parser.add_argument('--save_empty_mesh', action='store_true', help="If called, the mesh wo scar is also saved wo tags")
   
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



    # Open the .elem
    elemFile=os.path.join(args.data_path,args.mesh_name+".elem")

    data = np.loadtxt(elemFile, skiprows=1, usecols=range(1,6), dtype=int)
    elemMatrix=data[:,:-1]
    tagMatrix=data[:,-1]


    # Open the .pts
    pointFile=os.path.join(args.data_path,args.mesh_name+".pts")
    pointMatrix = np.loadtxt(pointFile, skiprows=1, dtype=float)

    # Open the .lon
    lonFile=os.path.join(args.data_path,args.mesh_name+".lon")
    lonMatrix = np.loadtxt(lonFile, skiprows=1, dtype=float)



    #Remove tags

    # layersCells_aux=np.squeeze(layersCells)

    #Find ids of Scar cells
    cells2keep=np.ones(tagMatrix.shape)
    for tagaux in args.label_remove:
        for tagaux_2 in args.label_keep:
            # aux=(layersCells==np.array(tagaux) & layersCells!=np.array(tagaux_2)).any()
            #Ce
            aux = np.logical_and(tagMatrix==np.array(tagaux), tagMatrix!=np.array(tagaux_2))
            cells2keep[aux]=0 #Turn to 0 the cells to remove

    cells2keepBool=cells2keep.astype(bool)
    # cells=mesh.cells_dict[args.cell_type]
    cells2keep=elemMatrix[cells2keepBool,:]
    pointss2keep=np.unique(cells2keep) #Get the points that are still left in the mesh

    newPoints=pointMatrix[pointss2keep,:]

    #Renumber cells in cell matrix
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
    # cell_data_aux["elemTag"]=tagMatrix[cells2keepBool]

    newMesh=meshio.Mesh(newPoints,newCells,  cell_data=cell_data_aux)
    
    # mesh_container = nano.MeshContainer(points=newPoints,cells=newCells,point_data=mesh.point_data, cell_data=mesh.cell_data[args.data_label])

    newMesh.write(os.path.join(args.data_path,args.new_mesh_name+"_micrometers.vtk"))

    if args.save_empty_mesh:
        newMeshEmpty=meshio.Mesh(newPoints,newCells)

        newMeshEmpty.write(os.path.join(args.data_path,args.new_mesh_name+"_micrometers_empty.vtk"))

    

    
# #----------------------------------------------------------------------------------------------------
    
    #Save new .elem , .pts and .lon
    if args.saveOpenCARP:
        #Save pts in carp format
        print("Getting points as .pts file-------------")
        ut.writePointsFile(newMesh.points, os.path.join(args.data_path, "{}.pts".format(args.new_mesh_name+"_micrometers")))

        #Save cells in carp format
        print("Getting cells as .elem file-------------")
        # ut.writeCellsFile(mesh.cells_dict[args.cell_type], os.path.join(args.outFolder, "{}.elem".format(fileName2Use)), cell_type=ut.meshioOCCellsMap[args.cell_type],layers)
        ut.writeCellsFile(newMesh.cells_dict[args.cell_type], os.path.join(args.data_path, "{}.elem".format(args.new_mesh_name+"_micrometers")),cell_data_aux["elemTag"][0], cellType=ut.meshioOCCellsMap[args.cell_type])#Add the tags to cells. #JRDZC 20/03/2025
        #writeCellsFile(arr, outName, cell_type="Tt", tags)

        
        # print("Getting fibers for elem as .lon file-------------")
        # fibsCells = np.mean(newMesh.point_data["fibers"][newMesh.cells_dict["tetra"]], axis=1)
        # fibsCells = ut.getArrNormalization(fibsCells)
        # ut.writeFibsFile(fibsCells, os.path.join(args.data_path, "{}.lon".format(args.new_mesh_name)))

        print("Getting fibers for elem as .lon file-------------")
        # fibsCells = np.mean(newMesh.point_data["fibers"][newMesh.cells_dict["tetra"]], axis=1)
        # fibsCells = ut.getArrNormalization(fibsCells)
        ut.writeFibsFile(cell_data_aux["fibers"][0], os.path.join(args.data_path, "{}.lon".format(args.new_mesh_name+"_micrometers")))
        cell_data_aux['fibers']

   

    print("Finished:",args.data_path)

if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))