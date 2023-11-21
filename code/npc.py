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

animation_names = ['knuckles_sprite_sheet.png', 'tails_sprite_sheet.png', 'bean_sprite_sheet']


class Standing:
    @staticmethod
    def enter(ball, e):
        global FRAMES_PER_ACTION
        ball.frame = 0
        FRAMES_PER_ACTION = 6
        ball.x = 450
        ball.y = 100
        ball.location = [42, 1625]
        ball.real_size = [30, 45]
        ball.size = [100, 150]
        pass

    @staticmethod
    def exit(ball, e):
        pass

    @staticmethod
    def do(ball):
        ball.frame = (ball.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION


    @staticmethod
    def draw(ball):
        if ball.dir[0] <= 0:
            NPC.img.clip_draw(ball.location[0] + ball.real_size[0] * int(ball.frame), ball.location[1], ball.real_size[0], ball.real_size[1], ball.x, ball.y,
                                ball.size[0], ball.size[1])
        else:
            NPC.img.clip_composite_draw(ball.location[0] + ball.real_size[0] * int(ball.frame), ball.location[1],
                                            ball.real_size[0], ball.real_size[1], 0, 'h', ball.x, ball.y,
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
    images = None
    def load_images(self):
        if NPC.images == None:
            NPC.images = {}
            for name in animation_names:
                NPC.images[name] = [load_image("../resource/" + name + ".png")]

    def __init__(self):
        self.x = 450
        self.y = 100
        self.location = [42, 1625]
        self.real_size = [30, 45]
        self.size = [100, 150]
        self.dir = [0, 0]
        self.frame = 0
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def get_bb(self):
        return self.x - self.size[0] // 2 + 10, self.y - self.size[1] // 2 + 10, self.x + self.size[
            0] // 2 - 10, self.y + self.size[1] // 2 - 10

    def handle_collision(self, group, other):
        if group == 'ball:pin':
            pass