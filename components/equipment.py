from __future__ import annotations
from typing import Optional, TYPE_CHECKING, Tuple

from IMPULSE.components.base_component import BaseComponent
from IMPULSE.equipment_types import EquipmentType
from IMPULSE.color import invalid
if TYPE_CHECKING:
    from IMPULSE.entity import Actor, Item

class Equipment(BaseComponent):
    parent: Actor
    def __init__(self, right_hand: Optional[Item] = None, left_hand: Optional[Item]=None, bonus_slot: Optional[Item]=None,
                armor: Optional[Item]=None):
        self.right_hand = right_hand
        self.left_hand = left_hand
        self.bonus_slot =bonus_slot
        self.armor = armor

        self.bonus_active=False
        self.slots=("right_hand", "left_hand", "bonus_slot")

    def toggle_bonus(self):
        item_in_slot = getattr(self, "bonus_slot")
        if item_in_slot is not None:
            self.toggle_equip(item_in_slot, add_message=True)
        self.bonus_active=not self.bonus_active

    @property
    def is_unarmed(self):
        return ( self.right_hand is None and self.left_hand is None and self.bonus_slot is None)
    @property
    def defense_bonus(self) -> int:
        bonus =0
        for slot in self.slots:
            weapon = getattr(self,slot)
            if weapon is not None and weapon.equippable is not None:

                bonus += weapon.equippable.defense_bonus

        if self.armor is not None and self.armor.equippable is not None:
            bonus += self.armor.equippable.defense_bonus

        return bonus
    @property
    def reflex_bonus(self):
        if self.armor is not None and self.armor.equippable is not None:
                return  self.armor.equippable.reflex_bonus
        return 0
    @property
    def dodge_bonus(self):
        bonus = 0
        if self.armor is not None and self.armor.equippable is not None:
                bonus+= self.armor.equippable.dodge_bonus
        else:
            for slot in self.slots:
                weapon = getattr(self, slot)
                if weapon is not None and weapon.equippable is not None:
                    bonus += weapon.equippable.dodge_bonus
        return bonus


    @property
    def reflex_malice(self):
        malice=0
        if self.armor is not None and self.armor.equippable is not None:
            if self.parent.fighter.power < self.armor.equippable.power_needed :
                malice+=  self.armor.equippable.reflex_malice
        else:
            for slot in self.slots:
                weapon = getattr(self, slot)
                if weapon is not None and weapon.equippable is not None:
                    if self.parent.fighter.power < weapon.equippable.power_needed:
                        malice += weapon.equippable.reflex_malice
                    if self.parent.fighter.focus < weapon.equippable.focus_needed:
                        malice += weapon.equippable.reflex_malice
        return malice

    def attack_bonus(self, slot):
        bonus=0
        weapon = getattr(self, slot)
        if weapon is not None and weapon.equippable is not None:
            if self.parent.fighter.power < weapon.equippable.power_needed or self.parent.fighter.reflex < weapon.equippable.reflex_needed:
                bonus += weapon.equippable.attack_bonus//2
            else:
                bonus += weapon.equippable.attack_bonus
            if weapon.equippable.range_bonus==1:
                bonus += int(self.parent.fighter.power//3)

        if self.armor is not None and self.armor.equippable is not None:
            bonus += self.armor.equippable.attack_bonus

        return bonus


    @property
    def total_attack_bonus(self) -> int:
        bonus = 0

        for slot in self.slots:
            weapon = getattr(self, slot)
            if weapon is not None and weapon.equippable is not None:
                bonus += weapon.equippable.attack_bonus

        if self.armor is not None and self.armor.equippable is not None:
            bonus += self.armor.equippable.attack_bonus

        return bonus

    @property
    def total_range_bonus(self)->int:
        bonus=0
        for slot in self.slots:
            weapon = getattr(self, slot)
            if weapon is not None and weapon.equippable is not None:
                if bonus < weapon.equippable.range_bonus:
                    bonus = weapon.equippable.range_bonus

        return bonus

    @property
    def total_shock_resist(self)->int:
        bonus=0
        if self.armor is not None and self.armor.equippable is not None:
            bonus += self.armor.equippable.shock_resist
        return bonus

    @property
    def total_burn_resist(self)->int:
        bonus=0
        if self.armor is not None and self.armor.equippable is not None:
            bonus += self.armor.equippable.burn_resist
        return bonus


    def item_is_equipped(self, item: Item) -> bool:
        for slot in self.slots:
            weapon = getattr(self, slot)
            if weapon==item:
                return  True
        return self.armor== item

    def unequip_message(self, item_name: str) -> None:
        self.parent.gamemap.engine.message_log.add_message(
            f" You unequip the {item_name}"
        )

    def equip_message(self, item_name: str) -> None:
         self.parent.gamemap.engine.message_log.add_message(
            f"You equip the {item_name}"
        )

    def equip_to_slot (self, slot: str, item: Item, add_message: bool) -> None:
        current_item = getattr(self, slot)
        if current_item is not None:
            self.unequip_from_slot(slot, add_message)
        setattr(self, slot, item)
        if add_message:
            self.equip_message(item.name)

        if item.equippable.reflex_needed>0:
            if item.equippable.reflex_needed > self.parent.fighter.reflex:
                self.parent.gamemap.engine.message_log.add_message(
                    f"You lack the REFLEX to use the {item.name} effectively...", fg=invalid
                )
        if item.equippable.power_needed > 0:
            if item.equippable.power_needed > self.parent.fighter.power:
                self.parent.gamemap.engine.message_log.add_message(
                f"You lack the POWER to use the {item.name} effectively...", fg=invalid
            )
        if item.equippable.focus_needed > 0:
            if item.equippable.focus_needed > self.parent.fighter.focus:
                self.parent.gamemap.engine.message_log.add_message(
                    f"You lack the POWER to use the {item.name} effectively...", fg=invalid
                )


    def unequip_from_slot(self, slot: str, add_message: bool) -> None:
        current_item = getattr(self, slot)

        if add_message:
            self.unequip_message(current_item.name)

        setattr(self,slot,None)

    def toggle_equip(self, equippable_item: Item, add_message: bool= True, hand: Optional[int] =None) -> None:

        if(equippable_item.equippable and equippable_item.equippable.equipment_type==EquipmentType.ARMOR
        ):
            print("this is armor")
            slot = "armor"
            ##print("Is it already being worn?")
            if getattr(self, slot) == equippable_item:
              ##  print("yes, remove it")
                self.unequip_from_slot(slot, add_message)
            else:
                ##print("no, put it on")
                self.equip_to_slot(slot, equippable_item, add_message)
        elif self.is_unarmed:
            ##print("this is a weapon, and we're unarmed")
            slot = "right_hand"
            ##print("equip to the right hand")
            self.equip_to_slot(slot, equippable_item, add_message)

            if equippable_item.equippable.two_handed:

                if self.bonus_active:
                    self.equip_to_slot("bonus_slot", equippable_item, False)
                else:
                    self.equip_to_slot("left_hand", equippable_item, False)
        else:
            ##print("This is a weapon")
            slots=("right_hand", "left_hand", "bonus_slot")
            needs_equipped=True


            for slot in slots:
                if getattr(self, slot) == equippable_item:
                    ##print("this item is already being held in slot",slot)
                    ##print("unequip it")
                    self.unequip_from_slot(slot, add_message=needs_equipped)
                    needs_equipped=False

            if needs_equipped:
                ##print("it isnt being held")
                if equippable_item.equippable.two_handed:
                  ##  print("it is a two handed weapon")
                    if self.bonus_active:
                    ##    print("we have the heavy weapons platform")


                        #look for two handed weapons and remove them!
                        for index in slots:
                            weapon = getattr(self,index)
                            if weapon is not None:
                                if weapon.equippable.two_handed:
                                    message=True
                                    for slot in slots:
                                        if getattr(self, slot) == weapon:
                                            ##print("this item is already being held in slot",slot)
                                            ##print("unequip it")
                                            self.unequip_from_slot(index, add_message=message)
                                            message = False
                        slot2="bonus_slot"
                        if self.right_hand is None:
                      #      print("the right hand is empty")
                            slot1="right_hand"
                        else:
                            slot1="left_hand"
                    else:
                       # print("we do not have the bonus")
                        slot1="right_hand"
                        slot2="left_hand"


                    weapon1= None
                    if getattr(self, slot1) is not None:
                        weapon1=getattr(self, slot1)
                        self.unequip_from_slot(slot1, add_message=True)
                    if getattr(self, slot2) is not None:
                        weapon2 = getattr(self, slot2)
                        self.unequip_from_slot(slot2, add_message=(weapon1!=weapon2))

                  # print("equipping to slot", slot1, "then", slot2)
                    self.equip_to_slot(slot1, equippable_item, add_message)
                    self.equip_to_slot(slot2, equippable_item, add_message=False)

                else:

                    #print("equiping to slot",self.slots[hand]," as specified")
                    slot = self.slots[hand]

                    if getattr(self, slot) is not None:
                        #print(f"theres a weapon in slot {slot}")
                        weapon=getattr(self, slot)
                        #print(f" it is the {weapon.name}")
                        message=True
                        for index in slots:
                            #print(f"look in slot {index}")
                            if getattr(self, index) == weapon:
                                #print(f"it is here, remove it")
                                ##print("this item is already being held in slot",slot)
                                ##print("unequip it")
                                self.unequip_from_slot(index, add_message=message)
                                message = False



                    self.equip_to_slot(self.slots[hand], equippable_item, add_message)







