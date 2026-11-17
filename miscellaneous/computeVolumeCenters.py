'''Compute the elements volume and the center and save. Volume as an array in cell data.
Preferably add the center to the mesh that already has the tags
'''

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
    parser.add_argument('--data_path',  type=str, required=True, help='path to data')
    parser.add_argument('--save_image',action='store_true',  help='save histogram with edgelengths')
    args = parser.parse_args()

    ht=os.path.split(args.data_path)
    meshName=ht[1].split(".vtk")[0]

    #Open mesh
    mesh = pv.read(args.data_path)
    mesh = mesh.compute_cell_sizes(length=False, area=False, volume=True)
    

    centers = mesh.cell_centers().points
    mesh.cell_data['Centers']=centers

    mesh.save(os.path.join(ht[0],"{}_centers_volumes.vtk".format(meshName)))

    #Histogram
    if args.save_image:
        volumes = mesh["Volume"]
        print("The edges lengths are: Mean: {0:.6f}, Median: {1:.6f}, Min: {2:.6f}, Max: {3:.6f}".format(np.mean(volumes), np.median(volumes), np.min(volumes), np.max(volumes)))

        f, (ax_box, ax_hist) = plt.subplots(2, sharex=True, gridspec_kw={"height_ratios": (.15, .85)})
        f.suptitle('Element volumes') #JRDZC Add 14/01/2025
        sns.boxplot(x=volumes, ax=ax_box,)
        sns.histplot(x=volumes, ax=ax_hist)
        ax_box.set(yticks=[])
        ax_hist.set_ylabel("Count", fontdict=dict(weight='bold'))
        ax_hist.set_xlabel("element volume", fontdict=dict(weight='bold'))
        ax_hist.axvline(np.median(volumes), color='g', linestyle='dashed', linewidth=2,label='Median='+str(np.median(volumes)))
        ax_hist.axvline(np.mean(volumes), color='r', linestyle='dashed', linewidth=2,label='Mean='+str(np.mean(volumes)))
        ax_hist.axvline(np.min(volumes), color='m', linestyle='dashed', linewidth=2,label='Min='+str(np.min(volumes)))
        ax_hist.axvline(np.max(volumes), color='y', linestyle='dashed', linewidth=2,label='Max='+str(np.max(volumes)))
        ax_hist.legend()
        sns.despine(ax=ax_hist)
        sns.despine(ax=ax_box, left=True)
        #Save plot
        plt.savefig(os.path.join(ht[0],"elemsvolumes_{}.png".format(meshName)), dpi=400)  
    

if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))