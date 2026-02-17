from __future__ import  annotations
from typing import TYPE_CHECKING

from IMPULSE import exceptions
import lzma
import pickle
from tcod.console import Console
from tcod.map import compute_fov

from IMPULSE import render_functions

from IMPULSE.message_log import MessageLog
if TYPE_CHECKING:
    from IMPULSE.entity import Actor
    from IMPULSE.game_map import GameMap, GameWorld


class Engine:
    game_map: GameMap
    game_world: GameWorld
    def save_as(self, filename: str)-> None:
        save_data=lzma.compress(pickle.dumps(self))
        with open(filename, "wb") as f:
            f.write(save_data)

    def __init__(self, player: Actor):
        self.player = player
        self.mouse_location = (0,0)
        self.mouse_gameTile=(0,0)
        self.message_log = MessageLog()
        self.danger_x=0
        self.danger_y=0
        self.danger_rad=0
        self.danger_on=False
        self.game_win=False

    def handle_enemy_turns(self)-> None:
        for entity in set(self.game_map.actors) - {self.player}:
               if entity.ai:
                   entity.status.update_effects()
                   if entity.can_act() and entity.is_alive:
                       try:
                           entity.ai.perform()
                       except exceptions.Impossible:
                           pass
                   else:
                        entity.decrement_wait_counter()

    def update_fov(self) -> None:
        radius =8
        if self.player.cyberware.has_los_perk:
            radius+=2
        self.game_map.visible[:]= compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius = radius    ,
        )
        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console,) -> None:
        self.game_map.render(console)
        viewport=self.game_map.get_viewport()
        self.mouse_gameTile=(self.mouse_location[0]+viewport[0]-viewport[4], self.mouse_location[1]+viewport[1]-1)

        self.message_log.render(console=console, x=21, y=45, width=40, height=5)

        render_functions.render_bars(console=console,
                   current_hp=self.player.fighter.hp,
                   maximum_hp=self.player.fighter.max_hp,
                   current_fp=self.player.fighter.fp,
                   maximum_fp=self.player.fighter.max_fp,
                   total_width=20,
                   name=self.player.name
                   )

        render_functions.render_dungeon_level(console=console, dungeon_level=self.game_world.current_floor, location=(0,49))
        render_functions.render_names_at_mouse_location(console=console, x=21, y=44, engine=self)
        render_functions.render_coords(console=console, x=21, y=42, engine=self)
        render_functions.render_danger_box(console=console, x=self.danger_x, y=self.danger_y, engine=self, radius=self.danger_rad, on=self.danger_on)

