'''Compute percentage of scar and bz
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
    parser.add_argument('--out_path',  type=str, required=True, help='path to save image and volumes')
    parser.add_argument('--mesh_path_tags',  type=str, required=True, help='mesh with layers as elem_data')
    parser.add_argument('--mesh_path_volumes',  type=str, required=True, help='mesh with volumes')
    parser.add_argument('--units_volumes',  type=str, required=True, help='units of mesh with volumes')
    parser.add_argument('--label_name',  type=str, required=True, help='name of label for tags')
    parser.add_argument('--labels_tags_scar',   nargs='+',    type=int, required=True, help="tags of scar")
    parser.add_argument('--labels_tags_bz',   nargs='+',    type=int, required=True, help="tags for bz")
    parser.add_argument('--save_image',action='store_true',  help='save histogram with percentages')
    args = parser.parse_args()

    # "--out_path",  "/mnt/e/Jimena/HCULB/IHD/Segmentations/MI_MRI_32",
    # "--mesh_path_tags","/mnt/e/Jimena/HCULB/IHD/Segmentations/MI_MRI_32/mesh_rough_apex_micometers.vtk",
    # "--mesh_path_volumes","/mnt/e/Jimena/HCULB/IHD/Segmentations/MI_MRI_32/mesh/tetmesh_rough.1_centers_volumes.vtk",
    # "--units_volumes","mm",
    # "--label_name","layers_scar",
    # "--labels_tags_scar","23","33","43","53",
    # "--labels_tags_bz","22","32","42","52",
    # "--save_image", //  "",

    ht=os.path.split(args.mesh_path_volumes)
    meshName=ht[1].split(".vtk")[0]

    #Open mesh with volumes
    # mesh = meshio.read(os.path.join(args.data_path, args.mesh_name))
    mesh_volumes = pv.read(args.mesh_path_volumes)

    #Open mesh with tags of scar and bz
    mesh_tags=pv.read(args.mesh_path_tags)
    tags=mesh_tags.cell_data[args.label_name]

    volumes=mesh_volumes.cell_data['Volume']

    tags_scar=np.zeros(tags.shape[0])
    tags_bz=np.zeros(tags.shape[0])

    volume_total=np.sum(volumes)

    #Find BZ
    for auxbz in args.labels_tags_bz:
        tags_bz[tags==auxbz]=1

    #Find scar
    for auxscar in args.labels_tags_scar:
        tags_scar[tags==auxscar]=1

    volume_bz=volumes[tags_bz.astype(bool)]
    volume_scar=volumes[tags_scar.astype(bool)]

    volume_bz=np.sum(volume_bz)
    volume_scar=np.sum(volume_scar)

    percent_vol_bz=volume_bz/volume_total*100
    percent_vol_scar=volume_scar/volume_total*100

    file_percentages=os.path.join(args.out_path,"volval_{}_{}.txt".format(meshName,args.units_volumes))
    with open(file_percentages, "w") as f:
        f.write("total_volume "+str(round(volume_total,2))+" \n")
        f.write("scar_volume "+str(round(volume_scar,2))+" \n")
        f.write("bz_volume "+str(round(volume_bz,2))+" \n")


    

if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))