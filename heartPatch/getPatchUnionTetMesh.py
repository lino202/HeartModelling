import os 
import numpy as np
import argparse
import meshio
from utils import getPointsEnclosedByMesh
from tqdm import tqdm

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--meshUnion',type=str, required=True, help='path to data mesh in ply with patch faces labels')
parser.add_argument('--meshHeart',type=str, required=True, help='path to data mesh')
parser.add_argument('--outPath',type=str, required=True, help='path to output file')
args = parser.parse_args()


meshUnion = meshio.read(args.meshUnion)
meshHeart = meshio.read(args.meshHeart)
meshHeart.point_data["obj:vn"] = -1 * meshHeart.point_data["obj:vn"]
unionCells = meshUnion.cells_dict["tetra"]

unionCellCentroids = np.mean(meshUnion.points[unionCells], axis=1)

#Get innerPatch and get innerHeart
step = 10000
totalIdxs = np.array([])
for idx in tqdm(range(0,unionCells.shape[0],step)):
    realIdxs = np.arange(idx, idx+step)
    # unionCellCentroids = np.mean(meshUnion.points[unionCells[idx:idx+step,:]], axis=1)
    idxs = getPointsEnclosedByMesh(unionCellCentroids[idx:idx+step,:], meshHeart)
    totalIdxs = np.concatenate((totalIdxs, realIdxs[idxs])) if totalIdxs.size else realIdxs[idxs]

patchCells = np.zeros(unionCells.shape[0])
patchCells[totalIdxs] = 1
cell_data = {"patchCells": [patchCells]}

meshOut = meshio.Mesh(meshUnion.points, meshUnion.cells, cell_data=cell_data)
meshOut.write(args.outPath)

