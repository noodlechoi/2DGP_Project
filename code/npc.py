import random

from pico2d import *
import game_framework
import game_world
from arrow import Arrow
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
import server

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 1.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10

class Dead:
    @staticmethod
    def enter(ball):
        global FRAMES_PER_ACTION
        global t
        t = 0
        game_world.remove_collision_object(ball)
        pass

    @staticmethod
    def exit(ball):
        ball.state_machine.cur_state = Standing
        ball.state_machine.start()
        game_world.add_collision_pair('ball:pin', ball, None)


        # 다음 캐릭터 순서로 넘어감
        server.round.turn -= 1
        if server.round.turn <= 0:
            server.round.turn_change()
        pass

    @staticmethod
    def do(ball):
        # rail 밖으로 나갔을 때
        if ball.x <= 0 - ball.size[0] // 2 + 10 or ball.x >= game_world.WIDTH + ball.size[0] // 2 or ball.y >= 530:
            ball.state_machine.cur_state.exit(ball)
            return

        global t
        ball.move_dead_line(t)
        t += game_framework.frame_time / 2

        # 크기가 원근감 있게 줄어듦
        ball.size[0] -= int(16 * RUN_SPEED_PPS * game_framework.frame_time)
        ball.size[1] -= int(16 * RUN_SPEED_PPS * game_framework.frame_time)

        ball.frame = (ball.frame + FRAMES_PER_ACTION * 4 * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

    @staticmethod
    def draw(ball):
        if ball.dir[0] <= 0:
            NPC.img.clip_draw(ball.location[0] + ball.real_size[0] * int(ball.frame) + ball.padding, ball.location[1],
                              ball.real_size[0], ball.real_size[1], ball.x, ball.y,
                              ball.size[0], ball.size[1])
        else:
            NPC.img.clip_composite_draw(ball.location[0] + ball.real_size[0] * int(ball.frame) + ball.padding,
                                        ball.location[1],
                                        ball.real_size[0], ball.real_size[1], 0, 'h', ball.x, ball.y,
                                        ball.size[0], ball.size[1])


class Throw:
    @staticmethod
    def enter(ball):
        global time
        ball.enter_init()
        time = 0

        pass

    @staticmethod
    def exit(ball):
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
        if server.npc_rail.dead_line(ball) or (ball.x <= 0 - ball.size[0] // 2 + 10 or ball.x >= game_world.WIDTH + ball.size[0] // 2 or ball.y >= 530):
            ball.state_machine.cur_state = Dead
            ball.state_machine.start()
            return

        ball.frame = (ball.frame + FRAMES_PER_ACTION * 4 * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

    @staticmethod
    def draw(ball):
        if ball.dir[0] <= 0:
            NPC.img.clip_draw(ball.location[0] + ball.real_size[0] * int(ball.frame) + ball.padding, ball.location[1],
                                ball.real_size[0], ball.real_size[1], ball.x, ball.y,
                                ball.size[0], ball.size[1])
        else:
            NPC.img.clip_composite_draw(ball.location[0] + ball.real_size[0] * int(ball.frame)+ ball.padding, ball.location[1],
                                          ball.real_size[0], ball.real_size[1], 0, 'h', ball.x, ball.y,
                                          ball.size[0], ball.size[1])


class Rolling:
    @staticmethod
    def enter(ball):
        ball.enter_init()

        ball.arrow = Arrow()
        game_world.add_object(ball.arrow, 1)
        pass

    @staticmethod
    def exit(ball):
        game_world.remove_object(ball.arrow)
        ball.dir = game_world.directtion([ball.x, ball.y], [ball.arrow.x, ball.arrow.y])
        ball.state_machine.cur_state = Throw
        ball.state_machine.start()
        pass

    @staticmethod
    def do(ball):
        global arrow


        ball.frame = (ball.frame + FRAMES_PER_ACTION * 3 * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        ball.frame_cal()

        ball.dir = game_world.directtion([ball.x, ball.y], [ball.arrow.x, ball.arrow.y])

    @staticmethod
    def draw(ball):
        if ball.dir[0] <= 0:
            NPC.img.clip_draw(ball.location[0] + ball.real_size[0] * int(ball.frame) + ball.padding, ball.location[1],
                                ball.real_size[0], ball.real_size[1], ball.x, ball.y,
                                ball.size[0], ball.size[1])
        else:
            NPC.img.clip_composite_draw(ball.location[0] + ball.real_size[0] * int(ball.frame)+ ball.padding, ball.location[1],
                                          ball.real_size[0], ball.real_size[1], 0, 'h', ball.x, ball.y,
                                          ball.size[0], ball.size[1])

class Run:
    @staticmethod
    def enter(ball):
        ball.enter_init()
        ball.frame = 0

        ball.arrow = Arrow()
        game_world.add_object(ball.arrow, 1)
        pass

    @staticmethod
    def exit(ball):
        # Run 상태에서 Thrown 상태가 될 수 있기 때문에
        game_world.remove_object(ball.arrow)
        ball.state_machine.cur_state = Rolling
        ball.state_machine.start()
        pass

    @staticmethod
    def do(ball):
        if ball.frame >= FRAMES_PER_ACTION - 1:
            ball.state_machine.cur_state.exit(ball)
            return

        ball.frame = (ball.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        ball.frame_cal()

        # 화살표에 따라 방향 설정
        ball.dir = game_world.directtion([ball.x, ball.y], [ball.arrow.x, ball.arrow.y])

        pass

    @staticmethod
    def draw(ball):

        if ball.dir[0] <= 0:
            NPC.img.clip_draw(ball.location[0] + ball.real_size[0] * int(ball.frame) + ball.padding, ball.location[1],
                                ball.real_size[0], ball.real_size[1], ball.x, ball.y,
                                ball.size[0], ball.size[1])
        else:
            NPC.img.clip_composite_draw(ball.location[0] + ball.real_size[0] * int(ball.frame) + ball.padding, ball.location[1],
                                          ball.real_size[0], ball.real_size[1], 0, 'h', ball.x, ball.y,
                                          ball.size[0], ball.size[1])


class Standing:
    @staticmethod
    def enter(ball):
        ball.x = 450
        ball.y = 100
        ball.wait_time = get_time()
        ball.enter_init()
        pass

    @staticmethod
    def exit(ball):
        ball.state_machine.cur_state = Run
        ball.state_machine.start()
        pass

    @staticmethod
    def do(ball):
        if (get_time() - ball.wait_time > 3):
            ball.state_machine.cur_state.exit(ball)

        ball.frame = (ball.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        # ball.frame = 9
        ball.frame_cal()
        pass

    @staticmethod
    def draw(ball):
        # print(ball.frame)
        NPC.img.clip_draw(ball.location[0] + ball.real_size[0] * int(ball.frame) + ball.padding, ball.location[1], ball.real_size[0], ball.real_size[1], ball.x, ball.y,
                            ball.size[0], ball.size[1])



class StateMachine:
    def __init__(self, npc):
        self.npc = npc
        self.cur_state = Standing

    def start(self):
        self.cur_state.enter(self.npc)

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
        self.padding = 0
        self.coin = 10
        self.layer = 6
        self.target_degree = 0
        self.state_machine = StateMachine(self)
        self.build_behavior_tree()


    def draw(self):
        if server.round.who_turn == 'npc':
            self.state_machine.draw()
            draw_rectangle(*self.get_bb())

    def update(self):
        if server.round.who_turn == 'npc':
            self.bt.run()
            self.state_machine.update()

    def get_bb(self):
        return self.x - self.size[0] // 2 + 10, self.y - self.size[1] // 2 + 10, self.x + self.size[
            0] // 2 - 10, self.y + self.size[1] // 2 - 10

    def handle_collision(self, group, other):
        if group == 'ball:pin':
            pass

    def move_dead_line(self, t):
        # 오른쪽 레일로 갈 때
        if self.dir[0] < 0:
            self.x, self.y = game_world.get_dots([self.x, self.y], server.npc_rail.line['right'][1], t)
        else:
            self.x, self.y = game_world.get_dots([self.x, self.y], server.npc_rail.line['left'][1], t)

    def is_my_turn(self):
        if server.round.who_turn == 'npc':
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL


    def is_remain_coin(self):
        if self.coin >= 10:
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL
        pass

    def use_skill(self):
        if self.state_machine.cur_state == Standing:
            self.coin -= 10
            # 스킬 사용

            self.wait_time = get_time()
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL
        pass

    def is_remained_turn(self):
        if server.round.turn >= 0:
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def set_range(self, s, e):
        if self.state_machine.cur_state == Standing:
            self.target_degree = random.randint(s, e)
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

        pass

    def throw(self):
        if self.state_machine.cur_state == Rolling:
            if int(self.arrow.degree) == self.target_degree:
                self.state_machine.cur_state.exit(self)
                return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL
        pass


class Knuckles(NPC):
    def __init__(self):
        super().__init__()

        if NPC.img == None:
            NPC.img = load_image('../resource/knuckles_sprite_sheet(2).png')

    def draw(self):
        super().draw()

    def update(self):
        super().update()

    def get_bb(self):
        return super().get_bb()

    def handle_collision(self, group, other):
        super().handle_collision(group, other)

    def enter_init(self):
        global FRAMES_PER_ACTION
        if self.state_machine.cur_state == Standing:
            FRAMES_PER_ACTION = 10
            self.size = [100, 150]
            self.frame = 0
            self.real_size = [32, 42]
            self.location = [0, 0]
            self.padding = 0
        elif self.state_machine.cur_state == Run:
            FRAMES_PER_ACTION = 14
            self.frame = 0
            self.real_size = [41, 40]
            self.location = [0, 44]
            self.padding = 0
        elif self.state_machine.cur_state == Rolling:
            FRAMES_PER_ACTION = 4
            self.frame = 0
            self.real_size = [32, 40]
            self.location = [5 + 32, 44 * 2]
            self.padding = 0
        elif self.state_machine.cur_state == Throw:
            FRAMES_PER_ACTION = 4
            self.frame = 0
            self.real_size = [32, 40]
            self.location = [5 + 32, 44 * 2]
            self.padding = 0

    def frame_cal(self):
        if self.state_machine.cur_state == Standing:
            match int(self.frame):
                case 0:
                    self.real_size = [32, 42]
                    self.padding = 0
                    self.size = [100, 150]
                case 2:
                    self.padding = -1
                case 3:
                    self.padding = -2
                case 4:
                    self.padding = -3
                case 5:
                    self.padding = -5
                case 6:
                    self.padding = -5
                case 7:
                    self.padding = -60
                    self.real_size[0] = 40
                    self.size[0] = 120
                case 8:
                    self.padding = -20
                    self.real_size[0] = 35
                case 9:
                    self.padding = -65
                    self.real_size[0] = 40
        elif self.state_machine.cur_state == Run:
            match int(self.frame):
                case 0:
                    self.real_size = [41, 40]
                    self.location = [0, 44]
                    self.padding = 0
                case 1:
                    self.real_size[0] = 33
                    self.padding = 8
                    pass
                case 2:
                    self.real_size[0] = 35
                    self.padding = 4
                case 3:
                    self.real_size[0] = 41
                    self.padding = -15
                case 4:
                    self.real_size[0] = 35
                    self.padding = 9
                case 7:
                    self.real_size[0] = 35
                    self.padding = 14
                case 10:
                    self.real_size[0] = 35
                    self.padding = 20
        elif self.state_machine.cur_state == Rolling:
            match int(self.frame):
                case 0:
                    self.padding = 0
                case 3:
                    self.padding = 3
        elif self.state_machine.cur_state == Throw:
            match int(self.frame):
                case 0:
                    self.padding = 0
                case 3:
                    self.padding = 3

    def build_behavior_tree(self):
        # 스킬 사용
        c1 = Condition('Did coin remain?', self.is_remain_coin)
        a1 = Action('use skill', self.use_skill)
        SEQ_SKILL = Sequence('use skill', c1, a1)

        # 발사
        c2 = Condition('Did turn remain?', self.is_remained_turn)
        a2 = Action('set range', self.set_range, 80, 90)
        a3 = Action('throw', self.throw)
        SEQ_THROW = Sequence('throw', c2, a2, a3)

        # 스킬/반사
        SEL_SKILL_THROW = Selector('skill or throw', SEQ_SKILL, SEQ_THROW)

        c3 = Condition('now my turn?', self.is_my_turn)
        root = Sequence('turn progress', c3, SEL_SKILL_THROW)

        self.bt = BehaviorTree(root)