"""This code takes a 1D purkinje tree and refine its edges to a certain size, this is specially important for projection into 
the epicardium as endbranches of two nodes are projected to the epi generating long branches with huge dx"""


import os
import meshio
import argparse
import time
import numpy as np
from lib.utils import getEdges, saveVtkInpMesh1D, checkRepeatedPoints


def main():
    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument('--filePath',type=str, required=True, help='path to data')
    parser.add_argument('--csName',type=str, required=True, help='path to data')
    parser.add_argument('--size',type=float, required=True, help='path to data')
    args = parser.parse_args()

    #Inputs
    mesh = meshio.read(os.path.join(args.filePath, "{}.vtk".format(args.csName))) 
    points = mesh.points
    edges = mesh.cells_dict['line']
    dists = points[edges,:]
    dists = np.linalg.norm(np.diff(dists, axis=1).squeeze(), axis=1)
    idxs  = np.where(dists>args.size)[0]
    edges2refine = {}
    edges2steps = {}
    for idx in idxs:
        steps = int(np.round(dists[idx]/args.size))
        if steps <= 2: continue # Theres no extra points
        edges2refine["edge_{}".format(str(idx))] = edges[idx,:]
        edges2steps["edge_{}".format(str(idx))] = steps

    for key in edges2refine.keys():
        i_edge = edges2refine[key]
        
        newPoints = np.linspace(points[i_edge[0],:], points[i_edge[1],:], edges2steps[key])
        newEdges = getEdges(newPoints)

        # Update the edges
        edge2delete = np.where((edges[:,0]==i_edge[0]) & (edges[:,1]==i_edge[1]))
        edges = np.delete(edges, edge2delete, axis=0)

        #Add new edges and points
        newEdges = newEdges + points.shape[0] - 1
        newEdges[np.where(newEdges==points.shape[0] - 1)] = i_edge[0]
        newEdges[np.where(newEdges==newEdges.max())] = i_edge[1]
        edges  = np.concatenate((edges, newEdges), axis=0)
        points = np.concatenate((points, newPoints[1:-1]), axis=0)

    nsets={}
    if 'purk_endnodes' in mesh.point_data.keys():
        nsets['purk_endnodes'] = np.where(mesh.point_data['purk_endnodes']==1)[0]
    # uniqueEdges, count = np.unique(edges, return_counts=True)   
    # uniqueEdges = uniqueEdges[count==1]
    # nsets["purk_endnodes"] = uniqueEdges[uniqueEdges!=0] # 0 is the av_node 
    checkRepeatedPoints(points)

    # Save
    print("-----------Saving------------")
    saveVtkInpMesh1D(points, edges, nsets, args.filePath, "{}".format(args.csName))

    
if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))