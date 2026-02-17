from __future__ import  annotations

import os

import tcod
from typing import Optional, Tuple, Callable, TYPE_CHECKING, Union


from IMPULSE import actions
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
from IMPULSE.exceptions import Impossible

if TYPE_CHECKING:
    from IMPULSE.engine import Engine
    from IMPULSE.entity import Item, Entity
    from entity import Actor
    from entity import Station



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

}

help_image = tcod.image.load("GRAPHICS/Help.png")[:, :, :3]

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
        self.engine.handle_enemy_turns()

        return self


    def handle_events(self, event: tcod.event.Event) -> BaseEventHandler:
        action_or_state=self.dispatch(event)
        if isinstance(action_or_state,BaseEventHandler):
            return action_or_state
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
            raise SystemExit()

        elif key == tcod.event.KeySym.V:
            return HistoryViewer(self.engine)

        elif key == tcod.event.KeySym.G:
            action = PickupAction(player)

        elif key == tcod.event.KeySym.I:
            return InventoryActivateHandler(self.engine)
        elif key == tcod.event.KeySym.O:
            return InventoryExamineHandler(self.engine)

        elif key == tcod.event.KeySym.D:
            return InventoryDropHandler(self.engine)

        elif key == tcod.event.KeySym.L:
            return LookHandler(self.engine)

        elif key == tcod.event.KeySym.C:
            return CharacterScreenEventHandler(self.engine)

        elif key == tcod.event.KeySym.J:
            if player.fighter.fp>0:
                return HackingSelectHandler(self.engine)
            else:
                raise Impossible("You are out of Focus Points")

        elif key == tcod.event.KeySym.H:
            return HelpScreen(MainGameEventHandler(self.engine))
        elif key in CONFIRM_KEYS:
            if (player.x, player.y) == self.engine.game_map.downstairs_location:
                return TakeStairsAction(player)

            atstation=False
            for station in self.engine.game_map.entities:
                if hasattr(station, "isStation"):
                    if (station.x == player.x and station.y == player.y):
                        atstation= True
                        break

            if atstation:
                return BodyModSelectionHandler(self.engine)

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
            0,0, log_console.width, 1, f"{self.entity.name}", alignment=tcod.CENTER
        )

        log_console.print_box(
        0, 5, log_console.width, 1, f"{self.entity.char}", alignment=tcod.CENTER,fg=self.entity.color
        )
        i=10
        for line in self.entity.description.text_lines:
            log_console.print_box(
                0, i, log_console.width, 1, f"{line}", alignment=tcod.CENTER,
            )
            i+=2
        log_console.blit(console, 3, 3)


    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[MainGameEventHandler]:
            return MainGameEventHandler(self.engine)

class HelpScreen(BaseEventHandler):
    def __init__(self, parent_handler: BaseEventHandler,):
            self.parent = parent_handler

    def on_render(self, console: tcod.Console) -> None:
            self.parent.on_render(console)
            console.draw_semigraphics(help_image, 0, 0)

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
            fg=(255,255,255),
            bg=(0,0,0)
        )
        if number_of_items_in_inventory >0:
            for i, item in enumerate(self.engine.player.inventory.items):
                item_key = chr(ord("a")+i)
                is_equipped=self.engine.player.equipment.item_is_equipped(item)
                item_string = f"({item_key}) {item.name}"
                if item.equippable is not None:
                    if item.equippable.ammo_count is not None:
                        item_string = f"{item_string} ({item.equippable.ammo_count}/{item.equippable.ammo_max})"

                if getattr(item,"consumable") is not None:

                    item_string =f"{item_string} ({item.consumable.rounds})"
                if is_equipped:
                    item_string = f"{item_string} (E)"

                console.print(x+1,y+i+1, f"{item_string}")
        else:
            console.print(x+1, y+1, "NO BITCHES")

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
            if item.equippable.equipment_type.WEAPON:
               # print("this is a weapon")
                if not item.equippable.two_handed:
                    #print("this is a one handed weapon")
                    if not self.engine.player.equipment.item_is_equipped(item):
                        #print("this item is not already equipped")
                       # print(item)
                        return WeaponSlotSelectionHandler(self.engine, item)
            #print("perform equip action")
            return  actions.EquipAction(self.engine.player, item)
        else:
            raise Impossible("Cyberware can only be installed at a medbay")



class WeaponSlotSelectionHandler(AskUserEventHandler):
    Title = "Select Hand To Wield With:"
    def __init__(self, engine: Engine, item: Item):
        super().__init__(engine)
        self.item = item

    def on_render(self, console: tcod.Console) -> None:
        super().on_render(console)

        height = 3
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
            fg=(255, 255, 255),
            bg=(0, 0, 0)
        )
        option_string = "a) Right Hand"
        if self.engine.player.equipment.right_hand is not None:
            equip_str=self.engine.player.equipment.right_hand.name
            option_string=option_string+" ("+equip_str+")"
        for i in range(2):
            if i >0:
                option_string="b) Left Hand"
                if self.engine.player.equipment.left_hand is not None:
                    equip_str = self.engine.player.equipment.left_hand.name
                    option_string = option_string + " (" + equip_str+")"

            console.print(x + 1, y + i + 1, f"({option_string}")

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        player = self.engine.player
        key=event.sym
        index = key - tcod.event.K_A
        if 0<=index<=1:
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
                print("a")

        for station in self.engine.game_map.entities:
            if hasattr(station, "isStation"):
                if (station.x == player.x and station.y == player.y):
                    self.at_station= True
                    break

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
        width = len(self.Title) + 5

        if len(self.ware_list)==0:
            console.print(x + 1, y + 1, f"You have no cyberware to install")

        else:
            for i, item in enumerate(self.ware_list):
                item_key = chr(ord("a") + i)
                item_string = f"({item_key}) {item.name}"
                console.print(x + 1, y + i + 1, f"({item_string}")

class InventoryExamineHandler(InventoryEventHandler):
    Title = "Using"
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
            print(x,y)
            return None
        elif key in CONFIRM_KEYS:
            x, y = self.engine.mouse_location
            index_x = x + viewport[0] - viewport[4]
            index_y = y + viewport[1] -1
            selectedTile=(index_x,index_y)
            return self.on_index_selected(*selectedTile)
        return super().ev_keydown(event)

    def ev_mousebuttondown(self, event: tcod.event.MouseButtonDown) -> Optional[ActionOrHandler]:
        if self.engine.game_map.in_bounds(*event.tile):
            if event.button == 1:
                viewport = self.engine.game_map.get_viewport()
                x = event.tile.x + viewport[0]-viewport[4]
                y = event.tile.y + viewport[1]-1
                return self.on_index_selected(int(x), int(y))

            return super().ev_mousebuttondown(event)

    def on_index_selected(self, x: int, y:int) -> Optional[ActionOrHandler]:
        raise NotImplementedError()

class  LookHandler(SelectIndexHandler):
    def on_index_selected(self, x: int, y:int) -> EntityDescriptionHandler | MainGameEventHandler:
        actor=self.engine.game_map.get_actor_at_location(x, y)
        if actor is not None and actor is not self.engine.player:
            return EntityDescriptionHandler(self.engine,actor)
        return MainGameEventHandler(self.engine)

class NormalAttackHandler(SelectIndexHandler):
    def __init__(self, engine: Engine):
        super().__init__(engine)
        self.player_coords = self.engine.mouse_location

    def on_render(self, console: tcod.Console):
        super().on_render(console)
        player=self.engine.player
        x0=self.player_coords[0]- player.fighter.max_range-1
        y0=self.player_coords[1]- player.fighter.max_range-1
        w=(1+player.fighter.max_range) * 2
        h=(1+player.fighter.max_range) * 2
        y1=y0+h
        x1=w+x0

        console.draw_frame(
            x=x0,
            y=y0,
            width=w+1,
            height=h+1,
            fg=color.red,
            clear=False,
        )

    def on_index_selected(self, x: int, y:int) -> Optional[ActionOrHandler]:

        return RangedAttackAction(self.engine.player,x,y)


class SingleRangedAttackHandler(SelectIndexHandler):
    def __init__(self, engine: Engine, callback: Callable[[Tuple[int,int]], Optional[Action]]):
        super().__init__(engine)
        self.callback = callback

    def on_index_selected(self, x: int, y: int) -> Optional[Action]:
        return self.callback((x,y))

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
            width=self.radius ** 2,
            height=self.radius ** 2,
            fg=color.red,
            clear=False,
        )

    def on_index_selected(self, x: int, y:int) -> Optional[Action]:
        return self.callback((x,y))

class HackingSelectHandler(SelectIndexHandler):
    def __init__(self, engine: Engine):
        super().__init__(engine)
        self.hack_success=False
        self.engine.message_log.add_message("SELECT TARGET", color.needs_target)

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

        width = len(self.TITLE) + 4

        console.draw_frame(
            x=0,
            y=0,
            width=width,
            height=10,
            title=self.TITLE,
            clear=True,
            fg=(255, 255, 255),
            bg=(0, 0, 0)
        )
        x=1
        y=1
        i=0

        for virus in self.virus_list:

            command_key = chr(ord("a") + i)
            Command=virus.name
            cost =  virus.cost
            command_string = f"({command_key} +{Command}, ({cost} fp) "
            if cost > self.fp_available:
                text_color=color.grey
            else:
                text_color=color.white
            console.print(x + 1, y + i + 1, f"({command_string}",text_color)
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


        x = 50

        y = 0

        width = len(self.TITLE) + 4

        console.draw_frame(
            x=x,
            y=y,
            width=15,
            height=7,
            title=self.TITLE,
            clear=True,
            fg=(255, 255, 255),
            bg=(0, 0, 0),
        )
        console.print(x=x + 1, y=1, string="Your Skill has increased")
        console.print(x=x + 1, y=2, string="Select an attribute to improve.")

        console.print(
            x=x + 1,
            y=4,
            string=f"a) Power (+1, from {self.engine.player.fighter.base_power})",
        )
        console.print(
            x=x + 1,
            y=5,
            string=f"b) Reflex (+1, from {self.engine.player.fighter.base_reflex})",
        )
        console.print(
            x=x + 1,
            y=6,
            string=f"c) Focus (+1, defense, from {self.engine.player.fighter.base_focus})",
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
            self.engine.message_log.add_message("come on girl just choose", color.invalid)

            return None
        return super().ev_keydown(event)

    def ev_mousebuttondown(self, event: tcod.event.MouseButtonDown) -> Optional[ActionOrHandler]:
        return None

class CharacterScreenEventHandler(AskUserEventHandler):
    TITLE = "USER '"

    def on_render(self, console: tcod.Console) -> None:
        super().on_render(console)

        y = 0
        TITLE="USER '"+self.engine.player.name+"'"
        width = len(self.TITLE) + 4
        x=56
        y=0
        console.draw_frame(
            x=55,
            y=y,
            width=24,
            height=49,
            title="USER '"+self.engine.player.name+"'",
            clear=True,
            fg=(255, 255, 255),
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
            x=x + 1, y=y + 5, string=f"__Attributes__"
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
            x=x + 1, y=y + 11, string=f"DODGE CHANCE: {self.engine.player.fighter.dodge_bonus}"
        )
        console.print(
            x=x + 1, y=y + 12, string=f"DEFENSE: {self.engine.player.fighter.defense}"
        )

        console.print(
            x=x + 1, y=y + 13, string=f"SHOCK RESIST: {self.engine.player.fighter.shock_resist}"
        )
        console.print(
            x=x + 1, y=y + 14, string=f"BURN RESIST {self.engine.player.fighter.burn_resist}"

        )

        console.print(
            x=x + 1, y=y + 15, string=f"Accuracy: {self.engine.player.fighter.accuracy}"
        )
        console.print(
            x=x + 1, y=y + 16, string=f"Speed: {self.engine.player.fighter.speed}"
        )


        console.print(
            x=x + 1, y=y + 21, string=f"__EQUIPMENT__")

        console.print(
            x=x + 1, y=y + 22, string=f"ARMOR: {self.engine.player.equipment.armor.name}"
        )
        console.print(
            x=x + 1, y=y + 23, string=f"RIGHT HAND: {self.engine.player.equipment.right_hand.name}"
        )

        console.print(
            x=x + 1, y=y + 24,
            string=f"Attack: {self.engine.player.fighter.attack_from_slot("right_hand")},"
                   f" Ammo: {self.engine.player.equipment.right_hand.equippable.ammo_count}/{self.engine.player.equipment.right_hand.equippable.ammo_max}"

        )

        try:
            console.print(
                x=x + 1, y=y + 25, string=f"LEFT HAND: {self.engine.player.equipment.left_hand.name}"
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
                x=x + 1, y=y + 27, string=f"PLATFORM: {self.engine.player.equipment.bonus_slot.name}"
            )

            console.print(
                x=x + 1, y=y + 28,
                string=f"Attack: {self.engine.player.fighter.attack_from_slot("bonus_slot")},"
                       f" Ammo: {self.engine.player.equipment.bonus_slot.equippable.ammo_count}/{self.engine.player.equipment.bonus_slot.equippable.ammo_max}"
            )
        except:
            pass

        console.print(

            x=x + 1, y=y + 30, string=f"___CYBERWAREZ___: "
        )
        try:
            console.print(
                x=x + 1, y=y + 31, string=f"HEAD: {self.engine.player.cyberware.head.name}"
            )
        except:
            console.print(
                x=x + 1, y=y + 31, string=f"HEAD: NONE"
            )
        try:
            console.print(
                x=x + 1, y=y + 32, string=f"BODY: {self.engine.player.cyberware.torso.name}"
            )
        except:
            console.print(
                x=x + 1, y=y + 32, string=f"BODY: NONE"
            )
        try:
            console.print(
                x=x + 1, y=y + 33, string=f"ARMS: {self.engine.player.cyberware.arms.name}"
            )
        except:
            console.print(
                x=x + 1, y=y + 33, string=f"ARMS: NONE"
            )

        try:
            console.print(
                x=x + 1, y=y + 34, string=f"LEGS: {self.engine.player.cyberware.legs.name}"
            )
        except:
            console.print(
                x=x + 1, y=y + 34, string=f"LEGS: NONE"
            )

        console.print(
            x=x + 1, y=y + 36, string=f"___STATUS___: "
        )

        i=0
        d=0
        for effect in self.engine.player.status.effects:

            if i<4:
                offset = i * 4
                console.print(
                x=x + 1+offset, y=y + 37, string=f"{effect.abrev} "

                )
                i+=1
            else:
                offset =  d*4
                console.print(
                    x=x + 1 + offset, y=y + 38, string=f"{effect.abrev} "

                )
                d+=1

        console.print(
            x=x + 1, y=y + 40, string=f"__NETWORK__ "
        )
        console.print(
            x=x + 1, y=y + 41, string=f"Network Slots: {self.engine.player.controller.num_minions()}/{self.engine.player.controller.minion_limit}"
        )
        i=0
        for minion in self.engine.player.controller.minion_list:
            console.print(
                x=x + 1, y=y + 42+i,
                string=f"{minion.name}: {minion.fighter.hp}/{minion.fighter.max_hp}"
            )
            i+=1




