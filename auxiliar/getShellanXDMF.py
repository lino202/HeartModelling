import meshio
import fenics
import os 

dataPath = "/home/maxi/Documents/PhD/Data/DTI_hearts/Data_Electra_DWI/sampleLE_Control2"
outputFormat = "pvd"  #"pvd" or "xdmf"
vtkPath = os.path.join(dataPath, "electra_tetmesh.vtk")


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