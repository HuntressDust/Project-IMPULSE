from __future__ import annotations
from typing import Optional, TYPE_CHECKING, Tuple

from IMPULSE.components.base_component import BaseComponent
from IMPULSE.equipment_types import EquipmentType
import IMPULSE.components.inventory


if TYPE_CHECKING:
    from IMPULSE.entity import Actor, Item

class Magazine(BaseComponent):
    parent: Item
    def __init__(self, loaded: Optional[Item] = None ):
        self.loaded=loaded

    def is_loaded(self):
        return getattr(self,"loaded") is not None

    def unload(self):
        setattr(self,'loaded',None)

    def load_message(self, rounds_name: str, gun_name: str):
        self.parent.gamemap.engine.message_log.add_message(
            f"You load {rounds_name} into the {gun_name}")

    def rounds_left(self):
        return self.loaded.amount

    def load_rounds(self, rounds: Item, add_message: bool=True):

        setattr(self, 'loaded', rounds)

        if add_message:
            self.load_message(rounds.name, self.parent.name)
