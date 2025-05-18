from typing import List
from cell_group import CellGroup
from gmsh_elem import *

import numpy as np


class GmshWriter:

    def __init__(self):
        pass

    def write(self, filename: str, nodes: np.array, cells: List[CellGroup]):
        with open(filename, 'w') as outfile:
            GmshWriter.__write_header(outfile)
            GmshWriter.__write_physical_names(outfile, cells)
            GmshWriter.__write_node_coordinates(outfile, nodes, cells)
            GmshWriter.__write_elem_connectivity(outfile, cells)

    def write_field(self, filename: str, cell_data: np.array):
        with open(filename, 'a') as outfile:
            GmshWriter.__append_cell_data(outfile, cell_data)

    @classmethod
    def __write_header(cls, outfile):
        outfile.write('$MeshFormat\n')
        outfile.write('2.2 0 8\n')
        outfile.write('$EndMeshFormat\n')

    @classmethod
    def __write_physical_names(cls, outfile, cells: List[CellGroup]):
        outfile.write('$PhysicalNames\n')

        phys_entities = []
        for dim in (1, 2):
            tmp_entity_info = [(dim, cgroup.tag, cgroup.name) for cgroup in cells if cgroup.ref_elem.topo_dim() == dim]
            phys_entities.extend(tmp_entity_info)

        outfile.write(f'{len(phys_entities)}\n')
        for (dim, tag, name) in phys_entities:
            outfile.write(f'{dim} {tag} \"{name}\"\n')

        outfile.write('$EndPhysicalNames\n')

    @classmethod
    def __write_node_coordinates(cls, outfile, nodes: np.array, cells: List[CellGroup]):
        outfile.write('$Nodes\n')

        num_nodes = nodes.shape[0]
        # numEntityBlocks numNodes minNodeTag maxNodeTag
        outfile.write(f'{num_nodes}\n')

        for node_id in range(num_nodes):

            outfile.write(str(node_id + 1))
            node_coords = nodes[node_id][:]
            for v in node_coords:
                outfile.write(f' {str(v)}')
            outfile.write(' 0.0\n')

        outfile.write('$EndNodes\n')

    @classmethod
    def __write_elem_connectivity(cls, outfile, cells: List[CellGroup]):
        outfile.write('$Elements\n')
        num_elems = 0
        for cell_group in cells:
            num_elems += cell_group.dof_ids.shape[0]

        outfile.write(f'{num_elems}\n')

        elem_idx = 1
        for cell_group in cells:
            gmsh_elem = gmsh_elem_from_shape_and_deg(cell_group.ref_elem.shape(),
                                                     cell_group.ref_elem.deg())

            gmsh_elem_type = gmsh_elem.elem_type_tag().value
            # Physical and elementary tag
            tags = (cell_group.tag, cell_group.tag)
            num_tags = len(tags)

            for cell in cell_group.dof_ids:
                outfile.write(f'{str(elem_idx)} {str(gmsh_elem_type)} {str(num_tags)}')
                for tag in tags:
                    outfile.write(f' {str(tag)}')

                for id in cell:
                    outfile.write(f' {str(id + 1)}')
                elem_idx += 1
                outfile.write('\n')

        outfile.write('$EndElements\n')

    @classmethod
    def __append_cell_data(cls, outfile, cell_data: np.array):
        n_cells = cell_data.shape[0]
        n_components = cell_data.shape[1]
        for component in range(n_components):
            outfile.write('$ElementData\n')
            # number-of-string-tags
            outfile.write('1\n')
            outfile.write(f'\"data_0{str(component)}\"\n')
            # number-of-real-tags
            outfile.write('1\n0.0\n')
            # number-of-integer-tags
            # time step index, number of components in view, number of cells
            outfile.write('3\n0\n1\n')
            outfile.write(f'{n_cells}\n')
            for i in range(n_cells):
                outfile.write(f'{i + 1} {cell_data[i][component]}\n')
            outfile.write('$EndElementData\n')
