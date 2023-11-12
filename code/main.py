from pico2d import *
import game_framework
import play_mode as start_mode
from game_world import WIDTH, HEIGHT

open_canvas(WIDTH, HEIGHT, sync = True)
game_framework.run(start_mode)
close_canvas()