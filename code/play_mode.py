from pico2d import clear_canvas, update_canvas, get_events
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT

import game_framework
import game_world
from rail import Rail
from pin import Pin


def init():
    global rail
    global pins

    player_rail = Rail()
    game_world.add_object(player_rail)

    pins = Pin()
    game_world.add_object(pins)

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
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            print(event.x, game_world.HEIGHT - event.y)

    pass


def pause():
    pass

def resume():
    pass

