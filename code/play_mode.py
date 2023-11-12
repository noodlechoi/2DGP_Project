from pico2d import clear_canvas, update_canvas, get_events
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT

import game_framework
import game_world
from rail import Rail
from pin import Pin
from sonic import Sonic
import title_mode
from arrow import Arrow

def init():
    global rail
    global pins
    global player
    global arrow

    player_rail = Rail()
    game_world.add_object(player_rail, 0)

    pins = Pin()
    game_world.add_object(pins, 1)

    player = Sonic()
    game_world.add_object(player, 2)

    arrow = Arrow()
    game_world.add_object(arrow, 1)

    pass


def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collisions()
    pass

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()
    pass


def handle_events():
    global player

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        else:
            player.handle_event(event)

    pass


def pause():
    pass

def resume():
    pass

