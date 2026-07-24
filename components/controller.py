from __future__ import annotations
from typing import Optional, TYPE_CHECKING, Tuple

from IMPULSE.components.base_component import BaseComponent
from IMPULSE.components.ai import Ally
from IMPULSE import color
from IMPULSE.exceptions import Impossible
import random

if TYPE_CHECKING:
    from IMPULSE.entity import Actor

class Controller(BaseComponent):
    parent:Actor
    def __init__(self,  limit: int=2):
        self.minion_list=list()
        self.limit=limit

    @property
    def minion_limit(self) -> int:
        limit=self.limit
        if self.parent.fighter.focus>9:
            limit+=1
        if self.parent.cyberware.has_control_perk:
            limit+=2
        return limit

    def num_minions(self):
        return len(self.minion_list)
    def add_minion(self, target: Actor):
        if len(self.minion_list)<self.minion_limit:
            self.minion_list.append(target)
            target.ai = Ally(target)
            self.parent.gamemap.engine.message_log.add_message(
                f"You have bound the {target.name} to your will.",color.ally)
        else:
            self.parent.gamemap.engine.message_log.add_message(f"Your psyche cannot handle the strain of controlling another mind!",color.impossible)

    def release_minion(self, target: Actor):
        if target.is_alive:
            target.ai=target.orig_ai
            self.parent.gamemap.engine.message_log.add_message(
                f"The mind of the {target.name} has slipped from your grasp.",color.enemy_atk)
        self.minion_list.remove(target)

    def release_all(self):
       if len(self.minion_list)>0:
            self.release_minion(self.minion_list[0])
            self.release_all()


    def set_minion_limit(self, limit: int):
        self.limit=0

    def is_actor_controlled(self, target: Actor) -> bool:
        return target in self.minion_list

    def update_minions(self):

        for minion in self.minion_list:
            if minion.can_act():
                focus_diff = self.parent.fighter.focus-minion.fighter.focus
                if minion.char!='d':
                    if focus_diff>0:
                        if random.randint(0,5+(5*focus_diff))==0:
                            self.parent.gamemap.engine.message_log.add_message(
                                f"The {minion.name} struggles against your control!", color.enemy_atk)
                            self.parent.fighter.drain_fp(1)

                    else:
                        if random.randint(0,9+focus_diff)==0:
                            self.release_minion(minion)

        if self.parent.fighter.fp<1:
            self.release_all()
