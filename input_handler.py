from __future__ import  annotations

import math
import os

import tcod
from typing import Optional, Tuple, Callable, TYPE_CHECKING, Union

from IMPULSE import actions
from IMPULSE.tile_types import usedMedbay
from IMPULSE.actions import (Action,
                             BumpAction,
                             EscapeAction,
                             PickupAction,
                             WaitAction,
                             RangedAttackAction,
                             TakeStairsAction

                             )
from IMPULSE import color
from IMPULSE import exceptions
from IMPULSE.equipment_types import EquipmentType
from IMPULSE.exceptions import Impossible

if TYPE_CHECKING:
    from IMPULSE.engine import Engine
    from IMPULSE.entity import Item, Entity
    from IMPULSE import setup_game



MOVE_KEYS = {
    # Arrow keys.
    tcod.event.KeySym.UP: (0, -1),
    tcod.event.KeySym.DOWN: (0, 1),
    tcod.event.KeySym.LEFT: (-1, 0),
    tcod.event.KeySym.RIGHT: (1, 0),
    tcod.event.KeySym.HOME: (-1, -1),
    tcod.event.KeySym.END: (-1, 1),
    tcod.event.KeySym.PAGEUP: (1, -1),
    tcod.event.KeySym.PAGEDOWN: (1, 1),
    # WASD

    tcod.event.KeySym.W: (0, -1),
    tcod.event.KeySym.S: (0, 1),
    tcod.event.KeySym.A: (-1, 0),
    tcod.event.KeySym.D: (1, 0),
    tcod.event.KeySym.Q: (-1, -1),
    tcod.event.KeySym.Z: (-1, 1),
    tcod.event.KeySym.E: (1, -1),
    tcod.event.KeySym.C: (1, 1),

    # Numpad keys.
    tcod.event.KeySym.KP_1: (-1, 1),
    tcod.event.KeySym.KP_2: (0, 1),
    tcod.event.KeySym.KP_3: (1, 1),
    tcod.event.KeySym.KP_4: (-1, 0),
    tcod.event.KeySym.KP_6: (1, 0),
    tcod.event.KeySym.KP_7: (-1, -1),
    tcod.event.KeySym.KP_8: (0, -1),
    tcod.event.KeySym.KP_9: (1, -1),
}

WAIT_KEYS = {
    tcod.event.KeySym.PERIOD,
    tcod.event.KeySym.KP_5,
    tcod.event.KeySym.CLEAR,
    tcod.event.KeySym.SPACE,

}
CONFIRM_KEYS = {
    tcod.event.KeySym.RETURN,
    tcod.event.KeySym.KP_ENTER

}

CURSOR_Y_KEYS = {
    tcod.event.K_UP: -1,
    tcod.event.K_DOWN: 1,
    tcod.event.K_PAGEUP: -10,
    tcod.event.K_PAGEDOWN: 10,
}


TEXT_KEYS={
    tcod.event.KeySym.A: "a",
    tcod.event.KeySym.B: "b",
    tcod.event.KeySym.C: "c",
    tcod.event.KeySym.D: "d",
    tcod.event.KeySym.E: "e",
    tcod.event.KeySym.F: "f",
    tcod.event.KeySym.G: "g",
    tcod.event.KeySym.H: "h",
    tcod.event.KeySym.I: "i",
    tcod.event.KeySym.J: "j",
    tcod.event.KeySym.K: "k",
    tcod.event.KeySym.L: "l",
    tcod.event.KeySym.M: "m",
    tcod.event.KeySym.N: "n",
    tcod.event.KeySym.O: "o",
    tcod.event.KeySym.P: "p",
    tcod.event.KeySym.Q: "q",
    tcod.event.KeySym.R: "r",
    tcod.event.KeySym.S: "s",
    tcod.event.KeySym.T: "t",
    tcod.event.KeySym.U: "u",
    tcod.event.KeySym.V: "v",
    tcod.event.KeySym.W: "w",
    tcod.event.KeySym.X: "x",
    tcod.event.KeySym.Y: "y",
    tcod.event.KeySym.Z: "z",
    tcod.event.KeySym.N0: "0",
    tcod.event.KeySym.N1: "1",
    tcod.event.KeySym.N2: "2",
    tcod.event.KeySym.N3: "3",
    tcod.event.KeySym.N4: "4",
    tcod.event.KeySym.N5: "5",
    tcod.event.KeySym.N6: "6",
    tcod.event.KeySym.N7: "7",
    tcod.event.KeySym.N8: "8",
    tcod.event.KeySym.N9: "9",

    tcod.event.KeySym.KP_0:"0",
    tcod.event.KeySym.KP_1:"1",
    tcod.event.KeySym.KP_2:"2",
    tcod.event.KeySym.KP_3:"3",
    tcod.event.KeySym.KP_4:"4",
    tcod.event.KeySym.KP_5:"5",
    tcod.event.KeySym.KP_6:"6",
    tcod.event.KeySym.KP_7:"7",
    tcod.event.KeySym.KP_8:"8",
    tcod.event.KeySym.KP_9:"9",


}

#help_image = tcod.image.load("GRAPHICS/Help.png")[:, :, :3]

ActionOrHandler = Union[Action, "BaseEventHandler"]
"""An event handler return value which can trigger an action or switch active handlers.

If a handler is returned then it will become the active handler for future events.
If an action is returned it will be attempted and if it's valid then
MainGameEventHandler will become the active handler.
"""

class BaseEventHandler(tcod.event.EventDispatch[ActionOrHandler]):
    def handle_events(self, event: tcod.event.Event) -> BaseEventHandler:
        state= self.dispatch(event)

        if isinstance(state, BaseEventHandler):
            return state
        assert not isinstance(state,Action), f"{self!r} can not handle actions"
        return self
    def on_render(self, console: tcod.Console) -> None:
        raise NotImplementedError()
    def ev_quit(self, event: tcod.event.Quit,) -> Optional[Action]:
        raise SystemExit()

class PopupMessage(BaseEventHandler):
    def __init__(self, parent_handler: BaseEventHandler, text: str):
        self.parent = parent_handler
        self.text = text

    def on_render(self, console: tcod.Console) -> None:
        self.parent.on_render(console)
        console.tiles_rgb["fg"] //= 8
        console.tiles_rgb["bg"] //= 8

        console.print(
            console.width // 2,
            console.height // 2,
            self.text,
            fg=color.white,
            bg=color.black,
            alignment=tcod.CENTER,
        )

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[BaseEventHandler]:
        return self.parent

class EventHandler(BaseEventHandler):
    def __init__(self, engine: Engine):
        self.engine = engine

    def skip_player(self) -> BaseEventHandler:

        self.engine.player.decrement_wait_counter()
        self.engine.player.status.update_effects()
        self.engine.handle_enemy_turns()

        return self


    def handle_events(self, event: tcod.event.Event) -> BaseEventHandler:
        action_or_state=self.dispatch(event)
        if isinstance(action_or_state,BaseEventHandler):
            return action_or_state
        if not self.engine.player.is_alive:
            return GameOverEventHandler(self.engine)
        if self.handle_action(action_or_state):
            #perform Action
            if not self.engine.player.is_alive:
                #player is dead
                return GameOverEventHandler(self.engine)
            elif self.engine.player.level.requires_level_up:
                return LevelUpHandler(self.engine)
            return MainGameEventHandler(self.engine)

        return self

    def handle_action(self, action: Optional[Action]) -> bool:
        """Handle actions returned from event methods.

        Returns True if the action will advance a turn.
        """
        if action is None:
            return False

        try:
            action.perform()
            if self.engine.player.is_alive:
                self.engine.player.status.update_effects()
        except exceptions.Impossible as exc:
            self.engine.message_log.add_message(exc.args[0], color.impossible)
            return False  # Skip enemy turn on exceptions.

        self.engine.handle_enemy_turns()

        self.engine.update_fov()
        return True

    def ev_mousemotion(self, event: tcod.event.MouseMotion) -> None:
        if self.engine.game_map.in_bounds(int(event.tile.x), int(event.tile.y)):
            self.engine.mouse_location = int(event.tile.x), int(event.tile.y)


    def on_render(self, console: tcod.Console) -> None:
        self.engine.render(console)


class MainGameEventHandler(EventHandler):
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        action: Optional[Action] = None
        key = event.sym
        modifier = event.mod

        player = self.engine.player
        if not player.is_alive:
            return GameOverEventHandler(self.engine)
        if key == tcod.event.KeySym.PERIOD and modifier &(
            tcod.event.KMOD_LSHIFT | tcod.event.KMOD_RSHIFT
        ):
            return actions.TakeStairsAction(player)

        if key in MOVE_KEYS:
            dx, dy = MOVE_KEYS[key]
            action = BumpAction(player, dx, dy)

        if key == tcod.event.KeySym.K:
            return NormalAttackHandler(self.engine)

        elif key in WAIT_KEYS:
            action = WaitAction(player)

        elif key == tcod.event.KeySym.ESCAPE:
            return EscapeHandler(self.engine)

        elif key == tcod.event.KeySym.V:
            return HistoryViewer(self.engine)

        elif key == tcod.event.KeySym.G:
            action = PickupAction(player)

        elif key == tcod.event.KeySym.I:
            return InventoryActivateHandler(self.engine)
        elif key == tcod.event.KeySym.O:
            return InventoryExamineHandler(self.engine)

        elif key == tcod.event.KeySym.R:
            return InventoryDropHandler(self.engine)

        elif key == tcod.event.KeySym.L:
            return LookHandler(self.engine)

        elif key == tcod.event.KeySym.J:
            return CharacterScreenEventHandler(self.engine)

        elif key == tcod.event.KeySym.M:
            if player.fighter.fp>0:
                return HackingSelectHandler(self.engine)
            else:
                self.engine.message_log.add_message("Out of FP!", color.invalid)


        elif key == tcod.event.KeySym.H:
            return HelpScreen(MainGameEventHandler(self.engine))

        elif key in CONFIRM_KEYS:
            if (player.x, player.y) == self.engine.game_map.downstairs_location:
                return TakeStairsAction(player)
            if (player.x,player.y) == self.engine.game_map.goal_location:
                return TakeStairsAction(player)

            if (player.x, player.y) == self.engine.game_map.med_location:
                if not self.engine.game_map.med_used:
                    return BodyModSelectionHandler(self.engine)
                else:
                    self.engine.message_log.add_message("This medbay has already been activated.", color.invalid)
        return action

class GameOverEventHandler(EventHandler):
    def on_quit(self) -> None:
        if os.path.exists("savegame.sav"):
            os.remove("savegame.sav")
        raise exceptions.QuitWithoutSaving()

    def ev_quit(self, event: tcod.event.Quit,) -> None:
        self.on_quit()

    def ev_keydown(self, event: tcod.event.KeyDown,) -> None:

        if event.sym ==  tcod.event.K_ESCAPE:
            self.on_quit()
        else:
            self.engine.game_over=True

class HistoryViewer(EventHandler):
    def __init__(self, engine: Engine):
        super().__init__(engine)
        self.log_length = len(engine.message_log.messages)
        self.cursor = self.log_length -1

    def on_render(self, console: tcod.Console) -> None:
        super().on_render(console)
        log_console = tcod.Console(console.width - 6, console.height - 6)
        log_console.draw_frame(0,0, log_console.width, log_console.height)
        log_console.print_box(
            0,0, log_console.width, 1, "Message history", alignment=tcod.CENTER
        )
        self.engine.message_log.render_messages(
            log_console,1,1, log_console.width-2,log_console.height - 2,
            self.engine.message_log.messages[: self.cursor +1])
        log_console.blit(console,3,3)

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[MainGameEventHandler]:
        if event.sym in CURSOR_Y_KEYS:
            adjust= CURSOR_Y_KEYS[event.sym]
            if adjust < 0 and self.cursor ==0:
                self.cursor =  self.log_length -1
            elif adjust > 0  and self.cursor ==  self.log_length - 1:
                self.cursor = 0
            else:
                self.cursor = max(0,min(self.cursor+ adjust, self.log_length -1))
        elif event.sym ==  tcod.event.K_HOME:
            self.cursor= 0
        elif event.sym ==  tcod.event.K_END:
            self.cursor = self.log_length - 1
        else:
            return MainGameEventHandler(self.engine)
        return None

class EntityDescriptionHandler(EventHandler):
    def __init__(self, engine: Engine, entity: Entity):
        super().__init__(engine)
        self.entity=entity


    def on_render(self, console: tcod.Console) -> None:
        super().on_render(console)

        log_console = tcod.Console(console.width - 6, console.height - 6)
        log_console.draw_frame(0,0, log_console.width, log_console.height)
        log_console.print_box(
            0,0, log_console.width-2, 1, f"{self.entity.name}", alignment=tcod.CENTER
        )

        log_console.print_box(
        0, 5, log_console.width-2, 1, f"{self.entity.char}", alignment=tcod.CENTER,fg=self.entity.color
        )
        i=10
        print(self.entity)
        for line in self.entity.description.text_lines:
            log_console.print_box(
                1, i, log_console.width-2, 2, f"{line}", alignment=tcod.CENTER,
            )
            i+=3
        if hasattr(self.entity,"equippable"):
            equippable=self.entity.equippable
            if equippable is not None:
                stat_line_1=""
                if self.entity.char != "[":
                    stat_line_1+=f"Range: {equippable.range_bonus} "
                if equippable.attack_bonus!=0:
                    stat_line_1+=f"Attack: {equippable.attack_bonus} "
                if equippable.defense_bonus!=0:
                    stat_line_1+=f"Defense: {equippable.defense_bonus}"

                log_console.print_box(
                    0, i, log_console.width, 1, f"{stat_line_1}",alignment=tcod.CENTER,
                )
                i += 2
                stat_line_2 = ""
                if equippable.burn_resist != 0:
                    stat_line_2 += f"Burn Resist {equippable.burn_resist} "
                if equippable.shock_resist != 0:
                    stat_line_2 += f"Shock Resist: {equippable.shock_resist} "
                if equippable.reflex_bonus != 0:
                    stat_line_2 += f"REFLEX Bonus: {equippable.reflex_bonus} "
                if equippable.dodge_bonus !=0:
                    stat_line_2 += f"DODGE Bonus: {equippable.dodge_bonus}"
                if equippable.two_handed:
                    stat_line_2 += f"Two-Handed Weapon"

                log_console.print_box(
                    0, i, log_console.width, 1, f"{stat_line_2}", alignment=tcod.CENTER,
                )
                i += 2
                requirement_str=""
                if equippable.power_needed>0:
                    requirement_str = f"POWER required: {equippable.power_needed} "
                if equippable.reflex_needed>0:
                    requirement_str += f"REFLEX required: {equippable.reflex_needed} "
                if equippable.focus_needed>0:
                    requirement_str += f"FOCUS required: {equippable.focus_needed} "
                if equippable.reflex_malice >0:
                    requirement_str += f"(REFLEX penalty: {equippable.reflex_malice})"
                log_console.print_box(
                    0, i, log_console.width, 1, f"{requirement_str}", alignment=tcod.CENTER)
        elif hasattr(self.entity,"fighter"):
            fighter=self.entity.fighter
            log_console.print_box(
                0, i, log_console.width, 1, f"HP: {fighter.hp} / {fighter.max_hp}, Attack: {fighter.attack}, "
                                            f"Defense: {fighter.defense}, Speed: {fighter.speed}, Accuracy: {fighter.accuracy}", alignment=tcod.CENTER,
            )
            i += 2
            log_console.print_box(
                0, i, log_console.width, 1, f"Burn Resist {fighter.burn_resist}, Shock Resist: {fighter.shock_resist}, Range: {fighter.max_range}, Focus: {fighter.focus}", alignment=tcod.CENTER,
            )
            i += 2
            allegience=self.entity.get_team
            if allegience=="Hostile":
                fg=color.combat_doll
            elif allegience=="Friendly":
                fg=color.ally
                allegience="a slave to your will."
            else:
                fg=color.white
            log_console.print_box(
                0, i, log_console.width, 1, f"This one is {allegience}", fg=fg, alignment=tcod.CENTER)
            if hasattr(self.entity,"cyberware"):
                i+=2
                log_console.print_box(
                    0, i, log_console.width, 1, f"This entity may be hacked.", alignment=tcod.CENTER)




        log_console.blit(console, 3, 3)


    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[MainGameEventHandler]:
            return MainGameEventHandler(self.engine)

class HelpScreen(BaseEventHandler):
    def __init__(self, parent_handler: BaseEventHandler,):
            self.parent = parent_handler

    def on_render(self, console: tcod.Console) -> None:
            log_console = tcod.Console(console.width, console.height)
            log_console.draw_frame(1, 1, log_console.width-1, log_console.height-1)
            console.print_box(
                0, 0, log_console.width, 1, "||HELP||", alignment=tcod.CENTER
            )
            console.print_box(
                console.width//2, 3, console.width//2-5, 2, "ESCAPE will quit the game. \n The game will autosave.", alignment=tcod.CENTER
            )



            console.print(
                0, 1, "_____Controls_____"
            )
            console.print(
                1, 3, "Movement"
            )

            movestring=f"\\↑/← →/↓\\"

            console.draw_frame(x=1, y=4, width=3, height=3, decoration=movestring)
            console.print(
                5, 5, "use numpad"
            )
            console.draw_frame(x=16, y=4, width=3, height=3, decoration="7894 6123")
            console.print(
                20, 5, "or"
            )
            console.draw_frame(x=23, y=4, width=3, height=3, decoration="qwea dzsc")
            console.print(
                1, 8, "5 and SPACE waits"
            )
            console.print(
                1, 10, "K makes a Ranged Attack"
            )
            console.print(
                1, 12, "G Picks up an Item"
            )

            console.print(1,14, "i Opens the inventory and Uses Items"),
            console.print(
                1, 16, "O Examines an Item, R Drops Items"
            )
            console.print(
            1, 18, "L Looks around, then Press ENTER to examine an enemy"
            )
            console.print(
                1, 20, "M Activates hacking"
            )
            console.print(
                1, 22, "J Opens the Character Sheet"
            )
            console.print(
                1, 24, "V Opens Message History"
            )

            console.print(
            1, 26, "You can only Hack enemies with cybernetic enhancements"
            )

            console.print(
                5, 27, "and with a lower FOCUS than you"
            )
            console.print(
                1, 29, "You can only equip Cyberware at a Medbay [X],")


            console.print(5,30,"activate a Medbay or go down stairs [>] with ENTER"
            )

            console.print(
            0, 32, "_____Attributes_____"
            )

            console.print(
                1, 34, "POWER: Your physical prowess"
            )
            console.print(
                5,35,"Affects HP and Melee Damage"
            )
            console.print(
                1, 37, "REFLEX: Your agility and coordination"
            )
            console.print(
                5, 38, "Affects Accuracy and Dodge"
            )
            console.print(
                1, 40, "FOCUS: Your mental faculties"
            )
            console.print(
                5, 41, "Affects FP and Hacking"
            )


            console.print(
                1, 43, "At 10 POWER, you gain +6 carry capacity"
            )
            console.print(
                1, 45, "At 10 REFLEX, you gain +1 movement speed"
            )
            console.print(
                1, 47, "At 10 FOCUS, you gain +1 Network slot (you can control 1 more NPC)"
            )

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[BaseEventHandler]:
        return self.parent

class AskUserEventHandler(EventHandler):
    def handle_action(self, action: Optional[Action]) -> bool:
        if super().handle_action(action):
            self.engine.event_handler = MainGameEventHandler(self.engine)
            return True
        return False

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        if event.sym in {  # Ignore modifier keys.
            tcod.event.K_LSHIFT,
            tcod.event.K_RSHIFT,
            tcod.event.K_LCTRL,
            tcod.event.K_RCTRL,
            tcod.event.K_LALT,
            tcod.event.K_RALT,
        }:
            return None
        return  self.on_exit()
    def ev_mousebuttondown(self, event: tcod.event.MouseButtonDown) -> Optional[ActionOrHandler]:
        return  self.on_exit()

    def on_exit(self) -> Optional[ActionOrHandler]:
        return MainGameEventHandler(self.engine)


class InventoryEventHandler(AskUserEventHandler):
    Title="Inventory"

    def on_render(self, console: tcod.Console) -> None:
        super().on_render(console)
        number_of_items_in_inventory = len(self.engine.player.inventory.items)
        height= number_of_items_in_inventory +2

        height=20
        x=0
        y=0
        width=24

        console.draw_frame(
            x=x,
            y=y,
            width=width,
            height=height,
            title=self.Title,
            clear=True,
            fg=color.haxor_green,
            bg=(0,0,0)
        )
        if number_of_items_in_inventory >0:
            for i, item in enumerate(self.engine.player.inventory.items):
                item_key = chr(ord("a")+i)
                is_equipped=self.engine.player.equipment.item_is_equipped(item)
                item_string = f"({item_key}) {item.shortname}"
                if item.equippable is not None:
                    if item.equippable.ammo_count is not None:
                        item_string = f"{item_string} ({item.equippable.ammo_count}/{item.equippable.ammo_max})"

                if getattr(item,"consumable") is not None:
                    if hasattr(item.consumable,"rounds"):
                        item_string =f"{item_string} ({item.consumable.rounds})"
                if is_equipped:
                    item_string = f"{item_string} (E)"

                console.print(x+1,y+i+1, f"{item_string}",fg=color.white)
        else:
            console.print(x+1, y+1, "__EMPTY__")

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        player = self.engine.player
        key=event.sym
        index = key - tcod.event.K_A

        if 0<=index<=26:
            try:
                selected_item =  player.inventory.items[index]
            except IndexError:
                self.engine.message_log.add_message("You selected nothing lmao", color.invalid)
                return None

            return  self.on_item_selected(selected_item)
        return super().ev_keydown(event)

    def on_item_selected(self, item: Item) -> Optional[ActionOrHandler]:
        raise NotImplementedError()


class InventoryDropHandler(InventoryEventHandler):
    Title = "Discarding"

    def on_item_selected(self, item: Item) -> Optional[ActionOrHandler]:
        return actions.DropItem(self.engine.player, item)



class InventoryActivateHandler(InventoryEventHandler):
    Title = "Using"
    def on_item_selected(self, item: Item) -> Optional[ActionOrHandler]:
        if item.consumable:

            return item.consumable.get_action(self.engine.player)

        elif item.equippable:
            #print("handling item equip")

            if item.equippable.equipment_type == EquipmentType.WEAPON:

               # print("this is a weapon")
                if not item.equippable.two_handed:
                    #print("this is a one handed weapon")
                    if not self.engine.player.equipment.item_is_equipped(item):
                        #print("this item is not already equipped")
                       # print(item)
                        return WeaponSlotSelectionHandler(self.engine, item)
            #print("perform equip action")
            print("Skipped")
            return  actions.EquipAction(self.engine.player, item)
        else:
            self.engine.message_log.add_message("Cyberware can only be installed at a medbay", color.invalid)
            return None



class WeaponSlotSelectionHandler(AskUserEventHandler):
    Title = "Select Hand To Wield With:"
    def __init__(self, engine: Engine, item: Item):
        super().__init__(engine)
        self.item = item

    def on_render(self, console: tcod.Console) -> None:
        super().on_render(console)

        height = 5
        x = 0
        y = 0
        width = len(self.Title) + 5

        console.draw_frame(
            x=x,
            y=y,
            width=width,
            height=height,
            title=self.Title,
            clear=True,
            fg=color.haxor_green,
            bg=(0, 0, 0)
        )
        option_string = "a) Right Hand"
        if self.engine.player.equipment.right_hand is not None:
            equip_str=self.engine.player.equipment.right_hand.shortname
            option_string=option_string+" ("+equip_str+")"

        for i in range(2):
            if i >0:
                option_string="b) Left Hand"
                if self.engine.player.equipment.left_hand is not None:
                    equip_str = self.engine.player.equipment.left_hand.shortname
                    option_string = option_string + " (" + equip_str+")"

            console.print(x + 1, y + i + 1, f"{option_string}")

        if self.engine.player.cyberware.has_slot_perk:
            option_string = "c) Platform"
            if self.engine.player.equipment.bonus_slot is not None:
                equip_str = self.engine.player.equipment.bonus_slot.shortname

                option_string = option_string + " (" + equip_str + ")"
            console.print(x + 1, 3, f"{option_string}")

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        player = self.engine.player
        key=event.sym
        index = key - tcod.event.K_A
        if 0<=index<=2:
            try:
                selected_item =  index
            except IndexError:
                self.engine.message_log.add_message("You selected nothing lmao", color.invalid)
                return None

            return  self.on_item_selected(selected_item)
        return super().ev_keydown(event)


    def on_item_selected(self, hand) -> Optional[ActionOrHandler]:
        return actions.EquipAction(self.engine.player, self.item, hand )

class BodyModSelectionHandler(AskUserEventHandler):
    Title="Choose Cyberware to Install"
    def __init__(self, engine: Engine):
        super().__init__(engine)
        player = engine.player
        self.ware_list =[]
        self.at_station = False
        for i, item in enumerate(self.engine.player.inventory.items):

            if item.bodymod is not None:
                self.ware_list.append(item)

        if (player.x,player.y)==engine.game_map.med_location:
            self.at_station= True
            if not self.engine.game_map.med_used:
                self.engine.player.fighter.full_heal()
                self.engine.message_log.add_message("The Med-Bay opens its doors and reveals a needle-tipped robotic arm. It quickly injects you with first-aid nanobots, bringing you to full health!", color.health_recovered)
                self.engine.game_map.med_used=True
                self.engine.game_map.tiles[player.x,player.y]=usedMedbay
            else:
                self.engine.message_log.add_message("The Med-Bay can no longer heal you.")

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        key=event.sym
        index = key - tcod.event.K_A
        if 0<=index<=26:
            try:
                selected_item =  self.ware_list[index]
            except IndexError:
                self.engine.message_log.add_message("Invalid Selection", color.invalid)
                return None
            return  self.on_item_selected(selected_item)
        return super().ev_keydown(event)

    def on_item_selected(self, item: Item) -> Optional[ActionOrHandler]:
            return actions.ModAction(self.engine.player, item)

    def on_render(self, console: tcod.Console) -> None:
        super().on_render(console)
        height = 5
        x = 0
        y = 0
        width = len(self.Title) + 7
        console.draw_frame(
            x=x,
            y=y,
            width=width,
            height=len(self.ware_list) + 3,
            title=self.Title,
            clear=True,
            fg=color.haxor_green,
            bg=(0, 0, 0)
        )
        if len(self.ware_list)==0:

            console.print(x + 1, y + 1, f"You have no cyberware to install")

        else:


            for i, item in enumerate(self.ware_list):
                item_key = chr(ord("a") + i)
                item_string = f"({item_key}) {item.shortname}"
                console.print(x + 1, y + i + 1, f"{item_string}")

class InventoryExamineHandler(InventoryEventHandler):
    Title = "Examining"
    def on_item_selected(self, item: Item) -> Optional[ActionOrHandler]:
        return EntityDescriptionHandler(self.engine,item)


class SelectIndexHandler(AskUserEventHandler):
    def __init__(self, engine: Engine):
        super().__init__(engine)
        player = self.engine.player
        viewport = self.engine.game_map.get_viewport()
        engine.mouse_location = player.x - viewport[0]+viewport[4], player.y-viewport[1]+1

    def on_render(self, console: tcod.Console) -> None:
        super().on_render(console)
        x,y = self.engine.mouse_location
        console.tiles_rgb["bg"][x,y] = color.white
        console.tiles_rgb["fg"][x,y] = color.black

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        viewport = self.engine.game_map.get_viewport()
        key = event.sym
        if key in MOVE_KEYS:
            modifier = 1
            if event.mod & (tcod.event.Modifier.LSHIFT |tcod.event.Modifier.RSHIFT ):
                modifier *= 5
            if event.mod & (tcod.event.Modifier.LCTRL| tcod.event.Modifier.RCTRL):
                modifier *= 10
            if event.mod & (tcod.event.Modifier.LALT | tcod.event.Modifier.RALT):
                modifier *= 20

            x, y = self.engine.mouse_location
            dx, dy = MOVE_KEYS[key]
            x += dx * modifier
            y += dy * modifier
            # Clamp the cursor index to the map size.
            x = max(viewport[4], min(x, viewport[2]-viewport[0]+viewport[4]))
            y = max(1, min(y, viewport[3]-viewport[1]+1))
            self.engine.mouse_location = x, y
            return None
        elif key in CONFIRM_KEYS:
            x, y = self.engine.mouse_location
            index_x = x + viewport[0] - viewport[4]
            index_y = y + viewport[1] -1
            selectedTile=(index_x,index_y)
            return self.on_index_selected(*selectedTile)
        return super().ev_keydown(event)

    def ev_mousebuttondown(self, event: tcod.event.MouseButtonDown) -> Optional[ActionOrHandler]:

        if self.engine.game_map.in_bounds(*self.engine.mouse_location):
            if event.button == 1:
                return self.on_index_selected(*self.engine.mouse_gameTile)

        return super().ev_mousebuttondown(event)



    def on_index_selected(self, x: int, y:int) -> Optional[ActionOrHandler]:
        raise NotImplementedError()

class  LookHandler(SelectIndexHandler):
    def on_index_selected(self, x: int, y:int) -> EntityDescriptionHandler | MainGameEventHandler:
        actor=self.engine.game_map.get_actor_at_location(x, y)
        if actor is not None and actor is not self.engine.player:
            return EntityDescriptionHandler(self.engine,actor)
        else:
            for station in self.engine.game_map.stations():
                if (station.x,station.y)==(x,y):
                    return EntityDescriptionHandler(self.engine, station)
        return MainGameEventHandler(self.engine)

class NormalAttackHandler(SelectIndexHandler):
    def __init__(self, engine: Engine):
        super().__init__(engine)
        self.player_coords = self.engine.mouse_location

    def on_render(self, console: tcod.Console):
        super().on_render(console)
        player=self.engine.player
        radius=player.fighter.max_range
        x0=self.player_coords[0]- radius-1
        y0=self.player_coords[1]- radius-1
        viewport = self.engine.game_map.get_viewport()

        width = 1 + (1 + radius) * 2
        height = 1 + (1 + radius) * 2


        console.draw_frame(
            x=x0,
            y=y0,
            width=width,
            height=height,
            fg=color.red,
            clear=False,
        )
        for x in range(player.x-radius, player.x+radius+1 ):
            for y in range(player.y-radius,player.y+radius+1):
                if int(player.distance(x,y))>max(radius,1):
                    console.print(x- viewport[0]+viewport[4], y-viewport[1]+1,"#",fg=color.red)

    def on_index_selected(self, x: int, y:int) -> Optional[ActionOrHandler]:

        return RangedAttackAction(self.engine.player,x,y)

class SingleRangedAttackHandler(SelectIndexHandler):
    def __init__(self, engine: Engine, callback: Callable[[Tuple[int,int]], Optional[Action]], radius: Optional[int]):
        super().__init__(engine)
        self.callback = callback
        self.player_coords = self.engine.mouse_location
        if radius is not None:
            self.radius=radius

    def on_index_selected(self, x: int, y: int) -> Optional[Action]:
        return self.callback((x,y))
    def on_render(self, console: tcod.Console):
        super().on_render(console)

        if hasattr(self,"radius"):
            player = self.engine.player
            x0 = self.player_coords[0] - self.radius - 1
            y0 = self.player_coords[1] - self.radius - 1
            viewport = self.engine.game_map.get_viewport()

            width = 1 + (1 + self.radius) * 2
            height = 1 + (1 + self.radius) * 2

            console.draw_frame(
                x=x0,
                y=y0,
                width=width,
                height=height,
                fg=color.red,
                clear=False,
            )
            for x in range(player.x - self.radius, player.x + self.radius + 1):
                for y in range(player.y - self.radius, player.y + self.radius + 1):
                    if int(player.distance(x, y)) > self.radius:
                        console.print(x - viewport[0] + viewport[4], y - viewport[1] + 1, "#", fg=color.red)


class RangedAOEAttackHandler(SelectIndexHandler):
    def __init__(self, engine: Engine, radius: int,
                 callback: Callable[[Tuple[int, int]], Optional[Action]],):
        super().__init__(engine)

        self.radius = radius
        self.callback = callback

    def on_render(self, console: tcod.Console):
        super().on_render(console)
        viewport = self.engine.game_map.get_viewport()
        x, y = self.engine.mouse_location
        console.draw_frame(
            x=x - self.radius - 1,
            y=y - self.radius - 1,
            width= 1+(1+ self.radius)*2,
            height=1+(1+ self.radius)*2,
            fg=color.red,
            clear=False,
        )
        x_tile=x+ viewport[0]-viewport[4]
        y_tile=y+viewport[1] - 1
        for i in range(x_tile-self.radius, x_tile+self.radius+1 ):
            for j in range(y_tile-self.radius,y_tile+self.radius+1):
                distance=int(math.sqrt((x_tile-i)**2+(y_tile-j)**2))
                if  distance>self.radius:
                    console.print(i- viewport[0]+viewport[4], j-viewport[1]+1,"#",fg=color.red)

    def on_index_selected(self, x: int, y:int) -> Optional[Action]:
        return self.callback((x,y))

class HackingSelectHandler(SelectIndexHandler):
    def __init__(self, engine: Engine):
        super().__init__(engine)
        self.hack_success=False
        self.engine.message_log.add_message("SELECT TARGET", color.hypno_drone)

    def on_index_selected(self, x: int, y: int) -> Optional[ActionOrHandler]:

        self.hack_success = actions.HackAction(self.engine.player, [x,y]).perform()

        if self.hack_success:

            return HackingMenuHandler(self.engine,x,y)

class HackingMenuHandler(AskUserEventHandler):
    TITLE= "Select Virus to Upload"
    def __init__(self, engine: Engine, target_x: int, target_y: int):
        super().__init__(engine)

        self.target = self.engine.game_map.get_actor_at_location(target_x, target_y)
        self.virus_list=self.engine.player.hacker.get_virus_list()
        self.fp_available=self.engine.player.fighter.fp
    def on_render(self, console: tcod.Console) -> None:
        super().on_render(console)

        width = len(self.TITLE) + 8

        console.draw_frame(
            x=0,
            y=0,
            width=width,
            height=20,
            title=self.TITLE,
            clear=True,
            fg=color.haxor_green,
            bg=(0, 0, 0)
        )
        x=1
        y=1
        i=0

        for virus in self.virus_list:

            command_key = chr(ord("a") + i)
            Command=virus.name
            cost =  virus.cost
            command_string = f"{command_key}) {Command} ({cost} fp)"
            if cost > self.fp_available:
                text_color=color.grey
            else:
                text_color=color.haxor_green
            console.print(x + 1, y + i*2 + 1, f"{command_string}",text_color)
            i+=1


    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        key=event.sym
        index = key - tcod.event.K_A

        if 0<=index<len(self.virus_list):


            try:

                assert self.virus_list[index].cost <= self.fp_available
                self.virus_list[index].perform(self.engine.player, self.target)

            except IndexError:
                self.engine.message_log.add_message("Virus Not Selected", color.invalid)
                return None
            except AssertionError:
                self.engine.message_log.add_message("Not Enough FP", color.invalid)
                return None

        return super().ev_keydown(event)

class LevelUpHandler(AskUserEventHandler):
    TITLE = "LEVEL UP"

    def on_render(self, console: tcod.Console) -> None:
        super().on_render(console)


        x = 45

        y = 0

        width = len(self.TITLE) + 4

        console.draw_frame(
            x=x,
            y=y,
            width=34,
            height=11,
            title=self.TITLE,
            clear=True,
            fg=color.haxor_green,
            bg=(0, 0, 0),
        )
        console.print(x=x + 1, y=1, string="Your Skill has increased",fg=color.hypno_sentry,bg=color.black)
        console.print(x=x + 1, y=2, string="Select an attribute to improve.",fg=color.hypno_sentry,bg=color.black)

        console.print(
            x=x + 1,
            y=4,
            string=f"a) Power (+1, from {self.engine.player.fighter.base_power})",fg=color.white,bg=color.black
        )
        console.print(
            x=x + 1,
            y=5,
            string=f"b) Reflex (+1, from {self.engine.player.fighter.base_reflex})",fg=color.white,bg=color.black
        )
        console.print(
            x=x + 1,
            y=6,
            string=f"c) Focus (+1, from {self.engine.player.fighter.base_focus})",fg=color.white,bg=color.black
        )

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        player = self.engine.player
        key= event.sym
        index=key-tcod.event.KeySym.A

        if 0<= index <=2:
            if index ==0:
                player.level.increase_power()
            elif index ==1:
                player.level.increase_reflex()
            else:
                player.level.increase_focus()

        else:
            self.engine.message_log.add_message("You Must choose, miss.", color.invalid)

            return None
        return super().ev_keydown(event)

    def ev_mousebuttondown(self, event: tcod.event.MouseButtonDown) -> Optional[ActionOrHandler]:
        return None

class EscapeHandler(AskUserEventHandler):
    TITLE="Are you sure you want to quit?"
    def on_render(self, console: tcod.Console) -> None:
        super().on_render(console)

        width = len(self.TITLE) + 2

        x=(console.width-width)//2

        y = 3


        console.draw_frame(
            x=x,
            y=y,
            width=width,
            height=5,
            title=self.TITLE,
            clear=True,
            fg=color.haxor_green,
            bg=(0, 0, 0),
        )
        console.print_box( x=x+1,y=4, width=width-2,height=1,string="[Y] or [ESC] Save and Quit", fg=color.hypno_drone,bg=color.black,alignment=tcod.CENTER)
        console.print_box( x=x+1,y=6, width=width-2,height=1,string="[Q] Quit without Saving",fg=color.hypno_drone,bg=color.black, alignment=tcod.CENTER,)


    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        key= event.sym

        if key in (tcod.event.KeySym.Y, tcod.event.KeySym.ESCAPE):
            raise SystemExit()
        if key == tcod.event.KeySym.Q:
            raise exceptions.QuitWithoutSaving()
        if key == tcod.event.KeySym.N:
            return self.on_exit()
        return super().ev_keydown(event)

class CharacterScreenEventHandler(AskUserEventHandler):
    TITLE = "USER '"

    def on_render(self, console: tcod.Console) -> None:
        super().on_render(console)

        y = 0
        TITLE="USER '"+self.engine.player.name+"'"
        width = len(self.TITLE) + 4
        x=50
        y=0
        console.draw_frame(
            x=x,
            y=y,
            width=29,
            height=49,
            title="USER '"+self.engine.player.name+"'",
            clear=True,
            fg=color.haxor_green,
            bg=(0, 0, 0),
        )

        console.print(
            x=x + 1, y=y + 1, string=f"LEVEL: {self.engine.player.level.current_level}"
        )
        console.print(
            x=x + 1, y=y + 2, string=f"XP: {self.engine.player.level.current_xp}"
        )
        console.print(
            x=x + 1,
            y=y + 3,
            string=f"XP for next Level: {self.engine.player.level.experience_to_next_level}",
        )

        console.print(
            x=x + 1, y=y + 5, string=f"__Attributes__",fg=color.hypno_drone
        )
        console.print(
            x=x + 1, y=y + 6, string=f"Power: {self.engine.player.fighter.power} (Base: {self.engine.player.fighter.base_power})"
        )
        console.print(
            x=x + 1, y=y + 7, string=f"Reflex: {self.engine.player.fighter.reflex} (Base: {self.engine.player.fighter.base_reflex})"
        )
        console.print(
            x=x + 1, y=y + 8, string=f"Focus: {self.engine.player.fighter.focus} (Base: {self.engine.player.fighter.base_focus})"
        )

        console.print(
            x=x + 1, y=y + 9, string=f"HP: {self.engine.player.fighter.hp}/{self.engine.player.fighter.max_hp}"
        )

        console.print(
            x=x + 1, y=y + 10, string=f"FP: {self.engine.player.fighter.fp}/{self.engine.player.fighter.max_fp}"
        )

        console.print(
            x=x + 1, y=y + 11, string=f"DODGE: {self.engine.player.fighter.dodge_bonus}"
        )
        console.print(
            x=x + 1, y=y + 12, string=f"DEFENSE: {self.engine.player.fighter.defense}"
        )

        console.print(
            x=x + 1, y=y + 13, string=f"SHOCK RESIST: {self.engine.player.fighter.shock_resist}"
        )
        console.print(
            x=x + 1, y=y + 14, string=f"BURN RESIST: {self.engine.player.fighter.burn_resist}"

        )

        console.print(
            x=x + 1, y=y + 15, string=f"Accuracy: {self.engine.player.fighter.accuracy}"
        )
        console.print(
            x=x + 1, y=y + 16, string=f"Speed: {self.engine.player.fighter.speed}"
        )


        console.print(
            x=x + 1, y=y + 21, string=f"__EQUIPMENT__",fg=color.hypno_drone)

        try:
            console.print(
                x=x + 1, y=y + 22, string=f"ARMOR: {self.engine.player.equipment.armor.shortname}"
            )

        except:
            console.print(
                x=x + 1, y=y + 22, string=f"ARMOR: NONE"
            )

        try:
            console.print(
            x=x + 1, y=y + 23, string=f"RIGHT HAND: {self.engine.player.equipment.right_hand.shortname}"
            )

        except:
            console.print(
                x=x + 1, y=y + 23, string=f"RIGHT HAND: NONE"
            )

        try: console.print(
            x=x + 1, y=y + 24,
            string=f"Attack: {self.engine.player.fighter.attack_from_slot("right_hand")},"
                   f" Ammo: {self.engine.player.equipment.right_hand.equippable.ammo_count}/{self.engine.player.equipment.right_hand.equippable.ammo_max}")

        except: console.print(
            x=x + 1, y=y + 24,
            string=f"Attack: {self.engine.player.fighter.attack},"
                   f" Ammo: NONE")



        try:
            console.print(
                x=x + 1, y=y + 25, string=f"LEFT HAND: {self.engine.player.equipment.left_hand.shortname}"
            )

            console.print(
            x=x + 1, y=y + 26,
            string=f"Attack: {self.engine.player.fighter.attack_from_slot("left_hand")},"
                   f" Ammo: {self.engine.player.equipment.left_hand.equippable.ammo_count}/{self.engine.player.equipment.left_hand.equippable.ammo_max}"

            )
        except:
            pass

        try:
            console.print(
                x=x + 1, y=y + 27, string=f"PLATFORM: {self.engine.player.equipment.bonus_slot.shortname}"
            )

            console.print(
                x=x + 1, y=y + 28,
                string=f"Attack: {self.engine.player.fighter.attack_from_slot("bonus_slot")},"
                       f" Ammo: {self.engine.player.equipment.bonus_slot.equippable.ammo_count}/{self.engine.player.equipment.bonus_slot.equippable.ammo_max}"
            )
        except:
            pass

        console.print(

            x=x + 1, y=y + 30, string=f"___CYBERWAREZ___",fg=color.hypno_drone
        )
        try:
            console.print(
                x=x + 1, y=y + 31, string=f"HEAD: {self.engine.player.cyberware.head.shortname}"
            )
        except:
            console.print(
                x=x + 1, y=y + 31, string=f"HEAD: NONE"
            )
        try:
            console.print(
                x=x + 1, y=y + 32, string=f"BODY: {self.engine.player.cyberware.torso.shortname}"
            )
        except:
            console.print(
                x=x + 1, y=y + 32, string=f"BODY: NONE"
            )
        try:
            console.print(
                x=x + 1, y=y + 33, string=f"ARMS: {self.engine.player.cyberware.arms.shortname}"
            )
        except:
            console.print(
                x=x + 1, y=y + 33, string=f"ARMS: NONE"
            )

        try:
            console.print(
                x=x + 1, y=y + 34, string=f"LEGS: {self.engine.player.cyberware.legs.shortname}"
            )
        except:
            console.print(
                x=x + 1, y=y + 34, string=f"LEGS: NONE"
            )

        console.print(
            x=x + 1, y=y + 36, string=f"___STATUS___: ",fg=color.hypno_drone,
        )

        i=0
        d=0
        for effect in self.engine.player.status.effects:

            if i<4:
                offset = i * 5
                console.print(
                x=x + 1+offset, y=y + 37, string=f"{effect.abrev} "

                )
                i+=1
            else:
                offset =  d*5

                console.print(
                    x=x + 1 + offset, y=y + 38, string=f"{effect.abrev} "

                )
                d+=1

        console.print(
            x=x + 1, y=y + 40, string=f"___NETWORK___ ",fg=color.hypno_drone
        )
        console.print(
            x=x + 1, y=y + 41, string=f"Puppet Slots: {self.engine.player.controller.num_minions()}/{self.engine.player.controller.minion_limit}"
        )
        i=0
        for minion in self.engine.player.controller.minion_list:
            console.print(
                x=x + 1, y=y + 42+i,
                string=f"{minion.name}: {minion.fighter.hp}/{minion.fighter.max_hp}"
            )
            i+=1




