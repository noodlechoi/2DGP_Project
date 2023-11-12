from pico2d import *

import game_framework
from game_world import isConflict
from game_world import HEIGHT


PIXEL_PER_METER = (10.0 / 0.3)
Run_SPEED_KMPH = 1.0
Run_SPEED_MPM = Run_SPEED_KMPH * 1000.0 / 60.0
Run_SPEED_MPS = Run_SPEED_MPM / 60.0
Run_SPEED_PPS = Run_SPEED_MPS * PIXEL_PER_METER

# 시간 당 프레임
TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
# 날아갈 때 프레임은 4개
FRAMES_PER_ACTION = 6

run_location = [[185, 1525], [398, 1525]]
run_size = [[50, 40], [41, 40]]

def mouse_left_down(e, ball):
    return e[0] == 'INPUT' and e[1].type == SDL_MOUSEBUTTONDOWN and e[1].button == SDL_BUTTON_LEFT and  isConflict([ball.x, ball.y], ball.size, [e[1].x, HEIGHT - e[1].y])

def mouse_left_up(e, ball):
    return e[0] == 'INPUT' and e[1].type == SDL_MOUSEBUTTONUP and e[1].button == SDL_BUTTON_LEFT and  isConflict([ball.x, ball.y], ball.size, [e[1].x, HEIGHT - e[1].y])

def mouse_motion(e, ball):
    return e[0] == 'INPUT' and e[1].type == SDL_MOUSEMOTION

def time_out(e, ball):
    return e[0] == 'TIME_OUT'
class Thrown:
    @staticmethod
    def enter(ball, e):
        global FRAMES_PER_ACTION
        FRAMES_PER_ACTION = 5
        ball.frame = 0
        ball.real_size = [40, 35]
        ball.location = [605, 1210]
        pass

    @staticmethod
    def exit(ball, e):
        pass

    @staticmethod
    def do(ball):
        ball.frame = (ball.frame + FRAMES_PER_ACTION * 4 * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

    @staticmethod
    def draw(ball):
        Sonic.img.clip_draw(ball.location[0] + ball.real_size[0] * int(ball.frame), ball.location[1], ball.real_size[0], ball.real_size[1], ball.x, ball.y,
                            ball.size[0], ball.size[1])

class Rolling:
    @staticmethod
    def enter(ball, e):
        global FRAMES_PER_ACTION
        FRAMES_PER_ACTION = 5
        ball.frame = 0
        ball.real_size = [40, 35]
        ball.location = [605, 1210]
        pass

    @staticmethod
    def exit(ball, e):
        pass

    @staticmethod
    def do(ball):
        ball.frame = (ball.frame + FRAMES_PER_ACTION * 4 * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

    @staticmethod
    def draw(ball):
        Sonic.img.clip_draw(ball.location[0] + ball.real_size[0] * int(ball.frame), ball.location[1], ball.real_size[0], ball.real_size[1], ball.x, ball.y,
                            ball.size[0], ball.size[1])


class Run:
    @staticmethod
    def enter(ball, e):
        global FRAMES_PER_ACTION
        global frame_idx
        frame_idx = 0
        ball.frame = 0
        ball.real_size = [43, 40]
        ball.location = [10, 1525]
        FRAMES_PER_ACTION = 4
        ball.wait_time = get_time()
        pass

    @staticmethod
    def exit(ball, e):
        pass

    @staticmethod
    def do(ball):
        global run_size, run_location, frame_idx
        # 프레임 수가 적기 때문에 느려짐 => 프레임 * 2
        ball.frame = (ball.frame + FRAMES_PER_ACTION * 2 * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        # 시간이 흐르면 공 상태로
        if(get_time() - ball.wait_time > 3):
            ball.state_machine.handle_event(('TIME_OUT', 0))

        if(ball.frame >= FRAMES_PER_ACTION - 1):
            ball.real_size = run_size[frame_idx]
            ball.location = run_location[frame_idx]
            if frame_idx < 1:
                frame_idx += 1
        pass


    @staticmethod
    def draw(ball):
        Sonic.img.clip_draw(ball.location[0] + ball.real_size[0] * int(ball.frame), ball.location[1], ball.real_size[0], ball.real_size[1], ball.x, ball.y,
                            ball.size[0], ball.size[1])



class Standing:
    @staticmethod
    def enter(ball, e):
        global FRAMES_PER_ACTION
        ball.frame = 0
        FRAMES_PER_ACTION = 6
        pass

    @staticmethod
    def exit(ball, e):
        pass

    @staticmethod
    def do(ball):
        ball.frame = (ball.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION


    @staticmethod
    def draw(ball):
        Sonic.img.clip_draw(ball.location[0] + ball.real_size[0] * int(ball.frame), ball.location[1], ball.real_size[0], ball.real_size[1], ball.x, ball.y,
                            ball.size[0], ball.size[1])


class StateMachine:
    def __init__(self, sonic):
        self.sonic = sonic
        self.cur_state = Standing
        self.transitions = {
            Standing : {mouse_left_down: Run},
            Run : {time_out: Rolling, mouse_left_up : Thrown},
            Rolling : {mouse_left_up : Thrown},
            Thrown : {}
        }

    def start(self):
        self.cur_state.enter(self.sonic, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.sonic)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e, self.sonic):
                self.cur_state.exit(self.sonic, e)
                self.cur_state = next_state
                self.cur_state.enter(self.sonic, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.sonic)


class Sonic():
    img = None
    def __init__(self):
        self.x = 450
        self.y = 100
        self.location = [42, 1625]
        self.real_size = [30, 45]
        self.size = [100, 150]
        self.dir = 0
        self.frame = 0
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        if Sonic.img == None:
            Sonic.img = load_image('../resource/sonic_sprite_sheet(1).png')

    def draw(self):
        self.state_machine.draw()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))
