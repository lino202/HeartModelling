import os  
import argparse
import numpy as np
import vtk
from vtk.util import numpy_support  # type: ignore
import time


def main():

    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument('--filePath',  type=str, required=True, help='path to data')
    args = parser.parse_args()

    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName(args.filePath)
    reader.Update()
    mesh    = reader.GetOutput()

    filter = vtk.vtkExtractEdges()
    filter.SetInputData(mesh)
    filter.Update()
    mesh = filter.GetOutput()

    filter = vtk.vtkCellSizeFilter()
    filter.ComputeVertexCountOff()
    filter.ComputeLengthOn()
    filter.SetInputData(mesh)
    filter.Update()
    mesh = filter.GetOutput()

    lengths = vtk.util.numpy_support.vtk_to_numpy(mesh.GetCellData().GetArray('Length'))
    print("The edges lengths are: Mean: {0:.6f}, Median: {1:.6f}, Min: {2:.6f}, Max: {3:.6f}".format(np.mean(lengths), np.median(lengths), np.min(lengths), np.max(lengths)))



if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))