from pico2d import *

import game_framework
import game_world
from arrow import Arrow
import math
import server

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 1.0
RUN_SPEED_MPM = RUN_SPEED_KMPH * 1000.0 / 60.0
RUN_SPEED_MPS = RUN_SPEED_MPM / 60.0
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

# 시간 당 프레임
TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
# 날아갈 때 프레임은 4개
FRAMES_PER_ACTION = 6

run_location = [[185, 1525], [398, 1525]]
run_size = [[50, 40], [41, 40]]

def mouse_left_down(e, ball):
    return e[0] == 'INPUT' and e[1].type == SDL_MOUSEBUTTONDOWN and e[1].button == SDL_BUTTON_LEFT and  game_world.is_conflict([ball.x, ball.y], ball.size, [e[1].x, game_world.HEIGHT - e[1].y])

def mouse_left_up(e, ball):
    return e[0] == 'INPUT' and e[1].type == SDL_MOUSEBUTTONUP and e[1].button == SDL_BUTTON_LEFT

def mouse_motion(e, ball):
    return e[0] == 'INPUT' and e[1].type == SDL_MOUSEMOTION


def a_down(e, ball):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a

def time_out(e, ball):
    return e[0] == 'TIME_OUT'


class Dead:
    @staticmethod
    def enter(ball, e):
        global FRAMES_PER_ACTION
        global t
        t = 0
        FRAMES_PER_ACTION = 5
        ball.frame = 0
        ball.real_size = [40, 35]
        ball.location = [605, 1210]
        game_world.remove_collision_object(ball)
        pass

    @staticmethod
    def exit(ball, e):
        ball.state_machine.cur_state = Standing
        ball.state_machine.start()
        game_world.add_collision_pair('ball:pin', ball, None)
        pass

    @staticmethod
    def do(ball):
        global t
        ball.move_dead_line(t)
        t += game_framework.frame_time / 2

        # 크기가 원근감 있게 줄어듦
        ball.size[0] -= int(16 * RUN_SPEED_PPS * game_framework.frame_time)
        ball.size[1] -= int(16 * RUN_SPEED_PPS * game_framework.frame_time)

        # rail 밖으로 나갔을 때
        if ball.x <= 0 - ball.size[0] // 2 + 10 or ball.x >= game_world.WIDTH + ball.size[0] // 2 or ball.y >= 530:
            ball.state_machine.cur_state.exit(ball, [])
            return

        ball.frame = (ball.frame + FRAMES_PER_ACTION * 4 * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

    @staticmethod
    def draw(ball):
        if ball.dir[0] <= 0:
            Sonic.img.clip_draw(ball.location[0] + ball.real_size[0] * int(ball.frame), ball.location[1],
                                ball.real_size[0], ball.real_size[1], ball.x, ball.y,
                                ball.size[0], ball.size[1])
        else:
            Sonic.img.clip_composite_draw(ball.location[0] + ball.real_size[0] * int(ball.frame), ball.location[1],
                                          ball.real_size[0], ball.real_size[1], 0, 'h', ball.x, ball.y,
                                          ball.size[0], ball.size[1])


class Thrown:
    @staticmethod
    def enter(ball, e):
        global FRAMES_PER_ACTION
        global time
        time = 0
        FRAMES_PER_ACTION = 5
        ball.frame = 0
        ball.real_size = [40, 35]
        ball.location = [605, 1210]
        pass

    @staticmethod
    def exit(ball, e):
        ball.state_machine.cur_state = Standing
        ball.state_machine.start()
        pass

    @staticmethod
    def do(ball):
        global time
        # 시간이 지나면 회전하도록
        curve = -110 * math.sin(math.radians(time))
        # curve가 -3이 넘으면 다시 아래로 내려가는 것을 방지
        if curve <= -3: curve = -2

        time += game_framework.frame_time

        ball.x += (-1) * ball.dir[0] * RUN_SPEED_PPS * game_framework.frame_time + curve
        ball.y += (-1) * ball.dir[1] * RUN_SPEED_PPS * game_framework.frame_time + curve

        # 크기가 원근감 있게 줄어듦
        ball.size[0] -= int(14 * RUN_SPEED_PPS * game_framework.frame_time)
        ball.size[1] -= int(14 * RUN_SPEED_PPS * game_framework.frame_time)

        
        # rail 밖으로 나갔을 때
        if ball.x <= 0 - ball.size[0] // 2 + 10 or ball.x >= game_world.WIDTH + ball.size[0] // 2 or ball.y >= 530:
            ball.state_machine.cur_state.exit(ball, [])
            return
        if server.player_rail.dead_line(ball):
            ball.state_machine.cur_state = Dead
            ball.state_machine.start()
            return
        
        ball.frame = (ball.frame + FRAMES_PER_ACTION * 4 * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION


    @staticmethod
    def draw(ball):
        if ball.dir[0] <= 0:
            Sonic.img.clip_draw(ball.location[0] + ball.real_size[0] * int(ball.frame), ball.location[1],
                                ball.real_size[0], ball.real_size[1], ball.x, ball.y,
                                ball.size[0], ball.size[1])
        else:
            Sonic.img.clip_composite_draw(ball.location[0] + ball.real_size[0] * int(ball.frame), ball.location[1],
                                          ball.real_size[0], ball.real_size[1], 0, 'h', ball.x, ball.y,
                                          ball.size[0], ball.size[1])

class Rolling:
    @staticmethod
    def enter(ball, e):
        global FRAMES_PER_ACTION
        global arrow
        FRAMES_PER_ACTION = 5
        ball.frame = 0
        ball.real_size = [40, 35]
        ball.location = [605, 1210]

        arrow = Arrow()
        game_world.add_object(arrow, 1)
        pass

    @staticmethod
    def exit(ball, e):
        global arrow

        # 나갈 때 방향 결정, dir = 볼과 화살표 거리 및 방향
        ball.dir = game_world.directtion([ball.x, ball.y], [arrow.x, arrow.y])
        game_world.remove_object(arrow)
        pass

    @staticmethod
    def do(ball):
        ball.frame = (ball.frame + FRAMES_PER_ACTION * 4 * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

    @staticmethod
    def draw(ball):
        if ball.dir[0] <= 0:
            Sonic.img.clip_draw(ball.location[0] + ball.real_size[0] * int(ball.frame), ball.location[1],
                                ball.real_size[0], ball.real_size[1], ball.x, ball.y,
                                ball.size[0], ball.size[1])
        else:
            Sonic.img.clip_composite_draw(ball.location[0] + ball.real_size[0] * int(ball.frame), ball.location[1],
                                          ball.real_size[0], ball.real_size[1], 0, 'h', ball.x, ball.y,
                                          ball.size[0], ball.size[1])


class Run:
    @staticmethod
    def enter(ball, e):
        global FRAMES_PER_ACTION
        global frame_idx
        global arrow
        frame_idx = 0
        ball.frame = 0
        ball.real_size = [43, 40]
        ball.location = [10, 1525]
        FRAMES_PER_ACTION = 4
        ball.wait_time = get_time()

        arrow = Arrow()
        game_world.add_object(arrow, 1)
        pass

    @staticmethod
    def exit(ball, e):
        global arrow

        # Run 상태에서 Thrown 상태가 될 수 있기 때문에
        ball.dir = game_world.directtion([ball.x, ball.y], [arrow.x, arrow.y])
        game_world.remove_object(arrow)
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
        if ball.dir[0] <= 0:
            Sonic.img.clip_draw(ball.location[0] + ball.real_size[0] * int(ball.frame), ball.location[1],
                                ball.real_size[0], ball.real_size[1], ball.x, ball.y,
                                ball.size[0], ball.size[1])
        else:
            Sonic.img.clip_composite_draw(ball.location[0] + ball.real_size[0] * int(ball.frame), ball.location[1],
                                          ball.real_size[0], ball.real_size[1], 0, 'h', ball.x, ball.y,
                                          ball.size[0], ball.size[1])



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
            Sonic.img.clip_draw(ball.location[0] + ball.real_size[0] * int(ball.frame), ball.location[1], ball.real_size[0], ball.real_size[1], ball.x, ball.y,
                                ball.size[0], ball.size[1])
        else:
            Sonic.img.clip_composite_draw(ball.location[0] + ball.real_size[0] * int(ball.frame), ball.location[1],
                                            ball.real_size[0], ball.real_size[1], 0, 'h', ball.x, ball.y,
                                            ball.size[0], ball.size[1])


class StateMachine:
    def __init__(self, sonic):
        self.sonic = sonic
        self.cur_state = Standing
        self.transitions = {
            Standing : {mouse_left_down: Run, a_down: Standing},
            Run : {time_out: Rolling, mouse_left_up : Thrown},
            Rolling : {mouse_left_up : Thrown},
            Thrown : {},
            Dead : {},
        }

    def start(self):
        self.cur_state.enter(self.sonic, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.sonic)

    def handle_event(self, e):
        if e[0] == 'INPUT' and e[1].type == SDL_MOUSEMOTION and self.cur_state != Thrown:
            self.sonic.dir = game_world.directtion([self.sonic.x, self.sonic.y ], [e[1].x, game_world.HEIGHT - e[1].y])

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
        self.dir = [0, 0]
        self.frame = 0
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        if Sonic.img == None:
            Sonic.img = load_image('../resource/sonic_sprite_sheet(1).png')

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def get_bb(self):
        return self.x - self.size[0] // 2 + 10, self.y - self.size[1] // 2+ 10, self.x + self.size[0] // 2 - 10, self.y + self.size[1] // 2 - 10

    def handle_collision(self, group, other):
        if group == 'ball:pin':
            pass


    def move_dead_line(self, t):
        # 오른쪽 레일로 갈 때
        if self.dir[0] < 0:
            self.x, self.y = game_world.get_dots([self.x, self.y], server.player_rail.line['right'][1], t)
        else:
            self.x, self.y = game_world.get_dots([self.x, self.y], server.player_rail.line['left'][1], t)
