from IMPULSE.components.ai import BaseAI
from IMPULSE.components.bodymod import sheilding
from IMPULSE.components.hackable import Hackable
from components.equipment import Equipment
from components.cyberware import Cyberware
from components.ai import HostileEnemy, Ally
from components.fighter import Fighter
from components import consumable, equippable, bodymod
from components.inventory import  Inventory
from components.level import Level
from components.status import Status
from entity import Actor, Item, Station, Trap


player = Actor(char="@",
               color = (255,255,255),
               name= "Player",
               ai_cls=BaseAI,
               fighter=Fighter(hp=30, base_defense=2, base_power=5,base_speed=5),
               inventory=Inventory(capacity=26),
               level=Level(level_up_base=200),
               equipment=Equipment(),
               cyberware=Cyberware(),
                hackable = Hackable(),
               status=Status()
               )
doll = Actor(char="d",
               color = (69,200,255),
               name= "doll",
               ai_cls=Ally,
               fighter=Fighter(hp=30, base_defense=1, base_power=5,base_speed=5),
               inventory=Inventory(capacity=0),
               level=Level(level_up_base=200),
               equipment=Equipment(),
               cyberware=Cyberware(),
                hackable = Hackable(),
               status=Status()
               )
orc = Actor(char="o",
               color = (63,127,63),
               name= "Orc",
               ai_cls=HostileEnemy,
               fighter=Fighter(hp=10, base_defense=0, base_power=3,base_speed=5),
               inventory=Inventory(capacity=0),
               level=Level(xp_given=100),
               equipment=Equipment(),
                status=Status()

               )

troll = Actor(char="T",
               color = (0,127,0),
               name= "Troll",
               ai_cls=HostileEnemy,
              equipment=Equipment(),
               fighter=Fighter(hp=16, base_defense=1, base_power=4,base_speed=5),
               inventory=Inventory(capacity=0),
               level=Level(xp_given=250),
                status=Status()

               )

speedFuck = Actor(char="s",
               color = (0,0,127),
               name= "SpeedTest",
               ai_cls=HostileEnemy,
              equipment=Equipment(),
               fighter=Fighter(hp=16, base_defense=1, base_power=4,base_speed=8),
               inventory=Inventory(capacity=0),
               level=Level(xp_given=250),
                status=Status()

               )
slowBitch = Actor(char="U",
               color = (127,0,0),
               name= "SlowTest",
               ai_cls=HostileEnemy,
              equipment=Equipment(),
               fighter=Fighter(hp=16, base_defense=1, base_power=4,base_speed=2),
               inventory=Inventory(capacity=0),
               level=Level(xp_given=250),
                status=Status()

               )
cyberTest= Actor(char="C",
               color = (127,0,127),
               name= "Cybork",
               ai_cls=HostileEnemy,
              equipment=Equipment(),
               fighter=Fighter(hp=16, base_defense=1, base_power=4,base_speed=2),
               inventory=Inventory(capacity=0),
               level=Level(xp_given=250),
               hackable=Hackable(),
                status=Status()
               )

health_potion = Item(
    char="!",
    color=(127,0,255),
    name="Health Potion",
    consumable=consumable.HealingConsumable(amount=4),
)
pistol_ammo = Item(
    char=":",
    color=(0,0,255),
    name="9mm Rounds",
    consumable=consumable.Ammo(rounds=12, gun_type="Pistol"),
)

lithium_battery = Item(
    char="~",
    color=(2, 100, 0),
    name="Old Lithium Battery",
    consumable=consumable.ArcDamageConsumable(damage=20, maximum_range=50),
)
ketamine_scroll = Item(
    char="~",
    color=(207, 63, 255),
    name="Ketamine Scroll",
    consumable=consumable.ConfusionConsumable(number_of_turns=10),
)
fire_grenade= Item(
    char="~",
    color=(255, 0, 0),
    name="Molotov Cocktail",
    consumable=consumable.FireExplosionConsumable(damage=12, radius=3),
)

cool_knife=Item(
    char="/", color=(0,191,255), name="Cool Knife", equippable=equippable.cool_knife()
)

pistol=Item(
    char="/", color=(255,0,255), name="Pistol", equippable=equippable.pistol()
)
rapier=Item(
    char="/", color=(0,191,255), name="Rapier", equippable=equippable.rapier()
)
leather_jacket=Item(
    char="[", color=(139,69,19), name="Leather Jacket", equippable=equippable.leather_jacket()

)
hazard_suit = Item(
    char="[", color=(169,69,69), name="Hazard Suit", equippable= equippable.hazard_suit()
)
spear = Item(
    char="/", color=(169,69,69), name="Spear", equippable= equippable.spear()
)

hack_upgrade = Item(
    char="i", color=(255,0,255), name="Hacking Upgrade", bodymod= bodymod.hack_upgrade()
)

sheilding = Item(
    char="i", color=(255,0,100), name="Sheilding Upgrade", bodymod= bodymod.sheilding()
)

super_legs = Item(
    char= "i", color=(255,30,100), name="Leg Upgrade", bodymod=bodymod.super_legs()
)


MedBay = Station(
    char="X", color=(1,1,1), name="MedBay")