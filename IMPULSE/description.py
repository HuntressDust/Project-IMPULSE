from __future__ import annotations

from IMPULSE.components import bodymod


class Description:
    def __init__(self, line1: str="", line2:str="", line3:str=""):
        self.line1=line1
        self.line2=line2
        self.line3=line3
        self.text_lines=list([line1,line2,line3])

default_description = Description("placeholder1",
                                  "placeholder2",
                                  "placeholder3")

class pistol(Description):
    def __init__(self)->None:
        super().__init__(
        line1="A 9mm handgun. Can be wielded one handed. holds 12 9mm rounds, single-fire",
        line2="Small, reliable. Polished plexsteel body, nyla-max grip. Feels good to hold.",
        line3="Good all-around weapon."
    )

class assault(Description):
    def __init__(self)->None:
        super().__init__(
    line1="A milspec assault rifle, requires 2 hands. holds 24 5.57 rounds, fires in 3 round burts",
    line2="An older but powerful model, probably dropped by some corpo running-dog from the cobalt wars",
    line3="Solid weapon if you can use it.",
    )
class ChainGun(Description):
    def __init__(self)->None:
        super().__init__(
    line1="A hulking beast of a gun. Requiresd two hands, fires 6 rounds of 5.57 per action",
    line2="Designed to rip through crowds of unarmored targets. the noise is overwhelming",
    line3="Kicks like a cyber-mare. Designed to be used by super soldiers"
)

class leather_jacket(Description):
    def __init__(self)->None:
        super().__init__(
    line1="A sturdy Leather Jacket. Real leather, too.",
    line2="Designed of neo-cycle drivers, lots of pockets, and its warm too.",
    line3="Protects agains cuts, scraps, and has some insulating properites. Plus you look hot in it"

)
class dress(Description):
    def __init__(self)->None:
        super().__init__(
    line1="A beautiful black dress",
    line2="High quality and elegant, it catches the air and blows all badass.",
    line3="Allows a freedom of movement that pants simply do not allow."

)
class bodysuit(Description):
    def __init__(self)->None:
        super().__init__(
    line1="A latec bodysuit. Insulates you from electicity",
    line2="Impractical? Yes. Sexy? Very Yes.",
    line3="Doesnt Protect from imapact or heat, but it hugs your curves.",
)

class umpsuit(Description):
    def __init__(self)->None:
        super().__init__(
    line1="A Hi-viz work uniform. Flame and cut resistant",
    line2="Blue with yellow reflective sripes, used by mechanics and therians alike.",
    line3="Decently protective and quite fasionable to the right crowd."
)
class knife(Description):
    def __init__(self)->None:
        super().__init__(
    line1='A big knife. can be wielded in one hand',
    line2="Razor sharp and deadly, from your own personal collection. Girls find it very hot",
    line3="Good for sex and self defense, but not meant for prolonged combats"
)
class misiericorde(Description):
    def __init__(self)->None:
        super().__init__(
    line1="A long dagger like weapon meant to deliver a killing blow",
    line2="Used by security forces for getting around kevlar.",
    line3="Can be used in ine hand can attack twice"
)
class labrys(Description):
    def __init__(self)->None:
        super().__init__(
    line1= "A large two-headed axe. Used with two hands.",
    line2="The traditional weapon of the amazons and those from the Ilse of Lesbos",
    line3="huge and powerful. Probably left by an underground dyke group")
class ShockClaw(Description):
    def __init__(self)->None:
        super().__init__(
    line1="Electically charged gauntel tipped with razor sharp claws",
    line2='The claws rip though wire and break through insulating skin, allowing the electicity to be delivered to vulnerable areas',
    line3="Can be painted a varity of fun colors, and you dont have to worry about hangnails ",
)


class hack_upgrade(Description):
    def __init__(self)->None:
        super().__init__(
    line1="A co-processor directly enhancing your mental faculties",
    line2="connects to your brainstem via a series of tubes",
    line3=f"Enhances FOCUS by {bodymod.hack_upgrade.focus_bonus} points",
)

class los_upgrade(Description):
    def __init__(self)->None:
        super().__init__(
    line1="sensors that consinuously sweep your surroundings",
    line2="feeds sonar data directy into your visual cortex",
    line3="Increases the distances at which tiles are revealed by 5 points",
)
class accuracy_upgrade(Description):
    def __init__(self)->None:
        super().__init__(
    line1="Fine-motor control stimulation that enhances your hand-eye coordination",
    line2="Standard issue for corpo sentry drones",
    line3=f"Enhances ranged accuracy by {bodymod.accuracy_upgrade.accuracy_bonus} points",
)
class control_upgrade(Description):
    def __init__(self)->None:
        super().__init__(
    line1="networking co processor that handles connection between conciouness",
    line2="Reduces the stress of puppetering immensly",
    line3=f"Allows you to puppet 2 additional beings",
)


class weapon_slot(Description):
    def __init__(self)->None:
        super().__init__(
    line1="Swivel mount for heavy weaponds attached to your side",
    line2="Remeber the butch from Aliens? Its that",
    line3=f"Unlocks an additional weapon slot"

)
class sheilding(Description):
    def __init__(self)->None:
        super().__init__(
    line1="PlexSteel plating embeded in your torsi",
    line2="Protects againts all attacks",
    line3=f"Enhnaces HP by {bodymod.sheilding.health_bonus} points",
)

class electric_sheilding(Description):
    def __init__(self)->None:
        super().__init__(
    line1="A seriens of conductive pathways embeded between cyberware",
    line2="allows electicity to pass harmlessly to ground",
    line3=f"Enhances SHOCK RESISTANCE by {bodymod.electric_sheilding.shock_resist} points",
)
class fire_sheilding(Description):
    def __init__(self)->None:
        super().__init__(
    line1="An integrated cooling system throughtout your bodd",
    line2="includings a heat sink near the spine and radiating wings",
    line3=f"Enhances FIRE RESISTANCE by {bodymod.fire_sheilding.fire_resist} points",
)
class boobs(Description):
    def __init__(self)->None:
        super().__init__(
    line1="K-cup breasts",
    line2="theyre big and bouncy and awesome",
    line3="Grants a permanant state of GENDER EUPHORIA (+1 to POWER, REFLEX, and FOCUS)",
)

class reflex_upgrade(Description):
    def __init__(self)->None:
        super().__init__(
    line1="A network of semi-autonomous computers throughout your arms",
    line2="takes raw sensory data reacts without  waiting on the brain to process it",
    line3=f"Enhances REFLEX by {bodymod.reflex_upgrade.reflex_bonus} points",
)

class bionic_arm(Description):
    def __init__(self)->None:
        super().__init__(
    line1="A fully robotic arm",
    line2="made of plexsteel and fiber-optics. Top of the line stuff",
    line3=f"Enhances POWER by {bodymod.bionic_arm.power_bonus} points",

)

class rocket_fist(Description):
    def __init__(self)->None:
        super().__init__(
    line1="Rocket. Powered. Fist",
    line2="Not implemented yet.",
    line3="Allows you to make a powerful ranged attack while UNARMED",
)

class power_legs(Description):
    def __init__(self)->None:
        super().__init__(
    line1="Metal Talons that grip the ground with each step",
    line2="provides a solid base from which to strike",
    line3=f"Enhances POWER by {bodymod.power_legs.power_bonus} points",
)
class carrymod(Description):
    def __init__(self)->None:
        super().__init__(
    line1="Enhanced tibia and femurs",
    line2="allows weight to be dstributed more evenly into the ground",
    line3=f"Allows you to carry 6 additional items",
)


class super_legs(Description):
    def __init__(self)->None:
        super().__init__(
    line1="Ultra-light bionic legs",
    line2="includes high-powered motors and rocket boosters",
    line3=f"Enhances SPEED by {bodymod.super_legs.speed_bonus} points",
)

class itchy_legs(Description):
    def __init__(self)->None:
        super().__init__(
        line1 = "A network of semi-autonomous computers throughout your legs",
        line2 = "takes raw sensory data reacts without waiting on the brain to process it",
        line3 = f"Enhances REFLEX by {bodymod.itchy_legs.reflex_bonus} points",
        )