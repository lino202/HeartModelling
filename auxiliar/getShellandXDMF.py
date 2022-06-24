import meshio
import fenics
import os 
import argparse

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--data_path',type=str, required=True, help='path to data')
parser.add_argument('--out_format',type=str, required=True, help='output format: pvd | xdmf')
args = parser.parse_args()

dataPath = args.data_path
outputFormat = args.out_format 
vtkPath = os.path.join(dataPath, "tetmesh.vtk")

# Transform to xdmf for reading wiht fenics
xmlPath = vtkPath.replace('vtk', 'xdmf')
meshIn = meshio.read(vtkPath)
meshOut = meshio.Mesh(meshIn.points, meshIn.cells)
meshOut.write(xmlPath) 


# Create mesh and get boundary points
mesh = fenics.Mesh()
f = fenics.XDMFFile(fenics.MPI.comm_world, xmlPath)
f.read(mesh)
bmesh = fenics.BoundaryMesh(mesh, "exterior", True)

if "pvd" in outputFormat:
    fenics.File(os.path.join(dataPath, "mesh_boundary.pvd")) << bmesh
elif "xdmf" in outputFormat:
    outXdmf= fenics.XDMFFile(os.path.join(dataPath, "mesh_boundary.xdmf"))
    outXdmf.write(bmesh,0)
else: raise ValueError("Wrong output Format")