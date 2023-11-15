from pico2d import *
import game_framework
import play_mode as start_mode
from game_world import WIDTH, HEIGHT

open_canvas(WIDTH, HEIGHT, sync = True)
game_framework.run(start_mode)
close_canvas()

# pin 끼리의 충돌 구현
# pin 사라지면 다시 생성
# 소닉이 굴러갈 때 소닉 확대
