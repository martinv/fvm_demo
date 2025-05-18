from abc import ABC, abstractmethod
from typing import List
import numpy as np
from topological_entity import TopologicalEntity
from elem_shape import ElemShape


class RefElemBuilderBase(ABC):
    def __init__(self, shape: ElemShape, deg: int):
        self.__shape = shape
        self.__deg = deg

    def shape(self) -> ElemShape:
        """ Return element shape """
        return self.__shape

    def deg(self) -> int:
        """ Return element degree (interpolation order)"""
        return self.__deg

    @abstractmethod
    def topo_dim(self) -> int:
        """ Return topological dimension of element, regardless of order"""
        pass

    @abstractmethod
    def num_entities(self, dim) -> int:
        """ Number of entities of given dimension. 
            Example: the number of 1D entities in triangle is 3, because a triangle has 3 edges
                     the nubmer of 2D entities in a cube is 6 (faces) and the number of
                     1D entities in a cube is 12 (edges)
        """
        pass

    @abstractmethod
    def entities(self) -> List[List[TopologicalEntity]]:
        """ Return all entities of all dimensions that this element is composed of"""
        pass

    @abstractmethod
    def coordinates(self) -> np.array:
        """ Node coordinates """
        pass

    def __str__(self) -> str:
        return self.__shape.name + '_P' + str(self.__deg)


class RefElemBuilderLineP1(RefElemBuilderBase):
    def __init__(self):
        """ Constructor """
        super().__init__(ElemShape.LINE, 1)

        entities_1d = [TopologicalEntity(ElemShape.LINE, 1, np.array([0, 1]))]
        entities_2d = []
        entities_3d = []
        self.__entities = [[], entities_1d, entities_2d, entities_3d]

    def topo_dim(self) -> int:
        """ Return topological dimension of element """
        return 1

    def num_entities(self, dim) -> int:
        """ Return number of entities of given dimension. For triangle for example,
            the number of 1D entities (edges) = 3
        """
        return len(self.__entities[dim])

    def entities(self) -> List[List[TopologicalEntity]]:
        return self.__entities

    def coordinates(self):
        return np.array([[-1.0], [1.0]], dtype=float)


class RefElemBuilderTriP1(RefElemBuilderBase):
    def __init__(self):
        """ Constructor """
        super().__init__(ElemShape.TRI, 1)

        entities_1d = [TopologicalEntity(ElemShape.LINE, 1, np.array([0, 1])),
                       TopologicalEntity(ElemShape.LINE, 1, np.array([1, 2])),
                       TopologicalEntity(ElemShape.LINE, 1, np.array([2, 0]))]
        entities_2d = [TopologicalEntity(ElemShape.TRI, 1, np.array([0, 1, 2]))]
        entities_3d = []
        self.__entities = [[], entities_1d, entities_2d, entities_3d]

    def topo_dim(self) -> int:
        """ Return topological dimension of element """
        return 2

    def num_entities(self, dim) -> int:
        """ Return number of entities of given dimension. For triangle for example,
            the number of 1D entities (edges) = 3
        """
        return len(self.__entities[dim])

    def entities(self) -> List[List[TopologicalEntity]]:
        return self.__entities

    def coordinates(self):
        return np.array([[-1.0, -1.0], [1.0, -1.0], [-1.0, 1.0]], dtype=float)


class RefElemBuilderQuadP1(RefElemBuilderBase):
    def __init__(self):
        """ Constructor """
        super().__init__(ElemShape.QUAD, 1)

        entities_1d = [TopologicalEntity(ElemShape.LINE, 1, np.array([0, 1])),
                       TopologicalEntity(ElemShape.LINE, 1, np.array([1, 2])),
                       TopologicalEntity(ElemShape.LINE, 1, np.array([2, 3])),
                       TopologicalEntity(ElemShape.LINE, 1, np.array([3, 0]))]
        entities_2d = [TopologicalEntity(ElemShape.QUAD, 1, np.array([0, 1, 2, 3]))]
        entities_3d = []
        self.__entities = [[], entities_1d, entities_2d, entities_3d]

    def topo_dim(self) -> int:
        """ Return topological dimension of element """
        return 2

    def num_entities(self, dim) -> int:
        """ Return number of entities of given dimension. For triangle for example,
            the number of 1D entities (edges) = 3
        """
        return len(self.__entities[dim])

    def entities(self) -> List[List[TopologicalEntity]]:
        return self.__entities

    def coordinates(self):
        return np.array([[-1.0, -1.0], [1.0, -1.0], [1.0, 1.0], [-1.0, 1.0]], dtype=float)
