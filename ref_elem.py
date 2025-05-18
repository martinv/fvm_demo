from typing import List
from elem_shape import ElemShape
from topological_entity import TopologicalEntity


class RefElem:
    def __init__(self, ref_elem_builder):
        self.__shape = ref_elem_builder.shape()
        self.__deg = ref_elem_builder.deg()
        self.__dim = ref_elem_builder.topo_dim()
        self.__entities = ref_elem_builder.entities()
        self.__coordinates = ref_elem_builder.coordinates()

    def shape(self) -> ElemShape:
        return self.__shape

    def deg(self) -> int:
        return self.__deg

    def topo_dim(self) -> int:
        return self.__dim

    def num_dofs(self) -> int:
        topological_entity = self.__entities[self.__dim][0]
        return topological_entity.dofs.shape[0]

    def num_entities(self, dim) -> int:
        return len(self.__entities[dim])

    def entity(self, dim: int, index: int) -> TopologicalEntity:
        return self.__entities[dim][index]

    def entities(self, dim: int) -> List[TopologicalEntity]:
        return self.__entities[dim]

    def coordinates(self):
        return self.__coordinates

    def __str__(self) -> str:
        return self.__shape.name + '_P' + str(self.__deg)
