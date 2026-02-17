from __future__ import annotations

from typing import Optional, TYPE_CHECKING


from IMPULSE import status_effects


if TYPE_CHECKING:
    from IMPULSE.entity import Actor




class Virus:
    def __init__(self):
        self.wait_time=5
        self.cost=0
        self.name="placeholder"

    def use_fp(self,hacker:Actor,amount: int):
        hacker.fighter.drain_fp(amount)

    def perform(self, hacker: Actor, target: Actor):
        raise NotImplementedError

class vShortCircuit(Virus):
        def __init__(self):
            super().__init__()
            self.damage = 5
            self.cost = 2
            self.name = "Short Circuit"

        def perform(self, hacker: Actor, target: Actor):
            target.fighter.take_damage(self.damage)
            target.gamemap.engine.message_log.add_message(f"{hacker.name} hacks the {target.name} for {self.damage} damage")
            self.use_fp(hacker,self.cost)
            hacker.set_wait_counter(5)


class vConfuse(Virus):
    def __init__(self):
        super().__init__()
        self.name = "Confuse"
        self.cost = 5
    def perform(self, hacker: Actor, target: Actor):
        target.status.add_effect(status_effects.Confused(target=target, max_time=100,))
        target.gamemap.engine.message_log.add_message(
        f"{hacker.name} sends the {target.name} into a haze")
        self.use_fp(hacker,self.cost)
        hacker.set_wait_counter(5)

class vBlaze(Virus):
    def __init__(self):
        super().__init__()
        self.name = "Blaze"
        self.cost=10
        self.max_time = 100

    def perform(self, hacker: Actor, target: Actor):

        target.status.add_effect(status_effects.Burning(target=target, max_time=100,))

        target.gamemap.engine.message_log.add_message(
            f"{hacker.name} set the {target.name} ON FUCKING FIRE")
        self.use_fp(hacker,self.cost)
        hacker.set_wait_counter(5)

class vControl(Virus):
    def __init__(self):
        super().__init__()
        self.name="Control"
        self.cost=12

    def perform(self, hacker: Actor, target: Actor):
        hacker.controller.add_minion(target)
        self.use_fp(hacker,self.cost)
        hacker.set_wait_counter(5)

ShortCirc = vShortCircuit()
Confuse = vConfuse()
Blaze= vBlaze()
Control=vControl()
std_viruses = [ShortCirc,Confuse,Blaze,Control ]