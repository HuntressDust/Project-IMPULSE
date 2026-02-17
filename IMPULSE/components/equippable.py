from __future__ import annotations


from typing import TYPE_CHECKING, Optional

from IMPULSE.components.base_component import BaseComponent
from IMPULSE.damage_types import DamageType
from IMPULSE.equipment_types import EquipmentType

if TYPE_CHECKING:
    from IMPULSE.entity import Item

class Equippable(BaseComponent):
    parent: Item

    def __init__(
        self,
        equipment_type: EquipmentType,
        attack_bonus: int =0,
        defense_bonus: int=0,
        range_bonus: int=1,
        ammo_count: Optional[int] = None,
        ammo_max: int = 0,
        two_handed: bool = False,
        shock_resist:int=0,
        burn_resist:int=0,
        hit_floor:int=10,
        attack_times: int=1,
        damage_type: DamageType=DamageType.KINETIC
    ):
        self.equipment_type = equipment_type
        self.attack_bonus = attack_bonus
        self.defense_bonus = defense_bonus
        self.range_bonus = range_bonus
        self.two_handed = two_handed
        self.ammo_count=ammo_count
        self.ammo_max=ammo_max
        self.shock_resist=shock_resist
        self.burn_resist=burn_resist
        self.hit_floor=hit_floor
        self.attack_times=attack_times
        self.damage_type=damage_type

    def decrement_ammo(self):
        self.ammo_count -=1

    def is_empty(self):
        if self.ammo_count is not None:
            return self.ammo_count==0
        else:
            return False



class cool_knife(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, attack_bonus=2)

class shock_claws(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, attack_bonus=2, attack_times=2, damage_type=DamageType.SHOCK)

class misericorde(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, attack_bonus=5)

class labrys(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, attack_bonus=10, two_handed=True)

class rapier(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, attack_bonus=4,defense_bonus=1)


class pistol(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, attack_bonus=5, range_bonus=4,ammo_count=12,ammo_max=12)

class assualtRifle(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON,
                         attack_bonus=5, range_bonus=5,ammo_count=12,ammo_max=24, attack_times=3,
                         hit_floor=8,two_handed=True)
class flameThrower(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON,
                         attack_bonus=5, range_bonus=3,ammo_count=5,ammo_max=10,
                         hit_floor=12,two_handed=True, damage_type=DamageType.FIRE)

class chainGun(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON,
                         attack_bonus=5, range_bonus=5,ammo_count=10,ammo_max=30,
                         hit_floor=8,two_handed=True, attack_times=6)


class leather_jacket(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=3)

class latex_bodysuit(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=1,shock_resist=30)
class jumpsuit(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=1,burn_resist=30)
class dress(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=1,)
class  hazard_suit(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=3)