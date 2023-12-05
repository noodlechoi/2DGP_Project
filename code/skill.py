from pico2d import *
import server

def a_down(e, ball):
    if ball.coin < 5:
        return False
    else:
        ball.coin -= 5
        return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a

def s_down(e, ball):
    if ball.coin < 10:
        return False
    else:
        ball.coin -= 10
        return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s

def d_down(e, ball):
    if ball.coin < 20:
        return False
    else:
        ball.coin -= 20
        return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s


def dead_ball(e, ball):
    return e[0] == 'Dead'

class Upsize:
    @staticmethod
    def enter(ball, e):
        ball.size = [200, 200]
        pass

    @staticmethod
    def exit(ball, e):
        ball.size = [100, 150]
        pass

    @staticmethod
    def do(ball):
        if server.is_dead:
            ball.skill.handle_event( ('Dead', 0))

        pass

    @staticmethod
    def draw(ball):
        pass

class No_skill:
    @staticmethod
    def enter(ball, e):
        pass

    @staticmethod
    def exit(ball, e):
        pass

    @staticmethod
    def do(ball):
        pass

    @staticmethod
    def draw(ball):
        pass

class Skill():
    def __init__(self, ball):
        self.ball = ball
        self.cur_skill = No_skill
        self.transitions = {
            No_skill: {a_down:Upsize},
            Upsize: {dead_ball:No_skill}
        }


    def start(self):
        self.cur_skill.enter(self.ball, ('NONE', 0))

    def update(self):
        self.cur_skill.do(self.ball)

    def handle_event(self, e):
        for check_event, next_skill in self.transitions[self.cur_skill].items():
            if check_event(e, self.ball):
                self.cur_skill.exit(self.ball, e)
                self.cur_skill = next_skill
                self.cur_skill.enter(self.ball, e)
                return True

        return False

    def draw(self):
        self.cur_skill.draw(self.ball)
