from __future__ import annotations
import copy
import math
from typing import  Tuple, TypeVar, TYPE_CHECKING, Optional, Type, Union

from IMPULSE.components.cyberware import Cyberware
from render_order import RenderOrder

if TYPE_CHECKING:
    from components.ai import BaseAI
    from components.fighter import Fighter
    from components.equipment import Equipment
    from components.equippable import Equippable
    from components.cyberware import Cyberware
    from components.bodymod import BodyMod
    from components.consumable import Consumable
    from components.inventory import Inventory
    from components.bodymod import BodyPart
    from components.level import Level
    from components.hackable import Hackable
    from components.status import Status
    from game_map import GameMap


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
        render_order: RenderOrder = RenderOrder.CORPSE,
    ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        self.render_order = render_order
        if parent:
            # If parent isn't provided now then it will be set later.
            self.parent = parent
            parent.entities.add(self)

    @property
    def gamemap(self) -> GameMap:
        return self.parent.gamemap

    def spawn(self: T, gamemap: GameMap, x: int, y: int) -> T:
        """Spawn a copy of this instance at the given location."""
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.parent = gamemap
        gamemap.entities.add(clone)
        return clone

    def place(self, x: int, y: int, gamemap: Optional[GameMap] = None) -> None:
        """Place this entitiy at a new location.  Handles moving across GameMaps."""
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
        equipment: Equipment,
        fighter: Fighter,
        inventory: Inventory,
        status: Status,
        cyberware: Optional[Cyberware]=None,
        level: Level,
        hackable: Optional[Hackable] =None
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=True,
            render_order=RenderOrder.ACTOR,
        )

        self.ai: Optional[BaseAI] = ai_cls(self)

        self.fighter = fighter
        self.fighter.parent = self

        self.inventory = inventory
        self.inventory.parent = self
        self.equipment: Equipment = equipment
        if cyberware is not None:
            self.cyberware=cyberware
            self.cyberware.parent=self
        if hackable is not None:
            self.hackable=hackable
            self.hackable.parent=self
        self.status=status
        self.status.parent=self
        self.equipment.parent = self
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
        consumable: Optional[Consumable]=None,
        equippable: Optional[Equippable]= None,
        bodymod: Optional[BodyMod]=None,
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=False,
            render_order=RenderOrder.ITEM,
        )

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
