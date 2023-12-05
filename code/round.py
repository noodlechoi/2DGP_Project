import play_mode
import game_world
from pin import Pin
from pico2d import *
import game_framework
import server
from font import Font


PIXEL_PER_METER = (10.0 / 0.3)
DROP_SPEED_KMPH = 1.0
DROP_SPEED_MPM = DROP_SPEED_KMPH * 1000.0 / 60.0
DROP_SPEED_MPS = DROP_SPEED_MPM / 60.0
DROP_SPEED_PPS = DROP_SPEED_MPS * PIXEL_PER_METER

class Ready: # 핀이 내려오고 있는 단계
    @staticmethod
    def enter(round):

        pass

    @staticmethod
    def exit(round):
        round.state_machine.cur_state = Processing
        round.state_machine.start()
        pass

    @staticmethod
    def do(round):
        pass

    def draw(round):
        pass

class Processing:# 핀이 내려오고 난 후
    @staticmethod
    def enter(round):
        pass

    @staticmethod
    def exit(round):
        pass

    @staticmethod
    def do(round):
        round.reproduce_pins()
        pass

    def draw(round):
        pass

class TurnStart: # 한 턴이 시작될 때
    @staticmethod
    def enter(round):
        round.turn = 2
        round.reproduce_pins()
        round.state_machine.cur_state = Ready
        round.state_machine.start()
        pass

    @staticmethod
    def exit(round):
        pass

    @staticmethod
    def do(round):
        pass

    def draw(round):
        pass

class Next:
    @staticmethod
    def enter(round):
        global fonts

        round.cur_round += 1
        if(round.cur_round == 1):
            round.player_score = dict()
            round.npc_score = dict()
            round.is_last = False
        if(round.cur_round == 10):
            round.is_last = True
        round.score_x, round.score_y = game_world.WIDTH // 2, game_world.HEIGHT

        # font
        fonts = []
        player_first_score = [[35, 445], [60, 463], [95, 463]]
        next_round = 85
        # {0:{2:10, 1:10}}
        for r, s in round.player_score.items():
            for turn in s.keys():
                if round.is_last:
                    if turn == 3:
                        fonts.append(
                            Font(s[turn], player_first_score[0][0] + next_round * (r - 1), player_first_score[0][1],
                                 [27, 35]))
                    elif turn == 2:
                        fonts.append(
                            Font(s[turn], player_first_score[1][0] + next_round * (r - 1), player_first_score[1][1],
                                 [20, 30]))
                    else:
                        fonts.append(
                            Font(s[turn], player_first_score[2][0] + next_round * (r - 1), player_first_score[2][1],
                                 [20, 30]))
                else:
                    if turn == 2:
                        fonts.append(
                            Font(s[turn], player_first_score[0][0] + next_round * (r - 1), player_first_score[0][1],
                                 [27, 35]))
                    elif turn == 1:
                        fonts.append(
                            Font(s[turn], player_first_score[1][0] + next_round * (r - 1), player_first_score[1][1],
                                 [20, 30]))

        npc_first_score = [[35, 340], [60, 360]]
        for r, s in round.npc_score.items():
            for turn in s.keys():
                if round.is_last:
                    if turn == 3:
                        fonts.append(
                            Font(s[turn], npc_first_score[0][0] + next_round * (r - 1), npc_first_score[0][1], [27, 35]))
                    elif turn == 2:
                        fonts.append(
                            Font(s[turn], npc_first_score[1][0] + next_round * (r - 1), npc_first_score[1][1], [20, 30]))
                    else:
                        fonts.append(
                            Font(s[turn], npc_first_score[2][0] + next_round * (r - 1), npc_first_score[2][1], [20, 30]))
                else:
                    if turn == 2:
                        fonts.append(
                            Font(s[turn], npc_first_score[0][0] + next_round * (r - 1), npc_first_score[0][1], [27, 35]))
                    elif turn == 1:
                        fonts.append(
                            Font(s[turn], npc_first_score[1][0] + next_round * (r - 1), npc_first_score[1][1], [20, 30]))

        pass

    @staticmethod
    def exit(round):
        if round.is_last:
            round.last()
            return
        round.processing()

        pass

    @staticmethod
    def do(round):
        if round.score_y >= game_world.HEIGHT // 2:
            round.score_y -= DROP_SPEED_PPS * game_framework.frame_time * 20
            round.wait_time = get_time()

        if get_time() - round.wait_time > 2:
            round.state_machine.cur_state.exit(round)
        pass

    @staticmethod
    def draw(round):
        global fonts
        Round.score_img.clip_draw(5, 65, 410, 145, round.score_x, round.score_y, game_world.WIDTH - 20, game_world.HEIGHT // 3)

        if round.score_y <= game_world.HEIGHT // 2:
            for font in fonts:
                font.draw()
        pass


class Last:
    @staticmethod
    def enter(round):
        round.turn = 3
        round.reproduce_pins()
        round.processing()
        pass

    @staticmethod
    def exit(round):

        pass

    @staticmethod
    def do(round):
        pass

    def draw(round):
        pass

class StateMachine:
    def __init__(self, round):
        self.round = round
        self.cur_state = Next

    def start(self):
        self.cur_state.enter(self.round)

    def update(self):
        self.cur_state.do(self.round)

    def draw(self):
        self.cur_state.draw(self.round)


# 게임 라운드를 다루는 클래스, 다음 순서를 지정해줌
class Round:
    score_img = None
    def __init__(self):
        self.turn = 2
        self.cur_round = 0
        self.who_turn = 'player'
        self.score_x, self.score_y = game_world.WIDTH // 2, game_world.HEIGHT
        self.is_last = False
        self.player_score = dict()
        self.npc_score = dict()
        self.is_strike, self.is_spare = False, False
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        if Round.score_img == None:
            Round.score_img = load_image('../resource/Score_Sheet.png')


    def update(self):
        self.state_machine.update()

        # 마지막 차례에 스페어나 스트라이크가 아니면 기회 X
        if self.cur_round == 10:
            if self.turn == 1:
                if not self.is_all_thrown():
                    self.turn_change()

        if self.who_turn == 'player':
            score = self.player_score
        else:
            score = self.npc_score
        if self.cur_round in score.keys():
            if self.turn in score[self.cur_round].keys():
                # strike면 다음 턴
                if score[self.cur_round][self.turn] == 10:
                    self.is_strike = True
                    self.wait_time = get_time()
                    self.turn -= 1
                # spare
                elif self.turn < 2 or (self.is_last and self.turn < 3):
                    if score[self.cur_round][self.turn] + score[self.cur_round][self.turn + 1] == 10:
                        self.is_spare = True
                        self.wait_time = get_time()
                        self.turn -= 1




    def draw(self):
        self.state_machine.draw()

        if self.is_strike:
            img = load_image('../resource/bowling_sprite_sheet(1).png')
            # img.clip_draw(0, 0, 150, 50, 300, 300, 100, 100)
            img.clip_draw(0, 50, 150, 70, game_world.WIDTH // 2, game_world.HEIGHT // 2, 300, 200)
            if get_time() - self.wait_time > 1:
                self.is_strike = False

        if self.is_spare:
            img = load_image('../resource/bowling_sprite_sheet(1).png')
            img.clip_draw(0, 0, 150, 50, game_world.WIDTH // 2, game_world.HEIGHT // 2, 300, 200)
            if get_time() - self.wait_time > 1:
                self.is_spare = False




    def turn_change(self):
        if not self.is_last:
            self.state_machine.cur_state = TurnStart
        else:
            self.state_machine.cur_state = Last

        self.state_machine.start()
        self.change_pins()


        if self.who_turn == 'player':
            self.who_turn = 'npc'
        else:
            self.who_turn = 'player'
            self.next()


        pass

    def next(self):
        self.state_machine.cur_state = Next
        self.state_machine.start()
        pass


    def last(self):
        self.state_machine.cur_state = Last
        self.state_machine.start()
        pass

    def processing(self):
        self.state_machine.cur_state = Processing
        self.state_machine.start()

    def ready(self):
        self.state_machine.cur_state = Ready
        self.state_machine.start()

    def is_processing(self):
        if self.state_machine.cur_state == Processing:
            return True
        return False

    def is_all_thrown(self):
        global pins
        # pin이 다 쓰러지면 다시 생기기
        is_exist_pin = False
        for ol in game_world.objects:
            for o in ol:
                if Pin.__name__ == type(o).__name__:
                    is_exist_pin = True

        if not is_exist_pin:
            return True
        return False

    def reproduce_pins(self):
        if self.is_all_thrown():
            self.refill_pins()

    def change_pins(self):
        # 핀이 있는 모든 원소 지우기
        for ol in game_world.objects:
            for o in ol:
                if Pin.__name__ == type(o).__name__:
                    ol.clear()

        for pairs in game_world.collision_pairs.values():
            for o in pairs[0]:
                if Pin.__name__ in type(o).__name__:
                    pairs[0].clear()
            for o in pairs[1]:
                if Pin.__name__ in type(o).__name__:
                    pairs[1].clear()

        self.refill_pins()

    def refill_pins(self):
        pins = [Pin(play_mode.pin_list[i][0], play_mode.pin_list[i][1]) for i in range(10)]
        game_world.add_objects(pins, 1)
        for pin in pins:
            game_world.add_collision_pair('ball:pin', None, pin)

        self.ready()