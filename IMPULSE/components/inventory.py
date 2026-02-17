from __future__ import annotations

from typing import  List, TYPE_CHECKING

from tcod.sdl.mouse import capture

from IMPULSE.components.base_component import BaseComponent

if TYPE_CHECKING:
    from IMPULSE.entity import Actor, Item

class Inventory(BaseComponent):
    parent: Actor

    def __init__(self, capacity: int):
        self.cap = capacity
        self.items: List[Item] =[]

    @property
    def capacity(self)-> int:
        capacity=self.cap
        if self.parent.cyberware.has_carry_perk:
            capacity+=6
        return capacity
    def drop(self, item: Item) -> None:

        self.items.remove(item)
        item.place(self.parent.x, self.parent.y, self.gamemap)

        self.engine.message_log.add_message(f"You Dropped the Freakin {item.name}!")
