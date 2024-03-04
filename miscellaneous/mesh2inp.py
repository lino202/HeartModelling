import meshio 
import numpy as np
import argparse

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--inPath',type=str, required=True, help='path to file and file name')
parser.add_argument('--outPath',type=str, required=True, help='path to file and file name')
parser.add_argument('--isMyo', action='store_true')
args = parser.parse_args()

validKeys = ["endo", "endoBZ", "mid", "midBZ", "epi", "epiBZ", "myo", "scar", "bz", "patch", "unatt"]
myo_flag = 1
scar_flag = 8
endo_flag = 3
mid_flag = 4
epi_flag = 5
uncertain_flag = 6
bz_flag = 7
patch_flag = 9
unatt_flag = 10

mesh = meshio.read(args.inPath)
pointData = mesh.point_data
pointDataKeys = pointData.keys()
nsets={}

if args.isMyo:

    # Get layers or tissue types
    #Only layers is defined
    if "layers" in pointDataKeys and ((not "endo" in pointDataKeys) and (not "mid" in pointDataKeys) and (not "epi" in pointDataKeys)):
        for key in pointDataKeys:
            if pointData[key].ndim == 1 and "layers" in key:
                for pointKey in validKeys:
                    if not "BZ" in pointKey:
                        nsets["{}_nodes".format(pointKey)] = np.where(pointData["layers"] == globals()["{}_flag".format(pointKey)])[0]
            elif pointData[key].ndim == 1 and "cover" in key:
                nsets["cover_nodes"] = np.where(pointData[key]==1)[0]
    #If we have endo-mid-epi and bz defined separately we use got them separately
    else:
        for key in pointDataKeys:
            if key in validKeys:
                nsets["{}_nodes".format(key)] = np.where(pointData[key]==1)[0]

    #Get stims
    for key in pointDataKeys:
        if "stim" in key and pointData[key].ndim == 1 and np.min(pointData[key])==0 and np.max(pointData[key])==1:
            nsets["{}_nodes".format(key.lower())] = np.where(pointData[key]==1)[0]
else:
    for key in pointDataKeys:
        nsets[key] = np.where(pointData[key]==1)[0]




#Get elems sets
cellData     = mesh.cell_data
cellDataKeys = cellData.keys()
elsets       = {}
for key in cellDataKeys:
    if cellData[key][0].ndim == 1:
        elsets["{}_elems".format(key)] = [list(np.where(cellData[key][0] == 1)[0])]

meshOut = meshio.Mesh(mesh.points, mesh.cells, point_sets=nsets, cell_sets=elsets)
meshOut.write(args.outPath)
