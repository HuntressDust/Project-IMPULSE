from __future__ import annotations
from typing import TYPE_CHECKING
from IMPULSE import color
from IMPULSE.components.base_component import BaseComponent

from IMPULSE.render_order import RenderOrder

from IMPULSE.components.ai import SelfDestruct
from IMPULSE.damage_types import DamageType

if  TYPE_CHECKING:
    from IMPULSE.entity import Actor

class Fighter(BaseComponent):
    parent: Actor

    def __init__(self,
                 hp: int,
                 fp: int=0,
                 base_defense: int=1,
                 base_attack : int=1,
                 base_speed : int=5,
                 base_accuracy: int=5,
                 base_burn_resist: int = 0,
                 base_shock_resist: int=0,
                 base_range: int = 1,
                 base_power: int=1,
                 base_reflex: int=1,
                 base_focus: int=1,
                 base_dodge: int=0,

                 ):
        self.base_max_hp = hp
        self.base_max_fp = fp
        self._hp = hp
        self._fp=fp
        self.base_defense = base_defense
        self.base_attack = base_attack
        self.base_speed=base_speed
        self.base_accuracy = base_accuracy
        self.base_range=base_range

        self.base_shock_resist=base_shock_resist
        self.base_burn_resist=base_burn_resist
        self.base_dodge = base_dodge


        #PLAYER ATTRIBUTES
        self.base_power=base_power
        self.base_reflex=base_reflex
        self.base_focus=base_focus

    @property
    def hp(self) -> int:
        return  self._hp

    @property
    def fp(self)-> int:
        return self._fp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))
        if self._hp == 0 and self.parent.ai:
            self.die()

    @fp.setter
    def fp(self, value: int) -> None:
        self._fp = max(0, min(value, self.max_fp))

    @property
    def max_hp(self)-> int:
        return self.base_max_hp + self.hp_bonus
    @property
    def max_fp(self)-> int:
        return self.base_max_fp + self.fp_bonus




    def full_heal(self):
        self.hp=self.max_hp
        self.fp=self.max_fp
    @property
    def defense(self) -> int:
        return self.base_defense + self.defense_bonus+self.dodge_bonus


    @property
    def power(self) -> int:
        return self.base_power + self.power_bonus

    @property
    def reflex(self) -> int:
        return self.base_power + self.reflex_bonus


    @property
    def focus(self) -> int:
        return self.base_power + self.focus_bonus


    @property
    def accuracy(self) -> int:
        return self.base_accuracy + self.accuracy_bonus

    @property
    def attack(self)->int:
        return self.base_attack + self.attack_bonus

    def attack_from_slot(self,slot):
        return self.base_attack + self.weapon_attack_bonus(slot)

    @property
    def speed(self) -> int:
        return self.base_speed + self.speed_bonus

    @property
    def defense_bonus(self) -> int:
        if hasattr(self.parent,"equipment"):
            return self.parent.equipment.defense_bonus
        else:
            return 0
    @property
    def dodge(self) -> int:
        return self.base_dodge + self.dodge_bonus

    @property
    def dodge_bonus(self) -> int:
        dodge_bonus =0
        if hasattr(self.parent,"cyberware"):
            dodge_bonus+=self.parent.cyberware.total_dodge_bonus

        dodge_from_reflex=int(self.base_reflex/3)
        dodge_bonus+=dodge_from_reflex
        return dodge_bonus

    @property
    def max_range(self) -> int:
        if hasattr(self.parent,"equipment"):
            return self.parent.equipment.total_range_bonus
        else:
            return self.base_range

    @property
    def attack_bonus(self) -> int:
        attack_bonus = 0
        if hasattr(self.parent,"equipment"):
            attack_bonus+= self.parent.equipment.total_attack_bonus
        return attack_bonus

    @property
    def power_bonus(self) -> int:
        power_bonus = 0
        if hasattr(self.parent,"cyberware"):
            power_bonus += self.parent.cyberware.total_power_bonus
        return power_bonus

    @property
    def reflex_bonus(self) -> int:
        reflex_bonus = 0
        if hasattr(self.parent,"cyberware"):
            reflex_bonus += self.parent.cyberware.total_reflex_bonus
        return reflex_bonus

    @property
    def focus_bonus(self) -> int:
        focus_bonus = 0
        if hasattr(self.parent,"cyberware"):
            focus_bonus += self.parent.cyberware.total_focus_bonus
        return focus_bonus

    @property
    def hp_bonus(self) -> int:
        hp_bonus=0
        if hasattr(self.parent,"cyberware"):
            hp_bonus += self.parent.cyberware.total_hp_bonus
        hp_bonus+=self.power
        return hp_bonus

    @property
    def fp_bonus(self) -> int:
        fp_bonus=0
        if hasattr(self.parent,"cyberware"):
            fp_bonus += self.parent.cyberware.total_fp_bonus

        fp_bonus+=self.focus
        return fp_bonus

    @property
    def speed_bonus(self) -> int:
        speed_bonus=0
        if hasattr(self.parent,"cyberware"):
            speed_bonus+=self.parent.cyberware.total_speed_bonus
        if self.reflex > 9:
            speed_bonus+= 1
        return speed_bonus

    @property
    def accuracy_bonus(self) -> int:
        accuracy_bonus=0
        if hasattr(self.parent,"cyberware"):
            accuracy_bonus+=self.parent.cyberware.total_accuracy_bonus
        accuracy_bonus+=self.reflex
        return accuracy_bonus


    def weapon_attack_bonus(self, slot) -> int:
        if self.parent.equipment:
            return self.parent.equipment.attack_bonus(slot)
        else:
            return 0


    @property
    def shock_resist(self) -> int:
        shock_resist=0
        if hasattr(self.parent,"cyberware"):
            shock_resist += self.parent.cyberware.total_shock_resist
        if hasattr(self.parent,"equipment"):
            shock_resist+= self.parent.equipment.total_shock_resist
        return shock_resist

    @property
    def burn_resist(self) -> int:
        burn_resist=0
        if hasattr(self.parent,"cyberware"):
            burn_resist += self.parent.cyberware.total_burn_resist
        if hasattr(self.parent,"equipment"):
            burn_resist+= self.parent.equipment.total_burn_resist
        return burn_resist


    def die(self) -> None:
        if isinstance(self.parent.ai,SelfDestruct):
            self.engine.danger_on=False
        if self.engine.player is self.parent:
            death_message = "You have been struck down. Thoughts and prayers."
            death_message_color = color.player_die


        else:
            death_message =f"{self.parent.name} has been eliminated."
            death_message_color = color.enemy_die

        if self.parent in self.engine.player.controller.minion_list:
            self.engine.player.controller.release_minion(self.parent)

        self.parent.char="%"
        self.parent.color = (200,0,0)
        self.parent.blocks_movement = False
        self.parent.ai = None
        self.parent.name = f"{self.parent.name} corpse"
        self.parent.render_order = RenderOrder.CORPSE

        self.engine.message_log.add_message(death_message,death_message_color)
        self.engine.player.level.add_xp(self.parent.level.xp_given)

    def heal(self,amount: int) -> int:
        if self.hp == self.max_hp:
            return 0

        new_hp_value = self.hp + amount

        if new_hp_value > self.max_hp:
            new_hp_value = self.max_hp

        amount_recovered = new_hp_value - self.hp

        self.hp = new_hp_value
        return amount_recovered

    def heal_FP(self, amount: int) -> int:

        if self.fp == self.max_fp:
            return 0

        new_fp_value = self.fp + amount

        if new_fp_value > self.max_hp:
            new_fp_value = self.max_hp

        amount_recovered = new_fp_value - self.fp

        self.fp = new_fp_value
        return amount_recovered


    def take_damage(self, amount: int , damagetype: DamageType = DamageType.KINETIC) -> int:
        damage = amount
        if damagetype==DamageType.FIRE:
            damage -= int(self.burn_resist/10)
        if damagetype==DamageType.SHOCK:
            damage -= int(self.shock_resist/10)
        self.hp -= damage
        return damage

    def drain_fp(self, amount: int) -> int:
        new_fp = self.fp -  amount
        if new_fp<=0:
            drain_amount=self.fp
            self.fp = 0
            if hasattr(self.parent,"controller"):
                self.parent.controller.release_all()
            return drain_amount
        else:
            self.fp -= amount
            return amount



