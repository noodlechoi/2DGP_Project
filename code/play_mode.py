import random

from pico2d import clear_canvas, update_canvas, get_events, load_image
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT, SDL_MOUSEMOTION

import game_framework
import game_world
from rail import Rail
from pin import Pin
from sonic import Sonic
import title_mode
import server
from round import Round
from npc import NPC, Knuckles, Tails
from ring import Ring

first_pin = [450, 480]
pin_list = [
    [first_pin[0] - 30 * 3, first_pin[1] + 25 * 3], [first_pin[0] - 30 , first_pin[1] + 25 * 3], [first_pin[0] + 30 , first_pin[1] + 25 * 3], [first_pin[0] + 30 * 3, first_pin[1] + 25 * 3],
    [first_pin[0] - 30 * 2, first_pin[1] + 25 * 2], [first_pin[0], first_pin[1] + 25 * 2], [first_pin[0] + 30 * 2, first_pin[1] + 25 * 2],
    [first_pin[0] - 30 , first_pin[1] + 25], [first_pin[0] + 30, first_pin[1] + 25],
    [first_pin[0], first_pin[1]]
]
layer_place = {2:450, 3:370, 4:300, 5:250}
random_range = {2:[300, 600], 3:[300, 600], 4:[300, 600], 5:[300, 600]}
def init():
    global pins



    server.round = Round()

    server.player_rail = Rail()
    game_world.add_object(server.player_rail, 0)
    server.npc_rail = Rail()
    game_world.add_object(server.npc_rail, 0)

    pins = [Pin(pin_list[i][0], pin_list[i][1]) for i in range(10)]
    game_world.add_objects(pins, 1)

    server.npc = Tails()
    game_world.add_object(server.npc, 6)

    server.player = Sonic()
    game_world.add_object(server.player, 6)


    for i in range(4):
        ring = Ring(i+2, random.randint(random_range[i+2][0], random_range[i+2][1]), layer_place[i+2])
        game_world.add_object(ring, i+2)
        game_world.add_collision_pair('ball:ring', None, ring)
    game_world.add_collision_pair('ball:ring', server.player, None)
    game_world.add_collision_pair('ball:ring', server.npc, None)

    game_world.add_collision_pair('ball:pin', server.player, None)
    game_world.add_collision_pair('ball:pin', server.npc, None)
    for pin in pins:
        game_world.add_collision_pair('ball:pin', None, pin)

    pass


def finish():
    game_world.clear()
    server.clear()
    pass

def update():
    server.round.update()

    game_world.update()
    game_world.handle_collisions()
    pass

def draw():
    clear_canvas()
    game_world.render()
    server.round.draw()
    update_canvas()
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        else:
            if server.round.who_turn == 'player' and server.round.is_processing():
                server.player.handle_event(event)
            # if(event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT):
            #     print(event.x, game_world.HEIGHT - event.y)

    pass


def pause():
    pass

def resume():
    pass
