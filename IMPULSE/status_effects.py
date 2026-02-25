from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from IMPULSE.components.ai import HostileEnemy, ConfusedEnemy

from color import status_effect

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



    def decrement_timer(self):
        self.time_remaining -=1
    def update(self):
        if self.time_remaining>=-1:
            self.decrement_timer()
            if self.time_remaining>0:
                self.perform()
            else:
                self.on_timer_end()
        else:
            self.perform()
    def perform(self):
        raise NotImplementedError
    def end_effect(self):
        raise NotImplementedError
    def on_timer_end(self):
        self.end_effect()

class Burning(StatusEffect):
    abrev="BURN"
    def __init__(self, target: Actor,max_time: int, str="BURN"):
        super().__init__(target, max_time)

    def perform(self):
        if self.time_remaining % 15 >0:
            if self.parent.char==self.orig_char:
                self.parent.char='!'
                self.parent.color=(255,0,0)
                self.parent.fighter.take_damage(3)
                self.parent.gamemap.engine.message_log.add_message(f"THE {self.parent.name} IS BURNING!")

            else:
                self.parent.char=self.orig_char
                self.parent.color=self.orig_color


    def end_effect(self):
        self.parent.char =self.orig_char
        self.parent.color=self.orig_color
        self.parent.gamemap.engine.message_log.add_message(f"The {self.parent.name} has been extinguished")

class Confused(StatusEffect):
    abrev="CONF"
    def __init__(self, target: Actor, max_time: int):
        super().__init__(target, max_time)
        self.orig_ai=self.parent.ai

    def perform(self):
        if self.parent.ai is not ConfusedEnemy:
            self.parent.ai=ConfusedEnemy(self.parent)
            self.parent.gamemap.engine.message_log.add_message(f"The {self.parent.name} is disassociating...")

        if self.time_remaining % 15 > 0:
            if self.parent.char == self.orig_char:
                self.parent.char = '?'
                self.parent.color = (255, 0, 255)

    def end_effect(self):
        self.parent.char = self.orig_char
        self.parent.color = self.orig_color
        self.parent.ai=self.orig_ai
        self.parent.gamemap.engine.message_log.add_message(f"The {self.parent.name} has regained its wits")


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
            if self.parent is not self.parent.gamemap.engine.player:
                messageStr= "The "+messageStr
            self.parent.gamemap.engine.message_log.add_message(messageStr)

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

            messageStr = f"{self.parent.name} is experiencing euphoria!"
            if self.parent is not self.parent.gamemap.engine.player:
                messageStr = "The " + messageStr
            self.parent.gamemap.engine.message_log.add_message(messageStr)

        if self.from_body:
            try:
                if self.parent.cyberware.torso.name=="Breast Forms":
                    if self.time_remaining==-2:
                        self.time_remaining -=1
            except:
                self.end_effect()
        # Raise POWER REFLEX AND FOCUS BY 1 only once!

    def end_effect(self):
        self.parent.status.power_bonus -= 1
        self.parent.status.reflex_bonus -= 1
        self.parent.status.focus_bonus -= 1

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

            messageStr = f"{self.parent.name} is seething with lust!"
            if self.parent is not self.parent.gamemap.engine.player:
                messageStr = "The " + messageStr
            self.parent.gamemap.engine.message_log.add_message(messageStr)

        # Raise POWER 2 only once!

    def end_effect(self):
        self.parent.status.power_bonus -= 2
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
            self.parent.status.reflex_bonus += 2
            messageStr = f"{self.parent.name} is hyper-responsive!"
            if self.parent is not self.parent.gamemap.engine.player:
                messageStr = "The " + messageStr
            self.parent.gamemap.engine.message_log.add_message(messageStr)


    def end_effect(self):
        self.parent.status.reflex_bonus -= 2
        messageStr = f"{self.parent.name} is no longer hyper-responsive."
        if self.parent is not self.parent.gamemap.engine.player:
            messageStr = "The " + messageStr
        self.parent.gamemap.engine.message_log.add_message(messageStr)

class Focused(StatusEffect):
    abrev = "FOC"
    def __init__(self, target: Actor, max_time: int):
        super().__init__(target, max_time)

    def perform(self):
        if self.time_remaining == self.max_time:
            self.parent.status.focus_bonus += 2
            messageStr = f"{self.parent.name} is hyperfocused!"
            if self.parent is not self.parent.gamemap.engine.player:
                messageStr = "The " + messageStr
            self.parent.gamemap.engine.message_log.add_message(messageStr)

        # Raise FOCUS 2 only once!

    def end_effect(self):
        self.parent.status.focus_bonus -= 2
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
            messageStr = f"{self.parent.name} is numbed to pain!"
            if self.parent is not self.parent.gamemap.engine.player:
                messageStr = "The " + messageStr
            self.parent.gamemap.engine.message_log.add_message(messageStr)

        # Raise HP 10 only once!

    def end_effect(self):
        self.parent.status.HP_bonus -= self.amount
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
            messageStr = f"{self.parent.name}'s processing has increased!"
            if self.parent is not self.parent.gamemap.engine.player:
                messageStr = "The " + messageStr
            self.parent.gamemap.engine.message_log.add_message(messageStr)

        # Raise FP 10 only once!

    def end_effect(self):
        self.parent.status.FP_bonus -= self.amount
        messageStr = f"{self.parent.name}'s processing has slowed back down."
        if self.parent is not self.parent.gamemap.engine.player:
            messageStr = "The " + messageStr
        self.parent.gamemap.engine.message_log.add_message(messageStr)

