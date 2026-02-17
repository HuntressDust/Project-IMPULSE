from __future__ import annotations
from typing import Optional, TYPE_CHECKING, Tuple

from IMPULSE.components.base_component import BaseComponent
from IMPULSE.body_parts import BodyPart

if TYPE_CHECKING:
    from IMPULSE.entity import Actor, Item

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


    @property
    def total_power_bonus(self) -> int:
        total_power_bonus = 0
        for slot in self.slots:
            cyberware = getattr(self, slot)
            if cyberware is not None:
                if cyberware.bodymod.power_bonus is not None:
                    total_power_bonus += cyberware.bodymod.power_bonus
        return total_power_bonus

    @property
    def total_accuracy_bonus(self) -> int:
        total_accuracy_bonus = 0
        for slot in self.slots:
            cyberware = getattr(self, slot)
            if cyberware is not None:
                if cyberware.bodymod.accuracy_bonus is not None:
                    total_accuracy_bonus += cyberware.bodymod.accuracy_bonus
        return total_accuracy_bonus

    @property
    def total_speed_bonus(self) -> int:
        total_speed_bonus = 0
        for slot in self.slots:
            cyberware = getattr(self, slot)
            if cyberware is not None:
                if cyberware.bodymod.speed_bonus is not None:
                    total_speed_bonus += cyberware.bodymod.speed_bonus
        return total_speed_bonus

    @property
    def total_focus_bonus(self) -> int:
        total_focus_bonus = 0
        for slot in self.slots:
            cyberware = getattr(self, slot)
            if cyberware is not None:
                if cyberware.bodymod.focus_bonus is not None:
                    total_focus_bonus += cyberware.bodymod.focus_bonus
        return total_focus_bonus

    @property
    def total_hp_bonus(self) -> int:
        total_health_bonus = 0
        for slot in self.slots:
            cyberware = getattr(self, slot)
            if cyberware is not None:
                if cyberware.bodymod.hp_bonus is not None:
                    total_health_bonus += cyberware.bodymod.hp_bonus
        return total_health_bonus

    @property
    def total_fp_bonus(self) -> int:
        total_fp_bonus = 0
        for slot in self.slots:
            cyberware = getattr(self, slot)
            if cyberware is not None:
                if cyberware.bodymod.fp_bonus is not None:
                    total_fp_bonus += cyberware.bodymod.fp_bonus
        return total_fp_bonus

    @property
    def total_shock_resist(self)-> int:
        total_shock_resist = 0
        for slot in self.slots:
            cyberware = getattr(self, slot)
            if cyberware is not None:
                if cyberware.bodymod.speed_bonus is not None:
                    total_shock_resist += cyberware.bodymod.shock_resist
        return total_shock_resist

    @property
    def total_burn_resist(self):
        total_burn_resist = 0
        for slot in self.slots:
            cyberware = getattr(self, slot)
            if cyberware is not None:
                if cyberware.bodymod.speed_bonus is not None:
                    total_burn_resist += cyberware.bodymod.burn_resist
        return total_burn_resist

    @property
    def total_reflex_bonus(self):
        total_reflex_bonus = 0
        for slot in self.slots:
            cyberware = getattr(self, slot)
            if cyberware is not None:
                if cyberware.bodymod.speed_bonus is not None:
                    total_reflex_bonus += cyberware.bodymod.reflex_bonus
        return total_reflex_bonus

    @property
    def total_dodge_bonus(self):
        total_dodge_bonus = 0
        for slot in self.slots:
            cyberware = getattr(self, slot)
            if cyberware is not None:
                if cyberware.bodymod.speed_bonus is not None:
                    total_dodge_bonus += cyberware.bodymod.dodge_bonus
        return total_dodge_bonus

    @property
    def has_slot_perk(self) -> bool:
        perk_active=False
        for slot in self.slots:
            cyberware = getattr(self, slot)
            if cyberware is not None:
                perk = getattr(cyberware.bodymod, "perk")
                if not perk_active:
                    perk_active = perk=="slot"
        return perk_active

    @property
    def has_carry_perk(self) -> bool:
        perk_active = False
        for slot in self.slots:
            cyberware = getattr(self, slot)
            if cyberware is not None:
                perk = getattr(cyberware.bodymod, "perk")
                if not perk_active:
                    perk_active = perk == "carry"
        return perk_active

    @property
    def has_los_perk(self) -> bool:
        perk_active=False
        for slot in self.slots:
            cyberware = getattr(self, slot)
            if cyberware is not None:
                perk = getattr(cyberware.bodymod, "perk")
                if not perk_active:
                    perk_active = perk=="LOS"
        return perk_active

    @property
    def has_control_perk(self) ->bool:
        perk_active=False
        for slot in self.slots:
            cyberware = getattr(self, slot)
            if cyberware is not None:
                perk = getattr(cyberware.bodymod, "perk")
                if not perk_active:
                    perk_active = perk=="control"
        return perk_active


    @property
    def has_euphoric_perk(self) ->bool:
        perk_active=False
        for slot in self.slots:
            cyberware = getattr(self, slot)
            if cyberware is not None:
                perk = getattr(cyberware.bodymod, "perk")
                if not perk_active:
                    perk_active = perk=="euph"
        return perk_active

    @property
    def has_RPF_perk(self) ->bool:
        perk_active=False
        for slot in self.slots:
            cyberware = getattr(self, slot)
            if cyberware is not None:
                perk = getattr(cyberware.bodymod, "perk")
                if not perk_active:
                    perk_active = perk=="RPF"
        return perk_active
