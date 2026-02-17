from __future__ import annotations

from typing import Iterable, TYPE_CHECKING, Optional, Iterator
import numpy as np
import tcod.los
from tcod.console import Console
from IMPULSE import tile_types
from IMPULSE import color

from IMPULSE.entity import Actor, Item
if TYPE_CHECKING:
    from IMPULSE.engine import Engine
    from IMPULSE.entity import Entity

class GameMap:
    def __init__(
            self, engine: Engine, width: int, height: int, entities: Iterable[Entity]=() ):
        self.engine = engine
        self.width, self.height = width, height
        self.entities = set(entities)
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")
        self.visible = np.full((width, height), fill_value=False, order="F")
        self.explored= np.full((width, height), fill_value=False, order="F")

        self.tiles[30:33,22]=tile_types.wall
        self.downstairs_location = (0,0)
        self.goal_location=(0,0)
    @property
    def gamemap(self) -> GameMap:
        return self

    @property
    def actors(self) -> Iterator[Actor]:
        yield from (entity for entity in self.entities
                    if isinstance(entity,Actor) and entity.is_alive)
    @property
    def items(self) -> Iterator[Item]:
        yield from (entity for entity in self.entities if isinstance(entity, Item))

    def get_blocking_entity_at_location(self, location_x: int, location_y: int) -> Optional[Entity]:
        for entity in self.entities:
            if (
                    entity.blocks_movement
                    and entity.x== location_x
                    and entity.y == location_y
            ):
                return entity
        return None

    def get_actor_at_location(self,x: int, y:int) -> Optional[Actor]:
        for actor in self.actors:
            if actor.x == x and actor.y==y:
                return actor
        return None

    def in_bounds(self, x: int, y:int) -> bool:
        return 0 <= x < self.width and 0<= y < self.height

    def get_actors_between_2_points(self,x0:int, y0: int, x1:int, y1:int) -> Optional[list[Actor]]:
        index_list=(tcod.los.bresenham((x0,y0),(x1,y1)).tolist())[1:-1]
        entity_list=[]

        for index in index_list:
            actor=self.get_actor_at_location(index[0], index[1])
            if actor:
                entity_list.append(actor)
        if len(entity_list)>0:
            print("Detection Successful")
            return entity_list
        else:
            return None




    #from flotsam rl
    def get_viewport(self):
        x=self.engine.player.x
        y=self.engine.player.y
        width=self.engine.game_world.viewport_width
        height=self.engine.game_world.viewport_height
        origin_x = x - int(width /2)
        origin_y = y - int(height/2)

        if origin_x < 0:
            origin_x = 0
        if origin_y <0:
            origin_y = 0

        end_x =  origin_x + width
        end_y = origin_y + height

        if end_x > self.width:
            x_diff = end_x - self.width
            origin_x -= x_diff
            end_x -= x_diff

        if end_y > self.height:
            y_diff = end_y - self.height
            origin_y -= y_diff
            end_y -= y_diff

        offset=int((80-width)/2)
        return ((origin_x, origin_y, end_x-1, end_y-1, offset))

    def render (self, console : Console) -> None:

        #from flotsam rl

        o_x, o_y,e_x,e_y,offset = self.get_viewport()
        s_x =  slice(o_x, e_x+1)
        s_y = slice(o_y, e_y+1)

        viewport_tiles = self.tiles[s_x,s_y]
        viewport_visible = self.visible[s_x,s_y]
        viewport_explored = self.explored[s_x,s_y]



        console.rgb[offset : offset + self.engine.game_world.viewport_width,  1 : self.engine.game_world.viewport_height+1] = np.select(
            condlist=[viewport_visible, viewport_explored],
            choicelist=[viewport_tiles["light"], viewport_tiles["dark"]],
            default=tile_types.SHROUD,
        )
        console.draw_frame(x=offset-1,y=0, width = self.engine.game_world.viewport_width+2,height = self.engine.game_world.viewport_height+2, fg=color.blue, clear=False,)


        entities_sorted_for_rendering = sorted(self.entities, key=lambda x: x.render_order.value)
        for entity in entities_sorted_for_rendering:

            if self.visible[entity.x, entity.y]:
                console.print(x=entity.x-o_x + offset, y=entity.y-o_y+1, string=entity.char, fg=entity.color)



class GameWorld:

    def __init__(
            self,
            *,
            engine: Engine,
            map_width: int,
            map_height: int,
            max_rooms: int,
            room_min_size: int,
            room_max_size: int,
            current_floor: int = 0,
            viewport_width,
            viewport_height
    ):
        self.engine = engine

        self.map_width = map_width
        self.map_height = map_height

        self.max_rooms = max_rooms

        self.room_min_size = room_min_size
        self.room_max_size = room_max_size
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height

        self.current_floor = current_floor

    def generate_floor(self,floor_type: int=0) -> None:
        from IMPULSE.procgen import generate_dungeon
        from IMPULSE.procgen import generate_mall
        from IMPULSE.procgen import generate_BSP
        from IMPULSE.procgen import generate_arena

        self.current_floor +=1
        if floor_type==0:
            self.engine.game_map = generate_dungeon(
            max_rooms=self.max_rooms,
            room_min_size=self.room_min_size,
            room_max_size=self.room_max_size,
            map_width=self.map_width,
            map_height=self.map_height,

            engine=self.engine,
            )
        if floor_type==1:
            self.engine.game_map=generate_mall(
            max_rooms=self.max_rooms,
            room_min_size=5,
            room_max_size=10,
            map_width=70,
            map_height=70,

            engine=self.engine,
            )
        if floor_type==2:
            self.engine.game_map=generate_BSP(
            max_rooms=self.max_rooms,
            room_min_size=5,
            room_max_size=10,
            map_width=70,
            map_height=70,

            engine=self.engine,
            )
        if floor_type==3:
            self.engine.game_map=generate_arena(
                map_width=70,
                map_height=70,
                engine=self.engine
            )