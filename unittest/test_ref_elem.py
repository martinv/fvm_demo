from ref_elem import RefElem
from ref_elem_builders import *
from ref_elem_factory import *

class TestReferenceElements:

    def test_ref_elem_line_p1(self):
        elem_factory = RefElemFactory()
        line_p1 = elem_factory.make_elem(ElemShape.LINE, 1)

        assert line_p1.shape() == ElemShape.LINE
        assert line_p1.deg() == 1
        assert line_p1.topo_dim() == 1
        assert line_p1.num_dofs() == 2

        assert line_p1.num_entities(0) == 0
        assert line_p1.num_entities(1) == 1
        assert line_p1.num_entities(2) == 0
        assert line_p1.num_entities(3) == 0

        entity_1d = line_p1.entity(1, 0)
        assert entity_1d == TopologicalEntity(elem_shape=ElemShape.LINE, degree=1, dofs=np.array([0,1]))

        assert np.array_equal(line_p1.coordinates(), np.array([[-1.0], [1.0]]))

    def test_ref_elem_tri_p1(self):
        elem_factory = RefElemFactory()
        tri_p1 = elem_factory.make_elem(ElemShape.TRI, 1)

        assert tri_p1.shape() == ElemShape.TRI
        assert tri_p1.deg() == 1
        assert tri_p1.topo_dim() == 2
        assert tri_p1.num_dofs() == 3

        assert tri_p1.num_entities(0) == 0
        assert tri_p1.num_entities(1) == 3
        assert tri_p1.num_entities(2) == 1
        assert tri_p1.num_entities(3) == 0

        entity_1d_a = tri_p1.entity(1, 0)
        assert entity_1d_a == TopologicalEntity(elem_shape=ElemShape.LINE, degree=1, dofs=np.array([0,1]))

        entity_1d_b = tri_p1.entity(1, 1)
        assert entity_1d_b == TopologicalEntity(elem_shape=ElemShape.LINE, degree=1, dofs=np.array([1,2]))

        entity_1d_c = tri_p1.entity(1, 2)
        assert entity_1d_c == TopologicalEntity(elem_shape=ElemShape.LINE, degree=1, dofs=np.array([2,0]))

        entity_2d = tri_p1.entity(2, 0)
        assert entity_2d == TopologicalEntity(elem_shape=ElemShape.TRI, degree=1, dofs=np.array([0,1,2]))

        assert np.array_equal(tri_p1.coordinates(), np.array([[-1.0,-1.0], [1.0,-1.0], [-1.0,1.0]]))

    def test_ref_elem_quad_p1(self):
        elem_factory = RefElemFactory()
        quad_p1 = elem_factory.make_elem(ElemShape.QUAD, 1)

        assert quad_p1.shape() == ElemShape.QUAD
        assert quad_p1.deg() == 1
        assert quad_p1.topo_dim() == 2
        assert quad_p1.num_dofs() == 4

        assert quad_p1.num_entities(0) == 0
        assert quad_p1.num_entities(1) == 4
        assert quad_p1.num_entities(2) == 1
        assert quad_p1.num_entities(3) == 0

        entity_1d_a = quad_p1.entity(1, 0)
        assert entity_1d_a == TopologicalEntity(elem_shape=ElemShape.LINE, degree=1, dofs=np.array([0,1]))

        entity_1d_b = quad_p1.entity(1, 1)
        assert entity_1d_b == TopologicalEntity(elem_shape=ElemShape.LINE, degree=1, dofs=np.array([1,2]))

        entity_1d_c = quad_p1.entity(1, 2)
        assert entity_1d_c == TopologicalEntity(elem_shape=ElemShape.LINE, degree=1, dofs=np.array([2,3]))

        entity_1d_d = quad_p1.entity(1, 3)
        assert entity_1d_d == TopologicalEntity(elem_shape=ElemShape.LINE, degree=1, dofs=np.array([3,0]))

        entity_2d = quad_p1.entity(2, 0)
        assert entity_2d == TopologicalEntity(elem_shape=ElemShape.QUAD, degree=1, dofs=np.array([0,1,2,3]))

        assert np.array_equal(quad_p1.coordinates(), np.array([[-1.0,-1.0], [1.0,-1.0], [1.0,1.0], [-1.0,1.0]]))
