from dataclasses import dataclass
import numpy as np
from elem_shape import ElemShape


@dataclass(frozen=True)
class TopologicalEntity:
    elem_shape: ElemShape
    degree: int
    dofs: np.array

    def __str__(self):
        return f'[{self.elem_shape.name}, deg={self.degree},  dofs={self.dofs}]'

    def __eq__(self, other):
        return (self.elem_shape == other.elem_shape) and \
               (self.degree == other.degree) and np.array_equal(self.dofs,other.dofs)
