import meshio
import argparse
import os
import numpy as np
import utils as ut
import time

def main():
    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument('--filePath',        type=str, required=True)
    parser.add_argument('--unit',            type=str, required=True)
    parser.add_argument('--cellType',        type=str, default="tetra")
    parser.add_argument('--stimPointData',   type=str)
    parser.add_argument('--fibersPointData', type=str)
    parser.add_argument('--layersPointData', type=str)
    parser.add_argument('--outFolder',       type=str, required=True)
    args = parser.parse_args()

    mesh = meshio.read(args.filePath)
    if not os.path.isdir(args.outFolder): os.mkdir(args.outFolder)
    fileName = args.filePath.split(".")[0].split("/")[-1]
    #Switch to um as opencarp only seems to support that
    if args.unit=="cm":
        mesh.points = mesh.points * 10000
    elif args.unit=="mm":
        mesh.points = mesh.points * 1000
    elif args.unit=="um":
        pass
    else: raise ValueError("Only units in cm, mm or um are supported")

    #Save pts in carp format
    print("Getting points as .pts file-------------")
    ut.writePointsFile(mesh.points, os.path.join(args.outFolder, "{}.pts".format(fileName)))

    #Save cells in carp format
    print("Getting cells as .elem file-------------")
    ut.writeCellsFile(mesh.cells_dict[args.cellType], os.path.join(args.outFolder, "{}.elem".format(fileName)), cellType=ut.meshioOCCellsMap[args.cellType])

    #Create .vtx files of point data of interest
    if args.stimPointData:
        print("Getting stim nodes as vtx file -------------")
        tmp = mesh.point_data[args.stimPointData]
        tmp = (tmp==1).nonzero()[0]
        ut.writeStimVtxFile(tmp, os.path.join(args.outFolder, "{}.vtx".format(args.stimPointData)))

    #Add fibers to cell data
    # if fibers are already or you want just default fibers from meshtool just dont pass the argument
    if args.fibersPointData:
        print("Getting fibers for elem as .lon file-------------")
        fibsCells = np.mean(mesh.point_data[args.fibersPointData][mesh.cells_dict["tetra"]], axis=1)
        fibsCells = ut.getArrNormalization(fibsCells)
        ut.writeFibsFile(fibsCells, os.path.join(args.outFolder, "{}.lon".format(fileName)))

    #Add tag to cell data for meshtool to understand
    # if hasattr(args, "layersPointData"):
        # print("Getting cells tags in the vtk file -------------")
        # fibsCells = np.mean(mesh.point_data["fibers"][mesh.cells_dict["tetra"]], axis=1)
        # fibsCells = getArrNormalization(fibsCells)
        # mesh.cell_data["fibers"] = [fibsCells]
        # writeFlag = 1

    # We are not using meshtool as meshio saves fibs in FIELD data and meshtool wants them in VECTOR (need more research)
    # #Convert mesh to carp format
    # print("Converting mesh to CARP format")
    # cmdMesh = 'meshtool convert -imsh={0} -omsh={1}/{2}'.format(args.filePath, args.outFolder, args.filePath.split(".")[0].split("/")[-1])
    # outMesh = os.system(cmdMesh)
    # if outMesh==0: print("Mesh conversion successfully") 
    # else: print("Mesh conversion failure")


if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))