from __future__ import annotations

from typing import Optional, TYPE_CHECKING



if TYPE_CHECKING:
    from entity import Actor

class StatusEffect:

    def __init__(self, target: Actor, max_time: int):
        self.parent=target
        self.max_time= max_time
        self.time_remaining = max_time
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
    def __init__(self, target: Actor,max_time: int):
        super().__init__(target, max_time)
        self.orig_char=self.parent.char
        self.orig_color=self.parent.color

    def perform(self):
        print(self.time_remaining)
        if self.time_remaining % 15 >0:
            if self.parent.char==self.orig_char:
                self.parent.char='!'
                self.parent.color=(0,0,0)

            else:
                self.parent.char=self.orig_char
                self.parent.color=self.orig_color

            self.parent.fighter.take_damage(1)
            self.parent.gamemap.engine.message_log.add_message(f"THE {self.parent.name} IS BURNING")


    def end_effect(self):
        self.parent.char =self.orig_char
        self.parent.color=self.orig_color