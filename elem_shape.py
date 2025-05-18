from enum import IntEnum


class ElemShape(IntEnum):
    """Eneration of element shapes that constitute a mesh"""

    LINE = 1
    TRI = 2
    QUAD = 3
