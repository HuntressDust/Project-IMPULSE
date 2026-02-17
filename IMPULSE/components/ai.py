from   __future__ import annotations
from typing import List, Tuple,TYPE_CHECKING, Optional
import random
import numpy as np
import tcod
from IMPULSE.actions import Action, MeleeAction,MovementAction,WaitAction, BumpAction,SelfDestructAction, RangedAttackAction
from IMPULSE.color import ally



if TYPE_CHECKING:
    from IMPULSE.entity import Actor

class BaseAI(Action):
    def getDistance(self,xf,yf):
        dx =xf - self.entity.x
        dy = yf - self.entity.y
        return max(abs(dx), abs(dy))

    def perform(self) -> None:
        raise NotImplementedError()

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

    def has_target(self) -> bool:
        if self.target is not None:
            return self.target.is_alive
        else:
            return False


    def pick_target(self):
        player=self.engine.player
        target_list =[]
        target_list.append(player)
        target_list=target_list+player.controller.minion_list

        index = random.randint(0,len(target_list)-1)
        return target_list[index]

class MeleeEnemy(HostileEnemy):
    def __init__(self, entity: Actor):
        super().__init__(entity)

    def perform(self) -> None:
        if not self.has_target():
            self.target=self.pick_target()
        target=self.target
        dx =target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))

        if self.engine.game_map.visible[self.entity.x, self.entity.y]:
            if distance <=1:
                return MeleeAction(self.entity, dx, dy).perform()
            self.path = self.get_path_to(target.x, target.y)

            if self.path:
                dest_x, dest_y = self.path.pop(0)
                return MovementAction( self.entity,
                                       dest_x - self.entity.x,
                                       dest_y - self.entity.y,).perform()
            return WaitAction(self.entity).perform()

class RangedEnemy(HostileEnemy):
    def __init__(self, entity: Actor):
        super().__init__(entity)

    def perform(self) -> None:
        if not self.has_target():
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
            return WaitAction(self.entity).perform()


class Angel(HostileEnemy):
    def __init__(self, entity: Actor):
        super().__init__(entity)

    def perform(self) -> None:
        self.target = self.pick_target()
        dx = self.target.x - self.entity.x
        dy = self.target.y - self.entity.y
        distance = max(abs(dx), abs(dy))

        if self.entity.fighter.hp > self.entity.fighter.max_hp/2:

            if self.engine.game_map.visible[self.entity.x, self.entity.y]:
                if distance < self.entity.fighter.max_range and distance>1:
                    print("Ranged attack")
                    return RangedAttackAction(self.entity, self.target.x, self.target.y).perform()
                elif distance<=1:
                    print("Melee attack")
                    return MeleeAction(self.entity, dx, dy).perform()
                self.path = self.get_path_to(self.target.x, self.target.y)

                if self.path:
                    dest_x, dest_y = self.path.pop(0)
                    print("moving")
                    return MovementAction(self.entity,
                                          dest_x - self.entity.x,
                                          dest_y - self.entity.y, ).perform()
                return WaitAction(self.entity).perform()

        else:
            if self.engine.game_map.visible[self.entity.x, self.entity.y]:
                if distance <= 1:
                    return MeleeAction(self.entity, dx, dy).perform()
                self.path = self.get_path_to(self.target.x, self.target.y)

                if self.path:
                    dest_x, dest_y = self.path.pop(0)
                    return MovementAction(self.entity,
                                          dest_x - self.entity.x,
                                          dest_y - self.entity.y, ).perform()
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


        return BumpAction(self.entity, dir_x, dir_y,).perform()





class Ally(BaseAI):
    def __init__(self, entity: Actor, target:Optional[Actor]=None):
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []
        self.target=target

    def AttackTarget(self):
        dx =self.target.x - self.entity.x
        dy = self.target.y - self.entity.y
        distance = max(abs(dx), abs(dy))
        print(distance)
        if self.engine.game_map.visible[self.entity.x, self.entity.y]:
            if distance <= 1:

                return MeleeAction(self.entity, dx, dy).perform()
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
                self.engine.message_log.add_message(f"Target Eliminated", ally)
                return False
            if self.engine.player.controller.is_actor_controlled(self.target):
                return False
            return True
        else:
            return False

    def pickTarget(self):
        min_distance=1000
        for entity in self.engine.game_map.entities:
            if hasattr(entity,"ai"):
                 if self.engine.game_map.visible[entity.x, entity.y]:
                     if isinstance(entity.ai, MeleeEnemy) or isinstance(entity.ai,RangedEnemy):
                         distance=self.getDistance(entity.x,entity.y)
                         if min_distance>distance:
                             self.target=entity
                             min_distance=distance

    def perform(self) -> None:
        if self.entity.fighter.hp > self.entity.fighter.max_hp/4:
            if not self.has_valid_target():
                self.target = None
                self.pickTarget()
                if self.has_valid_target():
                    self.engine.message_log.add_message(f"Engaging {self.target.name}!", ally)
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

        viewport = self.engine.game_map.get_viewport()
        x=self.entity.x
        y=self.entity.y
        self.engine.danger_x = x- viewport[0]+viewport[4]
        self.engine.danger_y = y-viewport[1]+1
        self.engine.danger_rad = self.radius
        self.engine.danger_on = True



    def perform(self) -> None:

        if self.timer >0:
            self.draw_box()

            if self.timer==self.init_timer:
                self.engine.message_log.add_message(f"This one apologizes, miss.",ally)
            elif  self.timer==int((self.init_timer/2)):
                self.engine.message_log.add_message(f"It is sorry it could not protect you.",ally)
            elif self.timer==1:
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
            self.engine.danger_on=False
            return SelfDestructAction(self.entity, radius=3, damage=10).perform()
















