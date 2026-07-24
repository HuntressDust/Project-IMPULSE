from __future__ import annotations


from typing import Optional, TYPE_CHECKING

from IMPULSE import actions
from IMPULSE import color
from IMPULSE.components.base_component import BaseComponent
import IMPULSE.components.ai
from IMPULSE.components.inventory import Inventory
from IMPULSE.damage_types import DamageType
from IMPULSE.exceptions import Impossible
from IMPULSE.input_handler import  ActionOrHandler, SingleRangedAttackHandler, RangedAOEAttackHandler
from IMPULSE import status_effects
from IMPULSE.status_effects import Confused, Burning

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
            execptionstr=f"No empty {gun_name} equipped"
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
                f" You patch yourself up with the {self.parent.name} and heal {amount_recovered} hp", color.health_recovered,
            )
            self.consume()
        else:
            raise Impossible("You're at full health dummy")

class FocusConsumable(HealingConsumable):
    def activate(self, action: actions.ItemAction) -> None:

        consumer = action.entity
        amount_recovered = consumer.fighter.heal_FP(self.amount)

        if amount_recovered > 0:
            self.engine.message_log.add_message(
                f"You drink the {self.parent.name} and recover {amount_recovered} FP.", color.fp,
            )
            self.consume()
        else:
            raise Impossible("You're already at full FP")

class EstrogenConsumable(Consumable):
    def __init__(self,duration: int):
        self.duration = duration

    def activate(self, action: actions.ItemAction) -> None:

        consumer = action.entity

        dysphoriaFlag = False
        for effect in consumer.status.effects:
            if effect.abrev=="DYS":
                dysphoriaFlag = True

                effect.end_effect()
                tempEffect=effect

            if effect.abrev=="EUP":
                raise Impossible("You are already Euphoric")

        if dysphoriaFlag:

            consumer.status.effects.remove(tempEffect)
        else:
            consumer.status.add_effect(status_effects.Euphoria(consumer,self.duration,))

        self.engine.message_log.add_message(
            f"You inject 3mg Estradiol intramuscular and immediately feel better", color.health_recovered,
        )
        self.consume()
class WeedConsumable(Consumable):
    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity

        debuff_list=list()
        for effect in consumer.status.effects:
            if effect.abrev == "DYS" or effect.abrev =="TRGT" or effect.abrev=="BURN":
                debuff_list.append(effect)

        if len(debuff_list)==0:
            raise Impossible("You have not status effects to clear")
        else:
            for debuff in debuff_list:
                debuff.end_effect()
                consumer.status.effects.remove(debuff)

            self.engine.message_log.add_message(
                f"You smoke some cyber-weed and feel your troubles melt away", color.health_recovered,
            )
            self.consume()

class ProgesteroneConsumable(Consumable):
    def __init__(self,duration: int):
        self.duration = duration
    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity

        for effect in consumer.status.effects:
            if effect.abrev == "UWU":
                raise Impossible("You are already seething with Lust")

        consumer.status.add_effect(status_effects.Horny(consumer, self.duration, ))

        self.engine.message_log.add_message(
            f"You boof your PROG and are overcome with Lust!", color.health_recovered,
        )
        self.consume()

class PoppersConsumable(Consumable):
    def __init__(self,duration: int, amount: int):
        self.duration = duration
        self.amount = amount
    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity

        for effect in consumer.status.effects:
            if effect.abrev == "HPUP":
                raise Impossible("You are already numbed to pain")

        consumer.status.add_effect(status_effects.HPBuff(consumer, self.duration, self.amount ))

        self.engine.message_log.add_message(
            f"You inhale your POPPERS and feel numb to pain!", color.health_recovered,
        )
        self.consume()


class AmphetameineConsumable(Consumable):
    def __init__(self,duration: int, amount: int):
        self.duration = duration
        self.amount = amount
    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity

        for effect in consumer.status.effects:
            if effect.abrev == "FPUP":
                raise Impossible("You are already alert!")

        consumer.status.add_effect(status_effects.FPBuff(consumer, self.duration, self.amount ))

        self.engine.message_log.add_message(
            f"You take your STIMS and and can think with intensity!", color.health_recovered,
        )
        self.consume()
class AdrenalineComsumable(Consumable):
    def __init__(self,duration: int):
        self.duration = duration
    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity

        for effect in consumer.status.effects:
            if effect.abrev == "RFLX":
                raise Impossible("You are already hyper-aware!")

        consumer.status.add_effect(status_effects.Hyper(consumer, self.duration, ))

        self.engine.message_log.add_message(
            f"You inject ADRENALINE and are now hyper-aware of your surroundings!", color.health_recovered,
        )
        self.consume()

class hypnofileConsumable(Consumable):
    def __init__(self,duration: int):
        self.duration = duration
    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity

        for effect in consumer.status.effects:
            if effect.abrev == "FOC":
                raise Impossible("You are already hyperfocused")

        consumer.status.add_effect(status_effects.Focused(consumer, self.duration, ))

        self.engine.message_log.add_message(
            f"You load your hypno-file and are hyperfocused!", color.health_recovered,
        )
        self.consume()

class pocket_shieldConsumable(Consumable):
    def __init__(self, duration: int, amount: int):
        self.duration = duration
        self.amount = amount

    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity

        for effect in consumer.status.effects:
            if effect.abrev == "SHLD":
                raise Impossible("You are already Shielded")

        consumer.status.add_effect(status_effects.Shielded(consumer, self.duration,self.amount ))

        self.engine.message_log.add_message(
            f"An energy shield crackles to life around you!", color.health_recovered,
        )
        self.consume()

class flareConsumable(Consumable):
    def __init__(self,damage: int):
        self.damage=damage
        range=1

    def get_action(self, consumer:Actor) -> SingleRangedAttackHandler:
        self.engine.message_log.add_message(
            "Select Target", color.needs_target
        )

        return SingleRangedAttackHandler(
            self.engine,
            callback = lambda xy: actions.ItemAction(consumer, self.parent, xy),radius=1
        )
    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity
        target = action.target_actor


        if not self.engine.game_map.visible[action.target_xy]:
            raise  Impossible("No Target Selected")
        if not target:
            raise Impossible("No Target Selected")
        if target is consumer:
            raise Impossible("You cannot burn yourself (yet)")

        distance = consumer.distance(target.x, target.y)
        if distance >=2:
            raise Impossible("Target out of range")

        damage=target.fighter.calculate_damage(self.damage,DamageType.FIRE)
        self.engine.message_log.add_message(
            f"You light the flare against the {target.name}, burning it for {damage} hp!", color.exterminator
        )
        target.fighter.apply_damage(damage)
        if target.fighter.burn_resist<=20:
            target.status.add_effect(status_effects.Burning(target))
            self.engine.message_log.add_message(f"The flare sets the {target.name} on fire!", color.red)

        self.consume()


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

            total = target.fighter.calculate_damage(self.damage, DamageType.SHOCK)
            self.engine.message_log.add_message(
                    f"Sparks fly and shocks the {target.name} for {total} hp."
            )
            target.fighter.apply_damage(total)
            self.consume()
        else:
            raise Impossible("There are no enemies to attack ")

class ConfusionConsumable(Consumable):
    def __init__(self, number_of_turns: int):
        self.number_of_turns = number_of_turns

    def get_action(self, consumer:Actor) -> SingleRangedAttackHandler:
        self.engine.message_log.add_message(
            "Select Target", color.needs_target
        )

        return SingleRangedAttackHandler(
            self.engine,
            callback = lambda xy: actions.ItemAction(consumer, self.parent, xy),radius=None
        )


    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity
        target = action.target_actor

        if not self.engine.game_map.visible[action.target_xy]:
            raise  Impossible("No Target Selected")
        if not target:
            raise Impossible("No Target Selected")
        if target is consumer:
            raise Impossible("Dissociative Drugs coming soon ^w^")
        self.engine.message_log.add_message(
            f"The {target.name} stumbles around in a dissociative haze!", color.status_effect
        )
        target.status.add_effect(Confused(target,self.number_of_turns))
        self.consume()


class AOEConsumable(Consumable):
    def __init__(self, damage: int, radius: int):
        self.damage = damage
        self.radius = radius

    def get_action(self, consumer: Actor) -> RangedAOEAttackHandler:
        self.engine.message_log.add_message(
            "Select Target", color.needs_target
        )

        return RangedAOEAttackHandler(
            self.engine,
            radius=self.radius,
            callback=lambda xy: actions.ItemAction(consumer, self.parent, xy),
        )

    def activate(self, action: actions.ItemAction) -> None:
        raise NotImplementedError


class FireExplosionConsumable(AOEConsumable):


    def activate(self, action: actions.ItemAction) -> None:
        target_xy = action.target_xy

        if not self.engine.game_map.visible[target_xy]:
            raise Impossible("Invalid Target")
        if not self.engine.game_map.tiles["walkable"][target_xy]:
            raise Impossible("Invalid Target")

        actor_list=[]
        for actor in self.engine.game_map.actors:
            if actor.distance(*target_xy) <= self.radius:
                actor_list.append(actor)
        message_color = color.player_atk
        for actor in actor_list:
            if actor.distance(*target_xy) <= self.radius:
                if actor is self.engine.player:
                    message_color = color.enemy_atk
                    damage_message = f"{actor.name} is caught in a blaze of fire "
                else:
                    damage_message=f"The {actor.name} is caught in a blaze of fire "
                damage = actor.fighter.calculate_damage(self.damage, damagetype=DamageType.FIRE)
                if damage == 0:
                    damage_message = damage_message + f"but takes no damage!"
                else:
                    damage_message = damage_message + f"for {damage} hit points!"
                self.engine.message_log.add_message(
                    damage_message,message_color
                )
                actor.fighter.apply_damage(damage)

                if actor.fighter.burn_resist < 40:
                    actor.status.add_effect(status_effects.Burning(actor))
                    self.engine.message_log.add_message(f"The {actor.name} has been set on fire!",color.red)

        self.consume()

class FragConsumable(AOEConsumable):


    def activate(self, action: actions.ItemAction) -> None:
        target_xy = action.target_xy

        if not self.engine.game_map.visible[target_xy]:
            raise Impossible("Invalid Target")
        if not self.engine.game_map.tiles["walkable"][target_xy]:
            raise Impossible("Invalid Target")

        actor_list=[]
        for actor in self.engine.game_map.actors:
            if actor.distance(*target_xy) <= self.radius:
                actor_list.append(actor)
        message_color=color.player_atk
        for actor in actor_list:
            if actor is self.engine.player:
                message_color=color.enemy_atk
                damage_message = f"{actor.name} is caught in an explosion "

            else:
                damage_message=f"The {actor.name} is caught in an explosion "
            damage = actor.fighter.calculate_damage(self.damage )
            if damage==0:
                damage_message=damage_message+ f"but takes no damage!"
            else:
                damage_message = damage_message +f"for {damage} hit points!"
            self.engine.message_log.add_message(
                damage_message,message_color
            )
            actor.fighter.apply_damage(damage)

        self.consume()
