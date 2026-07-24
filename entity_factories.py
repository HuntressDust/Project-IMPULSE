
from IMPULSE.components.ai import BaseAI


from IMPULSE.components.hacker import Hacker
from IMPULSE.components.equipment import Equipment
from IMPULSE.components.cyberware import Cyberware
from IMPULSE.components.ai import Idle, MeleeEnemy,RangedEnemy,Angel, charger, chaser, MaidAI, CombatDoll
from IMPULSE.components.fighter import Fighter
from IMPULSE.components import consumable, equippable, bodymod, description
from IMPULSE.components.inventory import  Inventory
from IMPULSE.components.level import Level
from IMPULSE.components.status import Status
from IMPULSE.entity import Actor, Item, Station
from IMPULSE.components.controller import Controller
from IMPULSE import virus
from IMPULSE import color
from IMPULSE.damage_types import DamageType
from IMPULSE.components import consumable



player = Actor(char="@",
               color = (255,255,255),
               name= "Player",
               ai_cls=BaseAI,
               fighter=Fighter(hp=15, fp=8,base_defense=1, base_power=1,base_speed=5,base_focus=1,base_accuracy=0,base_reflex=1,),
               inventory=Inventory(capacity=12),
               level=Level(level_up_base=200),
               equipment=Equipment(),
               cyberware=Cyberware(),
               hacker = Hacker(virus.std_viruses),
               status=Status(),
               controller=Controller()

               )
doll = Actor(char="d",
               color = color.doll,
               name= "doll",
               ai_cls=Idle,
               fighter=Fighter(hp=22, base_defense=1, base_attack=6,base_speed=5,base_focus=3,base_accuracy=0,base_power=0),
               inventory=Inventory(capacity=0),
               level=Level(level_up_base=200),

               cyberware=Cyberware(),
               status=Status(),
                desc=description.doll()
               )


angel= Actor(char="A",
               color = color.angel,
               name= "ANGEL",
               ai_cls=Angel,
              equipment=Equipment(),
               fighter=Fighter(hp=40, base_defense=2, base_attack=7,base_speed=8,base_focus=18,base_accuracy=0,base_power=0),
               inventory=Inventory(capacity=4),
               level=Level(xp_given=10000),
                cyberware=Cyberware(),
                status=Status(),
                desc=description.angel()
               )

corpo_drone= Actor(char="C",
               color = color.corpo_drone,
               name= "Corpo Drone",
               ai_cls=MeleeEnemy,
               fighter=Fighter(hp=8, base_defense=1, base_attack=4,base_speed=3,base_focus=0,base_accuracy=0,base_power=0),
               inventory=Inventory(capacity=0),
               level=Level(xp_given=100),
                cyberware=Cyberware(),
                status=Status(),
                desc=description.corpo_drone()

               )
corpo_sentry = Actor(char="T",
                     color=color.corpo_sentry,
                    name="Corpo Sentry",
                    ai_cls=RangedEnemy,
                    fighter=Fighter(hp=8, base_defense=1,  base_attack=3, base_speed=3, base_focus=0, base_accuracy=0,base_range=4,base_power=0),
                    inventory=Inventory(capacity=0),
                    level=Level(xp_given=100),
                    cyberware=Cyberware(),
                    status=Status(),
                    desc=description.corpo_sentry()

                    )

big_goop = Actor(char="S",
               color = color.slime,
                name="Slime",
                 ai_cls=MeleeEnemy,
                 fighter=Fighter(hp=12, base_defense=1, base_attack=4, base_speed=2, base_focus=0, base_accuracy=0, base_shock_resist=20,base_power=0),
                 inventory=Inventory(capacity=0),
                 level=Level(xp_given=100),
                 status=Status(),
                 desc=description.big_goop())
small_goop = Actor(char="s",
               color = color.slime,
                   name="Slime",
                   ai_cls=MeleeEnemy,
                   fighter=Fighter(hp=4, base_defense=1, base_attack=2, base_speed=2, base_focus=0, base_accuracy=0, base_shock_resist=20,base_power=0),
                   inventory=Inventory(capacity=0),
                   level=Level(xp_given=50),
                   status=Status(),
                   desc=description.goop())

big_chemslime = Actor(char="S",
               color = color.chem_slime,
                name="Chem-Slime",
                 ai_cls=MeleeEnemy,
                 fighter=Fighter(hp=12, base_defense=1, base_attack=4, base_speed=2, base_focus=0, base_accuracy=0, base_burn_resist=-40,base_power=0,),
                 inventory=Inventory(capacity=0),
                damage_type=DamageType.FIRE,

                 level=Level(xp_given=100),
                 status=Status(),
                 desc=description.big_chem())
small_chemslime = Actor(char="s",
               color = color.chem_slime,
                   name="Chem-Slime",
                   ai_cls=MeleeEnemy,
                   fighter=Fighter(hp=4, base_defense=1, base_attack=2, base_speed=2, base_focus=0, base_accuracy=0, base_burn_resist=-80,base_power=0),
                   inventory=Inventory(capacity=0),
                   level=Level(xp_given=50),
                    damage_type=DamageType.FIRE,
                   status=Status(),
                   desc=description.chem_slime())

Big_nanocloud =  Actor(char="N",
                color = color.nano_cloud,
                   name="Nano-Cloud",
                   ai_cls=MeleeEnemy,
                   fighter=Fighter(hp=12, base_defense=1, base_attack=5, base_speed=2, base_focus=5, base_accuracy=0, base_shock_resist=-80,base_power=0),
                   inventory=Inventory(capacity=0),
                   level=Level(xp_given=100),
                    damage_type=DamageType.SHOCK,
                       cyberware=Cyberware(),
                   status=Status(),
                   desc=description.big_cloud())

small_nanocloud = Actor(char="n",
               color = color.nano_cloud,
                   name="Nano-Cloud",
                   ai_cls=MeleeEnemy,
                   fighter=Fighter(hp=4, base_defense=1, base_attack=2, base_speed=2, base_focus=1, base_accuracy=0, base_shock_resist=-40,base_power=0),
                   inventory=Inventory(capacity=0),
                    damage_type=DamageType.SHOCK,
                   level=Level(xp_given=50),
                        cyberware=Cyberware(),
                   status=Status(),
                   desc=description.nano_cloud())


combat_doll =  Actor(char="d",
                     color=color.combat_doll,
                     name="Combat Doll",
                     ai_cls=CombatDoll,
                     fighter=Fighter(hp=26, base_defense=3, base_attack=8, base_speed=7, base_focus=10, base_accuracy=0,base_dodge=5,base_power=0),
                    inventory=Inventory(capacity=0),
                     level=Level(xp_given=500),
                     status=Status(),
                     cyberware=Cyberware(),
                     desc=description.combat_doll())

latex_drone =Actor(char="D",
                   color=color.hypno_drone,
                   name="Hypno Drone",
                   ai_cls=MeleeEnemy,
                   fighter=Fighter(hp=14, base_defense=1, base_attack=5, base_speed=5, base_focus=0, base_accuracy=0, base_dodge=3, base_shock_resist=50,base_power=0),
                   inventory=Inventory(capacity=0),

                   level=Level(xp_given=250),
                   status=Status(),
                   desc=description.hypno_drone())

latex_sentry =Actor(char="T",
    color = color.hypno_sentry,
    name = "Latex Sentry",
    ai_cls = RangedEnemy,
    fighter = Fighter(hp=16, base_defense=1, base_attack=4, base_speed=5, base_dodge=3, base_accuracy=2,base_range=4, base_shock_resist=50,base_power=0),
    inventory = Inventory(capacity=0),
    level = Level(xp_given=200),
    status = Status(),
desc=description.latex_sentry()
             )

exterminator = Actor(char="E",
                     color=color.exterminator,
                     name="Exterminator",
                     ai_cls=MaidAI,
                     fighter=Fighter(hp=25,base_defense=5,base_attack=6, base_speed=4, base_focus=8,base_accuracy=3,base_range=2, base_burn_resist=90,base_power=0),
                     damage_type=DamageType.FIRE,
                     inventory=Inventory(capacity=0),
                     level=Level(xp_given=500),
                     status=Status(),
                    desc=description.exterminator())

security_bot = Actor(char="T",
                     color=color.security_bot,
                     name="Security Bot",
                     ai_cls=RangedEnemy ,
                     fighter=Fighter(hp=20,base_defense=4,base_attack=6, base_speed=5, base_focus=7,base_accuracy=3,base_range=5,base_power=0),
                     damage_type=DamageType.SHOCK,
                     inventory=Inventory(capacity=0),
                     level=Level(xp_given=300),
                     status=Status(),
                     cyberware=Cyberware(),
                        desc=description.security_bot())

security_enforcer = Actor(char="B",
                     color=color.security_sentry,
                     name="Security Enforcer",
                     ai_cls=MeleeEnemy ,
                fighter=Fighter(hp=25,base_defense=4,base_attack=8, base_speed=5, base_focus=7,base_accuracy=3,base_shock_resist=20,base_burn_resist=20,base_power=0),
                     damage_type=DamageType.SHOCK,
                     inventory=Inventory(capacity=0),
                     level=Level(xp_given=400),
                     status=Status(),
                        cyberware=Cyberware(),
                        desc=description.security_enforcer())
charger = Actor(char="F",
                color=color.forklift,
                name="XX_FORKL1FT_XX",
                ai_cls=charger,
                fighter = Fighter(hp=10, base_defense=6, base_attack=8,  base_speed=4, base_focus=7, base_accuracy=10, base_burn_resist=20, base_range=6,base_power=0),
                damage_type = DamageType.KINETIC,
                inventory = Inventory(capacity=0),
                level = Level(xp_given=350),
                status = Status(),
                cyberware=Cyberware(),
                desc = description.charger())


#suicider = Actor(char="S",
               #  color=(100,80,200),
             #    ai_cls=charger,
           # #     fighter=Fighter(hp=10, base_defense=1, base_power=1, base_speed=7, base_focus=1, base_accuracy=0,),
           #      inventory=Inventory(capacity=0),
            #     level=Level(xp_given=200),
            #     status=Status(),
            #     )

chaser = Actor(char="g",
               name="Chaser",
               color=color.chaser,
               ai_cls=chaser,
               fighter=Fighter(hp=10, base_defense=1, base_attack=1, base_speed=6, base_focus=0,base_range=7,base_power=0,base_dodge=7),
               inventory=Inventory(capacity=0),
               level=Level(xp_given=250),
               status=Status(),
               desc=description.chaser())

maid =  Actor(char="M",
                     color=color.maid,
                     name="Maid",
                     ai_cls=MaidAI,
                     fighter=Fighter(hp=20, base_defense=3, base_attack=6, base_speed=5, base_focus=6, base_accuracy=0,base_dodge=4,base_power=0,base_burn_resist=50,base_shock_resist=-50),
                    inventory=Inventory(capacity=0),
                     level=Level(xp_given=400),
                     status=Status(),
                     cyberware=Cyberware(),
                    damage_type=DamageType.FIRE,
                     desc=description.maid())


aetheron =  Actor(char="a",
                     color=color.aetheron,
                     name="Aetheron",
                     ai_cls=MaidAI,
                     fighter=Fighter(hp=30, base_defense=3, base_attack=7, base_speed=5, base_focus=9, base_accuracy=0,base_dodge=5,base_power=0,base_shock_resist=-60),
                    inventory=Inventory(capacity=0),
                     level=Level(xp_given=500),
                     status=Status(),
                    damage_type=DamageType.SHOCK,
                     cyberware=Cyberware(),
                     desc=description.aetheron())


health_potion = Item(
    char="!",
    color=color.bar_filled,
    name="Bandage",
    consumable=consumable.HealingConsumable(amount=6),
    desc=description.bandage()
)

fp_potion = Item(
    char="!",
    color=color.fp,
    name="Glomp-Star Energy",
    shortname="Energy Drink",
    consumable=consumable.FocusConsumable(amount=4),
    desc=description.energy_drink()
)


pistol_ammo = Item(
    char=":",
    color=color.chaser,
    name="9mm Rounds",
    consumable=consumable.Ammo(rounds=12, gun_type="Pistol"),
    desc=description.pistol_ammo()
)
rifle_ammo = Item(
    char=":",
    color=color.combat_doll,
    name="5.57 Rounds",
    consumable=consumable.Ammo(rounds=24, gun_type="Assault Rifle"),
    desc=description.assault_ammo()
)
chaingun_ammo = Item(
    char=":",
    color=color.doll,
    name="20mm Rounds",
    consumable=consumable.Ammo(rounds=50, gun_type="Chain Gun"),
    desc=description.chain_ammo()
)


estrogen= Item(
char="~",
    color=color.doll,
    name="Estrogen",
    consumable=consumable.EstrogenConsumable(duration=200),
    desc=description.estrogen()
)



weed = Item(
char="~",
    color=color.haxor_green,
    name="Weed",
    consumable=consumable.WeedConsumable(),
    desc=description.weed()

)

progesterone= Item(
char="~",
    color=color.hypno_sentry,
    name="Progesterone",
    shortname="Prog",
    consumable=consumable.ProgesteroneConsumable(duration=200),
    desc=description.prog()



)
poppers = Item(
char="~",
    color=color.corpo_sentry,
    name="Poppers",
    consumable=consumable.PoppersConsumable(duration=200, amount=10),
    desc=description.poppers()


)

amphetamines= Item(
char="~",
    color=color.corpo_drone,
    name="Amphetamine Salts",
    shortname="Amphetamine",
    consumable=consumable.AmphetameineConsumable(duration=200, amount=10),
    desc=description.amphetamines()


)
hypnofile = Item(
char="~",
    color=color.hypno_drone,
    name="Hypno File",
    consumable=consumable.hypnofileConsumable(duration=200,),
    desc=description.hypnofile()

)
personal_shield=Item(
char="~",
    color=color.fp,
    name="Personal Shield",
    shortname="Pers. Shield",
    consumable=consumable.pocket_shieldConsumable(duration=200,amount=10),
    desc=description.pocket_shield()

)
flare=Item(
char="~",
    color=color.combat_doll,
    name="Flare",
    consumable=consumable.flareConsumable(damage=10),
    desc=description.flare()
)
lithium_battery = Item(
    char="~",
    color=color.security_bot,
    name="Old Lithium Battery",
    shortname="Old Battery",
    consumable=consumable.ArcDamageConsumable(damage=6, maximum_range=5),
    desc=description.battery()
)
adrenaline = Item(
    char="~",
    color=color.angel,
    name="Adrenal Stimulant",
    shortname="Adrnl Stim",
    consumable=consumable.AdrenalineComsumable(duration=200),
    desc=description.adrenaline())

ketamine_scroll = Item(
    char="~",
    color=color.white,
    name="Ketamine Dart",
    shortname="Ket Dart",
    consumable=consumable.ConfusionConsumable(number_of_turns=20),
    desc=description.ketamine()
)
fire_grenade= Item(
    char="~",
    color=color.exterminator,
    name="Molotov Cocktail",
    shortname="Mltv Cocktail",
    consumable=consumable.FireExplosionConsumable(damage=12, radius=3),
    desc=description.fire_grenade()
)
frag_grenade= Item(
    char="~",
    color=color.chaser,
    name="Grenade",
    consumable=consumable.FragConsumable(damage=15, radius=3),
    desc=description.frag_grenade()
)


cool_knife=Item(
    char="/", color=color.corpo_sentry, name="Cool Knife", equippable=equippable.cool_knife(), desc=description.knife()
)
shock_claws=Item(
    char="/", color=color.security_bot,name="Shock Claws", equippable=equippable.shock_claws(),desc=description.ShockClaw()
)
misericorde=Item(
    char="/", color=color.nano_cloud,name="Misericorde", equippable=equippable.misericorde(),desc=description.misiericorde())
labrys=Item(
    char="/", color=color.hypno_drone, name="Labrys", equippable= equippable.labrys(),desc=description.labrys()
)
rapier=Item(
    char="/", color=color.hypno_sentry, name="Rapier", equippable=equippable.rapier(),desc=description.rapier()
)

pistol=Item(
    char="/", color=color.forklift, name="Pistol", equippable=equippable.pistol(),desc=description.pistol()
)

assaultRifle=Item(
    char="/", color=color.combat_doll, name="Assault Rifle", shortname="As.Rfl", equippable=equippable.assualtRifle(),desc=description.assault()
)
#flameThrower=Item(
 #   char="/", color=(255,20,20), name="Flame Thrower", equippable=equippable.assualtRifle(), desc=description.assault()
#)
angelGun=Item(
    char="/", color=(255,255,255),name="HOLY LIGHT", equippable=equippable.angelGun(),desc=description.angelGun()
)

angelSword=Item(
    char="/", color=(255,255,255),name="DIVINE WRATH", equippable=equippable.angelSword(),desc=description.angelSword()
)

chainGun=Item(
    char="/", color=color.doll,name="Chain Gun", equippable=equippable.chainGun(),desc=description.ChainGun()
)
latexBodySuit=Item(
    char="[", color=color.hypno_drone, name="Latex BodySuit", shortname="Ltx Bdysuit", equippable=equippable.latex_bodysuit(),desc=description.bodysuit()
)
leather_jacket=Item(
    char="[", color=(139,69,19), name="Leather Jacket", shortname="Lthr Jacket",equippable=equippable.leather_jacket(),desc=description.leather_jacket()

)
jumpsuit=Item(
    char="[",color=color.forklift, name="Jumpsuit", equippable=equippable.jumpsuit(),desc=description.jumpsuit()
)
dress=Item(
    char="[", color=(50,50,50), name="Dress", equippable=equippable.dress(),desc=description.dress()
)

hazard_suit = Item(
    char="[", color=color.aetheron, name="Hazmat PPE ",equippable= equippable.hazard_suit(),desc=description.hazard_suit()
)
#body_armor=Item(
   # char="[", color=(5,5,10), name="Body Armor", equippable=equippable.body_armor(),desc=description.body_armor()
#)
hack_upgrade = Item(
    char="i", color=color.haxor_green, name="Prefrontal Cache",shortname="L1 Cache", bodymod= bodymod.hack_upgrade(),desc=description.hack_upgrade()
)

los_upgrade = Item(
    char="i", color=color.maid, name="Long Range Sensors", shortname="Sensors", bodymod= bodymod.los_upgrade(),desc=description.los_upgrade()
)
accuracy_upgrade=Item(
    char="i", color=(139,69,19), name="Integrated Fire Control", shortname="Int Fire Cntrl", bodymod= bodymod.accuracy_upgrade(),desc=description.accuracy_upgrade()
)

control_upgrade=Item(
    char="i",color=color.doll, name="Network Card", bodymod= bodymod.control_upgrade(),desc=description.control_upgrade()
)


weapon_slot = Item(
    char="i", color=color.hypno_drone, name="Heavy Weapon Platform", shortname="Hvy Wpn Pltfrm", bodymod= bodymod.weapon_slot(),desc=description.weapon_slot()
)
shielding = Item(
    char="i", color=color.hypno_sentry, name="Shielding Upgrade", shortname="Shlding", bodymod=bodymod.shielding(),desc=description.shielding()
)

electrical_shielding=Item(
    char="i", color=color.security_bot, name="Faraday Suite", shortname="Faraday", bodymod= bodymod.electrical_shielding(),desc=description.electrical_shielding()
)
fire_shielding=Item(
    char="i", color=color.exterminator, name="Rapid Cooling Trunk", shortname="Cooling Trunk",bodymod= bodymod.fire_sheilding(),desc=description.fire_sheilding()
)
boobs=Item(
    char="i", color=(50,50,50), name="Breast Forms", bodymod=bodymod.boobs(), desc=description.boobs()
)

reflex_upgrade=Item(
    char="i", color=color.combat_doll, name="Rapid Response Servos", shortname="Rpd Servos", bodymod=bodymod.reflex_upgrade(), desc=description.reflex_upgrade()
)


bionic_arm=Item(
    char="i", color=color.aetheron, name="High Tensile Tendons", shortname="HiTense Tndns",bodymod=bodymod.bionic_arm(), desc=description.bionic_arm()

)

rocket_fist=Item(
    char="i", color=color.chaser, name="R.P.F", bodymod=bodymod.rocket_fist(), desc=description.rocket_fist()
)

power_legs=Item(
    char="i", color=color.chem_slime, name="Stability Modules", shortname="Stblty Mdls",bodymod=bodymod.power_legs(), desc=description.power_legs()
)

carrymod=Item(
    char="i", color=color.forklift, name="Carbon Nano-Bones",shortname="Crbn Bones",bodymod=bodymod.carry(), desc=description.carrymod()
)


super_legs = Item(
    char= "i", color=color.security_sentry, name="Sprinter Package",shortname="Sprntr Pkg", bodymod=bodymod.super_legs(), desc= description.super_legs()
)


MedBay = Station(
    char=" ", color=color.white, name="Medbay",desc=description.med_bay())

DownStairs=Station(
    char=" ", color=color.white, name="Exit...",desc=description.down_stairs())

Goal=Station(
    char=" ", color=color.doll, name="THE AUTO-SURGEON!!!",desc=description.goal_tile())
