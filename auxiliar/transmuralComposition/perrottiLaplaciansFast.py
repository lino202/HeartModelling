""""Here we apply Regional segmentation of ventricular models to achieve
repolarization dispersion in cardiac electrophysiology modeling
L. E. Perotti1,2,3 , S. Krishnamoorthi1, N. P. Borgstrom2 ,
D. B. Ennis2,3 and W. S. Klug1,*,†
"""

import dolfin as df
import ldrb
import os
import argparse
import time
import meshio

def main():
    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument('--dataPath',type=str, required=True, help='path to data')
    args = parser.parse_args()

    outPath = os.path.join(args.dataPath, 'layers')
    if not os.path.isdir(outPath): os.mkdir(outPath)

    # Volume Mesh and FacetFunction reading
    mesh = df.Mesh()
    with df.XDMFFile(os.path.join(args.dataPath, "mesh", "mesh.xdmf")) as xdmf:
        xdmf.read(mesh)

    ffun = df.MeshFunction("size_t", mesh, 2)
    with df.XDMFFile(os.path.join(args.dataPath, "mesh", "ffun.xdmf")) as xdmf:
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

    # Find the rest of the laplace solutions
    V = df.FunctionSpace(mesh, "CG", 1)
    u = df.TrialFunction(V)
    v = df.TestFunction(V)

    a = df.dot(df.grad(u), df.grad(v)) * df.dx
    L = v * df.Constant(0) * df.dx

    cases = ['lv', 'rv', 'xv']
    solutions = dict((what, df.Function(V)) for what in cases)

    # Iterate over the three different cases
    df.info("Solving Laplace equation")

    for case in cases:

        # Solve linear system
        if case == 'rv':
            df.info("rv = -1;  lv, epi = 1")
            bcs = [
                df.DirichletBC(V, -1, ffun, markers['rv'][0],  "topological"),
                df.DirichletBC(V, 1,  ffun, markers['lv'][0],  "topological"),
                df.DirichletBC(V, 1,  ffun, markers['epi'][0], "topological"),
            ]
        elif case == 'lv':
            df.info("lv = -1;  rv, epi = 1")
            bcs = [
                df.DirichletBC(V, 1,  ffun, markers['rv'][0],  "topological"),
                df.DirichletBC(V, -1, ffun, markers['lv'][0],  "topological"),
                df.DirichletBC(V, 1,  ffun, markers['epi'][0], "topological"),
            ]
        elif case == 'xv':
            df.info("lv, rv = -1;  epi = 1")
            bcs = [
                df.DirichletBC(V, -1, ffun, markers['rv'][0],  "topological"),
                df.DirichletBC(V, -1, ffun, markers['lv'][0],  "topological"),
                df.DirichletBC(V, 1,  ffun, markers['epi'][0], "topological"),
            ]
        else:
            raise ValueError("Wrong case!!")

        A, b = df.assemble_system(a, L, bcs)
        solver.set_operator(A)
        solver.solve(solutions[case].vector(), b)

    # Save data 
    point_data = {}
    idxs = df.vertex_to_dof_map(solutions['rv'].function_space())
    point_data['rv'] = solutions['rv'].vector().get_local()[idxs]
    point_data['lv'] = solutions['lv'].vector().get_local()[idxs]
    point_data['xv'] = solutions['xv'].vector().get_local()[idxs]

    mesh_new = meshio.Mesh(mesh.coordinates(), [("tetra", list(mesh.cells()))], point_data=point_data)
    mesh_new.write(os.path.join(outPath, "laplacians.vtk"))


if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))
