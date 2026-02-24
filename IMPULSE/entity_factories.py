from IMPULSE.components.ai import BaseAI

from IMPULSE.components.hacker import Hacker
from IMPULSE.components.equipment import Equipment
from IMPULSE.components.cyberware import Cyberware
from IMPULSE.components.ai import Idle, MeleeEnemy,RangedEnemy,Angel
from IMPULSE.components.fighter import Fighter
from IMPULSE.components import consumable, equippable, bodymod
from IMPULSE.components.inventory import  Inventory
from IMPULSE.components.level import Level
from IMPULSE.components.status import Status
from IMPULSE.entity import Actor, Item, Station
from IMPULSE.components.controller import Controller
from IMPULSE import virus

player = Actor(char="@",
               color = (255,255,255),
               name= "Player",
               ai_cls=BaseAI,
               fighter=Fighter(hp=30, fp=10,base_defense=2, base_power=5,base_speed=5,base_focus=10,base_accuracy=0),
               inventory=Inventory(capacity=26),
               level=Level(level_up_base=200),
               equipment=Equipment(),
               cyberware=Cyberware(),
               hacker = Hacker(virus.std_viruses),
               status=Status(),
               controller=Controller()

               )
doll = Actor(char="d",
               color = (69,200,255),
               name= "doll",
               ai_cls=Idle,
               fighter=Fighter(hp=30, base_defense=1, base_power=5,base_speed=5,base_focus=10,base_accuracy=0),
               inventory=Inventory(capacity=0),
               level=Level(level_up_base=200),
               equipment=Equipment(),
               cyberware=Cyberware(),
               status=Status()
               )
drone =Actor(char="S",
    color = (63, 127, 63),
    name = "Security Drone",
    ai_cls = RangedEnemy,
    fighter = Fighter(hp=10, base_defense=0, base_power=6, base_speed=5, base_focus=10, base_accuracy=2,base_range=4),
    inventory = Inventory(capacity=0),
    level = Level(xp_given=100),
    status = Status(),
             )

angel= Actor(char="A",
               color = (255,255,255),
               name= "ANGEL",
               ai_cls=Angel,
              equipment=Equipment(),
               fighter=Fighter(hp=40, base_defense=2, base_power=7,base_speed=8,base_focus=20,base_accuracy=0),
               inventory=Inventory(capacity=4),
               level=Level(xp_given=1000),
                cyberware=Cyberware(),
                status=Status()
               )

cyberTest= Actor(char="C",
               color = (127,0,127),
               name= "Cybork",
               ai_cls=MeleeEnemy,
              equipment=Equipment(),
               fighter=Fighter(hp=16, base_defense=1, base_power=4,base_speed=2,base_focus=10,base_accuracy=0),
               inventory=Inventory(capacity=0),
               level=Level(xp_given=250),
                cyberware=Cyberware(),
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
shock_claws=Item(
    char="/", color=(0,100,255),name="Shock Claws", equippable=equippable.shock_claws()
)
misericorde=Item(
    char="/", color=(0,90,255),name="Misericorde", equippable=equippable.misericorde())
labrys=Item(
    char="/", color=(128,0,128), name="Labrys", equippable= equippable.labrys()
)
rapier=Item(
    char="/", color=(0,191,255), name="Rapier", equippable=equippable.rapier()
)

pistol=Item(
    char="/", color=(255,0,255), name="Pistol", equippable=equippable.pistol()
)

assaultRifle=Item(
    char="/", color=(255,0,200), name="Assault Rifle", equippable=equippable.assualtRifle()
)
flameThrower=Item(
    char="/", color=(255,20,20), name="Flame Thrower", equippable=equippable.assualtRifle()
)
chainGun=Item(
    char="/", color=(200,200,200),name="Chain Gun", equippable=equippable.chainGun()
)
latexBodySuit=Item(
    char="[", color=(10,10,10), name="Latex BodySuit", equippable=equippable.latex_bodysuit()
)
leather_jacket=Item(
    char="[", color=(139,69,19), name="Leather Jacket", equippable=equippable.leather_jacket()

)
jumpsuit=Item(
    char="[",color=(10,10,200), name="Jumpsuit", equippable=equippable.jumpsuit()
)
dress=Item(
    char="[", color=(50,50,50), name="Dress", equippable=equippable.dress()
)

hazard_suit = Item(
    char="[", color=(169,69,69), name="Hazard Suit", equippable= equippable.hazard_suit()
)

hack_upgrade = Item(
    char="i", color=(255,0,255), name="Hacking Upgrade", bodymod= bodymod.hack_upgrade()
)

los_upgrade = Item(
    char="i", color=(200,0,255), name="Long Range Sensors", bodymod= bodymod.los_upgrade()
)
accuracy_upgrade=Item(
    char="i", color=(150,0,255), name="Integrated Fire Control", bodymod= bodymod.accuracy_upgrade()
)

control_upgrade=Item(
    char="i",color=(100,0,255), name="Inegrated Fire Control", bodymod= bodymod.control_upgrade()
)


weapon_slot = Item(
    char="i", color=(255,0,255), name="Hvy Wpn Pltfrm", bodymod= bodymod.weapon_slot()
)
sheilding = Item(
    char="i", color=(255,0,100), name="Sheilding Upgrade", bodymod= bodymod.sheilding()
)

electric_sheilding=Item(
    char="i", color=(50,0,255), name="Faraday Suite", bodymod= bodymod.electric_sheilding()
)
fire_sheilding=Item(
    char="i", color=(0,50,255), name="Rapid Cooling Trunk", bodymod= bodymod.fire_sheilding()
)
boobs=Item(
    char="i", color=(50,50,255), name="Breast Forms [K]", bodymod=bodymod.boobs()
)

reflex_upgrade=Item(
    char="i", color=(100,50,255), name="Rapid Response Servos", bodymod=bodymod.reflex_upgrade()
)


bionic_arm=Item(
    char="i", color=(150,50,255), name="High Tensile Tendons", bodymod=bodymod.bionic_arm()

)

rocket_fist=Item(
    char="i", color=(200,50,255), name="R.P.F", bodymod=bodymod.rocket_fist()
)

power_legs=Item(
    char="i", color=(255,50,255), name="Stability Modules", bodymod=bodymod.power_legs())

carrymod=Item(
    char="i", color=(255,100,255), name=" Carbon Nano-Bones",bodymod=bodymod.carry()
)


super_legs = Item(
    char= "i", color=(255,30,100), name="Leg Upgrade", bodymod=bodymod.super_legs()
)


MedBay = Station(
    char="X", color=(1,1,1), name="MedBay")