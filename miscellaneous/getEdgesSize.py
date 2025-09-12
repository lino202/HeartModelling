import os  
import argparse
import numpy as np
import vtk
from vtk.util import numpy_support  # type: ignore
import time
import matplotlib.pyplot as plt
import seaborn as sns

def main():

    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument('--filePath',  type=str, required=True, help='path to data')
    parser.add_argument('--save',action='store_true',  help='save histogram with edgelengths')
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

    #Histogram of edge lengths
    f, (ax_box, ax_hist) = plt.subplots(2, sharex=True, gridspec_kw={"height_ratios": (.15, .85)})
    f.suptitle('Edge lengths') #JRDZC Add 14/01/2025
    sns.boxplot(x=lengths, ax=ax_box,)
    sns.histplot(x=lengths, ax=ax_hist)
    ax_box.set(yticks=[])
    ax_hist.set_ylabel("Count", fontdict=dict(weight='bold'))
    ax_hist.set_xlabel("Edge length", fontdict=dict(weight='bold'))
    ax_hist.axvline(np.median(lengths), color='g', linestyle='dashed', linewidth=2,label='Median='+str(np.median(lengths)))
    ax_hist.axvline(np.mean(lengths), color='r', linestyle='dashed', linewidth=2,label='Mean='+str(np.mean(lengths)))
    ax_hist.axvline(np.min(lengths), color='m', linestyle='dashed', linewidth=2,label='Min='+str(np.min(lengths)))
    ax_hist.axvline(np.max(lengths), color='y', linestyle='dashed', linewidth=2,label='Max='+str(np.max(lengths)))
    ax_hist.legend()
    sns.despine(ax=ax_hist)
    sns.despine(ax=ax_box, left=True)
    #Save plot
    plt.savefig(os.path.join(ht[0], "edgelength.png"), dpi=400) if args.save else plt.show(block=True)


if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))
