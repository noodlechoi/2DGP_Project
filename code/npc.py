from pico2d import *
import game_framework
import game_world
from arrow import Arrow
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 1.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10


class Rolling:
    @staticmethod
    def enter(ball):
        global arrow
        ball.enter_init()

        arrow = Arrow()
        game_world.add_object(arrow, 1)
        pass

    @staticmethod
    def exit(ball):
        global arrow

        game_world.remove_object(arrow)
        ball.dir = game_world.directtion([ball.x, ball.y], [arrow.x, arrow.y])
        pass

    @staticmethod
    def do(ball):
        ball.frame = (ball.frame + FRAMES_PER_ACTION * 3 * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        # ball.frame = 4
        ball.frame_cal()

        ball.dir = game_world.directtion([ball.x, ball.y], [arrow.x, arrow.y])

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
        global arrow
        ball.enter_init()
        ball.frame = 0

        arrow = Arrow()
        game_world.add_object(arrow, 1)
        pass

    @staticmethod
    def exit(ball):
        global arrow

        # Run 상태에서 Thrown 상태가 될 수 있기 때문에
        game_world.remove_object(arrow)
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
        ball.dir = game_world.directtion([ball.x, ball.y], [arrow.x, arrow.y])

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
        ball.enter_init()
        ball.wait_time = get_time()
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
            return

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
        self.transitions = {
        }

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
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.build_behavior_tree()


    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def update(self):
        self.state_machine.update()
        self.bt.run()

    def get_bb(self):
        return self.x - self.size[0] // 2 + 10, self.y - self.size[1] // 2 + 10, self.x + self.size[
            0] // 2 - 10, self.y + self.size[1] // 2 - 10

    def handle_collision(self, group, other):
        if group == 'ball:pin':
            pass


    def test(self):
        pass

    def build_behavior_tree(self):
        a1 = Action('test', self.test)
        root = Sequence('test', a1)
        self.bt = BehaviorTree(root)


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
            self.frame = 0
            self.real_size = [32, 40]
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

    pass

    def build_behavior_tree(self):
        super().build_behavior_tree()
