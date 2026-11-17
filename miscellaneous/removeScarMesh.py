'''Remove the cells that would have the scar label
'''

import os  
import argparse
import numpy as np
import meshio
import time
import dolfin as df

import sys
# sys.path.append("/mnt/e/Jimena/Programas/Simulations/Maxi/HeartModelling/auxiliar/rbm")


# print(sys.executable)
# print(sys.path)


from utils import points2Elements

import nanomesh as nano


# sys.path.append("/mnt/e/Jimena/Programas/Simulations/Maxi/HeartModelling/opencarpUtils")
# import utils as ut #From opencarputils

def main():

    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument('--data_path',type=str, required=True,  help='path to data')
    parser.add_argument('--mesh_name', type=str, required=True, help='name of the mesh to be used')
    parser.add_argument('--out_name',type=str, required=True, help='name of the result mesh')
    parser.add_argument('--data_label',       type=str, required=True, help='Name of label to be used to remove elements, data_label (cellData) or pointData')
    parser.add_argument('--removeLabel',nargs='+',type=int, help='data labelled with this number is removed')
    parser.add_argument('--keepLabel',nargs='+', type=int, help='data labelled with this number is not removed even with scar')
    parser.add_argument('--cellType',        type=str, default="tetra")
    parser.add_argument('--type_remove_label', type=str, default="cell", help="If the remove label is in the elem(cell)Data or the pointData. Options=cell or point")
    parser.add_argument('--save_empty_mesh', action='store_true', help="If called, the mesh wo scar is also saved wo tags")
   
    args = parser.parse_args()

    # --data_path    General path to all files. the out_name mesh will be saved there
    # --out_name'     Name of the result vtk mesh that will be stored in the general path
    # --infAsHealthy Flags to not join the transmurality and scar. If added, args.infAsHealthy is True.
    '''  
    --data path   E:\Jimena\HCULB\IHD\Segmentations\MI_MRI_32
    --mesh_name  mesh.vtk
    --removeLabel 8 

    myo_flag = 1

    FEC_flag = 2
    endo_flag = 3
    mid_flag = 4
    epi_flag = 5

    uncertain_flag = 6
    bz_flag = 7
    scar_flag = 8


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
    '''



    #Read mesh
    mesh = meshio.read(os.path.join(args.data_path,args.mesh_name))

    # mesh_container = nano.MeshContainer(points=mesh.points,cells=mesh.cells_dict[args.cellType],point_data=mesh.point_data, cell_data=mesh.cell_data[args.data_label])
    # mesh_container_2 = meshio.Mesh(mesh.points, mesh.cells_dict[args.cellType], 
    # cell_data={args.data_label: aux})

    # aux=np.asarray(mesh.cell_data[args.data_label])
    # cell_data_aux={args.data_label: aux}
    # cell_data_aux={args.data_label: mesh.cell_data[args.data_label]}
    
    # mesh_container.remove_cells(label=53,key='layes_scar')

    if args.type_remove_label=="cell":
        layersCells=np.asarray(mesh.cell_data[args.data_label])

    elif args.type_remove_label=="point":

        #Convert to elems to see which elements to remove
        layersPoints=mesh.point_data[args.data_label]
        layersCells=points2Elements(mesh.cells_dict[args.cellType], layersPoints)

    else:
        print("Error in type_remove_label")

    #Get label

    # if len(layersCells.shape)>2:
    #     layersCells_aux=np.squeeze(layersCells)

    layersCells_aux=np.squeeze(layersCells)

    #Find ids of Scar cells
    cells2keep=np.ones(layersCells_aux.shape)
    for tagaux in args.removeLabel:
        for tagaux_2 in args.keepLabel:
            # aux=(layersCells==np.array(tagaux) & layersCells!=np.array(tagaux_2)).any()
            #Where the labels are to be kept and not rem
            aux = np.logical_and(layersCells_aux==np.array(tagaux), layersCells_aux!=np.array(tagaux_2))
            cells2keep[aux]=0  #Turn to 0 the cells to remove

    cells2keepBool=cells2keep.astype(bool)

    # cells=mesh.cells_dict[args.cellType]
    cells2keep=mesh.cells_dict[args.cellType][cells2keepBool,:]
    pointss2keep=np.unique(cells2keep) #Get the points that are still left in the mesh

    newPoints=mesh.points[pointss2keep]

    #Add labels to points
    pointslables=np.arange(0, mesh.points.shape[0], dtype=int)
    pointsNumbered=np.concatenate((pointslables[:, None],mesh.points),axis=1)
    #Remove points that are eliminated
    pointsNumbered=pointsNumbered[pointss2keep]
    newpointslables=np.arange(0, pointsNumbered.shape[0], dtype=int)
    pointsNumbered=np.concatenate((pointsNumbered,newpointslables[:, None]),axis=1)

    mappings=dict(zip(pointsNumbered[:,0], pointsNumbered[:,-1]))
    
    replace_func = np.vectorize(lambda x: mappings.get(x, x))  # if not in dict, leave unchanged
    newCells={}
    newCells[args.cellType] = replace_func(cells2keep)

    

    point_data_aux = {}
    for lab in mesh.point_data.keys():
        point_data_aux[lab]=mesh.point_data[lab][pointss2keep]

    cell_data_aux = {}
    for lab in mesh.cell_data.keys():
        aux=np.asarray(mesh.cell_data[lab])
        aux=np.squeeze(aux)
        cell_data_aux[lab]=[aux[cells2keepBool]]

    newMesh=meshio.Mesh(newPoints,newCells, point_data=point_data_aux, cell_data=cell_data_aux)

    # mesh_container = nano.MeshContainer(points=newPoints,cells=newCells,point_data=mesh.point_data, cell_data=mesh.cell_data[args.data_label])

    newMesh.write(os.path.join(args.data_path,args.out_name))

    if args.save_empty_mesh:
        meshNameEmpty=args.out_name.split(".vtk")[0]
        newMeshEmpty=meshio.Mesh(newPoints,newCells)

        newMeshEmpty.write(os.path.join(args.data_path,meshNameEmpty+"_empty.vtk"))

    print("Finished:",args.data_path)




if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))


