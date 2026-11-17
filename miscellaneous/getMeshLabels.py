''' Get the labels included in the mesh
'''




import meshio
import os  
import argparse
import numpy as np
import vtk
from vtk.util import numpy_support  # type: ignore
import time
import matplotlib.pyplot as plt
import seaborn as sns
import pyvista as pv


def main():

    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument('--mesh_path',  type=str, required=True, help='mesh path')
    parser.add_argument('--mesh_name',  type=str, required=True, help='mesh name with labels')
    parser.add_argument('--mesh_layer_name',  type=str, required=True, help='label where to egt the labels')
    parser.add_argument('--type_layer',  type=str, required=True, help='layer egt the labels')
    

    args = parser.parse_args()
    
    # "--out_path",  "/mnt/e/Jimena/HCULB/IHD/Segmentations/MI_MRI_32",
    # "--mesh_path_tags","/mnt/e/Jimena/HCULB/IHD/Segmentations/MI_MRI_32/mesh_rough_apex_micometers.vtk",
    # "--mesh_path_volumes","/mnt/e/Jimena/HCULB/IHD/Segmentations/MI_MRI_32/mesh/tetmesh_rough.1_centers_volumes.vtk",
    # "--units_volumes","mm",
    # "--label_name","layers_scar",
    # "--labels_tags_scar","23","33","43","53",
    # "--labels_tags_bz","22","32","42","52",
    # "--save_image", //  "",

    ht=os.path.split(args.mesh_name)
    meshName=ht[1].split(".vtk")[0]

    #Open mesh with volumes
    # mesh = meshio.read(os.path.join(args.data_path, args.mesh_name))
    mesh_volumes = pv.read(os.path.join(args.mesh_path,args.mesh_name))

    if args.type_layer=="cell":
        tags=mesh_volumes.cell_data[args.mesh_layer_name]
    elif args.type_layer=="point":
        tags=mesh_volumes.point_data[args.mesh_layer_name]


    values, counts = np.unique(np.array(tags), return_counts=True)
    values = np.reshape(values,(np.size(values),1))
    counts = np.reshape(counts,(np.size(counts),1))

    # outvalues=[values,counts]

    outvalues=np.concatenate((values, counts), axis=1)

    np.savetxt(os.path.join(args.mesh_path,meshName+"_"+args.mesh_layer_name+"_labels.txt"), outvalues, fmt='%d')  


    

        



    

if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))