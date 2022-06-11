import meshio
import os 
import argparse

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--data_path',type=str, required=True, help='path to data')
args = parser.parse_args()

dataPath = args.data_path
names = ["lv_endo", "rv_endo", "epi"]

for name in names:
    mesh = meshio.read(os.path.join(dataPath, "{}.vtu".format(name)))
    cells = [("triangle", mesh.cells_dict["triangle"])]
    meshOut = meshio.Mesh(mesh.points, cells)
    meshOut.write(os.path.join(dataPath, "{}.obj".format(name)))



