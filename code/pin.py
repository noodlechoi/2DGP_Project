from pico2d import *
import game_world
import game_framework
import server

pin_frame = [
    # 왼쪽으로
    [48, 28], [40, 30], [38, 35], [23, 40],
    # 중간
    [15, 48],
    # 오른쪽으로
    [23, 40], [38, 35], [40, 30],[48, 28],
]
pin_size = [
    # 왼쪽으로
    [100, 50], [80, 70], [80, 70], [60, 90],
    # 중간
    [50, 100],
    # 오른쪽으로
    [60, 90], [80, 70], [80, 70],[100, 50],
]

PIXEL_PER_METER = (10.0 / 0.3)
Fall_SPEED_KMPH = 100.0
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
        # 충돌 오브젝트에서는 Standing에서 제거
        game_world.remove_object(pin)

        pass

    @staticmethod
    def do(pin):
        pin.frame = (pin.frame + (-1) * (pin.dir) * ( FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time))
        if pin.frame >= len(pin_frame) or pin.frame < 0:
            pin.state_machine.cur_state.exit(pin)
        pass

    @staticmethod
    def draw(pin):
        # 프레임에 따라 사이즈 변경
        pin.real_size = pin_frame[int(pin.frame)]
        pin.size = pin_size[int(pin.frame)]
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
        pin.state_machine.cur_state = Dead
        pin.state_machine.start()

        # 한번 부딪힌 핀은 소닉과 더 안 부딪힘
        game_world.remove_collision_object(pin)
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

class Producing:
    @staticmethod
    def enter(pin):
        pin.frame = 4
        pin.y += 170
        pass

    @staticmethod
    def exit(pin):
        pin.state_machine.cur_state = Standing
        pin.state_machine.start()

        # server.round.processing()
        pass

    @staticmethod
    def do(pin):
        pin.y -= Fall_SPEED_KMPH * game_framework.frame_time

        if pin.y <= pin.init_pos[1]:
            pin.y = int(pin.y)
            pin.state_machine.cur_state.exit(pin)
        pass

    @staticmethod
    def draw(pin):
        # 프레임에 따라 사이즈 변경
        pin.real_size = pin_frame[pin.frame]
        location = 0
        for i in range(0, pin.frame):
            location += pin_frame[i][0]
        Pin.img.clip_draw(location, 0, pin.real_size[0], pin.real_size[1], pin.x, pin.y, pin.size[0], pin.size[1])

class StateMachine:
    def __init__(self, pin):
        self.pin = pin
        self.cur_state = Producing

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
    thrown_sound = None
    def __init__(self, x = 450, y = 500):
        self.x = x
        self.y = y
        self.init_pos = x, y
        self.frame = 0
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.dir = 0
        # x, y
        self.real_size = pin_frame[0]
        self.size = [50, 100]
        if Pin.img == None:
            Pin.img = load_image('../resource/pin.png')
        if Pin.thrown_sound == None:
            Pin.thrown_sound = load_music('../resource/볼링.wav')

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

            # Standing exit
            self.state_machine.cur_state.exit(self)
            if server.round.who_turn == 'player':
                if not server.round.cur_round in server.round.player_score:
                    server.round.player_score[server.round.cur_round] = {}
                if not server.round.turn in server.round.player_score[server.round.cur_round]:
                    server.round.player_score[server.round.cur_round][server.round.turn] = 0

                server.round.player_score[server.round.cur_round][server.round.turn] += 1
            else:
                if not server.round.cur_round in server.round.npc_score:
                    server.round.npc_score[server.round.cur_round] = {}
                if not server.round.turn in server.round.npc_score[server.round.cur_round]:
                    server.round.npc_score[server.round.cur_round][server.round.turn] = 0

                server.round.npc_score[server.round.cur_round][server.round.turn] += 1

            Pin.thrown_sound.play()


