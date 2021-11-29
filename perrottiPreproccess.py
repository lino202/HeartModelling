import meshio
import fenics
import os 

rootPath = "./data/"
sample = "sampleMA_Control2"
vtkPath = os.path.join(rootPath, sample,"mesh.vtk")
xmlPath = vtkPath.replace('vtk', 'xml')
meshIn = meshio.read(vtkPath)
meshOut = meshio.Mesh(meshIn.points, meshIn.cells)
meshOut.write(xmlPath) 


# Create mesh and get boundary points
mesh = fenics.Mesh(xmlPath)
bmesh = fenics.BoundaryMesh(mesh, "exterior", True)

fenics.File(os.path.join(rootPath, sample, "mesh_boundary.pvd")) << bmesh
