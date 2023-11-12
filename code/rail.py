from pico2d import *
from game_world import WIDTH, HEIGHT


class Rail():
    img = None
    def __init__(self):
        if Rail.img == None:
            Rail.img = load_image('../resource/bowling_rail.png')

    def draw(self):
        # draw rail : WIDTH // 4 and HEIGHT // 2
        Rail.img.clip_draw(0, 0, 85, 208, WIDTH // 4, HEIGHT // 2, WIDTH // 2, HEIGHT)
        Rail.img.clip_composite_draw(0, 0, 85, 208, 0, 'h', WIDTH // 4 * 3, HEIGHT // 2, WIDTH // 2, HEIGHT)

    def update(self):
        pass
