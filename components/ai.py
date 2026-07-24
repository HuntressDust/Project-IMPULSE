from   __future__ import annotations
from typing import List, Tuple,TYPE_CHECKING, Optional
import random
import numpy as np
import tcod


from IMPULSE.actions import Action, MeleeAction,MovementAction,WaitAction, BumpAction,SelfDestructAction, RangedAttackAction,ChargeAction,HarrassmentAction
from IMPULSE.color import ally, doll, combat_doll,angel



if TYPE_CHECKING:
    from IMPULSE.entity import Actor

class BaseAI(Action):
    def getDistance(self,xf,yf):
        dx =xf - self.entity.x
        dy = yf - self.entity.y
        return max(abs(dx), abs(dy))

    def perform(self) -> None:
        raise NotImplementedError()
    def confuse(self):
        self.entity.ai=ConfusedEnemy(self.entity)
    def reset_ai(self, ai:BaseAI):
        self.entity.ai=ai
    def get_path_to(self, dest_x: int, dest_y: int) -> List[Tuple[int, int]]:
        cost = np.array(self.entity.gamemap.tiles["walkable"], dtype = np.int8)

        for entity in self.entity.gamemap.entities:
            if entity.blocks_movement and cost[entity.x, entity.y]:
                cost[entity.x, entity.y] += 10

        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pathfinder = tcod.path.Pathfinder(graph)

        pathfinder.add_root((self.entity.x, self.entity.y))

        path: List[List[int]] = pathfinder.path_to((dest_x, dest_y))[1:].tolist()


        return [(index[0], index[1]) for index in path]

class Idle(BaseAI):
    def __init__(self, entity: Actor):
        super().__init__(entity)
    def perform(self) -> None:
        pass

class HostileEnemy(BaseAI):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int,int]] =[]
        self.target=None
        self.is_hostile=True
        self.target_list = []

    def has_target(self) -> bool:
        if self.target is not None:
            return self.target.is_alive
        else:
            return False

    def update_target_list(self):
        list_size = len(self.engine.player.controller.minion_list) + 1
        if len(self.target_list) < list_size:
            self.target_list = [self.engine.player] + self.engine.player.controller.minion_list

    def pick_target(self):
        index = random.randint(0, len(self.target_list) - 1)
        return self.target_list[index]

class MeleeEnemy(HostileEnemy):
    def __init__(self, entity: Actor):
        super().__init__(entity)

    def perform(self) -> None:
        list_size = len(self.target_list)
        self.update_target_list()
        if (len(self.target_list) != list_size) or not self.has_target():
            self.target=self.pick_target()
        target=self.target
        dx =target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))

        if self.engine.game_map.visible[self.entity.x, self.entity.y]:
            if distance <=1:
                #print("Enemy ATTACK")
                return RangedAttackAction(self.entity, target.x, target.y).perform()
            self.path = self.get_path_to(target.x, target.y)

            if self.path:
                dest_x, dest_y = self.path.pop(0)
                return MovementAction( self.entity,
                                       dest_x - self.entity.x,
                                       dest_y - self.entity.y,).perform()


        elif self.path and self.entity.give_chase:
            dest_x, dest_y = self.path.pop(0)
            return MovementAction(self.entity,
                                  dest_x - self.entity.x,
                                  dest_y - self.entity.y, ).perform()

        else: return WaitAction(self.entity).perform()

class MaidAI(MeleeEnemy):
    def __init__(self, entity: Actor):
        super().__init__(entity)

    def perform(self) -> None:
        list_size = len(self.target_list)
        self.update_target_list()
        if (len(self.target_list) != list_size) or not self.has_target():
            self.target=self.pick_target()
        target=self.target
        dx =target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))

        if self.engine.game_map.visible[self.entity.x, self.entity.y]:
            if distance <=1:
                #print("Enemy ATTACK")
                return RangedAttackAction(self.entity, target.x, target.y).perform()
            self.path = self.get_path_to(target.x, target.y)

            if self.path:
                dest_x, dest_y = self.path.pop(0)
                return MovementAction( self.entity,
                                       dest_x - self.entity.x,
                                       dest_y - self.entity.y,).perform()


        elif self.path and self.entity.give_chase:
            dest_x, dest_y = self.path.pop(0)
            return MovementAction(self.entity,
                                  dest_x - self.entity.x,
                                  dest_y - self.entity.y, ).perform()

        else:
            while len(self.path) < 1:
                rand_index = random.randint(0, len(self.engine.game_map.entities) - 1)
                wander_target = list(self.engine.game_map.entities)[rand_index]

                self.path=self.get_path_to(wander_target.x,wander_target.y)
            dest_x, dest_y = self.path.pop(0)
            return MovementAction(self.entity,
                                  dest_x - self.entity.x,
                                  dest_y - self.entity.y, ).perform()


class RangedEnemy(HostileEnemy):
    def __init__(self, entity: Actor):
        super().__init__(entity)

    def perform(self) -> None:
        list_size = len(self.target_list)
        self.update_target_list()
        if (len(self.target_list) != list_size) or not self.has_target():
            self.target=self.pick_target()
        dx =self.target.x - self.entity.x
        dy = self.target.y - self.entity.y
        distance = max(abs(dx), abs(dy))

        if self.engine.game_map.visible[self.entity.x, self.entity.y]:
            if distance <=self.entity.fighter.max_range:

                return RangedAttackAction(self.entity, self.target.x, self.target.y).perform()
            self.path = self.get_path_to(self.target.x, self.target.y)

            if self.path:
                dest_x, dest_y = self.path.pop(0)
                return MovementAction( self.entity,
                                       dest_x - self.entity.x,
                                       dest_y - self.entity.y,).perform()

        elif self.path and self.entity.give_chase:
            dest_x, dest_y = self.path.pop(0)
            return MovementAction(self.entity,
                                  dest_x - self.entity.x,
                                  dest_y - self.entity.y, ).perform()
        else: return WaitAction(self.entity).perform()

class chaser(RangedEnemy):

    def perform(self) -> None:
        list_size = len(self.target_list)
        self.update_target_list()
        if not self.has_target():
            self.target=self.engine.player
        dx =self.target.x - self.entity.x
        dy = self.target.y - self.entity.y
        distance = max(abs(dx), abs(dy))

        harrass_range = self.entity.fighter.max_range

        danger_range = self.target.fighter.max_range
        if danger_range >= self.entity.fighter.max_range:
            danger_range = harrass_range - 1
        if self.engine.game_map.visible[self.entity.x, self.entity.y]:
            print(distance, danger_range, harrass_range)
            if distance <= harrass_range and distance > danger_range:
                self.path = self.get_path_to(self.target.x, self.target.y)
                return HarrassmentAction(self.entity, radius=self.entity.fighter.max_range).perform()
            else:
                for thing in self.engine.game_map.entities:

                    adx = self.entity.x - thing.x
                    if dx * adx >= 0:
                        ady = self.entity.y - thing.y
                        if dy * ady >= 0:
                            self.path = self.get_path_to(thing.x, thing.y)
                            break
            if distance > self.entity.fighter.max_range:
                self.path = self.get_path_to(self.target.x, self.target.y)

            if self.path:
                dest_x, dest_y = self.path.pop(0)
                return MovementAction(self.entity,
                                      dest_x - self.entity.x,
                                      dest_y - self.entity.y, ).perform()
            return WaitAction(self.entity).perform()

        elif self.path and self.entity.give_chase:
            dest_x, dest_y = self.path.pop(0)
            return MovementAction(self.entity,
                                  dest_x - self.entity.x,
                                  dest_y - self.entity.y, ).perform()
        else: return WaitAction(self.entity).perform()

class charger(RangedEnemy):
    def __init__(self, entity: Actor, ):
        super().__init__(entity)
        self.cooldown = 0

    def perform(self) -> None:
        list_size = len(self.target_list)
        self.update_target_list()
        if (len(self.target_list) != list_size) or not self.has_target():
            self.target=self.pick_target()
        dx =self.target.x - self.entity.x
        dy = self.target.y - self.entity.y
        distance = max(abs(dx), abs(dy))
        if self.cooldown > 0:
            self.cooldown -= 1

        if self.engine.game_map.visible[self.entity.x, self.entity.y]:
            if distance <= self.entity.fighter.max_range:
                if self.cooldown == 0:
                    self.cooldown += 10
                    self.engine.message_log.add_message(f"The {self.entity.name} begins to charge!")
                    self.path = self.get_path_to(self.target.x, self.target.y)
                    dest_x, dest_y = self.path.pop(0)

                    return ChargeAction(self.entity,
                                        dest_x - self.entity.x, dest_y - self.entity.y, recursion=0).perform()
            if distance <= 1:
                return RangedAttackAction(self.entity, self.target.x, self.target.y).perform()

            self.path = self.get_path_to(self.target.x, self.target.y)

            if self.path:
                dest_x, dest_y = self.path.pop(0)
                return MovementAction(self.entity,
                                      dest_x - self.entity.x,
                                      dest_y - self.entity.y, ).perform()

            return WaitAction(self.entity).perform()
        elif self.path and self.entity.give_chase:
            dest_x, dest_y = self.path.pop(0)
            return MovementAction(self.entity,
                                  dest_x - self.entity.x,
                                  dest_y - self.entity.y, ).perform()
        else: return WaitAction(self.entity).perform()


class Angel(HostileEnemy):
    def __init__(self, entity: Actor):
        super().__init__(entity)

    def perform(self) -> None:
        list_size = len(self.target_list)
        self.update_target_list()
        if (len(self.target_list) != list_size) or not self.has_target():
            self.target=self.pick_target()
        dx =self.target.x - self.entity.x
        dy = self.target.y - self.entity.y
        distance = max(abs(dx), abs(dy))

        if self.engine.game_map.visible[self.entity.x, self.entity.y]:
            if self.entity.fighter.hp > self.entity.fighter.max_hp/2:


                if distance < self.entity.fighter.max_range and distance>1:
                    #print("Ranged attack")
                    return RangedAttackAction(self.entity, self.target.x, self.target.y).perform()
                elif distance<=1:
                    #print("Melee attack")
                    return RangedAttackAction(self.entity, self.target.x, self.target.y).perform()
                self.path = self.get_path_to(self.target.x, self.target.y)

                if self.path:
                    dest_x, dest_y = self.path.pop(0)
                    #print("moving")
                    return MovementAction(self.entity,
                                          dest_x - self.entity.x,
                                          dest_y - self.entity.y, ).perform()

            else:

                if distance <= 1:
                    return RangedAttackAction(self.entity, dx, dy).perform()
                self.path = self.get_path_to(self.target.x, self.target.y)

                if self.path:
                    dest_x, dest_y = self.path.pop(0)
                    return MovementAction(self.entity,
                                          dest_x - self.entity.x,
                                          dest_y - self.entity.y, ).perform()

        else:
            self.path = self.get_path_to(20, 12)
            if len(self.path)>0:
                dest_x, dest_y = self.path.pop(0)
                return MovementAction(self.entity,
                                      dest_x - self.entity.x,
                                      dest_y - self.entity.y, ).perform()
            else:
                return WaitAction(self.entity).perform()





class ConfusedEnemy(HostileEnemy):
    def __init__(
            self, entity: Actor,):
        super().__init__(entity)

    def perform(self) -> None:

        dir_x, dir_y = random.choice(
            [
                (-1, -1),  # Northwest
                (0, -1),  # North
                (1, -1),  # Northeast
                (-1, 0),  # West
                (1, 0),  # East
                (-1, 1),  # Southwest
                (0, 1),  # South
                (1, 1),  # Southeast
            ]
        )


        return MovementAction(self.entity, dir_x, dir_y,).perform()

class CombatDoll(MeleeEnemy):

    def perform(self) -> None:
        print(self.entity.fighter.hp ,self.entity.fighter.max_hp,self.entity.fighter.max_hp/ 4)
        if self.entity.fighter.hp > self.entity.fighter.max_hp // 4:
            list_size = len(self.target_list)
            self.update_target_list()
            if (len(self.target_list) != list_size) or not self.has_target():
                self.target=self.pick_target()
            target=self.target
            dx =target.x - self.entity.x
            dy = target.y - self.entity.y
            distance = max(abs(dx), abs(dy))

            if self.engine.game_map.visible[self.entity.x, self.entity.y]:
                if distance <=1:
                    #print("Enemy ATTACK")
                    return RangedAttackAction(self.entity, target.x, target.y).perform()
                self.path = self.get_path_to(target.x, target.y)

                if self.path:
                    dest_x, dest_y = self.path.pop(0)
                    return MovementAction( self.entity,
                                           dest_x - self.entity.x,
                                           dest_y - self.entity.y,).perform()


            elif self.path and self.entity.give_chase:
                dest_x, dest_y = self.path.pop(0)
                return MovementAction(self.entity,
                                      dest_x - self.entity.x,
                                      dest_y - self.entity.y, ).perform()

            else: return WaitAction(self.entity).perform()
        else:
            self.target=self.engine.player
            self.entity.ai=CombatDoll_SelfDestruct(self.entity,timer=4, )
            self.entity.ai.perform()

class Ally(BaseAI):
    def __init__(self, entity: Actor, target:Optional[Actor]=None):
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []
        self.target=target
        self.is_ally=True

    def AttackTarget(self):
        dx =self.target.x - self.entity.x
        dy = self.target.y - self.entity.y
        distance = max(abs(dx), abs(dy))
        print(distance)
        if self.engine.game_map.visible[self.entity.x, self.entity.y]:
            if distance <=self.entity.fighter.max_range:

                return RangedAttackAction(self.entity, self.target.x, self.target.y).perform()
            self.path = self.get_path_to(self.target.x, self.target.y)

            if self.path:
                self.move_to()
            return WaitAction(self.entity).perform()

    def move_to(self):
        dest_x, dest_y = self.path.pop(0)
        return MovementAction(self.entity,
                              dest_x - self.entity.x,
                              dest_y - self.entity.y, ).perform()


    def IsNearPlayer(self)-> bool:
        target=self.engine.player
        dx =target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))
        return distance <3

    def pickTile(self):
        player_x=self.engine.player.x
        player_y=self.engine.player.y
        target_x=player_x
        target_y=player_y
        min_distance=1000
        for dx in range(-2,2):
            for dy in range(-2,2):
                posx=player_x+dx
                posy=player_y+dy
                if self.engine.game_map.tiles[posx,posy]["walkable"]:
                    distance=self.getDistance(posx,posy)
                    if distance<min_distance:
                        target_x=posx
                        target_y=posy
                        min_distance=distance
        return target_x, target_y

    def has_valid_target(self):
        if self.target:
            if not  self.target.is_alive:
                self.engine.message_log.add_message(f"The {self.entity.name} calls out: \"Target Eliminated\"", ally)
                return False
            if self.engine.player.controller.is_actor_controlled(self.target):
                return False
            if not self.target in self.entity.gamemap.actors:
                return False
            return True
        else:
            return False

    def pickTarget(self):
        min_distance=1000
        for entity in self.engine.game_map.actors:
             if self.engine.game_map.visible[entity.x, entity.y]:
                 if hasattr(entity.ai,"is_hostile"):
                     distance=self.getDistance(entity.x,entity.y)
                     if min_distance>distance:
                         self.target=entity
                         min_distance=distance

    def perform(self) -> None:
        if self.entity.fighter.hp > self.entity.fighter.max_hp/4  or self.entity.char != 'd':
            if not self.has_valid_target():
                self.target = None
                self.pickTarget()
                if self.has_valid_target():
                    self.engine.message_log.add_message(f"The {self.entity.name} calls out: \"Engaging {self.target.name}!\"", ally)
            if  self.has_valid_target():
                self.AttackTarget()
            else:
                if not self.IsNearPlayer():
                    dest_x, dest_y = self.pickTile()
                    self.path = self.get_path_to(dest_x,dest_y)
                    self.move_to()
                else:
                    return WaitAction(self.entity).perform()
        else:
            self.entity.ai=SelfDestruct(self.entity,timer=4, )
            self.entity.ai.perform()

class SelfDestruct(Ally):

    def __init__(self, entity: Actor, timer=int, target:Optional[Actor]=None):
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []
        self.target=target
        self.timer=timer
        self.init_timer=timer
        self.radius=3

    def decrement_timer(self):
        self.timer-=1


    def move_to_target(self):
        dx =self.target.x - self.entity.x
        dy = self.target.y - self.entity.y
        distance = max(abs(dx), abs(dy))

        if self.engine.game_map.visible[self.entity.x, self.entity.y]:
            if distance <= 1:
                self.entity.set_wait_counter(5)
                return WaitAction(self.entity).perform()
            self.path = self.get_path_to(self.target.x, self.target.y)

            if self.path:
                self.move_to()
            self.entity.set_wait_counter(5)
            return WaitAction(self.entity).perform()

    def move_to(self):
        dest_x, dest_y = self.path.pop(0)
        return MovementAction(self.entity,
                              dest_x - self.entity.x,
                              dest_y - self.entity.y, ).perform()

    def draw_box(self):
        self.engine.add_danger_box(self.radius,self.entity)

    def perform(self) -> None:
        if self.timer >0:

            if self.timer==self.init_timer:
                self.draw_box()
                self.engine.message_log.add_message(f"The {self.entity.name} calls out: \"This one apologizes, miss.",ally)
            if self.entity.fighter.hp < 3:
                self.timer-=2
            if  self.timer==int((self.init_timer/2)):
                self.engine.message_log.add_message(f"...It is sorry it could not protect you...",ally)
            elif self.timer<=1:
                self.engine.message_log.add_message(f"SELF DESTRUCTION IMMINENT",ally),

            if not self.has_valid_target():
                self.target = None
                self.pickTarget()

            self.decrement_timer()

            if self.has_valid_target():
                self.move_to_target()

            else:
                self.entity.set_wait_counter(5)
                return WaitAction(self.entity).perform()



        else:
            return SelfDestructAction(self.entity, radius=3, damage=10).perform()

class CombatDoll_SelfDestruct(SelfDestruct):

    def __init__(self, entity: Actor, timer=int, target:Optional[Actor]=None):
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []
        self.target=target
        self.timer=timer
        self.init_timer=timer
        self.radius=3
        self.is_ally=None
        self.is_hostile=True


    def perform(self) -> None:
        if self.timer >0:

            if self.timer==self.init_timer:
                self.draw_box()
                self.engine.message_log.add_message(f"The {self.entity.name} tosses its hair from its face.",combat_doll)
            if self.entity.fighter.hp < 3:
                self.timer-=2
            if  self.timer==int((self.init_timer/2)):
                self.engine.message_log.add_message(f"Hatred burns in the {self.entity.name}'s fabricated eyes.",combat_doll)
            elif self.timer<=1:
                self.engine.message_log.add_message(f"The {self.entity.name} scoffs: \"Nothing personal.\"",combat_doll),

            if not self.has_valid_target():
                self.target = None
                self.pickTarget()

            self.decrement_timer()

            if self.has_valid_target():
                self.move_to_target()

            else:
                self.entity.set_wait_counter(5)
                return WaitAction(self.entity).perform()


        else:
            return SelfDestructAction(self.entity, radius=3, damage=10).perform()

