from enum import IntEnum


class Dimension(IntEnum):
    """Enumeration to describe topological dimension of mesh elements"""

    _0D = 0
    _1D = 1
    _2D = 2
    _3D = 3


class Orientation(IntEnum):
    """Orientation of face normals"""

    LEFT = 0
    RIGHT = 1
