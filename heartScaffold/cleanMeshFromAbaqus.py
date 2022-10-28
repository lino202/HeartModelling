import argparse
import meshio

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--mesh',type=str, required=True, help='path to data mesh')
args = parser.parse_args()

mesh = meshio.read(args.mesh)
meshOut = meshio.Mesh(mesh.points, mesh.cells)
meshOut.write(args.mesh)