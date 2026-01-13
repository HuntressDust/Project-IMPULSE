from __future__ import annotations

from symtable import Class
from typing import TYPE_CHECKING, Optional

from components.base_component import BaseComponent
from body_parts import BodyPart

if TYPE_CHECKING:
    from entity import Item

class BodyMod(BaseComponent):
    parent: Item

    def __init__(
        self,
        bodypart: BodyPart,
        description: str ="placeholder",
        health_bonus: int =0,
        stress_bonus: int =0,
        accuracy_bonus: int=0,
        speed_bonus: int=0,
        perk: Optional[str]=None,

    ):
        self.bodypart = bodypart
        self.description = description
        self.health_bonus = health_bonus
        self.stress_bonus = stress_bonus
        self.accuracy_bonus = accuracy_bonus
        self.speed_bonus = speed_bonus
        self.perk=perk

class  hack_upgrade(BodyMod):
    def __init__(self) -> None:
        super().__init__(bodypart=BodyPart.HEAD, stress_bonus = 3)

class sheilding(BodyMod):
    def __init__(self) -> None:
        super().__init__(bodypart=BodyPart.BODY, health_bonus= 5)
class weapon_slot(BodyMod):
    def __init__(self) -> None:
        super().__init__(bodypart=BodyPart.ARMS, perk="bonus slot")

class super_legs(BodyMod):
    def __init__(self) -> None:
        super().__init__(bodypart=BodyPart.LEGS, speed_bonus = 3)