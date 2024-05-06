import os
import copy
import meshio
import argparse
import time


def main():
    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument('--filePath',type=str, required=True, help='path to data')
    parser.add_argument('--csName',type=str, required=True, help='path to data')
    args = parser.parse_args()

    #Inputs
    mesh     = meshio.read(os.path.join(args.filePath, args.csName)) 
    if "vtk" in args.csName:
        point_data = copy.deepcopy(mesh.point_data)
        for key in mesh.point_data.keys():
            if ("branch" in key) or ("endBranch" in key):
                del point_data[key]
        mesh.point_data = point_data
    
    elif "inp" in args.csName:
        point_sets = copy.deepcopy(mesh.point_sets)
        for key in mesh.point_sets.keys():
            if ("branch" in key) or ("endBranch" in key):
                del point_sets[key]
        mesh.point_sets = point_sets
    else:
        raise ValueError("We delete only .inp or .vtk point sets/data")

    mesh.write(os.path.join(args.filePath, args.csName))
    
if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))