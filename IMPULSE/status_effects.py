from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from IMPULSE.components.ai import HostileEnemy, ConfusedEnemy

if TYPE_CHECKING:
    from IMPULSE.entity import Actor

class StatusEffect:
    abrev="placeholder"
    def __init__(self, target: Actor, max_time: int,):
        self.parent=target
        self.max_time= max_time
        self.time_remaining = max_time
        self.orig_char=self.parent.char
        self.orig_color=self.parent.color



    def decrement_timer(self):
        self.time_remaining -=1
    def update(self):
        self.decrement_timer()
        if self.time_remaining>0:
            self.perform()
        else:
            self.on_timer_end()
    def perform(self):
        raise NotImplementedError
    def end_effect(self):
        raise NotImplementedError
    def on_timer_end(self):
        self.end_effect()

class Burning(StatusEffect):
    abrev="BURN"
    def __init__(self, target: Actor,max_time: int, str="BURN"):
        super().__init__(target, max_time)

    def perform(self):
        if self.time_remaining % 15 >0:
            if self.parent.char==self.orig_char:
                self.parent.char='!'
                self.parent.color=(255,0,0)
                self.parent.fighter.take_damage(3)
                self.parent.gamemap.engine.message_log.add_message(f"THE {self.parent.name} IS BURNING!")

            else:
                self.parent.char=self.orig_char
                self.parent.color=self.orig_color


    def end_effect(self):
        self.parent.char =self.orig_char
        self.parent.color=self.orig_color
        self.parent.gamemap.engine.message_log.add_message(f"The {self.parent.name} has been extinguished")

class Confused(StatusEffect):
    abrev="CONF"
    def __init__(self, target: Actor, max_time: int):
        super().__init__(target, max_time)
        self.orig_ai=self.parent.ai

    def perform(self):
        if self.parent.ai is not ConfusedEnemy:
            self.parent.ai=ConfusedEnemy(self.parent)
            self.parent.gamemap.engine.message_log.add_message(f"The {self.parent.name} is disassociating...")

        if self.time_remaining % 15 > 0:
            if self.parent.char == self.orig_char:
                self.parent.char = '?'
                self.parent.color = (255, 0, 255)

    def end_effect(self):
        self.parent.char = self.orig_char
        self.parent.color = self.orig_color
        self.parent.ai=self.orig_ai
        self.parent.gamemap.engine.message_log.add_message(f"The {self.parent.name} has regained its wits")
