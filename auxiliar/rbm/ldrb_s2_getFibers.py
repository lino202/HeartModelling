# # Creating fibers on a personalized BiV
import dolfin as df
import ldrb
import os
import argparse
import time

def main():
    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument('--dataPath',type=str, required=True, help='path to data')
    parser.add_argument('--addName',type=str, required=True, help='name for Fibers')
    parser.add_argument('--domainType',type=str, required=True, help='BiV (Biventricular) or LV')
    parser.add_argument('--alpha_endo_lv',type=int)
    parser.add_argument('--alpha_epi_lv',type=int)
    parser.add_argument('--alpha_endo_rv',type=int)
    parser.add_argument('--alpha_epi_rv',type=int)
    args = parser.parse_args()

    # Volume Mesh and FacetFunction reading
    mesh = df.Mesh()
    with df.XDMFFile(os.path.join(args.dataPath, "mesh", "mesh.xdmf")) as xdmf:
        xdmf.read(mesh)

    ffun = df.MeshFunction("size_t", mesh, 2)
    with df.XDMFFile(os.path.join(args.dataPath, "mesh", "ffun.xdmf")) as xdmf:
        xdmf.read(ffun)

    markers = ldrb.utils.default_markers()

    # Choose space for the fiber fields
    # This is a string on the form {family}_{degree}
    fiber_space = "Lagrange_1"
    outPath = os.path.join(args.dataPath, "RBM_LDRB")
    if not os.path.exists(outPath): os.mkdir(outPath)

    if args.domainType == "BiV":
        angles = dict(
            alpha_endo_lv=args.alpha_endo_lv,  # Fiber angle on the LV endocardium
            alpha_epi_lv=args.alpha_epi_lv,    # Fiber angle on the LV epicardium
            beta_endo_lv=0,                    # Sheet angle on the LV endocardium
            beta_epi_lv=0,                     # Sheet angle on the LV epicardium
            # alpha_endo_sept=60,              # Fiber angle on the Septum endocardium
            # alpha_epi_sept=-60,              # Fiber angle on the Septum epicardium
            beta_endo_sept=0,                  # Sheet angle on the Septum endocardium
            beta_epi_sept=0,                   # Sheet angle on the Septum epicardium
            alpha_endo_rv=args.alpha_endo_rv,  # Fiber angle on the RV endocardium
            alpha_epi_rv=args.alpha_epi_rv,    # Fiber angle on the RV epicardium
            beta_endo_rv=0,                    # Sheet angle on the RV endocardium
            beta_epi_rv=0
        )
    elif args.domainType == "LV":
        markers.pop("rv", None)
        angles = dict(alpha_endo_lv=args.alpha_endo_lv, alpha_epi_lv=args.alpha_epi_lv, beta_endo_lv=0, beta_epi_lv=0)
    else: raise ValueError("Wrong domainType parameter")


    # Compute the microstructure
    fiber, sheet, sheet_normal = ldrb.dolfin_ldrb(mesh=mesh, fiber_space=fiber_space, ffun=ffun, markers=markers, **angles)

    # Store the results
    with df.HDF5File(mesh.mpi_comm(), os.path.join(outPath, "{}.h5".format(args.domainType)), "w") as h5file:
        h5file.write(fiber, "/fiber")
        h5file.write(sheet, "/sheet")
        h5file.write(sheet_normal, "/sheet_normal")

    # If you run in parallel you should skip the visualisation step and do that in
    # serial in stead. In that case you can read the the functions from the xml
    # Using the following code

    # TODO From here it is unnecessary to reload and re save we can add here the saving of the fsn vector fields
    V = ldrb.space_from_string(fiber_space, mesh, dim=3)

    fiber = df.Function(V)
    sheet = df.Function(V)
    sheet_normal = df.Function(V)

    with df.HDF5File(mesh.mpi_comm(), os.path.join(outPath, "{}.h5".format(args.domainType)), "r") as h5file:
        h5file.read(fiber, "/fiber")
        h5file.read(sheet, "/sheet")
        h5file.read(sheet_normal, "/sheet_normal")

    # You can also store files in XDMF which will also compute the fiber angle as scalars on the glyph to be visualised in Paraview. 
    # Note that these functions don't work (yet) using mpirun
    # (These function are not tested in parallel)
    # Wrong nomenclature by the library. S is normal sheet in Bayer et al and T is transverse which is sheet (s) in other articles/Nico,
    # and T should be more or less radial to the epicardial plane: 
    # Nico/LeGrice "Laminar structure of the heart: ventricular myocyte arrangement and connective tissue architecture in the dog" 
    # and Bayer et al see pictures) 
    ldrb.fiber_to_xdmf(fiber,        os.path.join(outPath,"{}_fiber_{}".format(args.domainType, args.addName)))
    ldrb.fiber_to_xdmf(sheet,        os.path.join(outPath,"{}_sheet_normal_N_{}".format(args.domainType, args.addName)))
    ldrb.fiber_to_xdmf(sheet_normal, os.path.join(outPath,"{}_sheet_S_{}".format(args.domainType, args.addName)))

    #TODO the scalar computation is the angle with respect to z. So if the geometry is not aligned with its LA
    # in x this angle/scalar would not represent the angle put as input correctly

if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))