""""Here we use fenics, package ldrb for solving the apex to base gradient to for example
get the apex to base segmentation, in ldrb they use a first diffusion from the base to get the apex,
this is useful and enough for us and we keep that gradient for calculation of the apex_base segments
You need a triangle mesh labelled with the base.
"""

import dolfin as df
import ldrb
import os
import argparse
import time
import meshio
import numpy as np
from mpi4py import MPI

def main():
    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument('--data_path',type=str, required=True, help='path to data')
    parser.add_argument('--insert2Laplacians', action='store_true', help='If called the layers/laplacians.vtk mesh is searched and the apex_base grad is added')
    parser.add_argument('--radius',type=float, default=6, help='Radius for defining the apex subdomain for the BC')
    parser.add_argument('--mesh_name',     type=str, required=True, help='name of the mesh')
    args = parser.parse_args()

    # --data_path
    # --insert2Laplacians

    outPath = os.path.join(args.data_path, 'layers')
    if not os.path.isdir(outPath): os.mkdir(outPath)

    # Volume Mesh and FacetFunction reading
    
    mesh = df.Mesh()
    with df.XDMFFile(os.path.join(args.data_path, "mesh", "mesh_{}.xdmf".format(args.mesh_name))) as xdmf:
        xdmf.read(mesh)

    
    ffun = df.MeshFunction("size_t", mesh, 2)
    with df.XDMFFile(os.path.join(args.data_path, "mesh", "ffun_{}.xdmf".format(args.mesh_name))) as xdmf:
        xdmf.read(ffun)

    markers = ldrb.utils.default_markers()

    solver = df.PETScKrylovSolver()
    df.PETScOptions.set("ksp_type", "cg")
    df.PETScOptions.set("ksp_norm_type", "unpreconditioned")
    df.PETScOptions.set("ksp_atol", 1e-15)
    df.PETScOptions.set("ksp_rtol", 1e-10)
    df.PETScOptions.set("ksp_max_it", 10_000)
    df.PETScOptions.set("ksp_error_if_not_converged", False)
    df.PETScOptions.set("pc_type", "hypre")
    df.PETScOptions.set("pc_hypre_type", "boomeramg")
    solver.set_from_options()

    V = df.FunctionSpace(mesh, "CG", 1)

    u = df.TrialFunction(V)
    v = df.TestFunction(V)

    a = df.dot(df.grad(u), df.grad(v)) * df.dx
    L = v * df.Constant(1) * df.dx

    apex = df.Function(V)

    base_bc = [
        df.DirichletBC(V, 0, ffun, marker, "topological") for marker in markers['base']
    ]

    # Solver options
    A, b = df.assemble_system(a, L, base_bc)
    solver.set_operator(A)
    solver.solve(apex.vector(), b)

    # Save data 
    # Get reordering of idxs for correct saving
    idxs = df.vertex_to_dof_map(apex.function_space())
    apex_base_solution = apex.vector().get_local()[idxs] #apex is the actual solution
    apex_base_solution=apex_base_solution/np.max(apex_base_solution) #Normalize the apex to base values
    
    if args.insert2Laplacians:
        mesh_laplacians = meshio.read(os.path.join(outPath, "laplacians_{}.vtk".format(args.mesh_name)))
        mesh_laplacians.point_data['base_apex'] = apex_base_solution
        mesh_laplacians.write(os.path.join(outPath, "laplacians_{}.vtk".format(args.mesh_name)))
    else:
        point_data = {}
        point_data['base_apex'] = apex_base_solution
        mesh_new = meshio.Mesh(mesh.coordinates(), [("tetra", list(mesh.cells()))], point_data=point_data)
        mesh_new.write(os.path.join(outPath, "apex_base_{}.vtk".format(args.mesh_name)))
        


if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))
