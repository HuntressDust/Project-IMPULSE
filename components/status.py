from __future__ import annotations
from typing import Optional, TYPE_CHECKING

from IMPULSE.status_effects import StatusEffect,Euphoria,Dysphoria
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
        self.defense_bonus=0

    def add_effect(self, new_effect: StatusEffect):
        skip = False
        if isinstance(new_effect,Dysphoria):
            if hasattr(self.parent,'cyberware'):
                if self.parent.cyberware.has_euphoric_perk:
                    skip=True

        if not skip:
            try:
                for effect in self.effects:
                    if effect.abrev == new_effect.abrev:
                        raise Impossible("Cannot stack the same status effect")
                self.effects.append(new_effect)
                print(f"New effect: {self.effects[-1].abrev}")

            except:
                pass

    def update_effects(self):
        if self.parent is self.engine.player:
            if self.parent.cyberware.has_euphoric_perk:
                if not self.has_effects("EUPH"):
                    self.add_effect(Euphoria(self.parent,10,True))

        for effect in self.effects:
            if self.parent.is_alive:

                effect_running = effect.update()
                if not effect_running:
                    self.effects.remove(effect)
            else:
                self.effects.remove(effect)
    def is_healthy(self):
        return len(self.effects)==0

    def has_effects(self, abrev):
        for effect in self.effects:
            if effect.abrev == abrev:
                return True
        return False


