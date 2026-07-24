from __future__ import annotations

from typing import Optional, TYPE_CHECKING
from IMPULSE import color
if TYPE_CHECKING:
    from IMPULSE.entity import Actor


class StatusEffect:
    abrev="placeholder"
    def __init__(self, target: Actor, max_time: int,):
        self.parent=target
        self.max_time= max_time
        self.time_remaining = max_time
        self.orig_char=self.parent.char
        self.orig_color=self.parent.color
        self.parent_is_player = (target==target.gamemap.engine.player)


    def decrement_timer(self):
        self.time_remaining -=1

    def update(self) ->bool:
        print(self.time_remaining)
        if self.time_remaining>0:
            self.perform()
            self.decrement_timer()
            return True
        else:
            self.on_timer_end()
            return False

    def end_effect(self):
        raise NotImplementedError
    def on_timer_end(self):
        self.end_effect()
    def perform(self):
        raise NotImplementedError
class Burning(StatusEffect):
    abrev="BURN"
    def __init__(self, target: Actor,):
        max_time=100
        super().__init__(target, max_time)

    def perform(self):
        if self.time_remaining % 15 == 0:
            if self.parent.char==self.orig_char:
                self.parent.char='!'
                self.parent.color=(255,0,0)

                self.parent.fighter.apply_damage(3)
                if self.parent_is_player:
                    self.parent.gamemap.engine.message_log.add_message(f"YOU ARE ON FUCKING FIRE!!",color.red)
                else:
                    self.parent.gamemap.engine.message_log.add_message(f"THE {self.parent.name.upper()} IS BURNING!",color.red)

            else:
                self.parent.char=self.orig_char
                self.parent.color=self.orig_color


    def end_effect(self):
        self.parent.char =self.orig_char
        self.parent.color=self.orig_color
        if self.parent_is_player:
            self.parent.gamemap.engine.message_log.add_message(f"{self.parent.name} has been extinguished.")
        else:
            self.parent.gamemap.engine.message_log.add_message(f"The {self.parent.name} has been extinguished.")

class Confused(StatusEffect):
    abrev="CONF"
    def __init__(self, target: Actor, max_time: int):
        super().__init__(target, max_time)
        self.orig_ai=self.parent.ai
        if self.parent_is_player:
            self.parent.gamemap.engine.message_log.add_message(f"{self.parent.name} is dissociating...",color.impossible)
        else:
            self.parent.gamemap.engine.message_log.add_message(f"The {self.parent.name} is dissociating...",color.impossible)
    def perform(self):

        self.parent.ai.confuse()


        if self.time_remaining % 15 > 0:
            if self.parent.char == self.orig_char:
                self.parent.char = '?'
                self.parent.color = (255, 0, 255)

    def end_effect(self):
        self.parent.char = self.orig_char
        self.parent.color = self.orig_color
        self.parent.ai.reset_ai(self.orig_ai)
        if self.parent_is_player:
            self.parent.gamemap.engine.message_log.add_message(f"You are no longer dissociating.")
        self.parent.gamemap.engine.message_log.add_message(f"The {self.parent.name} has regained awareness.")


class Stunned(StatusEffect):
    abrev = "STUN"


class Targeted(StatusEffect):
    abrev = "TRGT"

    def __init__(self, attacker: Actor, target: Actor, max_time: int, amount: int):
        super().__init__(target, max_time)
        self.amount = amount
        self.attacker = attacker


class Dysphoria(StatusEffect):
    abrev = "DYS"

    def __init__(self, target: Actor, max_time: int):
        super().__init__(target, max_time)

    def perform(self):
        if self.time_remaining == self.max_time:
            self.parent.status.power_bonus-=1
            self.parent.status.reflex_bonus -= 1
            self.parent.status.focus_bonus -= 1

            messageStr= f"{self.parent.name} is overcome with dysphoria!"

            if self.parent.fighter.hp>1:
                self.parent.fighter.hp -=1
            if self.parent.fighter.fp>1:
                self.parent.fighter.fp -=1

            if self.parent is not self.parent.gamemap.engine.player:
                messageStr= "The "+messageStr
            self.parent.gamemap.engine.message_log.add_message(messageStr,color.hypno_sentry)

        #Lower POWER REFLEX AND FOCUS BY 1 only once!

    def end_effect(self):
        self.parent.status.power_bonus += 1
        self.parent.status.reflex_bonus += 1
        self.parent.status.focus_bonus += 1


        messageStr = f"{self.parent.name} is no longer dysphoric."
        if self.parent is not self.parent.gamemap.engine.player:
            messageStr = "The " + messageStr
        self.parent.gamemap.engine.message_log.add_message(messageStr)



class Euphoria(StatusEffect):
    abrev = "EUPH"

    def __init__(self, target: Actor, max_time: int, from_body: bool = False):
        super().__init__(target, max_time)
        self.from_body=from_body

    def perform(self):
        if self.time_remaining == self.max_time:
            self.parent.status.power_bonus += 1
            self.parent.status.reflex_bonus += 1
            self.parent.status.focus_bonus += 1
            self.parent.fighter.hp += 1
            self.parent.fighter.fp += 1
            messageStr = f"{self.parent.name} is experiencing euphoria!"
            if self.parent is not self.parent.gamemap.engine.player:
                messageStr = "The " + messageStr
            self.parent.gamemap.engine.message_log.add_message(messageStr,color.health_recovered)

        if self.from_body:
            try:
                if self.parent.cyberware.torso.name=="Breast Forms":
                    self.time_remaining =  self.max_time*2

            except:
                self.end_effect()


        # Raise POWER REFLEX AND FOCUS BY 1 only once!

    def end_effect(self):
        self.parent.status.power_bonus -= 1
        self.parent.status.reflex_bonus -= 1
        self.parent.status.focus_bonus -= 1
        self.parent.fighter.drain_fp(1)
        if self.parent.fighter.hp > 1:
            self.parent.fighter.hp -= 1

        messageStr = f"{self.parent.name} is no longer euphoric."
        if self.parent is not self.parent.gamemap.engine.player:
            messageStr = "The " + messageStr

        self.parent.gamemap.engine.message_log.add_message(messageStr)

class Horny(StatusEffect):
    abrev = "UWU"

    def __init__(self, target: Actor, max_time: int):
        super().__init__(target, max_time)

    def perform(self):
        if self.time_remaining == self.max_time:
            self.parent.status.power_bonus += 2
            self.parent.fighter.hp += 2

            messageStr = f"{self.parent.name} is seething with lust!"
            if self.parent is not self.parent.gamemap.engine.player:
                messageStr = "The " + messageStr
            self.parent.gamemap.engine.message_log.add_message(messageStr, color.doll)

        # Raise POWER 2 only once!

    def end_effect(self):
        self.parent.status.power_bonus -= 2
        if self.parent.fighter.hp > 2:
            self.parent.fighter.hp -= 2
        elif self.parent.fighter.hp > 1:
            self.parent.fighter.hp -= 1
        messageStr = f"{self.parent.name} has calmed down."
        if self.parent is not self.parent.gamemap.engine.player:
            messageStr = "The " + messageStr
        self.parent.gamemap.engine.message_log.add_message(messageStr)



class Hyper(StatusEffect):
    abrev="RFLX"

    def __init__(self, target: Actor, max_time: int):
        super().__init__(target, max_time)

    def perform(self):
        if self.time_remaining == self.max_time:
            self.parent.status.reflex_bonus += 3
            messageStr = f"{self.parent.name} is hyper-responsive!"
            if self.parent is not self.parent.gamemap.engine.player:
                messageStr = "The " + messageStr
            self.parent.gamemap.engine.message_log.add_message(messageStr,color.security_bot)


    def end_effect(self):
        self.parent.status.reflex_bonus -= 3
        messageStr = f"{self.parent.name} is no longer hyper-responsive."
        if self.parent is not self.parent.gamemap.engine.player:
            messageStr = "The " + messageStr
        self.parent.gamemap.engine.message_log.add_message(messageStr,)

class Focused(StatusEffect):
    abrev = "FOC"
    def __init__(self, target: Actor, max_time: int):
        super().__init__(target, max_time)

    def perform(self):
        if self.time_remaining == self.max_time:
            self.parent.status.focus_bonus += 2
            self.parent.fighter.fp += 2
            messageStr = f"{self.parent.name} is hyperfocused!"
            if self.parent is not self.parent.gamemap.engine.player:
                messageStr = "The " + messageStr
            self.parent.gamemap.engine.message_log.add_message(messageStr,color.fp)

        # Raise FOCUS 2 only once!

    def end_effect(self):
        self.parent.status.focus_bonus -= 2
        self.parent.fighter.fp -= 2

        messageStr = f"{self.parent.name} is no longer hyperfocused."
        if self.parent is not self.parent.gamemap.engine.player:
            messageStr = "The " + messageStr
        self.parent.gamemap.engine.message_log.add_message(messageStr)


class HPBuff(StatusEffect):
    abrev = "HPUP"

    def __init__(self, target: Actor, max_time: int, amount:int):
        super().__init__(target, max_time)
        self.amount=amount
    def perform(self):
        if self.time_remaining == self.max_time:
            self.parent.status.HP_bonus += self.amount
            self.parent.fighter.hp += self.amount
            messageStr = f"{self.parent.name} is numbed to pain!"
            if self.parent is not self.parent.gamemap.engine.player:
                messageStr = "The " + messageStr
            self.parent.gamemap.engine.message_log.add_message(messageStr,color.haxor_green)

        # Raise HP 10 only once!

    def end_effect(self):
        self.parent.status.HP_bonus -= self.amount
        if self.parent.fighter.hp > self.parent.fighter.max_hp:
            self.parent.fighter.hp = self.parent.fighter.max_hp
        messageStr = f"{self.parent.name} can feel pain again."
        if self.parent is not self.parent.gamemap.engine.player:
            messageStr = "The " + messageStr
        self.parent.gamemap.engine.message_log.add_message(messageStr)


class FPBuff(StatusEffect):
    abrev = "FPUP"
    def __init__(self, target: Actor, max_time: int, amount:int):
        super().__init__(target, max_time)
        self.amount=amount
    def perform(self):
        if self.time_remaining == self.max_time:
            self.parent.status.FP_bonus += self.amount
            self.parent.fighter.fp += self.amount
            messageStr = f"{self.parent.name}'s processing has increased!"
            if self.parent is not self.parent.gamemap.engine.player:
                messageStr = "The " + messageStr
            self.parent.gamemap.engine.message_log.add_message(messageStr,color.fp)

        # Raise FP 10 only once!

    def end_effect(self):
        self.parent.status.FP_bonus -= self.amount
        if self.parent.fighter.fp > self.parent.fighter.max_fp:
            self.parent.fighter.fp = self.parent.fighter.max_fp
        messageStr = f"{self.parent.name}'s processing has slowed back down."
        if self.parent is not self.parent.gamemap.engine.player:
            messageStr = "The " + messageStr
        self.parent.gamemap.engine.message_log.add_message(messageStr)

class Reaper(StatusEffect):
    abrev ="DEATH"

    def __init__(self, target: Actor):
        super().__init__(target, max_time=100)


    def perform(self):


        if abs(self.time_remaining % 5)==0:

            self.parent.fighter.apply_damage(10)
            if not self.parent.is_alive:
                self.parent.char = '%'
                self.orig_char = '%'


            if self.parent.char==self.orig_char and self.orig_char !='%':
                self.parent.char='!'
                self.parent.color=(0,0,0)

            else:
                self.parent.char=self.orig_char
                self.parent.color=self.orig_color


    def end_effect(self):
        self.orig_char='%'
        self.parent.fighter.die()


class Shielded(StatusEffect):
    abrev = "SHLD"
    def __init__(self, target: Actor, max_time: int, amount:int):
        super().__init__(target, max_time)
        self.amount=amount
    def perform(self):
        if self.time_remaining == self.max_time:
            self.parent.status.defense_bonus += self.amount
            messageStr = f"{self.parent.name}'s defense has increased!"
            if self.parent is not self.parent.gamemap.engine.player:
                messageStr = "The " + messageStr
            self.parent.gamemap.engine.message_log.add_message(messageStr)

    def end_effect(self):
        self.parent.status.defense_bonus -= self.amount
        messageStr = f"{self.parent.name} is no longer shielded."
        if self.parent is not self.parent.gamemap.engine.player:
            messageStr = "The " + messageStr
        self.parent.gamemap.engine.message_log.add_message(messageStr)

class High(StatusEffect):
    abrev = "HIGH"
    def __init__(self, target: Actor, max_time: int, amount:int):
        super().__init__(target, max_time)
        self.amount=amount
    def perform(self):
        if self.time_remaining == self.max_time:
            messageStr = f"{self.parent.name} is feeling good."
            if self.parent is not self.parent.gamemap.engine.player:
                messageStr = "The " + messageStr
            self.parent.gamemap.engine.message_log.add_message(messageStr)

    def end_effect(self):
        messageStr = f"{self.parent.name} has come down."
        if self.parent is not self.parent.gamemap.engine.player:
            messageStr = "The " + messageStr
        self.parent.gamemap.engine.message_log.add_message(messageStr)