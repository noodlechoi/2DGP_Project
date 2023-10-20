from pico2d import *



open_canvas()
while True:
    clear_canvas()
    rail_img = load_image('../resource/bowling_rail.png')
    WIDTH = get_canvas_width()
    HEIGHT = get_canvas_height()
    # draw rail, WIDTH // 4 and HEIGHT // 2
    rail_img.clip_draw(0, 0, 85, 208, WIDTH // 4, HEIGHT // 2, WIDTH // 2, HEIGHT)
    rail_img.clip_composite_draw(0, 0, 85, 208, 0, 'h', WIDTH // 4 * 3, HEIGHT // 2, WIDTH // 2, HEIGHT)

    update_canvas()
    delay(0.1)

close_canvas()