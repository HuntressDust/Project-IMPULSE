from __future__ import annotations


from typing import Optional,Tuple, TYPE_CHECKING

from IMPULSE import color
from IMPULSE import exceptions
from math import sqrt
from random import randint



if TYPE_CHECKING:
    from IMPULSE.engine import Engine
    from IMPULSE.entity import Entity, Actor, Item


class Action:
    def __init__(self, entity:Actor) -> None:
        super().__init__()
        self.entity = entity
    @property
    def engine(self) -> Engine:
        return self.entity.gamemap.engine

    def perform(self) -> None:
        """Perform this action with the objects needed to determine its scope.

        `self.engine` is the scope this action is being performed in.

        `self.entity` is the object performing the action.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()

class EscapeAction(Action):
    def perform(self) -> None:
        raise SystemExit()

class WaitAction(Action):
    def perform(self) -> None:
        self.entity.fighter.heal_FP(1)

class ActionWithDirection(Action):
    def __init__(self, entity: Actor, dx: int, dy: int):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self) -> Tuple[int, int]:
        """Returns this actions destination."""
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Optional[Entity]:
        """Return the blocking entity at this actions destination.."""
        return self.engine.game_map.get_blocking_entity_at_location(*self.dest_xy)

    @property
    def target_actor(self) -> Optional[Actor]:
        """Return the actor at this actions destination."""
        return self.engine.game_map.get_actor_at_location(*self.dest_xy)

    def perform(self) -> None:
        raise NotImplementedError()

class AttackAction(Action):
    def __init__(self, entity: Actor, x: int, y: int, damage_type: str=""):
        super().__init__(entity)
        self.dest_x=x
        self.dest_y=y
        self.damage_type=damage_type

    @property
    def dest_xy(self) -> Tuple[int, int]:
            """Returns this actions destination."""
            return self.dest_x, self.dest_y

    @property
    def target_actor(self) -> Optional[Actor]:
        """Return the actor at this actions destination."""
        return self.engine.game_map.get_actor_at_location(*self.dest_xy)

    @property
    def distance_to_target(self) -> int:

        dx=self.entity.x-self.dest_x
        dy=self.entity.y-self.dest_y

        distance=sqrt(dx**2 + dy**2)

        return int(distance)

    def get_weapon_slots(self):
        two_hander_flag=False
        slotList=[]
        for slot in self.entity.equipment.slots:
            weapon=getattr(self.entity.equipment,slot)
            if weapon is not None:
                if not two_hander_flag:
                    two_hander_flag=weapon.equippable.two_handed
                    range=weapon.equippable.range_bonus


                    if (range >= self.distance_to_target):

                        if not weapon.equippable.is_empty():

                            slotList.append(slot)
                        else:
                            self.engine.message_log.add_message(
                            f"You squeeze the trigger, but the {weapon.name} is empty!", color.impossible)
        return slotList

    def attack_with_slot(self, slot, target,color):
        item_in_slot=getattr(self.entity.equipment,slot)
        if getattr(item_in_slot.equippable,"ammo_count") is not None:
            item_in_slot.equippable.decrement_ammo()

        damage = self.entity.fighter.attack_from_slot(slot) - target.fighter.defense

        self.engine.message_log.add_message(
        f"{self.entity.name.upper()} attacks the {target.name} with {item_in_slot.name}!", color)
        damage_type=item_in_slot.damage_type
        hit_floor=item_in_slot.equippable.hit_floor
        return damage, damage_type, hit_floor

class MeleeAction(AttackAction):

    def perform(self) -> None:
        target = self.target_actor
        if not target:
            raise exceptions.Impossible("Nothing to attack.")
        if self.entity is self.engine.player:
            attack_color = color.player_atk
        else:
            attack_color = color.enemy_atk

        total_damage=0

        if hasattr(self.entity,"equipment"):
            for slot in self.get_weapon_slots():
                item = getattr(self.entity.equipment, slot)
                attack_times = item.equippable.attack_times
                for i in range(attack_times):
                    damage, damage_type, null=self.attack_with_slot(slot,target,attack_color)
                    total_damage+=target.fighter.take_damage(damage,damage_type)

        else:
            damage= self.entity.fighter.attack - target.fighter.defense
            damage_type=self.entity.damage_type
            total_damage += target.fighter.take_damage(damage, damage_type)


        attack_desc = f"{self.entity.name.upper()} hits {target.name}"
        if total_damage>0:

            self.engine.message_log.add_message(
                f"{attack_desc} for {total_damage} hp", attack_color
            )


        else:
            self.engine.message_log.add_message(
                f"{attack_desc} but does no damage.", attack_color
            )
        self.entity.set_wait_counter(5)

class RangedAttackAction(AttackAction):

    def blocking_actors(self) -> Optional[list[Actor]]:
        blocking_actors = self.engine.game_map.get_actors_between_2_points(self.entity.x,self.entity.y,self.dest_x,self.dest_y)
        if blocking_actors:
            return blocking_actors
        else:
            return None

    def perform(self) -> None:
        hit_ceiling=20
        target = self.target_actor
        blocking_actors=self.blocking_actors

        if not target:
            raise exceptions.Impossible("No Target Acquired")

        if self.distance_to_target > self.entity.fighter.max_range:
            raise exceptions.Impossible("Target Out of Range ")

        if self.entity is self.engine.player:
            attack_color = color.player_atk
        else:
            attack_color = color.enemy_atk



        total_damage=0
        accuracy = self.entity.fighter.accuracy
        dodge=target.fighter.dodge
        miss_message=True

        if hasattr(self.entity,"equipment"):
            for slot in self.get_weapon_slots():
                item = getattr(self.entity.equipment,slot)
                attack_times=item.equippable.attack_times
                for i in range(attack_times):
                    damage, damage_type, hit_floor = self.attack_with_slot(slot, target, attack_color)

                    hit_roll = randint(hit_floor + accuracy - dodge, hit_ceiling)
                    target_hit = (hit_roll > 10)
                    if target_hit:
                        miss_message=False

                        total_damage += target.fighter.take_damage(damage, damage_type)
                    else:
                        self.engine.message_log.add_message( f"{self.entity.name.upper()} misses the {target.name}")

        else:
            hit_roll = randint(10 + accuracy -  dodge, hit_ceiling)
            target_hit = (hit_roll > 10)
            if target_hit:
                miss_message = False
                damage = self.entity.fighter.attack - target.fighter.defense
                damage_type = self.entity.damage_type
                total_damage += target.fighter.take_damage(damage, damage_type)
            else:
                self.engine.message_log.add_message(f"{self.entity.name.upper()} misses the {target.name}")

        attack_desc = f"{self.entity.name.upper()} hits {target.name}"


        if not miss_message:
            if total_damage > 0:
                if target_hit:
                    self.engine.message_log.add_message(
                        f"{attack_desc} for {total_damage} hp", attack_color
                    )

            else:
                self.engine.message_log.add_message(
                    f"{attack_desc}, but the attack glances off!", attack_color)

        self.entity.set_wait_counter(5)

class MovementAction(ActionWithDirection):
    def perform(self) -> None:
            dest_x, dest_y = self.dest_xy

            if not self.engine.game_map.in_bounds(dest_x, dest_y):
                raise exceptions.Impossible("Ye cannot go that far")  # Destination is out of bounds.
            if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
                raise exceptions.Impossible("WALLLLL")
            if self.engine.game_map.get_blocking_entity_at_location(dest_x,dest_y):
                raise exceptions.Impossible("THING THERE")

            self.entity.move(self.dx, self.dy)
            self.entity.set_wait_counter(10-self.entity.fighter.speed)


class BumpAction(ActionWithDirection):
    def perform(self) -> None:
        if self.target_actor:
            if self.target_actor.name != "doll":
                return  RangedAttackAction(self.entity, self.target_actor.x, self.target_actor.y).perform()
            else:
                return SwapAction(self.entity,self.target_actor).perform()
        else:

            return MovementAction(self.entity, self.dx, self.dy).perform()

class HackAction(Action) :
    def __init__(self, entity: Actor, target_xy: [int,int]):
        super().__init__(entity)
        self.target_xy = target_xy
        self.target_x=target_xy[0]
        self.target_y=target_xy[1]

    def target_actor(self) -> Optional[Actor]:
        return self.engine.game_map.get_actor_at_location(self.target_x, self.target_y)

    def perform(self) -> bool:
        hacker = self.entity
        target = self.target_actor()
        #print("ATTEMPING HACK ACTION", self.target_x,self.target_y)

        if not (self.engine.game_map.visible[self.target_x],self.engine.game_map.visible[self.target_y]):
            self.engine.message_log.add_message("No Target Selected", color.invalid)
            return False
        if not target:
            self.engine.message_log.add_message("No Target Selected", color.invalid)
            return False
        if target is hacker:
            self.engine.message_log.add_message("Invalid Target", color.invalid)
            return False
        if not hasattr(target,"cyberware"):
            self.engine.message_log.add_message("Invalid Target: No Cyberware Detected", color.invalid)
            return False
        if target.fighter.focus>=hacker.fighter.focus:
            self.engine.message_log.add_message(f"ERROR: UNABLE TO BREACH DEFENSES")

        self.engine.message_log.add_message(
            f"you successfully hack the {target.name}", color.status_effect
        )

        return True

class ItemAction(Action):
    def __init__(
    self, entity: Actor, item: Item, target_xy: Optional[Tuple[int,int]] = None
    ):
        super().__init__(entity)
        self.item = item
        if not target_xy:
            target_xy = entity.x, entity.y
        self.target_xy =  target_xy

    @property
    def target_actor(self) -> Optional[Actor]:
        return self.engine.game_map.get_actor_at_location(*self.target_xy)

    def perform(self) -> None:
        self.entity.set_wait_counter(5)
        if self.item.consumable:
            self.item.consumable.activate(self)

class DropItem(ItemAction):
    def perform(self) -> None:
        self.entity.set_wait_counter(5)
        if self.entity.equipment.item_is_equipped(self.item):
            self.entity.equipment.toggle_equip(self.item)

        self.entity.inventory.drop(self.item)

class ModAction(Action):
    def __init__(self, entity: Actor, item: Item):
        super().__init__(entity)
        self.item=item

    def perform(self) -> None:
        self.entity.cyberware.toggle_equip(self.item, add_message=True)
        self.entity.inventory.items.remove(self.item)
        if self.entity.cyberware.has_slot_perk:
            self.entity.equipment.toggle_bonus()


class EquipAction(Action):
    def __init__(self, entity: Actor, item: Item, hand: Optional[int]= None):
        super().__init__(entity)
        self.item = item
        if hand is not None:
            self.hand = hand

    def perform(self) -> None:
       # print("call toggle equip")
       self.entity.set_wait_counter(5)
       if hasattr(self,"hand"):
           print(self.hand)
           self.entity.equipment.toggle_equip(self.item, add_message=True,hand=self.hand)
       else:
           self.entity.equipment.toggle_equip(self.item,add_message=True,)

class PickupAction(Action):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.entity.set_wait_counter(1)

    def perform(self) -> None:
        actor_location_x = self.entity.x
        actor_location_y = self.entity.y
        inventory = self.entity.inventory

        for item in self.engine.game_map.items:
            if actor_location_x == item.x and actor_location_y == item.y:
                if len(inventory.items) >= inventory.capacity:
                    raise exceptions.Impossible("You tummy is too big and round")

                self.engine.game_map.entities.remove(item)
                item.parent = self.entity.inventory
                inventory.items.append(item)

                self.engine.message_log.add_message(f"you vored the {item.name}")
                return
        raise exceptions.Impossible("you scrounge around on the ground for scraps")

class TakeStairsAction(Action):
    def perform(self) -> None:

        if(self.entity.x, self.entity.y) == self.engine.game_map.downstairs_location:
            self.engine.game_world.generate_floor()
            self.engine.message_log.add_message(
                "GOOD JOB....... FOR NOW!!!!!", color.descend
            )
        elif(self.entity.x, self.entity.y) == self.engine.game_map.goal_location:
            self.engine.message_log.add_message(
                "YAY!!! YOU HAVE A PUSSY NOW!"
            )
            self.engine.game_win=True
        else:
            raise exceptions.Impossible("you CANNOT descend to the NEXT LEVEL! NO STAIRS LMAO!")

class SwapAction(Action):
    def __init__(self,entity: Actor,target:Actor):
        self.entity=entity
        self.target=target
        super().__init__(entity)

    def perform(self) -> None:
        actor1x=self.entity.x
        actor1y=self.entity.y
        self.entity.x=self.target.x
        self.entity.y=self.target.y
        self.target.x=actor1x
        self.target.y=actor1y
        self.entity.set_wait_counter(5)
        self.target.set_wait_counter(5)

class SelfDestructAction(Action):
    def __init__(self,entity: Actor,radius: int, damage: int):
        self.entity=entity
        self.radius=radius
        self.damage=damage
        super().__init__(entity)

    def perform(self) -> None:

        for actor in self.engine.game_map.actors:
            distance=actor.distance(self.entity.x,self.entity.y)
            print(actor.name,distance,self.radius)
            if distance <= self.radius:

                self.engine.message_log.add_message(
                    f"the {actor.name} gets fuuuuucked up for {self.damage} hit points"
                )
                actor.fighter.take_damage(self.damage)

        self.entity.fighter.die()
