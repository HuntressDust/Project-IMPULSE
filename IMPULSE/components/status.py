from __future__ import annotations
from typing import Optional, TYPE_CHECKING

from IMPULSE.status_effects import StatusEffect
from IMPULSE import actions
from IMPULSE import color
from IMPULSE.components.base_component import BaseComponent
from IMPULSE.components.fighter import Fighter
from IMPULSE.components import ai
from IMPULSE.exceptions import Impossible
from IMPULSE.input_handler import  ActionOrHandler, HackingSelectHandler
if TYPE_CHECKING:
    from IMPULSE.entity import Actor

class Status(BaseComponent):
    parent:Actor
    def __init__(self):
        self.effects=list()

    def add_effect(self, effect: StatusEffect):
        self.effects.append(effect)

    def update_effects(self):
        for effect in self.effects:

            effect.update()
            if effect.time_remaining<0:
                self.effects.remove(effect)

    def is_healthy(self):
        return len(self.effects)==0


