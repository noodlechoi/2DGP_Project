from pico2d import *

class Font():
    img = None
    def __init__(self, num, x, y, size = [80, 100]):
        self.x, self.y = x, y
        self.size = size
        self.number = num
        if Font.img == None:
            Font.img = load_image('../resource/font(1).png')

    def draw(self):
        # self.number = num
        match self.number:
            case 1:
                Font.img.clip_draw(5, 82, 7, 10, self.x, self.y, self.size[0], self.size[1])
            case 2:
                Font.img.clip_draw(12, 82, 7, 10, self.x, self.y, self.size[0], self.size[1])
            case 3:
                Font.img.clip_draw(20, 82, 7, 10, self.x, self.y, self.size[0], self.size[1])
            case 4:
                Font.img.clip_draw(29, 82, 7, 10, self.x, self.y, self.size[0], self.size[1])
            case 5:
                Font.img.clip_draw(37, 82, 7, 10, self.x, self.y, self.size[0], self.size[1])
            case 6:
                Font.img.clip_draw(45, 82, 7, 10, self.x, self.y, self.size[0], self.size[1])
            case 7:
                Font.img.clip_draw(53, 82, 7, 10, self.x, self.y, self.size[0], self.size[1])
            case 8:
                Font.img.clip_draw(61, 82, 7, 10, self.x, self.y, self.size[0], self.size[1])
            case 9:
                Font.img.clip_draw(69, 82, 7, 10, self.x, self.y, self.size[0], self.size[1])
            case 0:
                Font.img.clip_draw(77, 82, 7, 10, self.x, self.y, self.size[0], self.size[1])
            case 10:
                Font.img.clip_draw(185, 93, 7, 10, self.x, self.y, self.size[0], self.size[1])

