import numpy as np
from typing import Dict, List
from cell_group import CellGroup
from mesh_algorithm import Face, global_entity_coordinates


def cell_volumes(global_dofs: CellGroup, global_coordinates: np.array) -> np.array:
    all_dof_ids = global_dofs.dof_ids
    num_cells = global_dofs.dof_ids.shape[0]

    num_edges_per_elem = global_dofs.ref_elem.num_entities(1)

    volumes = np.zeros(num_cells)

    for idx_cell in range(num_cells):
        cell_dofs = all_dof_ids[idx_cell, :]
        elem_coords = global_entity_coordinates(
            cell_dofs, global_dofs.ref_elem, global_coordinates, 2
        )

        elem_coords_rolled = np.roll(elem_coords, -1, axis=0)
        delta_xy = elem_coords_rolled - elem_coords

        edge_midpoints = 0.5 * (elem_coords_rolled + elem_coords)

        edge_normals = np.zeros_like(delta_xy)

        cell_volume = 0.0
        for i_edge in range(num_edges_per_elem):
            nx = delta_xy[i_edge][1]
            ny = -delta_xy[i_edge][0]
            inv_norm = 1.0 / np.sqrt(nx * nx + ny * ny)

            edge_normals[i_edge, 0] = inv_norm * nx
            edge_normals[i_edge, 1] = inv_norm * ny

            x, y = (
                edge_midpoints[i_edge][0],
                edge_midpoints[i_edge][1],
            )
            cell_volume += 0.5 * (x * nx + y * ny)

        volumes[idx_cell] = cell_volume

    return volumes


def face_normals(
    global_faces: Dict[str, List[Face]], global_coordinates: np.array
) -> Dict[str, np.array]:
    all_face_normals = {}
    for name, face_list in global_faces.items():
        group_normals = np.zeros((len(face_list), 2))

        for idx, face in enumerate(face_list):
            # This returns 2x2 matrix
            # [[x_start, y_start]
            #  [x_end,   y_end]]
            face_pts = global_coordinates[face.dofs, :].squeeze()

            delta_xy = face_pts[1, :] - face_pts[0, :]
            inv_norm = 1.0 / np.sqrt(np.dot(delta_xy, delta_xy))
            # For face [dx, dy], the normals is [dy, -dx]
            group_normals[idx, :] = [inv_norm * delta_xy[1], -inv_norm * delta_xy[0]]

        all_face_normals[name] = group_normals

    return all_face_normals


def face_lengths(
    global_faces: Dict[str, List[Face]], global_coordinates: np.array
) -> Dict[str, np.array]:
    all_face_lengths = {}
    for name, face_list in global_faces.items():
        group_lengths = np.zeros((len(face_list)))

        for idx, face in enumerate(face_list):
            # This returns 2x2 matrix
            # [[x_start, y_start]
            #  [x_end,   y_end]]
            face_pts = global_coordinates[face.dofs, :].squeeze()

            delta_xy = face_pts[1, :] - face_pts[0, :]
            norm = np.linalg.norm(delta_xy)
            # For face [dx, dy], the normals is [dy, -dx]
            group_lengths[idx] = norm

        all_face_lengths[name] = group_lengths

    return all_face_lengths
