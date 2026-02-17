from __future__ import annotations
from typing import TYPE_CHECKING, Tuple



from IMPULSE import color

if TYPE_CHECKING:
    from tcod import Console
    from IMPULSE.engine import Engine
    from IMPULSE.game_map import GameMap

def get_names_at_location(x: int, y: int, game_map: GameMap) -> str:

    if not game_map.in_bounds(x, y) or not game_map.visible[x, y]:
        return ""

    names = ", ".join(
        entity.name for entity in game_map.entities if entity.x == x and entity.y == y
    )

    return names.capitalize()


def render_bars(
        console: Console, current_hp: int, maximum_hp : int, current_fp: int, maximum_fp: int, total_width : int, name: str
) -> None:
    bar_width_hp = int(float(current_hp)/ maximum_hp*total_width)

    console.print(
        x=0, y=44, string=name,fg=color.white
    )
    console.draw_rect(x=0, y = 45, width = total_width, height =1, ch =1, bg=color.bar_empty)

    if bar_width_hp>0:
        console.draw_rect(
            x=0, y=45, width = bar_width_hp, height=1, ch=1, bg=color.bar_filled
        )

    console.print(
        x=1, y=45, string=f"HP: {current_hp}/{maximum_hp}", fg=color.bar_text

    )
    try:
        bar_width_fp = int(float(current_fp) / maximum_fp * total_width)
        if bar_width_fp>0:
            console.draw_rect(
                x=0, y=47, width = bar_width_fp, height=1, ch=1, bg=color.ally
            )

        console.print(
            x=1, y=47, string=f"FP: {current_fp}/{maximum_fp}", fg=color.bar_text)
    except:
        pass

def render_dungeon_level(
    console: Console, dungeon_level: int, location: Tuple[int, int]
) -> None:
    """
    Render the level the player is currently on, at the given location.
    """
    x, y = location

    console.print(x=x, y=y, string=f"Dungeon level: {dungeon_level}")


def render_names_at_mouse_location(
        console: Console, x: int, y: int, engine: Engine) -> None:
    mouse_x, mouse_y =engine.mouse_gameTile


    names_at_mouse_location = get_names_at_location(x=mouse_x,y=mouse_y,game_map=engine.game_map)

    console.print(x=x, y=y, string=names_at_mouse_location)

def render_coords(console: Console, x: int, y: int, engine: Engine) -> None:
    mouse_x, mouse_y = engine.mouse_gameTile
    mouse_x_1, mouse_y_1 = engine.mouse_location
    console.print(x=x, y=y, string=f"Location in Map: {mouse_x}, {mouse_y}")
    console.print(x=x, y=y+1, string=f"Location in Window: {mouse_x_1}, {mouse_y_1}")

def render_danger_box(console: Console, x: int, y: int, engine: Engine, radius: int, on: bool) -> None:
    if on:
        console.draw_frame(
            x=x - radius - 1,
            y=y - radius - 1,
            width=radius ** 2,
            height=radius ** 2,
            fg=color.red,
            clear=False,
        )