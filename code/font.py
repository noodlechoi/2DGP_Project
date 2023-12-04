from pico2d import *

class Font():
    img = None
    def __init__(self, num, x, y):
        self.x, self.y = x, y
        self.number = num
        if Font.img == None:
            img = load_image('../resource/font(1).png')

    def draw(self):
        match self.number:
            case 1:
                Font.img.clip_draw(0, 40, 10, 10, self.x, self.y, 100, 100)
                pass