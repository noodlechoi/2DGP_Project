from pico2d import *

class Font():
    img = None
    def __init__(self):

        if Font.img == None:
            img = load_image('font(1).png')

    def num_print(self, num, p):
        match num:
            case 1:
                # Font.img.clip_draw(location, 0, pin.real_size[0], pin.real_size[1], pin.x, pin.y, pin.size[0], pin.size[1])
                pass