from enum import auto, Enum

class RenderOrder(Enum):
    CORPSE  = auto()
    TRAP = auto()
    STATION = auto()
    ITEM = auto()
    ACTOR = auto()