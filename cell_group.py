import numpy as np
from ref_elem import RefElem


class CellGroup:
    """Describes a group of mesh elements with the same element type"""

    def __init__(
        self,
        ref_elem: RefElem = None,
        dof_ids: np.array = None,
        tag: int = None,
        name: str = None,
    ):
        self.ref_elem = ref_elem
        self.dof_ids = dof_ids
        self.tag = tag
        self.name = name

    def print(self):
        print(f"Cell group with ref elem {self.ref_elem}")
        print(f" >>> tag =  {self.tag}")
        print(f" >>> name = {self.name}")
        print(f" >>> dof_ids =\n {self.dof_ids}\n\n")
