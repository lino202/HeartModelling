import os  
import argparse
import numpy as np
import meshio
import time
from miscellaneous.regions import regions
from tqdm import tqdm
from multiprocessing import Pool

def getNewLayerValueInit(_new_cells, _new_layers, _idxs_scar_layers):
    global new_cells, new_layers, idxs_scar_layers
    new_cells        = _new_cells
    new_layers       = _new_layers
    idxs_scar_layers = _idxs_scar_layers

def getNewLayerValue(idx):
    neighbour_nodes = new_cells[np.any(np.isin(new_cells, idx), axis=1),:].flatten()
    neighbour_nodes = neighbour_nodes[~np.isin(neighbour_nodes, idxs_scar_layers)] #without scar nodes
    new_values, counts = np.unique(new_layers[neighbour_nodes], return_counts=True)
    return new_values[np.argmax(counts)]

def main():

    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument('--meshPath',type=str, required=True,  help='path to data')
    parser.add_argument('--outPath',type=str, required=True,  help='path to data')
    parser.add_argument('--nProcesses',type=int, default=8,  help='N of workers, if exceeds cpu_count() then cpu_count-1 is used')
    parser.add_argument('--chunksize',type=int, default=0,  help='Numbers of nodes to be treated by worker, if 0 all nodes are divided in the number of workers')
    args = parser.parse_args()
    
    #Read Data
    mesh   = meshio.read(args.meshPath)
    points = mesh.points
    cells  = mesh.cells_dict['tetra']
    layers = mesh.point_data['layers']

    # Take cells out
    scar_idxs = np.where((layers>=regions["scar_base_endo_flag"]) & (layers<=regions["scar_apex_epi_flag"]))[0]
    new_cells = cells[np.logical_not(np.all(np.isin(cells, scar_idxs), axis=1)),:] # take tets with ALL scar nodes out, if we take ANY an isthmus can be lost
    
    # Define new points and get mapping with old ones
    new_cells = new_cells.flatten()
    new_points_idxs, inverse_idxs = np.unique(new_cells, return_inverse=True)
    new_points = points[new_points_idxs]
    
    # Update cell numbering
    tmp = np.arange(new_points.shape[0])
    new_cells = tmp[inverse_idxs]
    new_cells = new_cells.reshape(-1,4)

    # New point layers 
    # Tets with 1, 2 or 3 points tagged as scar can be present, so we see where they are and select the median value of the other nodes in tet that are not scar
    new_layers = layers[new_points_idxs]
    idxs_scar_layers = np.where((new_layers>=regions["scar_base_endo_flag"]) & (new_layers<=regions["scar_apex_epi_flag"]))[0]
    # We use a for as a scar node is connected to a variable number of other nodes, TODO it is too slow for single core

    if args.nProcesses >= os.cpu_count(): args.nProcesses = os.cpu_count()-1
    if args.chunksize == 0: args.chunksize = int(np.round(idxs_scar_layers.shape[0] / args.nProcesses))
    with Pool(args.nProcesses, initializer=getNewLayerValueInit, initargs=(new_cells, new_layers, idxs_scar_layers)) as p:
        res = list(tqdm(p.imap(getNewLayerValue, idxs_scar_layers, chunksize=args.chunksize), total=idxs_scar_layers.shape[0]))

    new_layers[idxs_scar_layers] = res

    #SaveData
    mesh_vtk = meshio.Mesh(new_points, cells=[('tetra', new_cells)], point_data={"layers":new_layers})
    mesh_vtk.write(os.path.join(args.outPath, "mesh_mi_noscar.vtk"))

    nsets = {}
    for key, value in regions.items():
        nset_name = key.replace("flag", "nodes")
        nsets[nset_name] = np.where(new_layers==value)[0]

    mesh_inp = meshio.Mesh(new_points, cells=[('tetra', new_cells)], point_sets=nsets)
    mesh_inp.write(os.path.join(args.outPath, "mesh_mi_noscar.inp"))

if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))

