from __future__ import annotations

import copy
import lzma
import pickle
import traceback
from typing import Optional
import os
import tcod

import color
from IMPULSE.components.bodymod import hack_upgrade
from IMPULSE.components.equippable import cool_knife, leather_jacket

from engine import Engine
from game_map import GameWorld
import entity_factories

import input_handler

background_image = tcod.image.load("GRAPHICS/menu_background.png")[:, :, :3]

def new_game() -> Engine:
    map_width = 80
    map_height=43
    room_max_size = 10
    room_min_size=6
    max_rooms=30


    player = copy.deepcopy(entity_factories.player)

    engine = Engine(player=player)

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
    engine.game_world.generate_floor()
    engine.update_fov()

    engine.message_log.add_message(
        "WELCOME TO YOUR DOOM", color.welcome_text
    )

    pistol = copy.deepcopy(entity_factories.pistol)
    pistol.parent = player.inventory

    leather_jacket=copy.deepcopy(entity_factories.leather_jacket)
    leather_jacket.parent=player.inventory

    pistol_ammo = copy.deepcopy(entity_factories.pistol_ammo)
    pistol_ammo.parent = player.inventory
    player.inventory.items.append(pistol_ammo)

    player.inventory.items.append(pistol)
    player.equipment.toggle_equip(pistol,add_message=True)

    player.inventory.items.append(leather_jacket)
    player.equipment.toggle_equip(leather_jacket,add_message=False)

    hack_upgrade=copy.deepcopy(entity_factories.hack_upgrade)
    hack_upgrade.parent = player.inventory
    player.inventory.items.append(hack_upgrade)

    return engine

def load_game(filename:str) -> Engine:
    with open(filename, "rb")as f:
        engine = pickle.loads(lzma.decompress(f.read()))
    assert isinstance(engine, Engine)
    return engine
class MainMenu(input_handler.BaseEventHandler):

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
            ["[N] New Game", "[C] Continue", "[Q] Quit"]
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
            return input_handler.MainGameEventHandler(new_game())
        return None