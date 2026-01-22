from __future__ import annotations
from typing import Optional, TYPE_CHECKING, Tuple

from components.base_component import BaseComponent
from body_parts import BodyPart

if TYPE_CHECKING:
    from entity import Actor, Item

class Cyberware(BaseComponent):
    parent: Actor
    def __init__(self, head: Optional[Item] = None, torso: Optional[Item]=None, arms: Optional[Item]=None,
                legs: Optional[Item]=None):
        self.head = head
        self.torso = torso
        self.arms = arms
        self.legs = legs

        self.bonus_active = False
        self.slots = ("head", "torso", "arms","legs")



    def unequip_message(self, item_name: str) -> None:
        self.parent.gamemap.engine.message_log.add_message(
            f"You no longer have the {item_name}."
        )

    def equip_message(self, item_name: str) -> None:
        self.parent.gamemap.engine.message_log.add_message(
            f"You are fitted with the {item_name}."
        )

    def equip_to_slot(self, slot: str, item: Item, add_message: bool) -> None:
        current_item = getattr(self, slot)

        if current_item is not None:
            self.unequip_from_slot(slot, add_message)

        setattr(self, slot, item)

        if add_message:
            self.equip_message(item.name)

    def unequip_from_slot(self, slot: str, add_message: bool) -> None:
        current_item = getattr(self, slot)

        if add_message:
            self.unequip_message(current_item.name)

        setattr(self, slot, None)

    def toggle_equip(self, cyberware: Item, add_message: bool = True) -> None:
        if ( cyberware.bodymod.bodypart == BodyPart.HEAD
        ):
            slot = "head"
        elif( cyberware.bodymod.bodypart == BodyPart.BODY
        ):
            slot = "torso"
        elif (cyberware.bodymod.bodypart == BodyPart.ARMS
        ):
            slot = "arms"

        else:
            slot= "legs"

        if getattr(self, slot) == cyberware:
            self.unequip_from_slot(slot, add_message)
        else:
            self.equip_to_slot(slot, cyberware, add_message)


    def total_power_bonus(self) -> int:
        total_power_bonus = 0
        for slot in self.slots:
            cyberware = getattr(self, slot)
            if cyberware is not None:
                if cyberware.bodymod.power_bonus is not None:
                    total_power_bonus += cyberware.bodymod.power_bonus
        return total_power_bonus

    def total_accuracy_bonus(self) -> int:
        total_accuracy_bonus = 0
        for slot in self.slots:
            cyberware = getattr(self, slot)
            if cyberware is not None:
                if cyberware.bodymod.accuracy_bonus is not None:
                    total_accuracy_bonus += cyberware.bodymod.accuracy_bonus
        return total_accuracy_bonus

    def total_speed_bonus(self) -> int:
        total_speed_bonus = 0
        for slot in self.slots:
            cyberware = getattr(self, slot)
            if cyberware is not None:
                if cyberware.bodymod.speed_bonus is not None:
                    total_speed_bonus += cyberware.bodymod.speed_bonus
        return total_speed_bonus

    def total_focus_bonus(self):
        total_focus_bonus = 0
        for slot in self.slots:
            cyberware = getattr(self, slot)
            if cyberware is not None:
                if cyberware.bodymod.focus_bonus is not None:
                    total_focus_bonus += cyberware.bodymod.focus_bonus
        return total_focus_bonus

    def total_health_bonus(self):
        total_health_bonus = 0
        for slot in self.slots:
            cyberware = getattr(self, slot)
            if cyberware is not None:
                if cyberware.bodymod.health_bonus is not None:
                    total_health_bonus += cyberware.bodymod.health_bonus
        return total_health_bonus

    def has_slot_perk(self) -> bool:
        cyberware = getattr(self, "torso")
        if cyberware is not None:
            return cyberware.bodymod.slot_perk
        else:
            return False