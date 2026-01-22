from __future__ import annotations
from typing import TYPE_CHECKING
import color
from components.base_component import BaseComponent

from render_order import RenderOrder
if  TYPE_CHECKING:
    from entity import Actor

class Fighter(BaseComponent):
    parent: Actor

    def __init__(self, hp: int, base_defense: int, base_power : int, base_speed : int, base_accuracy: int, base_focus: int):
        self.max_hp = hp
        self._hp = hp
        self.base_defense = base_defense
        self.base_power = base_power
        self.base_speed=base_speed
        self.base_accuracy = base_accuracy
        self.base_focus = base_focus

    @property
    def hp(self) -> int:
        return  self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))
        if self._hp == 0 and self.parent.ai:
            self.die()

    @property
    def defense(self) -> int:
        return self.base_defense + self.defense_bonus

    @property
    def power(self) -> int:
        return self.base_power + self.power_bonus

    @property
    def accuracy(self) -> int:
        return self.base_accuracy + self.accuracy_bonus


    def power_from_slot(self,slot):
        print("BASE:",self.base_power)
        print("BONUS:",self.weapon_power_bonus(slot))
        return self.base_power + self.weapon_power_bonus(slot)

    @property
    def speed(self) -> int:
        return self.base_speed + self.speed_bonus

    @property
    def defense_bonus(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.defense_bonus
        else:
            return 0

    @property
    def max_range(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.total_range_bonus
        else:
            return 1
    @property
    def power_bonus(self) -> int:
        power_bonus = 0
        if self.parent.cyberware:
            power_bonus += self.parent.cyberware.total_power_bonus
        if self.parent.equipment:
            power_bonus+= self.parent.equipment.total_power_bonus

        return power_bonus

    @property
    def speed_bonus(self) -> int:
        if self.parent.cyberware:
            return self.parent.cyberware.total_speed_bonus
        else:
            return 0

    @property
    def accuracy_bonus(self) -> int:
        if self.parent.cyberware:
            return self.parent.cyberware.total_accuracy_bonus
        else:
            return 0

    def weapon_power_bonus(self, slot) -> int:
        if self.parent.equipment:
            return self.parent.equipment.power_bonus(slot)
        else:
            return 0

    def die(self) -> None:
        if self.engine.player is self.parent:
            death_message = "You have been struck down. Thoughts and prayers."
            death_message_color = color.player_die


        else:
            death_message =f"{self.parent.name} has been eliminated."
            death_message_color = color.enemy_die


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

    def take_damage(self, amount: int) -> None:
        self.hp -= amount

