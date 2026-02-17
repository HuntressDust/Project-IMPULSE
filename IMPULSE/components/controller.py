from __future__ import annotations
from typing import Optional, TYPE_CHECKING, Tuple

from IMPULSE.components.base_component import BaseComponent
from IMPULSE.components.ai import Ally
from IMPULSE.exceptions import Impossible

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
                f"You have bound the {target.name} to your will")
        else:
            self.parent.gamemap.engine.message_log.add_message(f"Your psyche cannot handle the strain of controlling another mind!")

    def release_minion(self, target: Actor):
        if target.is_alive:
            target.ai=target.orig_ai
            self.parent.gamemap.engine.message_log.add_message(
                f"The mind of the {target.name} has slipped from your grasp")
        self.minion_list.remove(target)

    def release_all(self):
       if len(self.minion_list)>0:
            self.release_minion(self.minion_list[0])
            self.release_all()


    def set_minion_limit(self, limit: int):
        self.minion_limit=0

    def is_actor_controlled(self, target: Actor) -> bool:
        return target in self.minion_list