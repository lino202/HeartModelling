#Convert the vtk ot vtu mesh to xdmf

import meshio
import fenics
import os 
import argparse

# Add input arguments
parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--data_path',type=str, required=True, help='path to data')
parser.add_argument('--out_format',type=str, required=True, help='output format: pvd | xdmf')
parser.add_argument('--mesh_name',type=str, required=True, help='name of the mesh')
parser.add_argument('--in_format',type=str, required=True, help='input format: vtk | vtu')
parser.add_argument('--save_obj', action='store_true', help='if especified, save also he .obj (needed format xdmf)')
args = parser.parse_args()


dataPath = args.data_path
outputFormat = args.out_format 
inputFormat = args.in_format
meshName = args.mesh_name

meshName_format = args.mesh_name + "." + inputFormat

# dataPath = "/mnt/e/Jimena/OpenCARP/Temp_results/01/mesh"
# outputFormat = "xdmf" 
# inputFormat = "vtk"
# meshName = "01_BIV_HD_mm_volume_empty.vtk"

#vtkPath = os.path.join(dataPath, "tetmesh.vtk")
vtkPath = os.path.join(dataPath, meshName_format)

# Transform to xdmf for reading wiht fenics
# xmlPath = vtkPath.replace('vtk', 'xdmf')
# xmlPath = vtkPath.replace(inputFormat,outputFormat) #JRDZC 04/03/2025
xmlPath = os.path.join(dataPath, meshName+"_2."+outputFormat) #JRDZC 06/03/2025 #I added this because it wold not let me save the mesh with the same name because "it already existed"
meshIn = meshio.read(vtkPath)
meshOut = meshio.Mesh(meshIn.points, meshIn.cells)
meshOut.write(xmlPath) 


# Create mesh and get boundary points
mesh = fenics.Mesh()#Create empty mesh
f = fenics.XDMFFile(fenics.MPI.comm_world, xmlPath)
f.read(mesh)
bmesh = fenics.BoundaryMesh(mesh, "exterior", True)

surfaceMeshName = meshName + "_boundary"
if "pvd" in outputFormat:
    surfaceMeshNameOut = surfaceMeshName + ".pvd"
    fenics.File(os.path.join(dataPath, surfaceMeshNameOut)) << bmesh
elif "xdmf" in outputFormat:
    surfaceMeshNameOut = surfaceMeshName + ".xdmf"
    outXdmf= fenics.XDMFFile(os.path.join(dataPath, surfaceMeshNameOut))
    #outXdmf.write(bmesh,0) #Original
    outXdmf.write(bmesh)

if args.save_obj and "xdmf" in outputFormat:
    surfaceMeshNameXdmf = surfaceMeshName + ".xdmf"
    meshInXdmf = meshio.read(os.path.join(dataPath, surfaceMeshNameXdmf))
    surfaceMeshNameOut = surfaceMeshName + ".obj"
    meshInXdmf.write(os.path.join(dataPath, surfaceMeshNameOut))


else: raise ValueError("Wrong output Format")