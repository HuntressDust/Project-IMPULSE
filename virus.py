from __future__ import annotations

import random
from typing import Optional, TYPE_CHECKING
from IMPULSE import color
from IMPULSE import status_effects
from IMPULSE.damage_types import DamageType

if TYPE_CHECKING:
    from IMPULSE.entity import Actor




class Virus:
    def __init__(self):
        self.wait_time=5
        self.cost=0
        self.name="placeholder"

    def use_fp(self,hacker:Actor):
        hacker.fighter.drain_fp(self.cost)

    def perform(self, hacker: Actor, target: Actor):
        raise NotImplementedError

class vShortCircuit(Virus):
        def __init__(self):
            super().__init__()
            self.damage = 5
            self.cost = 3
            self.name = "Short_Circuit.bin"

        def perform(self, hacker: Actor, target: Actor):
            damage=target.fighter.calculate_damage(self.damage,DamageType.SHOCK)
            target.gamemap.engine.message_log.add_message(f"The cyberware in {target.name} overloads and deals {damage} damage!")
            target.fighter.apply_damage(damage)
            self.use_fp(hacker)
            hacker.set_wait_counter(5)


class vConfuse(Virus):
    def __init__(self):
        super().__init__()
        self.name = "Overstim.exe"
        self.cost = 5
    def perform(self, hacker: Actor, target: Actor):
        target.status.add_effect(status_effects.Confused(target=target, max_time=100,))
        target.gamemap.engine.message_log.add_message(
        f"{hacker.name} sends the {target.name} into a haze")
        self.use_fp(hacker)
        hacker.set_wait_counter(5)

class vBlaze(Virus):
    def __init__(self):
        super().__init__()
        self.name = "Blaze"
        self.cost=8
        self.max_time = 100

    def perform(self, hacker: Actor, target: Actor):

        target.status.add_effect(status_effects.Burning(target=target,))

        target.gamemap.engine.message_log.add_message(
            f"{hacker.name} set the {target.name} ON FUCKING FIRE")
        self.use_fp(hacker)
        hacker.set_wait_counter(5)

class vControl(Virus):
    def __init__(self):
        super().__init__()
        self.name="XxPuppetxX"
        self.cost=9

    def perform(self, hacker: Actor, target: Actor):
        hacker.controller.add_minion(target)
        self.use_fp(hacker)
        hacker.set_wait_counter(5)

class vTarget(Virus):
    def __init__(self):
        super().__init__()
        self.name = "Lock-On"
        self.cost=10
        self.max_time = 100

class vOverheat(Virus):
    def __init__(self):
        super().__init__()
        self.name = "Overheat.config"
        self.cost=10
        self.damage=8

    def perform(self, hacker: Actor, target: Actor):
        damage = target.fighter.calculate_damage(self.damage, DamageType.FIRE)
        target.gamemap.engine.message_log.add_message(
            f"The cyberware in the {target.name} reach critical temperatures and deals {damage} damage!!")
        burn_resist=target.fighter.burn_resist
        if burn_resist<40:
            burn_chance=random.randint(0,50-burn_resist)
            if burn_chance>=10:
                target.status.add_effect(status_effects.Burning(target))
                target.gamemap.engine.message_log.add_message(f"The {target.name} has been set on fire!", color.red)


        target.fighter.apply_damage(damage)
        self.use_fp(hacker)
        hacker.set_wait_counter(5)

class vDrain(Virus):
    def __init__(self):
        super().__init__()
        self.name = "Drain.bat"
        self.cost=8
        self.damage=10

    def perform(self, hacker: Actor, target: Actor):
        target.fighter.apply_damage(self.damage)
        hacker.fighter.heal((2*self.damage)//3)
        target.gamemap.engine.message_log.add_message(
            f"{hacker.name} siphons {self.damage} hp from {target.name}, healing itself for {(2*self.damage//3)}",color.health_recovered)
        self.use_fp(hacker)
        hacker.set_wait_counter(5)

class vRepair(Virus):
    def __init__(self):
        super().__init__()
        self.name = "Repair.dll"
        self.cost=11
        self.amount=10


    def perform(self, hacker: Actor, target: Actor):
        heal_amount=target.fighter.heal(self.amount)
        target.gamemap.engine.message_log.add_message(
            f"{hacker.name} repairs {target.name} for {heal_amount}")
        self.use_fp(hacker)
        hacker.set_wait_counter(5)


class vCripple(Virus):
    def __init__(self):
        super().__init__()
        self.name = "Cripple.mp3.exe"
        self.cost=5

    def perform(self, hacker: Actor, target: Actor):
        target.fighter.base_speed = int(target.fighter.base_speed/2)
        target.gamemap.engine.message_log.add_message(
            f"The servos in {target.name} lock up, halving its movement speed"
        )
        self.use_fp(hacker)
        hacker.set_wait_counter(5)


class vAnalyze(Virus):
    def __init__(self):
        super().__init__()
        self.name = "Analyze"
        self.cost=4

    def perform(self, hacker: Actor, target: Actor):
        target.fighter.base_defense = int(target.fighter.base_defense/2)
        target.gamemap.engine.message_log.add_message(
            f"You receive a full readout of the {target.name}'s  internals, revealing its weaknesses"
        )
        self.use_fp(hacker)
        hacker.set_wait_counter(5)

class vKill(Virus):
    def __init__(self):
        super().__init__()
        self.name = "Reaper Protocol"
        self.cost=20
    def perform(self, hacker: Actor, target: Actor):
        target.status.add_effect(status_effects.Reaper(target=target,))

        target.gamemap.engine.message_log.add_message(
            f"{hacker.name} infects the {target.name} with fatal malware. It's health will drain until it dies.")
        self.use_fp(hacker)

ShortCirc = vShortCircuit()
Confuse = vConfuse()
Blaze= vBlaze()
Control=vControl()
Overheat=vOverheat()
Drain=vDrain()
Repair=vRepair()
Cripple=vCripple()
Analyze=vAnalyze()
Kill=vKill()
std_viruses = [ShortCirc,
               Confuse,
               Control,
               Overheat,
               Drain,
               Repair,
               Cripple,
               Analyze,
               Kill
               ]