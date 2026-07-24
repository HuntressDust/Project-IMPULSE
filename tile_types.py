from typing import Tuple
import numpy as np
from IMPULSE import color

graphic_dt=np.dtype(
    [
        ("ch", np.int32),
        ("fg", "3B"),
        ("bg", "3B"),
    ]
)

tile_dt = np.dtype(
    [
        ("walkable", np.bool),
        ("transparent", np.bool),
        ("dark",graphic_dt),
        ("light", graphic_dt)
    ]
)

def new_tile(
        *,
        walkable: int,
        transparent: int,
        dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
        light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],

)  -> np.ndarray:
    return np.array((walkable, transparent, dark, light), dtype=tile_dt)



SHROUD = np.array((ord(" "), (255, 255, 255), (0,0,0)), dtype = graphic_dt)
floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), (50, 50, 50)),
    light=(ord(" "), (255, 255, 255), color.floor),
)
wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord(" "), (255, 255, 255), (20, 20, 50)),
    light=(ord(" "), (255, 255, 255), (50, 50, 80))
)
down_stairs = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(">"), (0, 0, 100), (50, 50, 50)),
    light=(ord(">"), (255, 255, 255), (20, 20, 80)),
)
goal=new_tile(
    walkable=True,
    transparent=True,
    dark=(ord("v"), (0, 0, 100), (50, 50, 150)),
    light=(ord("v"), (255, 143, 178), (0, 188, 255)),
)

medbay=new_tile(
    walkable=True,
    transparent=True,
    dark=(ord("X"), (100, 0, 0), (0, 100, 0)),
    light=(ord("X"), (255, 0, 0), (0, 255, 0)),
)
usedMedbay=new_tile(
    walkable=True,
    transparent=True,
    dark=(ord("X"), (50, 0, 0), (0, 50, 0)),
    light=(ord("X"), (100, 0, 0), (0, 100, 0)),
)

