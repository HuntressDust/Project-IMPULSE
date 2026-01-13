from __future__ import annotations


from typing import TYPE_CHECKING, Optional

from components.base_component import BaseComponent
from equipment_types import EquipmentType

if TYPE_CHECKING:
    from entity import Item

class Equippable(BaseComponent):
    parent: Item

    def __init__(
        self,
        equipment_type: EquipmentType,
        power_bonus: int =0,
        defense_bonus: int=0,
        range_bonus: int=0,
        ammo_count: Optional[int] = None,
        ammo_max: int = 0,
        two_handed: bool = False
    ):
        self.equipment_type = equipment_type
        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus
        self.range_bonus = range_bonus
        self.two_handed = two_handed
        self.ammo_count=ammo_count
        self.ammo_max=ammo_max

    def decrement_ammo(self):
        self.ammo_count -=1

    def is_empty(self):
        if self.ammo_count is not None:
            return self.ammo_count==0
        else:
            return False



class cool_knife(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=2)

class spear(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=2, range_bonus=2)

class pistol(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=3, range_bonus=6,ammo_count=12,ammo_max=12)

class rapier(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=4)

class leather_jacket(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=1)

class  hazard_suit(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=3)