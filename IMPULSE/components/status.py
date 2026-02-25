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
        self.power_bonus=0
        self.reflex_bonus=0
        self.focus_bonus=0
        self.HP_bonus=0
        self.FP_bonus=0
        self.dodge_bonus=0

    def add_effect(self, new_effect: StatusEffect):
        try:
            for effect in self.effects:
                if effect.abrev == new_effect.abrev:
                    raise Impossible("Cannot stack the same status effect")
            self.effects.append(new_effect)
        except:
            pass

    def update_effects(self):
        for effect in self.effects:

            effect.update()
            if effect.time_remaining<0:
                self.effects.remove(effect)

    def is_healthy(self):
        return len(self.effects)==0


