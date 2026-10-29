#Interpolate thw mesh cloud with the BZ, scar and healthy tissue within the complete mesh
import os  
import argparse
import numpy as np
import meshio
from scipy.interpolate import RBFInterpolator, griddata
from auxiliar.rbm.utils import writeFibers4JSON
import time


def main():

    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument('--dataPath1',  type=str, help='path to data. point cloud')
    parser.add_argument('--dataPath2',  type=str, required=True, help='path to data. mesh')
    # parser.add_argument('--mesh_name',     type=str, required=True, help='name of the mesh')
    parser.add_argument('--interpType', type=str, required=True, help='nearest or rbf')
    parser.add_argument('--neighbours', type=int, required=True, help='neighbours to take into account, only used in rbf')
    parser.add_argument('--nameValue',  type=str, required=True, help='value to interp, layers_mi for GE/MI model or dti_fibers for exvivo dwi model')
    parser.add_argument('--outPath',    type=str, required=True)
    args = parser.parse_args()

    #--dataPath1 = cloud point file. From the segmentation
    #--dataPath2 = complete mesh. 
    #--interpType = which method of interpolation to use, nearest or rbf
    #--neighbours=neighbours to take into account, only used in rbf
    #--nameValue=value to interp, layers_mi for GE/MI model or dti_fibers for exvivo dwi model
    #--outPath = Path where to store the results

    mesh2 = meshio.read(args.dataPath2)

    ht=os.path.split(args.dataPath2)
    mesh_name=ht[1].split(".vtk")
    mesh_name=mesh_name[0]
    
    #Read the meshes
    if args.dataPath1:
        mesh1 = meshio.read(args.dataPath1)
        

        #Extract the points
        points1 = mesh1.points
        points2 = mesh2.points
        values = mesh1.point_data[args.nameValue] #Take the nameValuea field

        if "cover" in mesh2.point_data.keys():
            realMyoIdxs = np.where(mesh2.point_data["cover"] == 0)[0]
            points2 = points2[realMyoIdxs]

        #Interpolation between the mesh cloud of points and the mesh with .
        if args.interpType == "nearest":
            values2 = griddata(points1, values, points2, method='nearest')
        elif args.interpType == "rbf":
            values2 = RBFInterpolator(points1, values, neighbors=args.neighbours)(points2)
        else: raise ValueError("Wrong interpolation type")

        #/home/jrdzc16/miniconda3/envs/ModellingOldFenics/lib/python3.11/site-packages/scipy/interpolate/_rbfinterp.py

        if "layers" in args.nameValue or "AHA" in args.nameValue or "LVRV" in args.nameValue or "nodes" in args.nameValue: 
            finalValues2 = np.zeros((mesh2.points.shape[0]))
        if "fibers" in args.nameValue: 
            finalValues2 = np.zeros((mesh2.points.shape[0], 3))
        finalValues2[:] = np.nan 
        if "cover" in mesh2.point_data.keys():
            finalValues2[realMyoIdxs] =  values2
        else:
            finalValues2 = values2

        #get round values for vtk and inp
        if "layers" in args.nameValue or "AHA" in args.nameValue or "LVRV" in args.nameValue or "nodes" in args.nameValue:
            finalValues2[finalValues2<np.nanmin(values)] = np.nanmin(values)#Modify the values lower than the minimum
            finalValues2[finalValues2>np.nanmax(values)] = np.nanmax(values)#Modify the values higher than the maximum
            finalValues2 = np.round(finalValues2)
        elif "fibers" in args.nameValue:
            fibersNorm = np.linalg.norm(finalValues2, axis=1)
            finalValues2 = finalValues2 /  np.array([fibersNorm, fibersNorm, fibersNorm]).T
            outPath = "/".join(args.outPath.split("/")[:-1])
            writeFibers4JSON(os.path.join(outPath, "fibersJsonElectra.txt"), finalValues2)
        else: raise ValueError("Wrong valueName")

    else:

        finalValues2 = np.ones(mesh2.points.shape[0]) #as healthy as chosen in ge_s1_getGeometry.py

    mesh2.point_data[args.nameValue] = finalValues2
    # fileOutName = args.outPath.split(".")[0] + "_{}.vtk".format(args.interpType)
    out_name=os.path.join(args.outPath, "{}_interpolated.vtk".format(mesh_name))#JRDZC 10/03/2025


    mesh2.write(out_name)

if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))