from   __future__ import annotations
from typing import List, Tuple,TYPE_CHECKING, Optional
import random
import numpy as np
import tcod
from IMPULSE.actions import Action, MeleeAction,MovementAction,WaitAction, BumpAction
from color import ally

if TYPE_CHECKING:
    from entity import Actor

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


class HostileEnemy(BaseAI):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int,int]] =[]
    def perform(self) -> None:
        target=self.engine.player
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

class ConfusedEnemy(BaseAI):
    def __init__(
            self, entity: Actor, previous_ai: Optional[BaseAI], turns_remaining: int):
        super().__init__(entity)
        self.previous_ai = previous_ai
        self.turns_remaining = turns_remaining

    def perform(self) -> None:

        if self.turns_remaining <=0:
            self.engine.message_log.add_message(
                f"The {self.entity.name} has come down from its high"
            )
            self.entity.ai = self.previous_ai
        else:
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
            self.turns_remaining -=1

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
                print("attacking")
                return MeleeAction(self.entity, dx, dy).perform()
            self.path = self.get_path_to(self.target.x, self.target.y)

            if self.path:
                print("moving")
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
            return self.target.is_alive
        else:
            print("no Targets")
            return False

    def pickTarget(self):
        min_distance=1000

        for entity in self.engine.game_map.entities:
            print(entity.name)
            if hasattr(entity,"ai"):

                if isinstance(entity.ai,HostileEnemy):

                 if self.engine.game_map.visible[entity.x, entity.y]:

                     distance=self.getDistance(entity.x,entity.y)
                     print(distance)
                     if min_distance>distance:
                           self.target=entity


    def perform(self) -> None:
        if not self.has_valid_target():
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











