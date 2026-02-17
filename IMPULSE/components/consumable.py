from __future__ import annotations


from typing import Optional, TYPE_CHECKING

from IMPULSE import actions
from IMPULSE import color
from IMPULSE.components.base_component import BaseComponent
import IMPULSE.components.ai
from IMPULSE.components.inventory import Inventory
from IMPULSE.exceptions import Impossible
from IMPULSE.input_handler import  ActionOrHandler, SingleRangedAttackHandler, RangedAOEAttackHandler
if TYPE_CHECKING:
    from IMPULSE.entity import Actor, Item


class Consumable(BaseComponent):
    parent: Item

    def get_action(self, consumer:Actor) -> Optional[ActionOrHandler]:
        """return action for this item"""
        return actions.ItemAction(consumer, self.parent)

    def activate(self, action: actions.ItemAction) -> None:

        raise NotImplementedError()

    def consume(self) ->None:
        entity = self.parent
        inventory = entity.parent
        if isinstance(inventory, IMPULSE.components.inventory.Inventory):
            inventory.items.remove(entity)

class Ammo(Consumable):
    def __init__(self, rounds: int, gun_type: Item):
        self.rounds=rounds
        self.gun_type=gun_type
    def get_ammo(self):
        return self.rounds
    def activate(self, action: actions.ItemAction):
        gun_name=self.gun_type
        consumer = action.entity
        equipment=consumer.equipment
        action_completed=False
        for slot in equipment.slots:
            if not action_completed:
                if getattr(equipment,slot) is not None:
                    item=getattr(equipment,slot)
                    if item.name == gun_name:
                     if item.equippable.ammo_count < item.equippable.ammo_max:
                        rounds_loaded =self.load_gun(item)
                        self.engine.message_log.add_message(
                            f"You load {rounds_loaded} {self.parent.name} into the {gun_name} ",
                            color.health_recovered)
                        action_completed=True

        if not action_completed:
            execptionstr="No empty "+gun_name+"equipped"
            raise Impossible(execptionstr)


    def load_gun(self, gun: Item):
        load_amount: int =0
        ammo_needed = gun.equippable.ammo_max-gun.equippable.ammo_count

        if self.rounds >= ammo_needed:
            load_amount= ammo_needed
        else:
            load_amount = self.rounds

        self.rounds -= load_amount
        gun.equippable.ammo_count += load_amount

        if self.rounds ==0:
            self.consume()
        return load_amount


class HealingConsumable(Consumable):
    def __init__(self, amount: int):
        self.amount = amount

    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity
        amount_recovered = consumer.fighter.heal(self.amount)

        if amount_recovered > 0:
            self.engine.message_log.add_message(
                f"you slurp that {self.parent.name} for {amount_recovered} fuel units", color.health_recovered,
            )
            self.consume()
        else:
            raise Impossible("youre at full health dummy")

class  ArcDamageConsumable(Consumable):
    def __init__(self, damage: int, maximum_range: int):
        self.damage = damage
        self.maximum_range = maximum_range

    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity
        target = None
        closest_distance = self.maximum_range + 1.0

        for actor in self.engine.game_map.actors:

            if actor is not consumer and self.parent.gamemap.visible[actor.x, actor.y]:
                distance = consumer.distance(actor.x, actor.y)

                if distance < closest_distance:
                    target = actor
                    closest_distance = distance

        if target:
            self.engine.message_log.add_message(
                    f"sparks fly and shocks the {target.name} for {self.damage}"
            )
            target.fighter.take_damage(self.damage)
            self.consume()
        else:
            raise Impossible("theres nobody heeeeeeereeee")

class ConfusionConsumable(Consumable):
    def __init__(self, number_of_turns: int):
        self.number_of_turns = number_of_turns

    def get_action(self, consumer:Actor) -> SingleRangedAttackHandler:
        self.engine.message_log.add_message(
            "pick the poor fucker", color.needs_target
        )

        return SingleRangedAttackHandler(
            self.engine,
            callback = lambda xy: actions.ItemAction(consumer, self.parent, xy)
        )


    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity
        target = action.target_actor

        if not self.engine.game_map.visible[action.target_xy]:
            raise  Impossible("you cant see that far")
        if not target:
            raise Impossible("theres no one there")
        if target is consumer:
            raise Impossible("Dissociative Drugs comming soon ^w^")
        self.engine.message_log.add_message(
            f"you get the {target.name} reallllllllly highhhhh duuuuude woah", color.status_effect
        )
        target.ai=components.ai.ConfusedEnemy(
            entity= target, previous_ai = target.ai, turns_remaining =self.number_of_turns,
        )
        self.consume()

class   FireExplosionConsumable(Consumable):

    def __init__(self, damage: int, radius: int):
        self.damage = damage
        self.radius = radius

    def get_action(self, consumer:Actor) -> RangedAOEAttackHandler:
        self.engine.message_log.add_message(
            "select target", color.needs_target
        )

        return RangedAOEAttackHandler(
            self.engine,
            radius = self.radius,
            callback = lambda xy:actions.ItemAction(consumer, self.parent, xy),
        )


    def activate(self, action: actions.ItemAction) -> None:
        target_xy = action.target_xy

        if not self.engine.game_map.visible[target_xy]:
            raise Impossible("Not allowed to fire blindly into darkness")

        target_hits =False

        for actor in self.engine.game_map.actors:
            if actor.distance(*target_xy) <= self.radius:
                self.engine.message_log.add_message(
                    f"the {actor.name} gets fuuuuucked up for {self.damage} hit points"
                )
                actor.fighter.take_damage(self.damage)
                target_hits = True

        if not target_hits:
            raise Impossible("Not yet allowed to attack nothing")
        self.consume()
