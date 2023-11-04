from pico2d import *
import game_framework
import title_mode as start_mode
from game_world import WIDTH, HEIGHT

open_canvas(WIDTH, HEIGHT)
game_framework.run(start_mode)
close_canvas()