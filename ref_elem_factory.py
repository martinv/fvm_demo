from ref_elem import RefElem
from ref_elem_builders import *
from elem_shape import ElemShape


class RefElemFactory:

    @classmethod
    def __make_elem_line_p1(cls):
        return RefElemBuilderLineP1()

    @classmethod
    def __make_elem_tri_p1(cls):
        return RefElemBuilderTriP1()

    @classmethod
    def __make_elem_quad_p1(cls):
        return RefElemBuilderQuadP1()

    def __init__(self):
        self.__elem_creators = {(ElemShape.LINE, 1): RefElemFactory.__make_elem_line_p1,
                                (ElemShape.TRI, 1): RefElemFactory.__make_elem_tri_p1,
                                (ElemShape.QUAD, 1): RefElemFactory.__make_elem_quad_p1}

    def make_elem(self, shape: ElemShape, degree: int) -> RefElem:
        elem_key = (shape, degree)
        assert elem_key in self.__elem_creators.keys()

        ref_elem_builder = self.__elem_creators[elem_key]()

        ref_elem = RefElem(ref_elem_builder)

        return ref_elem


if __name__ == '__main__':
    tri = RefElemBuilderTriP1()
    print(tri.entity(dim=1, index=0))
    print(tri.entity(dim=1, index=1))
    print(tri.entity(dim=1, index=2))
    print(tri.num_entities(dim=2))
    print(tri.entity(dim=2, index=0))

    elem_factory = RefElemFactory()
    line_p1 = elem_factory.make_elem(ElemShape.LINE, 1)
    print(f'Line p1: shape = {line_p1.shape()}, deg = {line_p1.deg()}, dim = {line_p1.topo_dim()}')
