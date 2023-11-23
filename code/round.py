from pico2d import *
import play_mode
import game_world
from pin import Pin



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

class TurnStart: # 한 턴이 시작될 때
    @staticmethod
    def enter(round):
        round.turn = 2
        round.state_machine.cur_state = Ready
        round.state_machine.start()
        pass

    @staticmethod
    def exit(round):

        pass

    @staticmethod
    def do(round):
        pass

class StateMachine:
    def __init__(self, round):
        self.round = round
        self.cur_state = TurnStart

    def start(self):
        self.cur_state.enter(self.round)

    def update(self):
        self.cur_state.do(self.round)


# 게임 라운드를 다루는 클래스, 다음 순서를 지정해줌
class Round:
    def __init__(self):
        self.turn = 2
        self.cur_round = 0
        self.state_machine = StateMachine(self)
        self.state_machine.start()


    def update(self):
        self.state_machine.update()

    def turn_change(self):
        print('다른 사람')
        self.state_machine.cur_state = TurnStart
        self.state_machine.start()
        pass

    def next(self):
        pass


    def last(self):
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

    def reproduce_pins(self):
        global pins
        # pin이 다 쓰러지면 다시 생기기
        is_exist_pin = False
        for ol in game_world.objects:
            for o in ol:
                if type(Pin()) == type(o):
                    is_exist_pin = True

        if not is_exist_pin:
            pins = [Pin(play_mode.pin_list[i][0], play_mode.pin_list[i][1]) for i in range(10)]
            game_world.add_objects(pins, 1)
            for pin in pins:
                game_world.add_collision_pair('ball:pin', None, pin)

            self.ready()

