from gmsh_elem_type_tag import GmshElemTypeTag
from elem_shape import ElemShape


class GmshElem:
    """Description of element according to Gmsh conventions"""

    __ELEM_SHAPES = {
        GmshElemTypeTag.LINE_P1: ElemShape.LINE,
        GmshElemTypeTag.TRI_P1: ElemShape.TRI,
        GmshElemTypeTag.QUAD_P1: ElemShape.QUAD,
    }

    __ELEM_NODES = {
        GmshElemTypeTag.LINE_P1: 2,
        GmshElemTypeTag.TRI_P1: 3,
        GmshElemTypeTag.QUAD_P1: 4,
    }

    __DEGREE = {
        GmshElemTypeTag.LINE_P1: 1,
        GmshElemTypeTag.TRI_P1: 1,
        GmshElemTypeTag.QUAD_P1: 1,
    }

    def __init__(self, elem_type_tag: GmshElemTypeTag):
        self.__type_tag = elem_type_tag

    def elem_type_tag(self) -> GmshElemTypeTag:
        """Return type tag following Gmsh conventions."""
        return self.__type_tag

    def shape(self) -> ElemShape:
        """Get element shape."""
        return GmshElem.__ELEM_SHAPES[self.__type_tag]

    def degree(self) -> int:
        """Polynomial degree of this element."""
        return GmshElem.__DEGREE[self.__type_tag]

    def num_local_nodes(self) -> int:
        """Number of local nodes (degrees of freedom) in element."""
        return GmshElem.__ELEM_NODES[self.__type_tag]


def gmsh_elem_from_shape_and_deg(shape: ElemShape, degree: int) -> GmshElem:
    """Given element shape and degree, construct corresponding Gmsh element representation"""
    # Map between internal element description (elem shape, elem degree)
    # and gmsh element types
    gmsh_elem_type = {
        (ElemShape.LINE, 1): GmshElemTypeTag.LINE_P1,
        (ElemShape.TRI, 1): GmshElemTypeTag.TRI_P1,
        (ElemShape.QUAD, 1): GmshElemTypeTag.QUAD_P1,
    }

    gmsh_tag = gmsh_elem_type[(shape, degree)]
    return GmshElem(gmsh_tag)
