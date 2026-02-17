from __future__ import annotations

from symtable import Class
from typing import TYPE_CHECKING, Optional

from IMPULSE.components.base_component import BaseComponent
from IMPULSE.body_parts import BodyPart

if TYPE_CHECKING:
    from IMPULSE.entity import Item

class BodyMod(BaseComponent):
    parent: Item

    def __init__(
        self,
        bodypart: BodyPart,
        name: str = "cyberware",
        description: str ="placeholder",
        health_bonus: int =0,
        power_bonus:int=0,
        focus_bonus: int =0,
        speed_bonus:int=0,
        dodge_bonus: int=0,
        accuracy_bonus: int=0,
        shock_resist: int=0,
        burn_resist: int=0,
        reflex_bonus:int=0,
        fp_bonus: int=0,
        perk: str="",

    ):
        self.bodypart = bodypart
        self.description = description
        self.power_bonus=power_bonus
        self.hp_bonus = health_bonus
        self.fp_bonus = fp_bonus
        self.focus_bonus = focus_bonus
        self.speed_bonus=speed_bonus
        self.dodge_bonus=dodge_bonus
        self.accuracy_bonus=accuracy_bonus
        self.shock_resist=shock_resist
        self.burn_resist=burn_resist
        self.reflex_bonus=reflex_bonus
        self.perk=perk

class  hack_upgrade(BodyMod):
    def __init__(self) -> None:
        super().__init__(bodypart=BodyPart.HEAD, name="Neural Enhancer",focus_bonus = 5)
class   los_upgrade(BodyMod):
    def __init__(self) -> None:
        super().__init__(bodypart=BodyPart.HEAD,name="Long Range Sensors", perk="LOS")
class   accuracy_upgrade(BodyMod):
    def __init__(self) -> None:
        super().__init__(bodypart=BodyPart.HEAD, name="Integrated Fire Control",accuracy_bonus=5)
class   control_upgrade(BodyMod):
    def __init__(self) -> None:
        super().__init__(bodypart=BodyPart.HEAD, name="Network Interface Adapter",perk="control")


class sheilding(BodyMod):
    def __init__(self) -> None:
        super().__init__(bodypart=BodyPart.BODY, name="Kinetic Plating",health_bonus= 5)
class electric_sheilding(BodyMod):
    def __init__(self) -> None:
        super().__init__(bodypart=BodyPart.BODY, name="Faraday Suite",shock_resist=50)
class fire_sheilding(BodyMod):
    def __init__(self) -> None:
        super().__init__(bodypart=BodyPart.BODY, name="Rapid Cooling Trunk",burn_resist=50)

class boobs(BodyMod):
    def __init__(self)-> None:
        super().__init__(bodypart=BodyPart.BODY, name="Breast Forms [K]", perk="euphoria")


class weapon_slot(BodyMod):
    def __init__(self) -> None:
        super().__init__(bodypart=BodyPart.ARMS, name="Heavy Weapons Platform",perk="slot")

class reflex_upgrate(BodyMod):
    def __init__(self) -> None:
        super().__init__(bodypart=BodyPart.ARMS, name="Rapid Response Servos",reflex_bonus=5)
class bionic_arm(BodyMod):
    def __init__(self) -> None:
        super().__init__(bodypart=BodyPart.ARMS, name="Full Bionic Upgrade",power_bonus=5)
class rocket_fist(BodyMod):
    def __init__(self) -> None:
        super().__init__(bodypart=BodyPart.ARMS, name="R.P.F.",perk="RPF")




class super_legs(BodyMod):
    def __init__(self) -> None:
        super().__init__(bodypart=BodyPart.LEGS, name="Enhanced Legs", speed_bonus=2)

class itchy_legs(BodyMod):
    def __init__(self) -> None:
        super().__init__(bodypart=BodyPart.LEGS, name="Fight-Or-Flight-By-Wire", reflex_bonus=5)

class power_legs(BodyMod):
    def __init__(self) -> None:
        super().__init__(bodypart=BodyPart.LEGS, name="Stability Modules", power_bonus=5)

class carry(BodyMod):
    def __init__(self) -> None:
        super().__init__(bodypart=BodyPart.LEGS, name="Carbon Nano-bones", perk="carry")