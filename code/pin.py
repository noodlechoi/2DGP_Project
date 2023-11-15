from pico2d import *
import game_world
import game_framework

pin_frame = [
    # 왼쪽으로
    [48, 48], [40, 48], [38, 48], [23, 48],
    # 중간
    [15, 48],
    # 오른쪽으로
    [23, 48], [38, 48], [40, 48],[48, 48],
    ]
pin_frame_size = 9

PIXEL_PER_METER = (10.0 / 0.3)
Fall_SPEED_KMPH = 0.05
Fall_SPEED_MPM = Fall_SPEED_KMPH * 1000.0 / 60.0
Fall_SPEED_MPS = Fall_SPEED_MPM / 60.0
Fall_SPEED_PPS = Fall_SPEED_MPS * PIXEL_PER_METER

# 시간 당 프레임
TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
# 날아갈 때 프레임은 4개
FRAMES_PER_ACTION = 4

FRAMES_PER_TIME = ACTION_PER_TIME * FRAMES_PER_ACTION

class Dead:
    @staticmethod
    def enter(pin):
        if pin.dir > 0:
            pin.frame = 3
        else:
            pin.frame = 5
        pass

    @staticmethod
    def exit(pin):
        pass

    @staticmethod
    def do(pin):
        pin.frame = (pin.frame + (-1) * (pin.dir) * ( FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time))
        if pin.frame >= pin_frame_size:
            game_world.remove_object(pin)
        elif pin.frame < 0:
            game_world.remove_object(pin)
        pass

    @staticmethod
    def draw(pin):
        # 프레임에 따라 사이즈 변경
        pin.real_size = pin_frame[int(pin.frame)]
        location = 0
        for i in range(0, int(pin.frame)):
                location += pin_frame[i][0]
        Pin.img.clip_draw(location, 0, pin.real_size[0], pin.real_size[1], pin.x, pin.y,  pin.size[0],  pin.size[1])


class Standing:
    @staticmethod
    def enter(pin):
        pin.frame = 4
        pass

    @staticmethod
    def exit(pin):
        pass

    @staticmethod
    def do(pin):
        pass

    @staticmethod
    def draw(pin):
        # 프레임에 따라 사이즈 변경
        pin.real_size = pin_frame[pin.frame]
        location = 0
        for i in range(0, pin.frame):
            location += pin_frame[i][0]
        Pin.img.clip_draw(location, 0, pin.real_size[0], pin.real_size[1], pin.x, pin.y,  pin.size[0],  pin.size[1])


class StateMachine:
    def __init__(self, pin):
        self.pin = pin
        self.cur_state = Standing

    def start(self):
        self.cur_state.enter(self.pin)

    def update(self):
        self.cur_state.do(self.pin)

    def handle_event(self):
        pass

    def draw(self):
        self.cur_state.draw(self.pin)


class Pin():
    img = None
    def __init__(self, x = 450, y = 500):
        self.x = x
        self.y = y
        self.frame = 0
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.dir = 0
        # x, y
        self.real_size = pin_frame[0]
        self.size = [50, 100]
        if Pin.img == None:
            Pin.img = load_image('../resource/pin.png')

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def update(self):
        self.state_machine.update()
        pass

    def get_bb(self):
        return self.x - self.size[0] // 2, self.y - self.size[1] // 2, self.x + self.size[0] // 2, self.y + self.size[1] // 2

    def handle_collision(self, group, other):
        if group == 'ball:pin':
            # 방향 결정
            if game_world.directtion([self.x, self.y], [other.x, other.y])[0] > 0:
                self.dir = -1
            else:
                self.dir = 1

            self.state_machine.cur_state = Dead
            self.state_machine.start()
            game_world.remove_collision_object(self)
            # game_world.add_collision_pair('pin:pin', None, self)
            pass
        if group == 'pin:pin':
            # 쓰러지는 핀이 서있는 핀을 쓰러뜨리도록
            if self.state_machine.cur_state == Dead and other.state_machine.cur_state == Standing:
                other.state_machine.cur_state = Dead
                other.state_machine.start()

