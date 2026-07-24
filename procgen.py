from __future__ import annotations
from typing import Iterator,Tuple , Dict, List, TYPE_CHECKING

from IMPULSE.entity_factories import rapier
from IMPULSE.game_map import GameMap
from IMPULSE import entity_factories
from IMPULSE import tile_types
import tcod
import random
import copy

import numpy as np

if TYPE_CHECKING:
    from IMPULSE.engine import Engine
    from IMPULSE.entity import Entity


max_consumables_by_floor = [
    (1, 1),
    (4, 2),
    (8, 3)
]
max_equipment_by_floor = [
    (1, 1),
]
max_monsters_by_floor = [
    (1, 2),
    (4,3),
    (5,2),
    (8, 3),
]
#Comsumables
#entity_factories.health_potion
#entity_factories.fp_potion
#entity_factories.estrogen
#entity_factories.weed
#entity_factories.progesterone
#entity_factories.poppers
#entity_factories.amphetamines
#entity_factories.hypnofile
#entity_factories.personal_shield
#entity_factories.adrenaline
#entity_factories.flare
#entity_factories.lithium_battery
#entity_factories.ketamine_scroll
#entity_factories.frag_grenade
#entity_factories.fire_grenade
#entity_factories.pistol_ammo
#entity_factories.rifle_ammo
#entity_factories.chaingun_ammo

#equipment
#entity_factories.cool_knife
#entity_factories.shock_claws
#entity_factories.misericorde
#entity_factories.labrys
#entity_factories.rapier
#entity_factories.pistol
#entity_factories.assaultRifle
#entity_factories.chainGun
#entity_factories.latexBodySuit
#entity_factories.leather_jacket
#entity_factories.jumpsuit
#entity_factories.dress
#entity_factories.hazard_suit

#cyberware
#entity_factories.hack_upgrade
#entity_factories.los_upgrade
#entity_factories.accuracy_upgrade
#entity_factories.control_upgrade
#entity_factories.weapon_slot
#entity_factories.shielding
#entity_factories.electrical_shielding
#entity_factories.fire_shielding
#entity_factories.boobs
#entity_factories.reflex_upgrade
#entity_factories.bionic_arm
#entity_factories.power_legs
#entity_factories.carrymod
#entity_factories.super_legs

#NPCS
#entity_factories.doll
#entity_factories.corpo_drone
#entity_factories.corpo_sentry
#entity_factories.big_goop
#entity_factories.big_chemslime
#entity_factories.Big_nanocloud
#entity_factories.latex_drone
#entity_factories.latex_sentry
#entity_factories.maid
#entity_factories.combat_doll
#entity_factories.chaser
#entity_factories.exterminator
#entity_factories.charger
#entity_factories.security_bot
#entity_factories.security_enforcer
#entity_factories.aetheron

consumable_chances: Dict[int, List[Tuple[Entity, int]]] = {

    1: [(entity_factories.health_potion, 40),(entity_factories.fp_potion,40),
     (entity_factories.weed,20),(entity_factories.personal_shield,20),
     (entity_factories.poppers,20),(entity_factories.hypnofile,20),
    (entity_factories.adrenaline,20),(entity_factories.flare,30),(entity_factories.frag_grenade,20),
    (entity_factories.fire_grenade,10),(entity_factories.ketamine_scroll,30),(entity_factories.lithium_battery,20),
    (entity_factories.pistol_ammo,30),],

    2:[(entity_factories.health_potion, 50),
       (entity_factories.fp_potion,40),
        (entity_factories.estrogen,30),
       (entity_factories.weed,20),
       (entity_factories.personal_shield,20),
       (entity_factories.poppers,20),
       (entity_factories.hypnofile,10),
       (entity_factories.adrenaline,10),
        (entity_factories.flare,20),
       (entity_factories.frag_grenade,30),
       (entity_factories.fire_grenade,20),
       (entity_factories.ketamine_scroll,20),
       (entity_factories.lithium_battery,20),
        (entity_factories.pistol_ammo,40),
       (entity_factories.rifle_ammo,20),
       (entity_factories.chaingun_ammo,10),


       ],

    4:[(entity_factories.health_potion, 50),
       (entity_factories.fp_potion,40),
        (entity_factories.estrogen,20),
       (entity_factories.weed,30),
       (entity_factories.personal_shield,20),
        (entity_factories.progesterone,20),
       (entity_factories.poppers,30),
       (entity_factories.hypnofile,20),
       (entity_factories.adrenaline,20),
        (entity_factories.flare,10),
       (entity_factories.frag_grenade,30),
       (entity_factories.fire_grenade,30),
       (entity_factories.ketamine_scroll,20),
       (entity_factories.amphetamines,30),
       (entity_factories.lithium_battery,20),
        (entity_factories.pistol_ammo,40),
       (entity_factories.rifle_ammo,15),
       (entity_factories.chaingun_ammo,10),],


    6:[(entity_factories.health_potion, 40),
       (entity_factories.fp_potion,40),
        (entity_factories.estrogen,20),
       (entity_factories.weed,20),
       (entity_factories.personal_shield,20),
        (entity_factories.progesterone,10),
       (entity_factories.poppers,10),
       (entity_factories.hypnofile,10),
       (entity_factories.adrenaline,20),
       (entity_factories.amphetamines, 10),
        (entity_factories.flare,10),
       (entity_factories.frag_grenade,30),
       (entity_factories.fire_grenade,20),
       (entity_factories.ketamine_scroll,20),
       (entity_factories.lithium_battery,20),
        (entity_factories.pistol_ammo,20),
       (entity_factories.rifle_ammo,20),
       (entity_factories.chaingun_ammo,20),],



    8:[(entity_factories.health_potion, 30),(entity_factories.fp_potion,30),(entity_factories.amphetamines, 20),
        (entity_factories.estrogen,10), (entity_factories.weed,20),(entity_factories.personal_shield,30),
        (entity_factories.progesterone,20),(entity_factories.poppers,20),(entity_factories.hypnofile,20),
        (entity_factories.flare,10),(entity_factories.frag_grenade,30),(entity_factories.fire_grenade,20),(entity_factories.ketamine_scroll,10),(entity_factories.lithium_battery,10),
        (entity_factories.pistol_ammo,10),(entity_factories.rifle_ammo,30),(entity_factories.chaingun_ammo,30),],




}

enemy_chances: Dict[int, List[Tuple[Entity, int]]] = {

    1: [(entity_factories.corpo_sentry,30),(entity_factories.corpo_drone,60),(entity_factories.big_goop,20)],

    2: [(entity_factories.corpo_sentry,60),
        (entity_factories.corpo_drone,30),
        (entity_factories.big_goop,20),
        (entity_factories.big_chemslime,10),
         (entity_factories.Big_nanocloud,10),
        (entity_factories.doll,10),
       ],

    3: [(entity_factories.corpo_sentry,60),
        (entity_factories.corpo_drone,30),
        (entity_factories.big_goop,30),
    (entity_factories.big_chemslime,30),
    (entity_factories.Big_nanocloud,30),
        (entity_factories.doll,20),(
            entity_factories.latex_drone,20)],

    4: [(entity_factories.corpo_sentry,40),
        (entity_factories.big_goop,20),
        (entity_factories.big_chemslime, 30),
        (entity_factories.Big_nanocloud, 30),
        (entity_factories.doll,20),
        (entity_factories.latex_drone,30),
        (entity_factories.latex_sentry,30),
        (entity_factories.maid,10)],

    5: [(entity_factories.corpo_sentry,30),
        (entity_factories.big_goop, 20),
        (entity_factories.big_chemslime, 30),
        (entity_factories.Big_nanocloud, 30),
        (entity_factories.doll, 20),
        (entity_factories.latex_drone, 30),
        (entity_factories.latex_sentry, 30),
         (entity_factories.security_enforcer, 10),
         (entity_factories.security_bot, 10),
        (entity_factories.maid, 20)],

    6: [(entity_factories.latex_drone,20),
        (entity_factories.latex_sentry,20),
        (entity_factories.security_enforcer,20),
        (entity_factories.security_bot,20),
        (entity_factories.chaser,30),
        (entity_factories.combat_doll,10),
        (entity_factories.doll,20),
        (entity_factories.charger, 10),
        (entity_factories.maid, 30),
        (entity_factories.big_chemslime, 10),
        (entity_factories.Big_nanocloud, 10),
        (entity_factories.exterminator,10),

        ],

    7:[(entity_factories.latex_drone,10),
        (entity_factories.latex_sentry,10),
        (entity_factories.security_enforcer,30),
        (entity_factories.security_bot,30),
        (entity_factories.chaser,30),
        (entity_factories.combat_doll,20),
        (entity_factories.doll,20),
        (entity_factories.exterminator, 20),
        (entity_factories.charger, 30),
        (entity_factories.maid, 10),
       (entity_factories.aetheron,20)
        ],


    8: [(entity_factories.security_enforcer,20),
        (entity_factories.security_bot,20),
        (entity_factories.chaser,30),
        (entity_factories.combat_doll,30),
        (entity_factories.doll,20),
        (entity_factories.exterminator, 30),
        (entity_factories.charger, 30),
       (entity_factories.aetheron,20),
        ],

}


equipment_chances: Dict[int, List[Tuple[Entity, int]]] = {
    1: [(entity_factories.rapier, 20), (entity_factories.pistol, 20),
        (entity_factories.leather_jacket, 30)],

    2: [(entity_factories.rapier, 20), (entity_factories.pistol, 30),
        (entity_factories.misericorde, 20), (entity_factories.lithium_battery,20),

        (entity_factories.leather_jacket,20),(entity_factories.dress,20),

        (entity_factories.hack_upgrade,10),(entity_factories.accuracy_upgrade,5),


        (entity_factories.shielding, 10), (entity_factories.electrical_shielding, 5),
         (entity_factories.fire_shielding, 5),

        (entity_factories.bionic_arm, 5), (entity_factories.reflex_upgrade, 5),
        (entity_factories.power_legs, 10),
        ],

    3: [(entity_factories.frag_grenade, 10), (entity_factories.assaultRifle, 20),
        (entity_factories.pistol, 10), (entity_factories.rapier, 30),(entity_factories.misericorde, 20),
        (entity_factories.lithium_battery,20),

        (entity_factories.leather_jacket,20),(entity_factories.dress,20),
        (entity_factories.latexBodySuit,20),(entity_factories.jumpsuit,20),

        (entity_factories.hack_upgrade, 10), (entity_factories.accuracy_upgrade, 10),
        (entity_factories.control_upgrade,5),

        (entity_factories.shielding, 10), (entity_factories.electrical_shielding, 10),
        (entity_factories.fire_shielding, 10),(entity_factories.boobs, 5),

        (entity_factories.bionic_arm, 10), (entity_factories.reflex_upgrade, 10),
        (entity_factories.power_legs, 10),(entity_factories.super_legs, 5),
        ],


    4: [(entity_factories.shock_claws, 20), (entity_factories.assaultRifle, 50), (entity_factories.rapier, 10),
       (entity_factories.dress,30),(entity_factories.latexBodySuit,30),(entity_factories.jumpsuit,30),(entity_factories.pistol_ammo,20),

        (entity_factories.hack_upgrade, 10), (entity_factories.accuracy_upgrade, 10),

        (entity_factories.shielding, 10), (entity_factories.electrical_shielding, 10),
        (entity_factories.fire_shielding, 10),

        (entity_factories.bionic_arm, 10), (entity_factories.reflex_upgrade, 10),
        (entity_factories.power_legs, 10),(entity_factories.super_legs, 5),

        ],

    5: [(entity_factories.shock_claws, 20), (entity_factories.assaultRifle, 20), (entity_factories.chainGun, 20),
        (entity_factories.rapier, 10), (entity_factories.misericorde, 10),(entity_factories.pistol_ammo,20),
        (entity_factories.dress, 30),
        (entity_factories.latexBodySuit, 30), (entity_factories.jumpsuit, 30),

        (entity_factories.hack_upgrade, 10), (entity_factories.accuracy_upgrade, 10),
        (entity_factories.control_upgrade,5),

        (entity_factories.shielding, 10), (entity_factories.electrical_shielding, 10),
        (entity_factories.fire_shielding, 10),(entity_factories.boobs, 5),

        (entity_factories.bionic_arm, 10), (entity_factories.reflex_upgrade, 10),
        (entity_factories.power_legs, 10),(entity_factories.super_legs, 5),
        ],


    6: [(entity_factories.shock_claws, 20), (entity_factories.assaultRifle, 20), (entity_factories.chainGun, 30),(entity_factories.rifle_ammo,10),
        (entity_factories.rapier, 10), (entity_factories.fire_grenade, 10),
        (entity_factories.hazard_suit, 30), (entity_factories.frag_grenade, 30),
        (entity_factories.latexBodySuit, 30), (entity_factories.jumpsuit, 30),

        (entity_factories.hack_upgrade, 10), (entity_factories.accuracy_upgrade, 10),
        (entity_factories.control_upgrade,10),(entity_factories.los_upgrade, 10),

        (entity_factories.shielding, 10), (entity_factories.electrical_shielding, 10),
        (entity_factories.fire_shielding, 10),(entity_factories.boobs, 10),
        (entity_factories.weapon_slot,10), (entity_factories.carrymod,10),


        (entity_factories.bionic_arm, 10), (entity_factories.reflex_upgrade, 10),
        (entity_factories.power_legs, 10),(entity_factories.super_legs, 10),

        ],

    7: [(entity_factories.shock_claws, 20), (entity_factories.assaultRifle, 20),
        (entity_factories.chainGun, 30),(entity_factories.labrys,20),
        (entity_factories.rapier,10),(entity_factories.misericorde,10),
        (entity_factories.hazard_suit,30),(entity_factories.lithium_battery,30),
        (entity_factories.health_potion,30),(entity_factories.fp_potion,30),


        (entity_factories.hack_upgrade, 10), (entity_factories.accuracy_upgrade, 10),
        (entity_factories.control_upgrade, 10), (entity_factories.los_upgrade, 10),

        (entity_factories.shielding, 10), (entity_factories.electrical_shielding, 10),
        (entity_factories.fire_shielding, 10), (entity_factories.boobs, 10),
        (entity_factories.weapon_slot, 10), (entity_factories.carrymod, 10),

        (entity_factories.bionic_arm, 10), (entity_factories.reflex_upgrade, 10),
        (entity_factories.power_legs, 10), (entity_factories.super_legs, 10),
        ],

    8: [(entity_factories.chainGun, 40),(entity_factories.labrys,40),
        (entity_factories.pistol_ammo,40),(entity_factories.rifle_ammo,20),
        (entity_factories.chaingun_ammo,10),

        (entity_factories.hack_upgrade, 10), (entity_factories.accuracy_upgrade, 10),
        (entity_factories.control_upgrade, 10), (entity_factories.los_upgrade, 10),

        (entity_factories.shielding, 10), (entity_factories.electrical_shielding, 10),
        (entity_factories.fire_shielding, 10), (entity_factories.boobs, 10),
        (entity_factories.weapon_slot, 10), (entity_factories.carrymod, 10),

        (entity_factories.bionic_arm, 10), (entity_factories.reflex_upgrade, 10),
        (entity_factories.power_legs, 10), (entity_factories.super_legs, 10),
        ],


}


def get_max_value_for_floor(
        max_value_by_floor: List[Tuple[int,int]], floor: int) -> int:
    current_value = 0
    for floor_minimum, value in max_value_by_floor:
        if floor_minimum > floor:
            break
        else:
            current_value = value

    return current_value

def get_entities_at_random(
        weighted_chances_by_floor: Dict[int, List[Tuple[Entity, int]]],
        number_of_entities: int,
        floor: int,
        )-> List[Entity]:
    entity_weighted_chances ={}

    for key, values in weighted_chances_by_floor.items():
        if key > floor:
            break
        else:
            for value in values:
                entity = value[0]
                weighted_chance=value[1]

                entity_weighted_chances[entity]=weighted_chance

    entities=list(entity_weighted_chances.keys())

    entity_weighted_chance_values = list(entity_weighted_chances.values())

    chosen_entities = random.choices(
        entities, weights=entity_weighted_chance_values, k=number_of_entities
    )
    return chosen_entities
class BSPTree:
    def __init__(self, tiles,origin):
        self.tiles = tiles
        self.origin=origin
        self.left = None
        self.right = None

    def has_children(self):
        return (self.left is not None and self.right is not None)

class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x+ width
        self.y2 = y+height

    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2)/2)
        center_y =  int((self.y1 + self.y2)/2)

        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice,slice]:
        return slice(self.x1+1, self.x2), slice(self.y1 +1, self.y2)

    def intersects(self, other: RectangularRoom)->bool:
        return(
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )



def place_entities(
room: RectangularRoom, dungeon: GameMap, floor_number: int) -> None:

    number_of_monsters=random.randint(0,
                                      get_max_value_for_floor(max_monsters_by_floor,floor_number))
    number_of_consumables = random.randint(0,
                                      get_max_value_for_floor(max_consumables_by_floor,floor_number))
    number_of_equipments = random.randint(0,
                                      get_max_value_for_floor(max_equipment_by_floor,floor_number))

    monsters: List[Entity]=get_entities_at_random(
        enemy_chances,number_of_monsters,floor_number)

    consumables: List[Entity]=get_entities_at_random(
        consumable_chances,number_of_consumables,floor_number)

    equipments: List[Entity]=get_entities_at_random(
        equipment_chances,number_of_equipments,floor_number)

    for entity in monsters + consumables+equipments:

        x = random.randint(room.x1 +1, room.x2 - 1)
        y= random.randint(room.y1 +1, room.y2 - 1)

        if not any( entity.x == x and entity.y ==y for entity in dungeon.entities):
            #print("spawning",entity.name)
            entity.spawn(dungeon,x,y)


def tunnel_between(
        start:Tuple[int,int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5:
        corner_x, corner_y =x2, y1
    else:
        corner_x, corner_y = x1, y2
    for x,y in tcod.los.bresenham((x1,y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y),(x2, y2)).tolist():
        yield x, y

def inOrderTraversal(node):
  if node is None:
    return
  inOrderTraversal(node.left)
  #print(node.data)
  inOrderTraversal(node.right)


def partition_dungeon(root: BSPTree, horizontal: bool,):
    root_width=root.tiles.shape[0]
    root_height=root.tiles.shape[1]
    change_shape=not horizontal
    origin=root.origin

    if horizontal:
        rmax=root_height

    else:
        rmax=root_width


    range_max=int(rmax*2/3)
    range_min= max(3,int(rmax/6))

    if rmax>6:
        partition_line=random.randint(range_min,range_max)

        if horizontal:
            origin_b = (origin[0], origin[1] + partition_line)
            slice_ax=slice(0,rmax)
            slice_ay = slice(0,partition_line)
            slice_bx = slice(0,rmax)
            slice_by=slice(partition_line,rmax)


        else:
            origin_b = (origin[0]+partition_line,origin[1])
            slice_ax = slice(0, partition_line)
            slice_ay = slice(0, rmax)
            slice_bx = slice(partition_line, rmax)
            slice_by = slice(0, rmax)


        leaf_a=BSPTree(root.tiles[slice_ax,slice_ay],origin)
        leaf_b=BSPTree(root.tiles[slice_bx,slice_by],origin_b)

        root.left=leaf_a
        root.right=leaf_b

        if rmax<20:
            coinflip = random.randint(0, 2)
            if coinflip>1:
                partition_dungeon(leaf_a, horizontal=change_shape, )
                partition_dungeon(leaf_b, horizontal=change_shape, )

        else:
            partition_dungeon(leaf_a,horizontal=change_shape,)
            partition_dungeon(leaf_b,horizontal=change_shape,)
        return root
    else:
        return root

def generate_rooms(leaf, rooms: List[RectangularRoom], dungeon):
    if leaf is None:
        return None
    room1_center = None
    room2_center = None

    room1_center=generate_rooms(leaf.left, rooms, dungeon)
    if room1_center is None:
        width = np.shape(leaf.tiles)[0]
        height = np.shape(leaf.tiles)[1]
        new_room = RectangularRoom(leaf.origin[0], leaf.origin[1], width, height)
        rooms.append(new_room)
        dungeon.tiles[new_room.inner] = tile_types.floor


    room2_center=generate_rooms(leaf.right, rooms, dungeon)

    if room1_center is not None and room2_center is not None:
        for x, y in tunnel_between(room1_center, room2_center):
            dungeon.tiles[x, y] = tile_types.floor


    return rooms[-1].center





def generate_BSP(
        max_rooms: int,
        room_min_size: int,
        room_max_size: int,
        map_width: int,
        map_height: int,

        engine: Engine) -> GameMap:

    player = engine.player
    dungeon = GameMap(engine, map_width, map_height, entities=[player])
    rooms: List[RectangularRoom] = []
    center_of_last_room = (0, 0)
    dungeon_tilemap = dungeon.tiles[slice(0,dungeon.width-1),slice(0,dungeon.height-1)]
    dungeon_root= BSPTree(dungeon_tilemap,(0,0))

    dungeon_root=partition_dungeon(dungeon_root,False)

    generate_rooms(dungeon_root,rooms,dungeon)

    first_room_index=random.randint(0,len(rooms)-1)
    last_room_index = first_room_index
    while last_room_index==first_room_index:
        last_room_index = random.randint(0,len(rooms)-1)
    med_room_index=last_room_index
    while med_room_index==first_room_index or med_room_index==last_room_index:
        med_room_index = random.randint(0,len(rooms)-1)

    center_of_last_room = rooms[last_room_index].center
    center_of_first_room =  rooms[first_room_index].center
    center_of_med_room = rooms[med_room_index].center

    for room_index in range(0, len(rooms)-1):
        room=rooms[room_index]
        place_entities(room, dungeon, dungeon.engine.game_world.current_floor)

    player.place(*center_of_first_room, dungeon)


    for minion in player.controller.minion_list:
        minion.place(*center_of_first_room, dungeon)




    dungeon.tiles[center_of_med_room] = tile_types.medbay
    dungeon.med_location = center_of_med_room
    dungeon.tiles[center_of_last_room] = tile_types.down_stairs
    dungeon.downstairs_location = center_of_last_room

    for item in dungeon.items:
        if (item.x,item.y) == center_of_med_room or (item.x,item.y) == center_of_last_room:
            item.place(item.x-1,item.y,dungeon)
            break
    Stairs = copy.deepcopy(entity_factories.DownStairs)
    Stairs.spawn(dungeon, *center_of_last_room)

    medbay = copy.deepcopy(entity_factories.MedBay)
    medbay.spawn(dungeon, *center_of_med_room)

    return dungeon



def generate_arena(
        map_width: int,
        map_height: int,
        engine: Engine)-> GameMap:

    player = engine.player
    dungeon = GameMap(engine,map_width, map_height, entities=[player])
    rooms: List[RectangularRoom]=[]

    dungeon.tiles[slice(10,30),slice(10,30)]=tile_types.floor
    dungeon.tiles[20,9]=tile_types.floor
    dungeon.tiles[slice(18, 23), slice(4, 9)] = tile_types.floor


    dungeon.tiles[slice(15,19),15]=tile_types.wall
    dungeon.tiles[15, slice(15,19)] = tile_types.wall

    dungeon.tiles[slice(21,25),15]=tile_types.wall
    dungeon.tiles[25,slice(15,19)]=tile_types.wall

    dungeon.tiles[slice(15, 19), 25] = tile_types.wall
    dungeon.tiles[15, slice(21, 25)] = tile_types.wall

    dungeon.tiles[slice(21, 25), 25] = tile_types.wall
    dungeon.tiles[25, slice(21, 25)] = tile_types.wall



    dungeon.tiles[20,6] =tile_types.goal
    dungeon.goal_location=(20,6)

    player.place(20, 30, dungeon)
    for minion in player.controller.minion_list:
        minion.place(20,30, dungeon)

    angel=copy.deepcopy(entity_factories.angel)
    angel.spawn(dungeon,20,12)
    angel=dungeon.get_actor_at_location(20,12)
    angel.equipment.bonus_active=True

    gun = copy.deepcopy(entity_factories.angelGun)
    gun.parent = angel.inventory
    angel.inventory.items.append(gun)
    angel.equipment.equip_to_slot("right_hand",gun,add_message=False)

    gun = copy.deepcopy(entity_factories.angelGun)
    gun.parent = angel.inventory
    angel.inventory.items.append(gun)
    angel.equipment.equip_to_slot("left_hand", gun, add_message=False)

    sword = copy.deepcopy(entity_factories.angelSword)
    sword.parent=angel.inventory
    angel.inventory.items.append(sword)
    angel.equipment.equip_to_slot("bonus_slot",sword,add_message=False)

    goal = copy.deepcopy(entity_factories.Goal)
    goal.spawn(dungeon, 20, 6)

    return dungeon

""""
def generate_mall(
        max_rooms: int,
        room_min_size: int,
        room_max_size: int,
        map_width: int,
        map_height: int,

        engine: Engine) -> GameMap:
    player = engine.player
    dungeon = GameMap(engine,map_width, map_height, entities=[player])
    rooms: List[RectangularRoom]=[]
    center_of_last_room =(0,0)

    horiz_hall_width=random.randint(int(dungeon.width/4), dungeon.width-1)
    horiz_hall_height=random.randint(4,10)

    vert_hall_width=random.randint(4,10)
    if horiz_hall_width > (dungeon.width / 2):
        vert_hall_height=random.randint(int(dungeon.height/4),int(3*dungeon.height/4)-1)
    else:
        vert_hall_height = random.randint(int(2*dungeon.height / 3), dungeon.height - 1)

    horiz_hall_x = random.randint(0,dungeon.width-horiz_hall_width-1)
    horiz_hall_y=random.randint(0,dungeon.height-horiz_hall_height-1)


    max_y_pos=min(dungeon.height-vert_hall_height-1,horiz_hall_y+horiz_hall_height-1)
    min_y_pos=max(0,horiz_hall_y-vert_hall_height)

    vert_hall_x=random.randint(max(0,horiz_hall_x-vert_hall_width-1),min(dungeon.width-1,horiz_hall_x+horiz_hall_width))
    vert_hall_y=random.randint(min_y_pos,max_y_pos)

    horiz_hall=RectangularRoom(horiz_hall_x,horiz_hall_y,horiz_hall_width,horiz_hall_height)
    vert_hall=RectangularRoom(vert_hall_x,vert_hall_y,vert_hall_width,vert_hall_height)

    rooms.append(horiz_hall)
    rooms.append(vert_hall)
    player.place(*horiz_hall.center, dungeon)
    entity_factories.doll.spawn(dungeon, player.x + 1, player.y)

    space_above = horiz_hall.y1
    space_below = dungeon.height-horiz_hall.y2-1
    space_left= vert_hall.x1
    space_right= dungeon.width-vert_hall.x2-1


    temp_room_above: List[RectangularRoom]=[]
    temp_room_below:List[RectangularRoom]=[]
    temp_room_left:List[RectangularRoom]=[]
    temp_room_right:List[RectangularRoom]=[]
    for r in range(max_rooms):

        if space_above>=room_min_size:
            room_width = random.randint(room_min_size, room_max_size)
            room_height = random.randint(room_min_size,  min(space_above ,room_max_size))
            if len(temp_room_above)<1:
                x =random.randint(max(0, horiz_hall_x-room_width),horiz_hall_x+3)

            else:
                last_room_x = temp_room_above[-1].x2
                space_between = random.randint(0, 4)
                end_of_hall = horiz_hall.x2 - 1
                last_valid_space = dungeon.width - room_width - 1
                if last_room_x + space_between + room_width - 1 >= end_of_hall:
                    x = min(last_room_x + space_between, last_valid_space)
                    space_above = 0
                else:
                    x = min(last_room_x + space_between, end_of_hall)

            y=horiz_hall_y-room_height+1

            new_room = RectangularRoom(x, y, room_width, room_height)
            temp_room_above.append(new_room)

        if space_below>=room_min_size:
            room_width = random.randint(room_min_size, room_max_size)
            room_height = random.randint(room_min_size,  min(space_below ,room_max_size))
            y = horiz_hall.y2 - 1
            if len(temp_room_below)<1:
                x =random.randint(max(0, horiz_hall_x-room_width),horiz_hall_x+3)

            else:
                last_room_x = temp_room_below[-1].x2
                space_between = random.randint(0, 4)
                end_of_hall = horiz_hall.x2 - 1
                last_valid_space = dungeon.width - room_width - 1
                if last_room_x + space_between + room_width - 1 >= end_of_hall:
                    x = min(last_room_x + space_between, last_valid_space)
                    space_below = 0
                else:
                    x = min(last_room_x + space_between, end_of_hall)

            new_room = RectangularRoom(x, y, room_width, room_height)
            temp_room_below.append(new_room)


        if space_left>=room_min_size:
            room_width = random.randint(room_min_size, min(space_left,room_max_size))
            room_height = random.randint(room_min_size, room_max_size)
            if len(temp_room_left)<1:
               y=random.randint(max(0,vert_hall_y-room_height+1),vert_hall_y+3)
            else:
               last_room_y = temp_room_left[-1].y2
               space_between = random.randint(0, 4)
               end_of_hall = vert_hall.y2 - 1
               last_valid_space = dungeon.height - room_height - 1
               if last_room_y + space_between + room_height - 1 >= end_of_hall:
                   y = min(last_room_y + space_between, last_valid_space)
                   space_left = 0
               else:
                   y = min(last_room_y + space_between, end_of_hall)

            x = vert_hall.x1-room_width+1

            new_room = RectangularRoom(x, y, room_width, room_height)
            temp_room_left.append(new_room)


        if space_right>=room_min_size:
            room_width = random.randint(room_min_size,  min(space_right,room_max_size))
            room_height = random.randint(room_min_size, room_max_size)
            if len(temp_room_right) < 1:
                y = random.randint(max(0, vert_hall_y - room_height + 1), vert_hall_y + 3)
            else:
                last_room_y=temp_room_right[-1].y2
                space_between=random.randint(0,4)
                end_of_hall=vert_hall.y2-1
                last_valid_space = dungeon.height - room_height - 1
                if last_room_y+space_between+room_height-1>=end_of_hall:
                    y=min(last_room_y+space_between,last_valid_space)
                    space_right=0
                else:
                    y=min(last_room_y+space_between,end_of_hall)

            x = vert_hall.x2 - 1
            new_room = RectangularRoom(x, y, room_width, room_height)
            temp_room_right.append(new_room)


    rooms = rooms + temp_room_right+temp_room_left+temp_room_above+temp_room_below



    for room in rooms:
        dungeon.tiles[room.inner] = tile_types.floor
        place_entities(room, dungeon, engine.game_world.current_floor)

    center_of_last_room=rooms[-1].center
    dungeon.tiles[center_of_last_room] = tile_types.down_stairs
    dungeon.downstairs_location = center_of_last_room

    return dungeon
"""

def generate_dungeon(
        max_rooms: int,
        room_min_size: int,
        room_max_size: int,
        map_width: int,
        map_height: int,

        engine: Engine) -> GameMap:
    player = engine.player
    dungeon = GameMap(engine,map_width, map_height, entities=[player])
    rooms: List[RectangularRoom]=[]
    center_of_last_room =(0,0)
    for r in range(max_rooms):
        room_width= random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size,room_max_size)

        x= random.randint(0, dungeon.width - room_width -1)
        y = random.randint(0, dungeon.height - room_height -1)

        new_room = RectangularRoom(x,y,room_width, room_height)

        if any(new_room.intersects(other_room) for other_room in rooms):
            continue
        dungeon.tiles[new_room.inner]=tile_types.floor

        if len(rooms) == 0:
            player.place(*new_room.center, dungeon)
            for minion in player.controller.minion_list:
                minion.place(*new_room.center,dungeon)
        else:
            for x,y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x,y] = tile_types.floor
            center_of_last_room=new_room.center
        place_entities(new_room, dungeon, engine.game_world.current_floor)

        dungeon.tiles[center_of_last_room]=tile_types.down_stairs
        dungeon.downstairs_location=center_of_last_room
        rooms.append(new_room)

    rand_room_number = random.randint(1,len(rooms)-2)
    center_of_med_room=rooms[rand_room_number].center

    dungeon.tiles[center_of_med_room] = tile_types.medbay
    dungeon.med_location=center_of_med_room


    #Check to make sure medbay overwrites item
    for item in dungeon.items:
        if (item.x,item.y) == center_of_med_room or (item.x,item.y) == center_of_last_room :
            item.place(item.x-1,item.y,dungeon)
            break
    Stairs = copy.deepcopy(entity_factories.DownStairs)
    Stairs.spawn(dungeon, center_of_last_room[0], center_of_last_room[1])

    medbay = copy.deepcopy(entity_factories.MedBay)
    medbay.spawn(dungeon, center_of_med_room[0], center_of_med_room[1])
    return dungeon
