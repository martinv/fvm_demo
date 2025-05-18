from enum import IntEnum


class GmshElemTypeTag(IntEnum):
    """Type tags as defined in Gmsh *.msh file format"""

    LINE_P1 = 1
    TRI_P1 = 2
    QUAD_P1 = 3
