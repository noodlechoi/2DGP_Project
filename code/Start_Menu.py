from pico2d import *

class Rail():
    rail_img = None
    def __init__(self):
        if Rail.rail_img == None:
            Rail.rail_img = load_image('../resource/bowling_rail.png')

    def draw(self):
        # draw rail : WIDTH // 4 and HEIGHT // 2
        Rail.rail_img.clip_draw(0, 0, 85, 208, WIDTH // 4, HEIGHT // 2, WIDTH // 2, HEIGHT)
        Rail.rail_img.clip_composite_draw(0, 0, 85, 208, 0, 'h', WIDTH // 4 * 3, HEIGHT // 2, WIDTH // 2, HEIGHT)

open_canvas()

# get screen size
WIDTH = get_canvas_width()
HEIGHT = get_canvas_height()

while True:
    clear_canvas()

    rail = Rail()
    rail.draw()

    update_canvas()
    delay(0.1)

close_canvas()