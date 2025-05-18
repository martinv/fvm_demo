import time
import numpy as np
import math
from gmsh_reader import GmshReader
from gmsh_writer import GmshWriter
from mesh import *
from numerical_flux import AUSM_flux
from mesh_geometry import *


def primitive_to_conservative_vars(
    rho: float, v1: float, v2: float, p: float
) -> np.array:
    gamma = 1.4
    # internal energy
    e = p / (gamma - 1) + 0.5 * rho * (v1 * v1 + v2 * v2)

    return np.array([rho, rho * v1, rho * v2, e])


def outflow_bc(u_in: np.array, u_farfield: np.array, normal: np.array) -> np.array:
    gamma = 1.4
    p = (gamma - 1) * (
        u_in[3] - 0.5 * (u_in[1] * u_in[1] + u_in[2] * u_in[2]) / u_in[0]
    )
    a = math.sqrt(gamma * p / u_in[0])

    v_n = (u_in[1] * normal[0] + u_in[2] * normal[1]) / u_in[0]

    if v_n < 0.0:
        if -v_n > a:
            return u_farfield
        else:
            e = u_in[3]
            return np.array([u_farfield[0], u_farfield[1], u_farfield[2], e])

    else:
        if v_n > a:
            return u_in
        else:
            e = u_farfield[3]
            return np.array([u_in[0], u_in[1], u_in[2], e])


def make_initial_solution(cells_2d: CellGroup, global_coords: np.array) -> np.array:
    # Init state on bottom left
    init_BL = primitive_to_conservative_vars(
        rho=0.1379928, v1=1.2060454, v2=1.2060454, p=0.0290323
    )
    # Init state on bottom right
    init_BR = primitive_to_conservative_vars(
        rho=0.5322581, v1=0.0, v2=1.2060454, p=0.3)
    # Init state on top right
    init_TR = primitive_to_conservative_vars(rho=1.5, v1=0.0, v2=0.0, p=1.5)
    # Init state on top left
    init_TL = primitive_to_conservative_vars(
        rho=0.5322581, v1=1.2060454, v2=0.0, p=0.3)

    num_cells = cells_2d.dof_ids.shape[0]
    init_solution = np.zeros((num_cells, 4))

    for idx_cell in range(num_cells):
        cell_coords = global_entity_coordinates(
            cells_2d.dof_ids[idx_cell, :], cells_2d.ref_elem, global_coords, 2
        )

        cell_center = np.average(cell_coords, axis=0)

        if cell_center[0] <= 0.5 and cell_center[1] <= 0.5:
            init_solution[idx_cell, :] = init_BL
        elif cell_center[0] >= 0.5 >= cell_center[1]:
            init_solution[idx_cell, :] = init_BR
        elif cell_center[0] >= 0.5 and cell_center[1] >= 0.5:
            init_solution[idx_cell, :] = init_TR
        elif cell_center[0] <= 0.5 <= cell_center[1]:
            init_solution[idx_cell, :] = init_TL

    return init_solution


def solution_update(
    U: np.array,
    Res: np.array,
    internal_faces: np.array,
    internal_normals: np.array,
    internal_lengths: np.array,
):
    for idx_face, face in enumerate(internal_faces):
        idx_L = face.adj_cell[0]
        idx_R = face.adj_cell[1]

        u_L = U[idx_L, :]
        u_R = U[idx_R, :]

        flux = AUSM_flux(u_L, u_R, internal_normals[idx_face, :])

        face_len = internal_lengths[idx_face]
        Res[idx_L, :] = Res[idx_L, :] + face_len * flux
        Res[idx_R, :] = Res[idx_R, :] - face_len * flux


def compute_time_step(
    U: np.array,
    global_faces: Dict[str, List[Face]],
    global_normals: Dict[str, np.array],
    global_face_lengths: Dict[str, np.array],
    cell_volumes: np.array,
) -> np.array:
    time_step = np.zeros((U.shape[0]))
    assert len(time_step) == len(cell_volumes)

    gamma = 1.4

    for name, face_list in global_faces.items():
        normal_list = global_normals[name]
        face_len_list = global_face_lengths[name]

        assert len(face_list) == normal_list.shape[0]
        assert normal_list.shape[0] == face_len_list.shape[0]

        for face, normal, face_len in zip(face_list, normal_list, face_len_list):
            idx_L = face.adj_cell[0]
            idx_R = face.adj_cell[1]

            u_L = U[idx_L, :]

            # LEFT STATE
            # pressure
            p_L = (gamma - 1) * (
                u_L[3] - 0.5 * (u_L[1] * u_L[1] + u_L[2] * u_L[2]) / u_L[0]
            )
            # local speed of sound
            a_L = math.sqrt(gamma * p_L / u_L[0])
            # normal speed
            v_L_n = (u_L[1] * normal[0] + u_L[2] * normal[1]) / u_L[0]

            jacobian_spectral_radius = max(
                abs(v_L_n), abs(v_L_n - a_L), abs(v_L_n + a_L)
            )

            time_step[idx_L] = time_step[idx_L] + \
                jacobian_spectral_radius * face_len

            # If right state exists, update it too
            if idx_R > -1:
                u_R = U[idx_R, :]

                # RIGHT STATE
                # pressure
                p_R = (gamma - 1) * (
                    u_R[3] - 0.5 * (u_R[1] * u_R[1] + u_R[2] * u_R[2]) / u_R[0]
                )
                # local speed of sound
                a_R = math.sqrt(gamma * p_R / u_R[0])
                # normal speed
                v_R_n = (u_R[1] * normal[0] + u_R[2] * normal[1]) / u_R[0]

                jacobian_spectral_radius = max(
                    abs(v_R_n), abs(v_R_n - a_R), abs(v_R_n + a_R)
                )

                time_step[idx_R] = (
                    time_step[idx_R] + jacobian_spectral_radius * face_len
                )

    for i in range(len(time_step)):
        time_step[i] = cell_volumes[i] / time_step[i]

    return time_step


if __name__ == "__main__":
    mesh_name = "riemann_square.msh"
    gmsh_reader = GmshReader()
    nodes, cell_groups = gmsh_reader.load(mesh_name)

    mesh = Mesh(cell_groups, nodes)

    num_cells = mesh.cells().dof_ids.shape[0]

    print(f"Solver: number of cells = {num_cells}")

    internal_cells = mesh.cells()

    # Prepare interior faces:
    all_faces = mesh.edges()
    internal_faces = all_faces["inside"]

    # Cell volumes
    cell_vol = cell_volumes(internal_cells, nodes)
    assert cell_vol.shape[0] == num_cells

    # Interior face normals
    all_face_normals = face_normals(all_faces, nodes)
    internal_normals = all_face_normals["inside"]
    assert internal_normals.shape[0] == len(internal_faces)

    # Face lengths
    all_face_lenghts = face_lengths(all_faces, nodes)
    internal_lengths = all_face_lenghts["inside"]
    assert internal_lengths.shape[0] == len(internal_faces)

    # Solution array
    U = make_initial_solution(internal_cells, mesh.node_coordinates())

    # Solver residuals
    Res = np.zeros_like(U)

    simulation_time = 0.0
    max_time = 0.3
    CFL = 0.7
    iter = 0

    start_time = time.time()
    # for iter in range(300):
    while simulation_time < max_time:
        # Process internal faces

        solution_update(U, Res, internal_faces,
                        internal_normals, internal_lengths)

        # Process boundary faces
        for name, face_list in all_faces.items():
            if name == "inside":
                continue

            boundary_normals = all_face_normals[name]
            boundary_face_lenghts = all_face_lenghts[name]

            for idx_face, face in enumerate(face_list):
                idx_L = face.adj_cell[0]
                u_L = U[idx_L, :]

                # flux = AUSM_flux(u_L, u_L, boundary_normals[idx_face, :])

                u_R = outflow_bc(u_L, u_L, boundary_normals[idx_face, :])
                flux = AUSM_flux(u_L, u_R, boundary_normals[idx_face, :])

                face_len = boundary_face_lenghts[idx_face]
                Res[idx_L, :] = Res[idx_L, :] + face_len * flux

        dt_arr = compute_time_step(
            U, all_faces, all_face_normals, all_face_lenghts, cell_vol
        )
        dt = CFL * np.min(dt_arr)

        if simulation_time + dt > max_time:
            dt = max_time - simulation_time + 1.0e-6

        """
        for idx_cell in range(num_cells):
            U[idx_cell, :] = U[idx_cell, :] - dt / cell_vol[idx_cell] * Res[idx_cell]
        """

        time_scale = dt / cell_vol
        time_scale = time_scale[:, np.newaxis]
        U = U - time_scale * Res

        simulation_time = simulation_time + dt
        print(
            f"Iter = {iter}, time = {simulation_time:.5f}, res = {
                np.linalg.norm(Res, axis=0)}"
        )
        iter = iter + 1

        Res[:, :] = 0.0

    end_time = time.time()
    print(f"Computation took {end_time - start_time} seconds")

    gmsh_writer = GmshWriter()
    gmsh_writer.write("riemann_output.msh", nodes, [mesh.cells()])

    gmsh_writer.write_field("riemann_output.msh", U)
