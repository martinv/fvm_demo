from typing import List
import numpy as np
from gmsh_elem import GmshElem
from ref_elem import RefElem
from ref_elem_factory import RefElemFactory
from elem_shape import ElemShape
from cell_group import CellGroup


class GmshReader:
    """Class to read finite element mesh in Gmsh format"""

    __sections = {
        "$MeshFormat": "$EndMeshFormat",
        "$PhysicalNames": "$EndPhysicalNames",
        "$Entities": "$EndEntities",
        "$Nodes": "$EndNodes",
        "$Elements": "$EndElements",
    }

    def __init__(self):
        pass

    def load(self, mesh_file_name: str):
        """Read mesh from file in Gmsh file format."""
        with open(mesh_file_name, encoding="utf-8") as infile:
            phys_sections = None
            nodes = None
            cell_groups = None

            line = infile.readline().strip()

            while line:
                if line in GmshReader.__sections:
                    section_data = []
                    section_start = line
                    section_stop = GmshReader.__sections[section_start]
                    line = infile.readline().strip()

                    while line and line != section_stop:
                        section_data.append(line)
                        line = infile.readline().strip()

                    match section_start:
                        case "$PhysicalNames":
                            phys_sections = GmshReader.__read_physical_names_section(
                                section_data
                            )
                        case "$Nodes":
                            nodes = GmshReader.__read_nodes_section(section_data)
                        case "$Elements":
                            cell_groups = GmshReader.__read_elements_section(
                                section_data
                            )

                else:
                    line = infile.readline().strip()

            assert phys_sections is not None
            assert nodes is not None
            assert cell_groups is not None

            for cg in cell_groups:
                for section in phys_sections:
                    if cg.ref_elem.topo_dim() == section[0] and cg.tag == section[1]:
                        cg.name = section[2]

            return nodes, cell_groups

    @classmethod
    def __read_physical_names_section(
        cls, data: List[str]
    ) -> List[tuple[int, int, str]]:
        """Take list of strings representing all lines in 'PhysicalNames' section
        and process it. Return a list of tuples
        (dimension, physical entity index, physical entity name)
        """
        num_entities = int(data[0])
        assert (num_entities + 1) == len(data)
        phys_sections = []
        for line in data[1:]:
            tmp_values = line.split()
            assert len(tmp_values) == 3
            dim = int(tmp_values[0])
            phys_id = int(tmp_values[1])
            phys_name = tmp_values[2].strip('"').rstrip('"')
            phys_sections.append((dim, phys_id, phys_name))
        return phys_sections

    @classmethod
    def __read_nodes_section(cls, data: List[str]) -> np.array:
        """
        number-of-nodes
        node-number x-coord y-coord z-coord
        """
        num_nodes = int(data[0])
        nodes = np.zeros((num_nodes, 3), dtype=float)

        data_pos = 1

        for _ in range(num_nodes):
            tmp_data = data[data_pos].split()
            assert len(tmp_data) == 4

            node_idx = int(tmp_data[0]) - 1

            nodes[node_idx][0] = float(tmp_data[1])
            nodes[node_idx][1] = float(tmp_data[2])
            nodes[node_idx][2] = float(tmp_data[3])

            data_pos = data_pos + 1
            # Ignore z-coordinate, code is 2d only
        return nodes[:, 0:2]

    @classmethod
    def __read_elements_section(cls, data: List[str]) -> List[CellGroup]:
        """
        number-of-elements
        elm-number elm-type number-of-tags < tag > … node-number-list
        """
        num_elems = int(data[0])

        # Maps physical tag to a list of all dofs of all elements
        # in this physical group
        phys_group_elem_dofs = {}

        # Maps physical tag to element type in this physical group
        # We assume one element type per physical group
        phys_group_elem_types = {}

        for eidx in range(1, num_elems + 1):
            tmp_data = data[eidx].split()

            gmsh_elem_type = int(tmp_data[1])
            num_elem_tags = int(tmp_data[2])
            elem_phys_tag = int(tmp_data[3])

            if elem_phys_tag not in phys_group_elem_dofs:
                phys_group_elem_dofs[elem_phys_tag] = []
                phys_group_elem_types[elem_phys_tag] = []

            for id in tmp_data[3 + num_elem_tags :]:
                phys_group_elem_dofs[elem_phys_tag].append(int(id) - 1)

            phys_group_elem_types[elem_phys_tag].append(int(gmsh_elem_type))

        connectivity_data = []
        ref_elem_factory = RefElemFactory()

        for phys_tag in phys_group_elem_dofs.keys():
            # Assume all elements are of the same type
            gmsh_elem_type = phys_group_elem_types[phys_tag][0]
            gmsh_elem = GmshElem(gmsh_elem_type)

            ref_elem = ref_elem_factory.make_elem(gmsh_elem.shape(), gmsh_elem.degree())
            # FIXME: do this via reference element
            all_elem_dofs_in_group = phys_group_elem_dofs[phys_tag]
            all_elem_types_in_group = phys_group_elem_types[phys_tag]
            num_dof_in_elem = int(
                len(all_elem_dofs_in_group) / len(all_elem_types_in_group)
            )

            elems = np.array(all_elem_dofs_in_group, dtype=int)
            elems = np.reshape(elems, (len(all_elem_types_in_group), num_dof_in_elem))

            cell_group = CellGroup(ref_elem, elems, phys_tag, "")

            connectivity_data.append(cell_group)

        return connectivity_data
