# We genereate random fibers for the MI region and save them for ELECTRA
# and into the .vtk mesh
import meshio
import numpy as np
import argparse
import time
import sys
import os
import copy
sys.path.append(os.path.dirname(os.path.dirname(sys.path[0])))
from miscellaneous.regions import regions
from auxiliar.rbm.utils import writeFibers4JSON

def main():
    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument('--mesh',type=str, required=True, help='path to data')
    parser.add_argument('--meshHE',type=str, required=True, help='path to data')
    parser.add_argument('--fiberName',type=str, required=True, help='name for the healthy fibers in the mesh')
    parser.add_argument('--outName',type=str, required=True, help='name for the output fibers')
    args = parser.parse_args()

    # Read Volume Mesh and fibers
    mesh = meshio.read(args.mesh)
    meshHE = meshio.read(args.meshHE)

    fibersHE = meshHE.point_data[args.fiberName]

    # Identify MI nodes and change those fibers to random
    miNodesIdxs = np.where(mesh.point_data['layers']>regions['apex_epi_flag'])[0]

    # Generate random fibers for MI nodes
    randomFibers = np.random.uniform(-1, 1, size=(len(miNodesIdxs),3))
    randomFibers /= np.linalg.norm(randomFibers, axis=1)[:, np.newaxis]

    # Create final fibers array
    fibersMI = copy.deepcopy(fibersHE)
    fibersMI[miNodesIdxs,:] = randomFibers

    # Save 
    outPath = os.path.dirname(args.mesh)
    mesh.point_data[args.outName] = fibersMI
    meshio.write(args.mesh, mesh)
    writeFibers4JSON(os.path.join(outPath, args.outName + '.json'), fibersMI)
    

if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))