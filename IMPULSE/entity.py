from __future__ import annotations
import copy
import math
import tcod
import numpy as np
from typing import  Tuple, TypeVar, TYPE_CHECKING, Optional, Type, Union,List

from IMPULSE.damage_types import DamageType
from IMPULSE.description import Description, default_description
from IMPULSE.render_order import RenderOrder

if TYPE_CHECKING:
    from IMPULSE.components.ai import BaseAI
    from IMPULSE.components.fighter import Fighter
    from IMPULSE.components.equipment import Equipment
    from IMPULSE.components.equippable import Equippable
    from IMPULSE.components.cyberware import Cyberware
    from IMPULSE.components.bodymod import BodyMod
    from IMPULSE.components.consumable import Consumable
    from IMPULSE.components.inventory import Inventory
    from IMPULSE.components.level import Level
    from IMPULSE.components.status import Status
    from IMPULSE.game_map import GameMap
    from IMPULSE.components.controller import Controller

    from IMPULSE.components.hacker import Hacker


T= TypeVar("T", bound="Entity")


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """

    parent: Union[GameMap, Inventory]

    def __init__(
        self,
        parent: Optional[GameMap] = None,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        blocks_movement: bool = False,
        desc : Description = default_description,
        render_order: RenderOrder = RenderOrder.CORPSE,
    ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        self.render_order = render_order
        self.description=desc
        if parent:
            # If parent isn't provided now then it will be set later.
            self.parent = parent
            parent.entities.add(self)

    @property
    def gamemap(self) -> GameMap:
        return self.parent.gamemap

    def spawn(self: T, gamemap: GameMap, x: int, y: int) -> T:
        """Spawn a copy of this instance at the given location."""

        if not self.is_tile_valid(x, y, gamemap):
            tile = self.find_close_tile(x, y, gamemap)
            x = tile[0]
            y = tile[1]

        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.parent = gamemap
        gamemap.entities.add(clone)
        return clone




    def is_tile_valid(self,x:int, y:int, gamemap:GameMap):
        tile=gamemap.tiles[x,y]
        if tile["walkable"]:
            if gamemap.get_actor_at_location(x,y) is None:
                return True
        return False


    def find_close_tile(self,x,y,  gamemap:GameMap,perimeter: int =0, tile: Optional[List]=None, pathmin: int=0):

        cost = np.array(gamemap.tiles["walkable"], dtype = np.int8)
        for entity in gamemap.entities:
            if entity.blocks_movement and cost[entity.x, entity.y]:
                cost[entity.x, entity.y] += 10
        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pathfinder = tcod.path.Pathfinder(graph)

        pathfinder.add_root((x, y))



        pathlist=np.array([])
        tile_list=list()


        if perimeter<3:

            for i in range(-1-perimeter,2+perimeter):
                for j in list([-1-perimeter,1+perimeter]):

                    dest_x=x+i
                    dest_y=y+j
                    print(dest_x, dest_y)
                    if self.is_tile_valid(dest_x, dest_y, gamemap):
                        print("is valid")
                        path: List[List[int]] = pathfinder.path_to((dest_x, dest_y))[1:].tolist()

                        pathcost = len(path)
                        print("pathlength", pathcost)
                        if pathcost == 0:
                            return [dest_x, dest_y]
                        pathlist=np.append(pathlist, pathcost)
                        tile_list.append([dest_x, dest_y])

            for j in range(0-perimeter,1+perimeter):
                for i in list([-1-perimeter,1+perimeter]):
                    dest_x = x + i
                    dest_y = y + j
                    print(dest_x,dest_y)
                    if self.is_tile_valid(dest_x, dest_y, gamemap):
                        print("is valid")
                        path: List[List[int]] = pathfinder.path_to((dest_x, dest_y))[1:].tolist()

                        pathcost = len(path)
                        print("pathlength", pathcost)
                        if pathcost == 0:
                            return [dest_x, dest_y]
                        pathlist = np.append(pathlist, pathcost)
                        tile_list.append([dest_x, dest_y])


            try:
                min_ind=np.argmin(pathlist, axis=0)[0]
            except:
                min_ind=np.argmin(pathlist)

            minimum=pathlist[min_ind]
            tile_min=tile_list[min_ind]
            if minimum>perimeter+1:
                if tile_min<tile:
                    tile_min=tile
                tile=self.find_close_tile(x,y,gamemap,perimeter+1,tile=tile_min, pathmin=minimum)
                return tile
            else:
                return tile_min
        else:
            return tile



    def place(self, x: int, y: int, gamemap: Optional[GameMap] = None) -> None:
        """Place this entitiy at a new location.  Handles moving across GameMaps."""

        if not self.is_tile_valid(x, y, gamemap):
            tile = self.find_close_tile(x, y, gamemap)
            x = tile[0]
            y = tile[1]

        self.x = x
        self.y = y
        if gamemap:
            if hasattr(self, "parent"):  # Possibly uninitialized.
                if self.parent is self.gamemap:
                    self.gamemap.entities.remove(self)
            self.parent = gamemap
            gamemap.entities.add(self)

    def distance(self, x: int, y: int) -> float:
        """
        Return the distance between the current entity and the given (x, y) coordinate.
        """
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def move(self, dx: int, dy: int) -> None:
        # Move the entity by a given amount
        self.x += dx
        self.y += dy



class Actor(Entity):
    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        ai_cls: Type[BaseAI],
        equipment: Optional[Equipment]=None,
        fighter: Fighter,
        inventory: Inventory,
        status: Status,
        cyberware: Optional[Cyberware]=None,
        level: Level,
        hacker: Optional[Hacker] =None,
        controller: Optional[Controller]= None,
        damage_type: DamageType= DamageType.KINETIC,
        desc: Description= default_description,
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=True,
            render_order=RenderOrder.ACTOR,
            desc=desc
        )

        self.ai: Optional[BaseAI] = ai_cls(self)
        if self.ai is not None:
            self.orig_ai=self.ai

        self.fighter = fighter
        self.fighter.parent = self

        self.inventory = inventory
        self.inventory.parent = self
        self.damage_type=damage_type

        if equipment is not None:
            self.equipment=equipment
            self.equipment.parent=self
        if cyberware is not None:
            self.cyberware=cyberware
            self.cyberware.parent=self
        if hacker is not None:
            self.hacker=hacker
            self.hacker.parent=self
        if controller is not None:
            self.controller = controller
            self.controller.parent = self


        self.status=status
        self.status.parent=self
        self.level = level
        self.level.parent = self
        self.wait_turns=0

    @property
    def is_alive(self) -> bool:
        """Returns True as long as this actor can perform actions."""
        return bool(self.ai)
    def is_hackable(self) -> bool:
        return hasattr(self, "hackable")
    def can_act(self) -> bool:
        if self.wait_turns < 0:
            self.wait_turns = 0

        return( self.wait_turns == 0)

    def set_wait_counter(self, turns) -> None:
        self.wait_turns=turns

    def decrement_wait_counter(self) -> None:
        self.wait_turns = self.wait_turns-1

class Item(Entity):
    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        damage_type="",
        consumable: Optional[Consumable]=None,
        equippable: Optional[Equippable]= None,
        bodymod: Optional[BodyMod]=None,
        desc: Description= default_description,
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=False,
            render_order=RenderOrder.ITEM,
            desc=desc
        )
        self.damage_type=damage_type
        self.consumable = consumable
        if self.consumable:
            self.consumable.parent=self

        self.equippable = equippable
        if self.equippable:
            self.equippable.parent=self

        self.bodymod = bodymod
        if self.bodymod:
            self.bodymod.parent = self

class Trap(Entity):
    def __init__(self,
    *,
    x: int=0,
    y: int =0,
    char: str = '?',
    color: Tuple[int, int, int] = (255, 255, 255),
    name: str = "<Unnamed>"):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=False,
            render_order=RenderOrder.TRAP,
        )

class Station(Entity):

    def __init__(self,
    *,
    x: int=0,
    y: int =0,
    char: str = '?',
    color: Tuple[int, int, int] = (255, 255, 255),
    isStation: bool = True,
    name: str = "<Unnamed>"):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=False,
            render_order=RenderOrder.STATION,
        )

        self.isStation = True
