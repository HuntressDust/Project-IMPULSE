#!/usr/bin/env python3
from os import system

import tcod
import color
import os
import traceback

import exceptions
import input_handler

import setup_game


def save_game(handler: input_handler.BaseEventHandler, filename: str)->None:
    if isinstance(handler, input_handler.BaseEventHandler):
        handler.engine.save_as(filename)
        print("Game Saved")

def main() -> None:
    screen_width = 80
    screen_height = 50
    GLOBAL_ACCEPT_INPUT = True



    tileset = tcod.tileset.load_tilesheet(
        "GRAPHICS/dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )


    handler: input_handler.BaseEventHandler = setup_game.MainMenu()

    with tcod.context.new_terminal(
            screen_width,
            screen_height,
            tileset=tileset,
            title="Yet Another Roguelike Tutorial",
            vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        try:
            while True:
                root_console.clear()
                handler.on_render(console=root_console)
                context.present(root_console)
                if hasattr(handler,"engine"):
                    GLOBAL_ACCEPT_INPUT=handler.engine.player.can_act()

                try:
                    if GLOBAL_ACCEPT_INPUT:
                        for event in tcod.event.wait():
                            context.convert_event(event)
                            handler = handler.handle_events(event)
                    else:
                        handler = handler.skip_player()

                except Exception:
                    traceback.print_exc()

                    if isinstance(handler, input_handler.EventHandler):
                        handler.engine.message_log.add_message(traceback.format_exc(), color.error)

        except exceptions.QuitWithoutSaving:
            raise
        except SystemExit:
            save_game(handler, "savegame.sav")
            raise
        except  BaseException:
            save_game(handler, "savegame.sav")
            raise

if __name__ == "__main__":
    main()