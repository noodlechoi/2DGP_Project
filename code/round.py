import play_mode
import game_world
from pin import Pin
import server


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
        if round.who_turn == 'npc':
            server.npc.state_machine.start()
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
        self.who_turn = 'player'
        self.state_machine = StateMachine(self)
        self.state_machine.start()


    def update(self):
        self.state_machine.update()

    def turn_change(self):
        if self.who_turn == 'player':
            self.who_turn = 'npc'
        else:
            self.who_turn = 'player'

        self.change_pins()

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
                if Pin.__name__ == type(o).__name__:
                    is_exist_pin = True

        if not is_exist_pin:
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