from __future__ import annotations

import copy
import lzma
import pickle
import traceback
import os
import typing
from typing import Optional

import tcod
from IMPULSE import color
from IMPULSE import exceptions

from IMPULSE.engine import Engine
from IMPULSE.game_map import GameWorld
from IMPULSE import entity_factories
from IMPULSE import input_handler
from IMPULSE.input_handler import BaseEventHandler, HelpScreen

background_image = tcod.image.load("GRAPHICS/menu_background.png")[:, :, :3]

def new_game(playercolor:int=color.black, playername: str="player", floornum: int=0,) -> Engine:
    map_width = 80
    map_height=43
    room_max_size = 10
    room_min_size=6
    max_rooms=30
    name=playername
    player = copy.deepcopy(entity_factories.player)
    player.name=name
    player.color=playercolor
    if name == "sweethound":
        player.fighter.base_power=20
        player.fighter.base_reflex=20
        player.fighter.base_focus=20
        player.fighter.full_heal()

    if name == "poncho":
         player.fighter.base_speed=9
         player.fighter.base_focus=10
         player.fighter.base_max_hp=100
         player.fighter.base_max_fp=100
         player.fighter.full_heal()

    if name == "foukona":
        player.fighter.base_power=2
        player.fighter.full_heal()

    if name == "Camille":
        player.fighter.base_power=6
        player.fighter.full_heal()
    if name == "admin":
        player.fighter.base_power=20
        player.fighter.base_reflex=20
        player.fighter.base_focus=20
        player.fighter.base_max_hp = 100
        player.fighter.base_max_fp = 100
        player.fighter.base_speed = 10
        player.fighter.full_heal()

    engine = Engine(player=player)

    engine.game_world = GameWorld(
        engine=engine,
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        current_floor=floornum,
        viewport_width=30,
        viewport_height=30,

    )

    engine.game_world.generate_floor("normal")
    engine.update_fov()

    engine.message_log.add_message(
        "WELCOME TO YOUR DOOM", color.hypno_drone
    )
    if name == "PEERLESS":
        gun = copy.deepcopy(entity_factories.angelGun)
        gun.parent = player.inventory

        sword = copy.deepcopy(entity_factories.angelSword)
        sword.parent = player.inventory

        player.inventory.items.append(gun)
        player.equipment.toggle_equip(gun, add_message=False)

    else:
        pistol = copy.deepcopy(entity_factories.pistol)
        pistol.parent = player.inventory
        player.inventory.items.append(pistol)
        player.equipment.toggle_equip(pistol,add_message=False)

        knife = copy.deepcopy(entity_factories.cool_knife)
        knife.parent = player.inventory
        player.inventory.items.append(knife)
    if name == "Raven":
        pistol = copy.deepcopy(entity_factories.pistol)
        pistol.parent = player.inventory

    if name == "poncho":
        estrogen = copy.deepcopy(entity_factories.estrogen)
        estrogen.parent = player.inventory
        player.inventory.items.append(estrogen)

        for i in range(5):
            grenade = copy.deepcopy(entity_factories.frag_grenade)
            grenade.parent = player.inventory
            player.inventory.items.append(grenade)


    if name == "Camille":
        estrogen = copy.deepcopy(entity_factories.estrogen)
        estrogen.parent = player.inventory
        player.inventory.items.append(estrogen)

        labrys = copy.deepcopy(entity_factories.labrys)
        labrys.parent = player.inventory
        player.equipment.toggle_equip(labrys, add_message=False)

    if name == "foukona":
        labrys = copy.deepcopy(entity_factories.labrys)
        labrys.parent = player.inventory
        player.inventory.items.append(labrys)
        rapier = copy.deepcopy(entity_factories.rapier)
        rapier.parent = player.inventory
        player.inventory.items.append(rapier)
        suit = copy.deepcopy(entity_factories.hazard_suit)
        suit.parent = player.inventory
        player.inventory.items.append(suit)

        dress = copy.deepcopy(entity_factories.dress)
        dress.parent = player.inventory
        player.inventory.items.append(dress)


    if  name == "admin":

        sword = copy.deepcopy(entity_factories.angelSword)
        sword.parent = player.inventory

        player.inventory.items.append(sword)


        poppers = copy.deepcopy(entity_factories.poppers)
        poppers.parent = player.inventory
        player.inventory.items.append(poppers)

        los= copy.deepcopy(entity_factories.los_upgrade)
        los.parent = player.inventory
        player.inventory.items.append(los)

        molotov = copy.deepcopy(entity_factories.fire_grenade)
        molotov.parent = player.inventory
        player.inventory.items.append(molotov)

        molotov = copy.deepcopy(entity_factories.fire_grenade)
        molotov.parent = player.inventory
        player.inventory.items.append(molotov)

        flare = copy.deepcopy(entity_factories.flare)
        flare.parent = player.inventory
        player.inventory.items.append(flare)

        flare = copy.deepcopy(entity_factories.flare)
        flare.parent = player.inventory
        player.inventory.items.append(flare)

        flare = copy.deepcopy(entity_factories.flare)
        flare.parent = player.inventory
        player.inventory.items.append(flare)

        flare = copy.deepcopy(entity_factories.flare)
        flare.parent = player.inventory
        player.inventory.items.append(flare)

        dart = copy.deepcopy(entity_factories.ketamine_scroll)
        dart.parent = player.inventory
        player.inventory.items.append(dart)

        claws=copy.deepcopy(entity_factories.shock_claws)
        claws.parent = player.inventory
        player.inventory.items.append(claws)

        accuracy = copy.deepcopy(entity_factories.accuracy_upgrade)
        accuracy.parent = player.inventory
        player.inventory.items.append(accuracy)

        hack_upgrade=copy.deepcopy(entity_factories.hack_upgrade)
        hack_upgrade.parent = player.inventory
        player.inventory.items.append(hack_upgrade)

        los=copy.deepcopy(entity_factories.los_upgrade)
        los.parent = player.inventory
        player.inventory.items.append(los)

        control=copy.deepcopy(entity_factories.control_upgrade)
        control.parent = player.inventory
        player.inventory.items.append(control)

    bandage = copy.deepcopy(entity_factories.health_potion)
    bandage.parent = player.inventory
    player.inventory.items.append(bandage)
    player.fighter.full_heal()
    return engine

def load_game(filename:str) -> Engine:
    with open(filename, "rb")as f:
        engine = pickle.loads(lzma.decompress(f.read()))
    assert isinstance(engine, Engine)
    return engine

class SplashScreen(BaseEventHandler):
    def __init__(self):
        super().__init__()
        self.line_num=0
        self.char_pos=0
        self.TITLE = "The year is 2XXX"
        self.LINE1 = "For decades the forces of humanity were tuned to a singular goal:"
        self.LINE2 = "      Profit."
        self.LINE3 = "To this end, great labyrinths "
        self.LINE35=  "     of twisting plastic and dull concrete were constructed"
        self.LINE4 = "Reaching miles into the sky above, and plunging into great crevices below"
        self.LINE5 = "And in their beating hearts, the loyal dogs of capital "
        self.LINE55=  "     were rewarded with wonderous tech;"
        self.LINE6 = "those who sold their soul were paid "
        self.LINE65=             "     in bodies that transcend the crude dispensation of nature."
        self.LINE7 = "Time passed, crisis after crisis led to mass exodus from our plastic prisons."
        self.LINE8 = "But, the technology remains."
        self.LINE9 = "You were born outside, in the wastes surrounding the ruins of Neo-Akron."
        self.LINE10 = "And as far as humanity has advanced, we have yet to cast off"
        self.LINE105= "     our limited conceptions of sex and gender."
        self.LINE11 = "So they reject you, just as you reject 'nature'."
        self.LINE12 = "Though you receive support from your friends, there is an ache from within."
        self.LINE13 = "And there, in the old ruins of Neo-Akron, lies a solution."
        self.LINE14 = "The last functioning Auto-Surgeon in the MegaCleveland Metro-Zone."
        self.LINE15 = "Fully functional, no WPATH, no bureaucracy, no copay."
        self.LINE16 = "It is time to make your body your own."
        self.wait_timer=0
        self.OPENING_CRAWL=[self.LINE1,self.LINE2,self.LINE3,self.LINE35,self.LINE4,self.LINE5,self.LINE55,self.LINE6,self.LINE65,self.LINE7,self.LINE8,
                            self.LINE9,self.LINE10,self.LINE105,self.LINE11,self.LINE12,self.LINE13,self.LINE14,self.LINE15,]
    def update_text(self):
        current_Line=self.OPENING_CRAWL[self.line_num]
        lineLength=len(current_Line)
        if self.char_pos+1 == lineLength:
            self.char_pos=0
            self.line_num+=1
        else:
            self.char_pos+=1




    def on_render(self, console: tcod.Console) -> None:
        console.print(
            console.width // 2,
            1,
            self.TITLE,
            fg=color.hypno_drone,
            alignment = tcod.CENTER,
        )

        linenum=1
        for line in self.OPENING_CRAWL:
            linenum+=2
            console.print(
                0,
                linenum,
                line,
                fg=color.haxor_green
         )
        console.print(
            console.width // 2,linenum+2,self.LINE16,fg=color.hypno_drone,alignment = tcod.CENTER)


    def ev_keydown(self, event: tcod.event.KeyDown, ) -> Optional[input_handler.BaseEventHandler]:
        if event.sym:
            return  MainMenu()
        return None





class MainMenu(BaseEventHandler):
    def on_render(self, console: tcod.Console) -> None:
        console.draw_semigraphics(background_image,0,0)

        console.print(
            console.width // 2,
            console.height // 2 - 4,
            "PROJECT IMPULSE",
            fg=color.hypno_drone,
            bg=color.black,
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
                fg=color.haxor_green,
                bg=color.black,
                alignment=tcod.CENTER,
            )

        console.print_box(
            0, console.height-8,console.width,1,
            "A game by Nova Zero. ",
                fg=color.haxor_green,
                bg=color.black,
                alignment=tcod.RIGHT,
                bg_blend=tcod.BKGND_ALPHA(64),
        )
        console.print_box(
            0, console.height - 7, console.width,1,
            "Email her with bug reports at HuntressDust@proton.me",
                fg=color.haxor_green,
                bg=color.black,
                alignment=tcod.RIGHT,


            )

        console.print_box(
            0, console.height-5,console.width,1,
            "Much thanks to rogueliketutorials.com, r/roguelikedev,",
                fg=color.haxor_green,
                bg=color.black,
                alignment=tcod.RIGHT,

        )

        console.print_box(
            0, console.height - 4,console.width,1,
            "and my girlfriend :3",
                fg=color.haxor_green,
                bg=color.black,
                alignment=tcod.RIGHT,

        )


        console.print_box(
            0, console.height-2,console.width,1,
            "Version 1.121, compiled 23-07-2026",
                fg=color.haxor_green,
                bg=color.black,
                alignment=tcod.RIGHT,

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
    def on_render(self, console: tcod.Console, ) -> None:

        console.print(
            console.width // 2,
            console.height // 2 - 4,
            "YOU DID IT",
            fg=color.hypno_sentry,
            alignment = tcod.CENTER,
        )

        console.print(
            console.width // 2,
            console.height // 2 - 8,
            "You've finally reached the Auto-Surgeon and got a vaginoplasty",
            fg=color.hypno_sentry,
            alignment=tcod.CENTER,
        )
        console.print(
            console.width // 2,
            console.height // 2 - 8,
            "You've finally reached the Auto-Surgeon and got a vaginoplasty",
            fg=color.hypno_sentry,
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
                fg=color.hypno_sentry,
                bg=color.black,
                alignment=tcod.CENTER,
                bg_blend=tcod.BKGND_ALPHA(64),

            )
    def ev_keydown(self, event: tcod.event.KeyDown, ) -> Optional[input_handler.BaseEventHandler]:
        if event.sym in (tcod.event.KeySym.Q, tcod.event.KeySym.ESCAPE):
            if os.path.exists("savegame.sav"):
                os.remove("savegame.sav")
            raise SystemExit()
        elif event.sym == tcod.event.KeySym.N:
            return name_entry()

        return None

class name_entry(input_handler.BaseEventHandler):
    def __init__(self):
        super().__init__()
        self.name: str=""
        self.is_valid=True
    def on_quit(self) -> None:
        if os.path.exists("savegame.sav"):
            os.remove("savegame.sav")
        raise exceptions.QuitWithoutSaving()

    def ev_quit(self, event: tcod.event.Quit,) -> None:
        self.on_quit()

    def on_render(self, console: tcod.Console) -> None:

        console.print(
            console.width // 2,
            console.height // 2 - 8,
            "Enter Your Name, Miss",
            fg=color.hypno_drone,
            alignment=tcod.CENTER,
        )


        console.draw_frame(
            console.width // 2 -7,
            console.height // 2 - 4,
            width=13,
            height=3,
            clear=False,
            fg=color.haxor_green,
            bg=(0, 0, 0)
        )
        console.print(
            console.width // 2-6,
            console.height // 2-3,
            self.name,
            fg=color.menu_title,
        )

        if not self.is_valid:
            console.print(
                console.width // 2,
                console.height // 2 ,
                "Error: Invalid Name",
                fg=color.red,
                alignment=tcod.CENTER,
            )
            console.print(
                console.width // 2,
                console.height // 2 + 2 ,
                f"{self.name}",
                fg=color.red,
                alignment=tcod.CENTER,
            )
    def ev_keydown(self, event: tcod.event.KeyDown, ) -> Optional[input_handler.BaseEventHandler]:
        key = event.sym
        if key is (tcod.event.KeySym.ESCAPE):
            raise SystemExit()
        elif key in input_handler.CONFIRM_KEYS:
            if self.name != "" and self.name !=" " and self.name != "  " and self.name != "   " and self.name != "    " and self.name != "     ":
                self.is_valid=False
                if self.name == "      "  or self.name == "       " or self.name == "        " or self.name == "         " :
                    self.name= "cunt"


                return color_handler(self.name)
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

class color_handler(input_handler.BaseEventHandler):
    def __init__(self,name):
        self.name=name
        self.player_color=color.black
    def on_quit(self) -> None:
        if os.path.exists("savegame.sav"):
            os.remove("savegame.sav")
        raise exceptions.QuitWithoutSaving()

    def ev_quit(self, event: tcod.event.Quit,) -> None:
        self.on_quit()

    def on_render(self, console: tcod.Console) -> None:

        console.print(
            console.width // 2,
            console.height // 2 - 8,
            "Please choose your Form.",
            fg=color.hypno_drone,
            alignment=tcod.CENTER,
        )

        if self.player_color==color.black:
            console.draw_frame(
                x=console.width // 2 -8,
            y=console.height // 2 - 5,
            width=7,
            height=7,
            fg=color.haxor_green,
            clear=False)
        else:
            console.draw_frame(
                x=console.width // 2 +1,
            y=console.height // 2 - 5,
            width=7,
            height=7,
            fg=color.haxor_green,
            clear=False)


        console.draw_rect(
            console.width // 2 -7,
            console.height // 2 - 4,
            width=5,
            height=5,
            ch=0,
            bg=color.floor,
            fg=color.floor,
        )

        console.draw_rect(
            console.width // 2 +2,
            console.height // 2 - 4,
            width=5,
            height=5,
            ch=0,
            bg=color.floor,
            fg=color.floor,
        )

        console.print(console.width//2-5,console.height//2-2,"@",color.black)
        console.print(console.width // 2 +4, console.height // 2 - 2, "@", color.white)


    def ev_keydown(self, event: tcod.event.KeyDown, ) -> Optional[input_handler.BaseEventHandler]:
        key = event.sym
        if key is (tcod.event.KeySym.ESCAPE):
            raise SystemExit()
        elif key is tcod.event.KeySym.LEFT:
            self.player_color=color.black
        elif key is tcod.event.KeySym.RIGHT:
            self.player_color=color.white
        elif key in input_handler.CONFIRM_KEYS:
            if self.name=="admin":
                return  debug_handler(self.name,self.player_color)
            return input_handler.MainGameEventHandler(new_game(self.player_color, self.name))


class debug_handler(input_handler.BaseEventHandler):

    def __init__(self, name,color):
        super().__init__()
        self.name=name
        self.floornum: str='0'
        self.is_valid=True
        self.error_latch=False
        self.player_color=color
    def on_quit(self) -> None:
        if os.path.exists("savegame.sav"):
            os.remove("savegame.sav")
        raise exceptions.QuitWithoutSaving()

    def on_render(self, console: tcod.Console) -> None:

        console.print(
            console.width // 2,
            console.height // 2 - 9,
            "Welcome, administrator.",
            fg=color.menu_title,
            alignment=tcod.CENTER,
        )
        console.print(
            console.width // 2,
            console.height // 2 - 8,
            "Please enter the starting floor.",
            fg=color.menu_title,
            alignment=tcod.CENTER,
        )
        console.draw_frame(
            console.width // 2 - 3,
            console.height // 2 - 4,
            width=4,
            height=3,
            clear=False,
            fg=(255, 255, 255),
            bg=(0, 0, 0)
        )

        console.print(
            console.width // 2 - 2,
            console.height // 2 - 3,
            self.floornum,
            fg=color.menu_title,

        )

        if not self.is_valid:
            self.is_valid=True

        if self.error_latch:
            console.print(
                console.width // 2,
                console.height // 2,
                "Error: Must be an integer 1-10",
                fg=color.red,
                alignment=tcod.CENTER,
            )



    def ev_keydown(self, event: tcod.event.KeyDown, ) -> Optional[input_handler.BaseEventHandler]:
            key = event.sym
            if key is (tcod.event.KeySym.ESCAPE):
                raise SystemExit()
            elif key in input_handler.CONFIRM_KEYS:
                starting_floor=0
                try:
                    starting_floor=int(self.floornum)
                    if starting_floor<1:
                        raise Exception
                except:
                    self.floornum = '0'
                    self.is_valid= False
                    self.error_latch=True

                if self.is_valid:
                    return input_handler.MainGameEventHandler(new_game(self.player_color,self.name,floornum=starting_floor-1))

            elif key is tcod.event.KeySym.BACKSPACE:
                self.floornum=self.floornum[:len(self.floornum)-1]

            elif key in input_handler.TEXT_KEYS:
                if len(self.floornum)<2:
                    mod=0
                    if event.mod & (tcod.event.Modifier.LSHIFT | tcod.event.Modifier.RSHIFT):
                        mod=32
                    char=input_handler.TEXT_KEYS[key]

                    char=chr(ord(char) - mod)

                self.floornum=self.floornum+char


class game_over_screen(End_Screen):
    def __init__(self,score: int, floor: int, name:str,playercolor):
        super().__init__()
        self.floor=floor
        self.score=score
        self.name=name
        self.color=playercolor
    def on_quit(self) -> None:
        if os.path.exists("savegame.sav"):
            os.remove("savegame.sav")
        raise exceptions.QuitWithoutSaving()

    def ev_keydown(self, event: tcod.event.KeyDown,) ->  Optional[input_handler.BaseEventHandler]:

        if event.sym in (tcod.event.KeySym.Q, tcod.event.KeySym.ESCAPE):
            self.on_quit()

        if event.sym==tcod.event.KeySym.R:
            return input_handler.MainGameEventHandler(new_game(self.color,self.name,))

        if event.sym ==tcod.event.KeySym.N:
            return name_entry()

    def on_render(self, console: tcod.Console) -> None:
        super().on_render(console)

        log_console = tcod.Console(console.width - 6, console.height - 6)
        log_console.draw_frame(0,0, log_console.width, log_console.height)
        log_console.print_box(

            0, 0, log_console.width, 1, f"!!{self.name} has been struck down!!", alignment=tcod.CENTER,
            fg=(255, 0, 0),
            bg=color.black,
        )

        log_console.print_box(
            0, 5, log_console.width, 2, f"Your sisters above will remember you always, even as your bones crumble and the slimes absorb your flesh.", alignment=tcod.CENTER,
        )
        log_console.print_box(
            0, 10, log_console.width, 1, f"Thoughts and Prayers.", alignment=tcod.CENTER
        )
        log_console.print_box(
            0, 15, log_console.width, 1, f"You made it to floor {self.floor}, and your score was {self.score}.", alignment=tcod.CENTER
        )
        for i, text in enumerate(
            ["[R] Restart", "[N] New Game", "[Q] Quit"]
        ):
            log_console.print_box(
                0,
                20 + i,
                log_console.width, 1,
                text,
                fg=(255,0,255),
                bg=color.black,
                alignment=tcod.CENTER,
            )
        log_console.blit(console, 3, 3)