'''Remove the tags from mesh
'''

import os  
import argparse
import numpy as np
import meshio
import time
import dolfin as df

from scipy.io import savemat

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
    parser.add_argument('--cellType',   type=str, default="tetra")
    parser.add_argument('--save_mat', action='store_true', help="If called, the mesh is saved as .mat")
   
    
    
    args = parser.parse_args()

    # --data_path    General path to all files. the out_name mesh will be saved there
    # --out_name'     Name of the result vtk mesh that will be stored in the general path
    # --infAsHealthy Flags to not join the transmurality and scar. If added, args.infAsHealthy is True.
    


    #Read mesh
    mesh = meshio.read(os.path.join(args.data_path,args.mesh_name))
    cells={}
    cells[args.cellType]=mesh.cells_dict[args.cellType]
    points=mesh.points
        

   
    meshNameEmpty=args.mesh_name.split(".vtk")[0]
    newMeshEmpty=meshio.Mesh(points,cells)
    newMeshEmpty.write(os.path.join(args.data_path,meshNameEmpty+"_empty.vtk"))

    print("Finished:",args.data_path)

    #Save as mat for pseudoECG
    if args.save_mat:
        # VTK_EMPTY_CELL = 0, VTK_VERTEX = 1, VTK_POLY_VERTEX = 2, VTK_LINE = 3, VTK_POLY_LINE = 4, VTK_TRIANGLE = 5, VTK_TRIANGLE_STRIP = 6,
        # VTK_POLYGON = 7, VTK_PIXEL = 8,  VTK_QUAD = 9, VTK_TETRA = 10, VTK_VOXEL = 11, VTK_HEXAHEDRON = 12, VTK_WEDGE = 13,
        # VTK_PYRAMID = 14, VTK_PENTAGONAL_PRISM = 15,   VTK_HEXAGONAL_PRISM = 16

        if args.cellType=="tetra": celltypenum=10
        elif args.cellType=="voxel": celltypenum=11
        elif args.cellType=="triangle": celltypenum=5

        cellsint323 = cells['tetra'].astype(np.int32)
        cellsint323=cellsint323+1


        # a = np.arange(20)
        mdic = {"DatasetType":"UNSTRUCTURED_GRID","xyz":points, "tri": cellsint323,"celltype": celltypenum, "HEADER":"# vtk DataFile Version 2.0","TITLE":"Unstructured Grid"}
        # mdic{'a': np.array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16,17, 18, 19]),'label': 'experiment'}
        savemat(os.path.join(args.data_path,meshNameEmpty+"_empty.mat"), mdic)





if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))


