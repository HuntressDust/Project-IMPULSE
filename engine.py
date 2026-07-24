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
        self.danger_boxes = {}
        self.danger_on=False
        self.game_win=False
        self.game_over=False
        self.playername=player.name
        self.playercolor=player.color

    def handle_enemy_turns(self)-> None:
        if self.player.is_alive:
            self.player.status.update_effects()
        for entity in set(self.game_map.actors) - {self.player}:
               if entity.ai:
                   entity.status.update_effects()
                   if entity.can_act() and entity.is_alive:
                       try:
                            if entity.get_team=="Friendly":
                                self.player.controller.update_minions()
                            entity.ai.perform()
                       except exceptions.Impossible:
                           pass
                   else:
                        entity.decrement_wait_counter()

    def update_fov(self) -> None:
        radius =8
        self.game_map.visible[:]= compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius = radius    ,
        )
        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console,) -> None:
        self.game_map.render_tiles(console)
        for actor,radius in zip(self.danger_boxes.keys(), self.danger_boxes.values()):
            console_x= actor.x - self.game_map.get_viewport()[0] + self.game_map.get_viewport()[4]
            console_y = actor.y - self.game_map.get_viewport()[1] + 1
            render_functions.render_danger_box(console=console,x=console_x,y=console_y,radius=radius)

        self.game_map.render_entities(console,self.player.cyberware.has_los_perk)
        viewport=self.game_map.get_viewport()
        self.mouse_gameTile=(self.mouse_location[0]+viewport[0]-viewport[4], self.mouse_location[1]+viewport[1]-1)

        self.message_log.render(console=console, x=21, y=42, width=40, height=8)

        render_functions.render_bars(console=console,
                   current_hp=self.player.fighter.hp,
                   maximum_hp=self.player.fighter.max_hp,
                   current_fp=self.player.fighter.fp,
                   maximum_fp=self.player.fighter.max_fp,
                   total_width=20,
                   name=self.player.name
                   )


        render_functions.render_dungeon_level(console=console, dungeon_level=self.game_world.current_floor, location=(0,49))
        render_functions.render_names_at_mouse_location(console=console, x=21, y=40, engine=self)
        #render_functions.render_coords(console=console, x=21, y=42, engine=self)


    def add_danger_box(self, radius: int, actor: Actor):
        self.danger_boxes.update({actor: radius})
    def remove_danger_box(self, actor: Actor):
        try:
            self.danger_boxes.pop(actor)
        except:
            return