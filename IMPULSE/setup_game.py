from __future__ import annotations

import copy
import lzma
import pickle
import traceback
from typing import Optional

import tcod

from IMPULSE import color


from IMPULSE.engine import Engine
from IMPULSE.game_map import GameWorld
from IMPULSE import entity_factories
from IMPULSE import input_handler
from IMPULSE.input_handler import BaseEventHandler, HelpScreen

background_image = tcod.image.load("GRAPHICS/menu_background.png")[:, :, :3]

def new_game(playername: str="player") -> Engine:
    map_width = 80
    map_height=43
    room_max_size = 10
    room_min_size=6
    max_rooms=30
    name=playername
    print(name)
    player = copy.deepcopy(entity_factories.player)
    player.name=name
    print(player.name)
    if name == "sweethound":
        player.fighter.base_power=10
        player.fighter.base_reflex=10
        player.fighter.base_focus=10
        player.fighter.full_heal()

    engine = Engine(player=player)
    print(engine.player.name)
    engine.game_world = GameWorld(
        engine=engine,
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        viewport_width=30,
        viewport_height=30,

    )
    engine.game_world.generate_floor(0)
    engine.update_fov()

    engine.message_log.add_message(
        "WELCOME TO YOUR DOOM", color.welcome_text
    )

    pistol = copy.deepcopy(entity_factories.pistol)
    pistol.parent = player.inventory

    labrys = copy.deepcopy(entity_factories.labrys)
    labrys.parent = player.inventory

    leather_jacket=copy.deepcopy(entity_factories.leather_jacket)
    leather_jacket.parent=player.inventory

    pistol_ammo = copy.deepcopy(entity_factories.pistol_ammo)
    pistol_ammo.parent = player.inventory

    player.inventory.items.append(pistol_ammo)
    player.inventory.items.append(labrys)

    player.inventory.items.append(pistol)
    player.equipment.toggle_equip(pistol,add_message=True)

    player.inventory.items.append(leather_jacket)
    player.equipment.toggle_equip(leather_jacket,add_message=False)

    slot=copy.deepcopy(entity_factories.weapon_slot)
    slot.parent = player.inventory
    player.inventory.items.append(slot)

    LOS=copy.deepcopy(entity_factories.los_upgrade)
    LOS.parent = player.inventory
    player.inventory.items.append(LOS)
    return engine

def load_game(filename:str) -> Engine:
    with open(filename, "rb")as f:
        engine = pickle.loads(lzma.decompress(f.read()))
    assert isinstance(engine, Engine)
    return engine



class MainMenu(BaseEventHandler):
    def on_render(self, console: tcod.Console) -> None:
        console.draw_semigraphics(background_image,0,0)

        console.print(
            console.width // 2,
            console.height // 2 - 4,
            "PROJECT IMPULSE",
            fg=color.menu_title,
            alignment = tcod.CENTER,
        )

        menu_width = 24
        for i, text in enumerate(
            ["[N] New Game", "[C] Continue", "[H] Help","[Q] Quit"]
        ):
            console.print(
                console.width // 2,
                console.height // 2 - 2 + i,
                text.ljust(menu_width),
                fg=color.menu_text,
                bg=color.black,
                alignment=tcod.CENTER,
                bg_blend=tcod.BKGND_ALPHA(64),
            )

    def ev_keydown(self, event: tcod.event.KeyDown, ) -> Optional[input_handler.BaseEventHandler]:
        if event.sym in (tcod.event.KeySym.Q, tcod.event.KeySym.ESCAPE):
            raise SystemExit()
        elif event.sym == tcod.event.KeySym.C:
            try:
                return input_handler.MainGameEventHandler(load_game("savegame.sav"))
            except FileNotFoundError:
                return input_handler.PopupMessage(self, "No saved game to load.")
            except Exception as exc:
                traceback.print_exc()  # Print to stderr.
                return input_handler.PopupMessage(self, f"Failed to load save:\n{exc}")
        elif event.sym == tcod.event.KeySym.N:
            return  name_entry()
        elif event.sym == tcod.event.KeySym.H:
            return HelpScreen(MainMenu())
        return None

class End_Screen(input_handler.BaseEventHandler):
    def on_render(self, console: tcod.Console) -> None:

        console.print(
            console.width // 2,
            console.height // 2 - 4,
            "YOU DID IT",
            fg=color.menu_title,
            alignment = tcod.CENTER,
        )

        console.print(
            console.width // 2,
            console.height // 2 - 8,
            "You've finally reached the Auto-Surgeon and got a vaginoplasty",
            fg=color.menu_title,
            alignment=tcod.CENTER,
        )

        menu_width = 24
        for i, text in enumerate(
            ["[N] New Game",  "[Q] Quit"]
        ):
            console.print(
                console.width // 2,
                console.height // 2 - 2 + i,
                text.ljust(menu_width),
                fg=color.menu_text,
                bg=color.black,
                alignment=tcod.CENTER,
                bg_blend=tcod.BKGND_ALPHA(64),

            )
    def ev_keydown(self, event: tcod.event.KeyDown, ) -> Optional[input_handler.BaseEventHandler]:
        if event.sym in (tcod.event.KeySym.Q, tcod.event.KeySym.ESCAPE):
            raise SystemExit()
        elif event.sym == tcod.event.KeySym.N:
            return name_entry()

        return None

class name_entry(input_handler.BaseEventHandler):
    def __init__(self):
        super().__init__()
        self.name: str=""

    def on_render(self, console: tcod.Console) -> None:

        console.print(
            console.width // 2,
            console.height // 2 - 8,
            "Enter Your Name, Miss",
            fg=color.menu_title,
            alignment=tcod.CENTER,
        )


        console.draw_frame(
            console.width // 2 -7,
            console.height // 2 - 4,
            width=13,
            height=3,
            clear=False,
            fg=(255, 255, 255),
            bg=(0, 0, 0)
        )
        console.print(
            console.width // 2-6,
            console.height // 2-3,
            self.name,
            fg=color.menu_title,
        )
    def ev_keydown(self, event: tcod.event.KeyDown, ) -> Optional[input_handler.BaseEventHandler]:
        key = event.sym
        if key is (tcod.event.KeySym.ESCAPE):
            raise SystemExit()
        elif key in input_handler.CONFIRM_KEYS:
            if self.name is not "" and self.name is not " " and self.name is not "  " and self.name is not "   ":
                return input_handler.MainGameEventHandler(new_game(self.name))
        elif key is tcod.event.KeySym.BACKSPACE:
            self.name=self.name[:len(self.name)-1]
        elif key is tcod.event.KeySym.SPACE:
            self.name = self.name + " "
        elif key in input_handler.TEXT_KEYS:
            if len(self.name)<11:
                mod=0
                if event.mod & (tcod.event.Modifier.LSHIFT | tcod.event.Modifier.RSHIFT):
                    mod=32
                char=input_handler.TEXT_KEYS[key]

                char=chr(ord(char) - mod)

                self.name=self.name+char


        return None