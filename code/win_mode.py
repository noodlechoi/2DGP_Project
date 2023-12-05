from pico2d import *
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT

import game_framework
import play_mode
from rail import Rail
from game_world import WIDTH, HEIGHT, is_conflict
import game_world

def init():
    global lose_img
    lose_img = load_image('../resource/win.jpg')
    pass


def finish():
    pass
    # del location

def update():
    pass

def draw():
    global lose_img
    lose_img.draw(game_world.WIDTH // 2, game_world.HEIGHT // 2, get_canvas_width(), get_canvas_height())
    pass

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
    pass