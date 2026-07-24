from enum import auto, Enum

class RenderOrder(Enum):
    CORPSE  = auto()
    TRAP = auto()
    ITEM = auto()
    ACTOR = auto()