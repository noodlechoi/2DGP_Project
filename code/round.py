from pico2d import *

# 게임 라운드를 다루는 클래스, 다음 순서를 지정해줌
class Round:
    @staticmethod
    def start(round):
        round = 0
        print(round)
        pass
    @staticmethod
    def turn_change(round):
        pass

    @staticmethod
    def next(round):
        round += 1
        print(round)
        pass


    @staticmethod
    def last(round):
        print(round)
        pass