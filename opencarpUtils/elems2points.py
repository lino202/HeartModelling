'''
Transform from elem data to point data

'''


import pyvista as pv
import numpy as np
import argparse
import os
import time
import utils as ut
import sys
import matplotlib.pyplot as plt
import meshio

import binascii

# import carputils as carp
import carputils.carpio.igb as carp
from scipy.signal import find_peaks

import scipy.io

import statistics

from collections import defaultdict
from scipy.stats import mode


from scipy.sparse import csr_matrix


def main():
    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument('--mesh_path',      type=str, required=True, help='path to mesh')
    parser.add_argument('--mesh_name',      type=str, required=True, help='name of mesh with the end')
    # parser.add_argument('--time_steps',type=int,help='time steps to plot results')
    parser.add_argument('--data_label',    type=str, required=True, help="Labels of where to get the zones")
    parser.add_argument('--cellType',        type=str, default="tetra")

    
    
    
    args = parser.parse_args()

    # 1. Load your large mesh
    meshName=os.path.join(args.mesh_path, args.mesh_name)
    # mesh = pv.read(meshName)
    mesh = meshio.read(meshName)

    # ht=os.path.split(args.mesh_name)
    fileName2Use=str(args.mesh_name).split(".vtk")[0]

    
    if args.data_label not in list(mesh.cell_data.keys()):
        raise ValueError("Invalid data label")

    if args.cellType not in mesh.cells_dict:
        raise ValueError("Invalid cell type")
   

    
    cells = mesh.cells_dict["tetra"]       # Shape: (num_cells, 4)
    cell_tags = mesh.cell_data[args.data_label][0]  # Shape: (num_cells,)

    num_points = len(mesh.points)
    num_cells = len(cells)

    # 2. Flatten the cells and repeat the tags so they align
    # Each cell has 4 vertices, so we repeat each cell's tag 4 times
    flat_vertices = cells.ravel()
    repeated_tags = np.repeat(cell_tags, 4)

    # 3. Find the unique tags to map them to local indices (if they aren't 0, 1, 2...)
    unique_tags, mapped_tags = np.unique(repeated_tags, return_inverse=True)
    num_unique_tags = len(unique_tags)

    # 4. Construct a sparse matrix: rows = points, cols = tag_indices
    # This acts as a massive histogram counter for every single point simultaneously
    ones = np.ones_like(flat_vertices)
    tag_counts_sparse = csr_matrix(
        (ones, (flat_vertices, mapped_tags)),
        shape=(num_points, num_unique_tags)
    )

    # 5. Get the index of the maximum count (the majority vote) for each point
    # argmax along the columns gives us the dominant tag index per row (point)
    dominant_tag_indices = np.asarray(tag_counts_sparse.argmax(axis=1)).flatten()

    # 6. Map back to your original tag values
    point_tags = unique_tags[dominant_tag_indices]

    # 7. Save the result
    mesh.point_data[args.data_label] = point_tags
    mesh.write(meshName)

    

    print("Finished: ", args.mesh_path)

    



if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))