from pico2d import clear_canvas, update_canvas, get_events
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT, SDL_MOUSEMOTION

import game_framework
import game_world
from rail import Rail
from pin import Pin
from sonic import Sonic
import title_mode

def init():
    global player_rail
    global pins
    global player
    global arrow
    global pin_list

    player_rail = Rail()
    game_world.add_object(player_rail, 0)

    first_pin = [450, 480]
    pin_list = [
        [first_pin[0] - 30 * 3, first_pin[1] + 25 * 3], [first_pin[0] - 30 , first_pin[1] + 25 * 3], [first_pin[0] + 30 , first_pin[1] + 25 * 3], [first_pin[0] + 30 * 3, first_pin[1] + 25 * 3],
        [first_pin[0] - 30 * 2, first_pin[1] + 25 * 2], [first_pin[0], first_pin[1] + 25 * 2], [first_pin[0] + 30 * 2, first_pin[1] + 25 * 2],
        [first_pin[0] - 30 , first_pin[1] + 25], [first_pin[0] + 30, first_pin[1] + 25],
        [first_pin[0], first_pin[1]]
    ]
    pins = [Pin(pin_list[i][0], pin_list[i][1]) for i in range(10)]

    game_world.add_objects(pins, 1)


    player = Sonic()
    game_world.add_object(player, 2)

    game_world.add_collision_pair('ball:pin', player, None)
    for pin in pins:
        game_world.add_collision_pair('ball:pin', None, pin)
        # game_world.add_collision_pair('ball:pin', pin, None)

    pass


def finish():
    game_world.clear()
    pass

def reproduce_pins():
    global pins
    global pin_list
    # pin이 다 쓰러지면 다시 생기기
    is_exist_pin = False
    for ol in game_world.objects:
        for o in ol:
            if type(Pin()) == type(o):
                is_exist_pin = True

    if not is_exist_pin:
        pins = [Pin(pin_list[i][0], pin_list[i][1]) for i in range(10)]
        game_world.add_objects(pins, 1)
        for pin in pins:
            game_world.add_collision_pair('ball:pin', None, pin)

def update():
    reproduce_pins()

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
            if(event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT):
                print(event.x, game_world.HEIGHT - event.y)

    pass


def pause():
    pass

def resume():
    pass

