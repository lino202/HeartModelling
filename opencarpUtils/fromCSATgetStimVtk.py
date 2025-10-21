import meshio
import argparse
import numpy as np
import utils as ut
import time
from scipy import spatial

def main():

    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument('--csLats',  type=str, required=True)
    parser.add_argument('--csMesh',  type=str, required=True)
    parser.add_argument('--myoMesh', type=str, required=True)
    parser.add_argument('--outVtk',  type=str, required=True)
    parser.add_argument('--outVtx',  type=str, required=True)
    args = parser.parse_args()

    csMesh = meshio.read(args.csMesh)
    myoMesh = meshio.read(args.myoMesh)
    endnodes = (csMesh.point_data['purk_endnodes']==1).nonzero()[0]

    with open(args.csLats, "r") as f:
        data = f.readlines()
    lats = np.array(data[4:]).astype(float)
    lats = lats - np.nanmin(lats)
    
    tree = spatial.KDTree(myoMesh.points)
    stimPointsIdxs = tree.query_ball_point(csMesh.points[endnodes], r=1)

    allStimPoints = np.zeros(myoMesh.points.shape[0])
    for stimPoints in stimPointsIdxs:
        #TODO work for assigning LAT
        allStimPoints[stimPoints] = 1

    print("Saving stim nodes as vtk and vtx file -------------")
    myoMesh.point_data['stim'] = allStimPoints
    myoMesh.write(args.outVtk)

    allStimPoints = (allStimPoints==1).nonzero()[0]
    ut.writeStimVtxFile(allStimPoints, args.outVtx)


if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))