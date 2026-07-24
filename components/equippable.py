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
        damage_type: DamageType=DamageType.KINETIC,
        power_needed: int=0,
        reflex_needed: int=0,
        focus_needed:int=0,
        reflex_malice:int=0,
        reflex_bonus:int=0,
        dodge_bonus:int=0,
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
        self.power_needed=power_needed
        self.reflex_needed=reflex_needed
        self.focus_needed=focus_needed
        self.reflex_malice=reflex_malice
        self.reflex_bonus=reflex_bonus
        self.dodge_bonus=dodge_bonus
    def decrement_ammo(self):
        self.ammo_count -=1

    def is_empty(self):
        if self.ammo_count is not None:
            return self.ammo_count==0
        else:
            return False



class cool_knife(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, attack_bonus=3)

class shock_claws(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, attack_bonus=4, attack_times=2,
                         damage_type=DamageType.SHOCK,two_handed=True,focus_needed=4,reflex_malice=1)

class misericorde(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, attack_bonus=3, attack_times=2,)

class labrys(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, attack_bonus=8, two_handed=True,power_needed=5,defense_bonus=1)

class rapier(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, attack_bonus=5,dodge_bonus=2,reflex_needed=4)


class pistol(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, attack_bonus=4, range_bonus=3,ammo_count=12,ammo_max=12,hit_floor=8)

class assualtRifle(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON,
                         attack_bonus=6, range_bonus=5,ammo_count=12,ammo_max=24, attack_times=3,
                         hit_floor=6,two_handed=True)
class flameThrower(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON,
                         attack_bonus=5, range_bonus=3,ammo_count=5,ammo_max=10,
                         hit_floor=12,two_handed=True, damage_type=DamageType.FIRE)

class chainGun(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON,
                         attack_bonus=4, range_bonus=5,ammo_count=10,ammo_max=30,
                         hit_floor=4,two_handed=True, attack_times=6)
class angelGun(Equippable):

    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, damage_type=DamageType.SHOCK,
                         attack_bonus=7, range_bonus=7,ammo_count=999,ammo_max=999,
                         hit_floor=6, attack_times=3)

class angelSword(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON,damage_type=DamageType.FIRE,
                         attack_bonus=15)
class leather_jacket(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=2,burn_resist=30,shock_resist=30)

class latex_bodysuit(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=2,shock_resist=60)
class jumpsuit(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=2,burn_resist=60)
class dress(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=1,attack_bonus=1,reflex_bonus=2)
class  hazard_suit(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=4,power_needed=5,shock_resist= 40, burn_resist= 40, reflex_malice=4)

class body_armor(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR,defense_bonus=9,shock_resist= -80, burn_resist= -80)