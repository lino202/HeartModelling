import meshio
import numpy as np
import time
import argparse


def create_1d_cardiac_fiber(
    length: float,
    dx: float,
    endo_pct: float,
    mid_pct: float,
    epi_pct: float,
    filename: str = "cardiac_fiber_1d.vtu",
):
    """Generates a 1D line mesh with transmural cardiac tags (Endo, Mid, Epi)

    and exports it for ParaView.

    Parameters:
    - length: Total length of the fiber (e.g., in mm or cm)
    - dx: Desired element resolution (length of each line segment)
    - endo_pct, mid_pct, epi_pct: Layer percentages (must sum to 100)
    - filename: Output mesh file (.vtu, .vtk, .msh, etc.)
    """

    FEC_flag = 2
    endo_flag = 3
    mid_flag = 4
    epi_flag = 5
    # 1. Validate percentages
    if not np.isclose(endo_pct + mid_pct + epi_pct, 100.0):
        raise ValueError(
            f"Percentages must sum to 100. Current sum: {endo_pct + mid_pct + epi_pct}"
        )

    # 2. Calculate number of elements and nodes
    num_elements = int(np.round(length / dx))
    actual_dx = length / num_elements
    if not np.isclose(dx, actual_dx):
        print(
            f"Note: Adjusted element size from {dx} to {actual_dx:.5f} to fit total length {length}."
        )

    num_nodes = num_elements + 1

    # 3. Create 3D coordinates (VTK/ParaView requires 3D points even for 1D meshes)
    x = np.linspace(0.0, length, num_nodes)
    points = np.column_stack((x, np.zeros(num_nodes), np.zeros(num_nodes)))

    # 4. Create 1D line element connectivity: [[0, 1], [1, 2], ..., [N-1, N]]
    cells = [("line", np.column_stack((np.arange(num_elements), np.arange(1, num_nodes))))]

    # 5. Assign transmural layer tags based on element midpoints
    # Tags: 1 = Endocardium, 2 = Midmyocardium, 3 = Epicardium
    element_midpoints = 0.5 * (x[:-1] + x[1:])
    endo_limit = length * (endo_pct / 100.0)
    mid_limit = length * ((endo_pct + mid_pct) / 100.0)

    tags = np.zeros(num_elements, dtype=np.int32)
    tags[element_midpoints <= endo_limit] = endo_flag
    tags[(element_midpoints > endo_limit) & (element_midpoints <= mid_limit)] = mid_flag
    tags[element_midpoints > mid_limit] = epi_flag

    # 6. Build and write the mesh using meshio
    mesh = meshio.Mesh(
        points=points,
        cells=cells,
        cell_data={"transmural_layer": [tags]},
    )
    mesh.write(filename)

    print(f"Mesh saved to '{filename}'")
    print(
        f"Total elements: {num_elements} | Endo (1): {np.sum(tags == 1)}, "
        f"Mid (2): {np.sum(tags == 2)}, Epi (3): {np.sum(tags == 3)}"
    )
    return mesh

def main ():

    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument('--fibre_length',        type=float, required=True, help='Length of the fiber in mm')
    parser.add_argument('--fibre_resolution',    type=float, required=True, help='Resolution of the fiber in mm (edgelength)')
    parser.add_argument('--endo_percentage',   type=float, default=40.0, help='Percentage of the fiber that is endocardium')
    parser.add_argument('--epi_percentage',   type=float, default=25.0, help='Percentage of the fiber that is epicardium')
    parser.add_argument('--out_path', type=str)
    # parser.add_argument('--groundPointData', action='store_true', help='To choose a ground point for bidomain simulations')
    
    # parser.add_argument('--save' ,action='store_true',  help='save histogram tags')
    
    args = parser.parse_args()

    # endo_per = 40; endo_per = endo_per /100
    # epi_per = 25; epi_per = epi_per /100


    create_1d_cardiac_fiber(
        length=args.fibre_length,
        dx=args.fibre_resolution,
        endo_pct=args.endo_percentage,
        mid_pct=100-args.epi_percentage-args.endo_percentage,
        epi_pct=args.epi_percentage,
        filename=args.out_path,
    )



if __name__ == "__main__":

    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))
    # Example: 10 mm transmural wedge, 0.1 mm resolution
    # 30% Endocardium, 40% Midmyocardium, 30% Epicardium
    