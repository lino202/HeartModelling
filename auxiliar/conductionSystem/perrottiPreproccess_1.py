import meshio
import fenics
import os

rootPath = "/home/maxi/Documents/PhD/Code/purkinje-py3/data/"
sample = "sampleMA_Control2"
outputFormat = "pvd"  #"pvd" or "xdmf"

# Transform to xdmf for readinf wiht fenics
vtkPath = os.path.join(rootPath, sample,"mesh.vtk")
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
    fenics.File(os.path.join(rootPath, sample, "mesh_boundary.pvd")) << bmesh
elif "xdmf" in outputFormat:
    outXdmf= fenics.XDMFFile(os.path.join(rootPath, sample, "mesh_boundary.xdmf"))
    outXdmf.write(bmesh,0)
else: raise ValueError("Wrong output Format")