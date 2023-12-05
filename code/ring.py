from pico2d import *
import game_framework
import game_world

PIXEL_PER_METER = (10.0 / 0.3)
TURN_SPEED_KMPH = 10.0
TURN_SPEED_MPM = TURN_SPEED_KMPH * 1000.0 / 60.0
TURN_SPEED_MPS = TURN_SPEED_MPM / 60.0
TURN_SPEED_PPS = TURN_SPEED_MPS * PIXEL_PER_METER

# 시간 당 프레임
TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
# 날아갈 때 프레임은 4개
FRAMES_PER_ACTION = 4

class Ring():
    img = None
    def __init__(self, layer, x, y):
        self.layer = layer
        self.x, self.y = x, y
        self.frame = 0
        self.ring_frame = {0:{'loc':[0,0], 'size':[17,17]}, 1:{'loc':[17,0], 'size':[10,17]}, 2:{'loc':[27,0], 'size':[6,17]}, 3:{'loc':[33,0], 'size':[12,17]}}
        self.size = [[100,80], [50, 80], [30, 80],[50, 80]]
        if Ring.img == None:
            Ring.img = load_image('../resource/ring.png')


    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * 4 * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        # self.frame = 3

    def draw(self):
        for frame, value in self.ring_frame.items():
            if int(self.frame) == frame:
                Ring.img.clip_draw(value['loc'][0], value['loc'][1], value['size'][0], value['size'][1], self.x, self.y, self.size[frame][0], self.size[frame][1])
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - self.size[int(self.frame)][0] // 2, self.y - self.size[int(self.frame)][1] // 2, self.x + self.size[int(self.frame)][0] // 2, self.y + self.size[int(self.frame)][1] // 2

    def handle_collision(self, group, other):
        if group == 'ball:ring':
            if other.layer == self.layer:
                other.coin += 1
                game_world.remove_object(self)
            pass
