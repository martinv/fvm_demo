import numpy as np

from mesh_algorithm import Face, build_faces
from cell_group import CellGroup


class Mesh:
    """Holds all data to represent a mesh as a geometric support of a simulation"""

    def __init__(self, cell_groups: list[CellGroup], node_coords: np.array):
        self.__cells_2d = [
            cell_group
            for cell_group in cell_groups
            if cell_group.ref_elem.topo_dim() == 2
        ]
        assert len(self.__cells_2d) == 1

        cells_1d = [
            cell_group
            for cell_group in cell_groups
            if cell_group.ref_elem.topo_dim() == 1
        ]

        self.__edges = build_faces(self.__cells_2d[0], cells_1d)
        self.__node_coords = node_coords

    def node_coordinates(self) -> np.array:
        return self.__node_coords

    def cells(self) -> CellGroup:
        return self.__cells_2d[0]

    def edges(self) -> dict[str, list[Face]]:
        return self.__edges

    def print_info(self):
        """Print information about cells in the mesh"""
        print("> 2D cell groups:")
        for cell_group in self.__cells_2d:
            print(f" :: {cell_group.name} -> reference element {cell_group.ref_elem}")

        print(f" > {self.__node_coords.shape[0]} nodes\n")

        print("> Edge lists:")
        for name, entity_list in self.__edges.items():
            print(f"  [{name}]")
            for entity in entity_list:
                print(f"    {entity}")
