from pico2d import *
import game_framework

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 1.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10


knuckles_location = [
    [270, 0], [1806, 1163]
]
knuckles_size = [
    [32, 42], [31, 42]
]

class Standing:
    @staticmethod
    def enter(ball, e):
        pass

    @staticmethod
    def exit(ball, e):
        pass

    @staticmethod
    def do(ball):
        # ball.frame = (ball.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        ball.frame = 2
        pass

    @staticmethod
    def draw(ball):
        size_x = 0
        for i in range(int(ball.frame)):
            size_x += knuckles_size[0][0]
        NPC.img.clip_draw(ball.location[0] + size_x, ball.location[1], ball.real_size[0], ball.real_size[1], ball.x, ball.y,
                            ball.size[0], ball.size[1])


class StateMachine:
    def __init__(self, npc):
        self.npc = npc
        self.cur_state = Standing
        self.transitions = {
        }

    def start(self):
        self.cur_state.enter(self.npc, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.npc)

    def draw(self):
        self.cur_state.draw(self.npc)


class NPC():
    img = None
    def __init__(self):
        self.x = 450
        self.y = 100
        self.location = [0, 0]
        self.real_size = [32, 42]
        self.size = [100, 150]
        self.dir = [0, 0]
        self.frame = 0
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        if NPC.img == None:
            NPC.img = load_image('../resource/knuckles_sprite_sheet(2).png')

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def update(self):
        self.state_machine.update()

    def get_bb(self):
        return self.x - self.size[0] // 2 + 10, self.y - self.size[1] // 2 + 10, self.x + self.size[
            0] // 2 - 10, self.y + self.size[1] // 2 - 10

    def handle_collision(self, group, other):
        if group == 'ball:pin':
            pass