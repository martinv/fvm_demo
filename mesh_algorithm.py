import numpy as np
from ref_elem import RefElem
from cell_group import CellGroup


class Face:
    """Class representing interface between two elements"""

    def __init__(self, adj_cell: list[int], dofs: list[int]):
        """Construct a face from adjacent cell indices and degrees of freedom on the interface"""
        self.adj_cell = adj_cell
        self.dofs = dofs

    def __str__(self):
        return f"Face  [{self.adj_cell[0]}, {self.adj_cell[1]}]  ({self.dofs[0]}, {self.dofs[1]})"


def face_nodes_match_inverse(face_l: Face, face_r: Face) -> bool:
    """
    Check if the the faces as seen from two different elements match.
    They should list their dofs in reverse order
    """
    return (face_l.dofs[0] == face_r.dofs[1]) and (face_l.dofs[1] == face_r.dofs[0])


def face_nodes_match(face_l: Face, face_r: Face) -> bool:
    """Check if the the faces as seen from two different elements match."""
    return (face_l.dofs[0] == face_r.dofs[0]) and (face_l.dofs[1] == face_r.dofs[1])


def global_entity_dofs(
    global_dofs: np.array, ref_elem: RefElem, dim: int
) -> list[np.array]:
    """Return global degrees of freedom for sub-entities of one element
    global_dofs ... degrees of freedom on ONE element
    ref_elem ... reference element (describes topology of one element and decomposition
                                    into sub-entities)
    dim ... dimension of sub-entities to extract
    """
    entity_dofs = [
        global_dofs[topo_entity.dofs] for topo_entity in ref_elem.entities(dim)
    ]
    return entity_dofs


def global_entity_coordinates(
    global_dofs: np.array, ref_elem: RefElem, global_coords: np.array, dim: int
) -> list[np.array]:
    entity_dofs = global_entity_dofs(global_dofs, ref_elem, dim)
    entity_coords = global_coords[entity_dofs].squeeze()
    return entity_coords


def build_faces(
    cells_2d: CellGroup, cells_1d: list[CellGroup]
) -> dict[str, list[Face]]:
    dofs2d = cells_2d.dof_ids
    num_cells2d = dofs2d.shape[0]

    tmp_faces = {}

    for idx_cell in range(num_cells2d):
        global_cell_dofs = dofs2d[idx_cell, :]
        global_edge_dofs = global_entity_dofs(global_cell_dofs, cells_2d.ref_elem, 1)

        for dof_pair in global_edge_dofs:
            face = Face(adj_cell=[idx_cell, -1], dofs=[dof_pair[0], dof_pair[1]])

            search_dof_key = min(face.dofs)
            if search_dof_key not in tmp_faces:
                tmp_faces[search_dof_key] = []

            match_found = False
            for j in range(len(tmp_faces[search_dof_key])):
                if face_nodes_match_inverse(tmp_faces[search_dof_key][j], face):
                    tmp_faces[search_dof_key][j].adj_cell[1] = idx_cell
                    match_found = True

            if not match_found:
                tmp_faces[search_dof_key].append(face)

    # Count internal faces:
    internal_faces = []
    for _, face_list in tmp_faces.items():
        for face in face_list:
            if face.adj_cell[0] >= 0 and face.adj_cell[1] >= 0:
                internal_faces.append(face)

    """
    print(f'Number of internal faces = {len(internal_faces)}')

    for key, face_list in tmp_faces.items():
        print(f'KEY {key + 1}')
        for face in face_list:
            print(f'    ({face.adj_cell[0]+1}, {face.adj_cell[1]+1})'
                    f' => nodes [{face.dofs[0]+1}, {face.dofs[1]+1}]')
    """

    face_dict = {cells_2d.name: internal_faces}

    # Detect boundary faces
    for cell_grp_1d in cells_1d:
        dofs1d = cell_grp_1d.dof_ids
        num_cells1d = dofs1d.shape[0]

        face_list_1d = []

        for idx_cell in range(num_cells1d):
            global_edge_dofs = global_entity_dofs(
                dofs1d[idx_cell, :], cell_grp_1d.ref_elem, 1
            )

            assert len(global_edge_dofs) == 1
            face = Face(adj_cell=[-1, -1], dofs=global_edge_dofs[0])

            search_dof_key = min(face.dofs)

            for j in range(len(tmp_faces[search_dof_key])):
                if face_nodes_match(tmp_faces[search_dof_key][j], face):
                    face.adj_cell[0] = tmp_faces[search_dof_key][j].adj_cell[0]
                    face_list_1d.append(face)
                    break

        face_dict[cell_grp_1d.name] = face_list_1d

    return face_dict
