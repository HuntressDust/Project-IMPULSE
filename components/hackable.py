from __future__ import annotations

from operator import truediv
from typing import Optional, TYPE_CHECKING

import actions
import color
from components.base_component import BaseComponent
from components.fighter import Fighter
import components.ai
from exceptions import Impossible
from input_handler import  ActionOrHandler, HackingSelectHandler
import status_effects
if TYPE_CHECKING:
    from entity import Actor

class Hackable(BaseComponent):
    parent: Actor

    def ShortCircuit(self, hacker: Actor):
        damage = 5

        self.parent.fighter.take_damage(damage)
        self.parent.gamemap.engine.message_log.add_message(f"{hacker.name} hacks the {self.parent.name} for {damage} damage")

    def Confuse(self,hacker: Actor):
        self.parent.status.add_effect(status_effects.Confused(target=self.parent, max_time=100,))


    def Blaze(self, hacker: Actor):
        self.parent.status.add_effect(status_effects.Burning(target=self.parent, max_time=100,))

        self.parent.gamemap.engine.message_log.add_message(
            f"{hacker.name} set the {self.parent.name} ON FUCKING FIRE")
