from pico2d import *
import game_world

# pin을 가려주기 위한 클래스
class RailBar():
    img = None
    bmg = None
    def __init__(self):
        if RailBar.img == None:
            RailBar.img = load_image('../resource/bowling_rail_bar.png')


    def draw(self):
        RailBar.img.draw(game_world.WIDTH // 4, game_world.HEIGHT - 100, game_world.WIDTH // 2, game_world.HEIGHT // 4)
        RailBar.img.clip_composite_draw(0, 0, 88, 50, 0, 'h', game_world.WIDTH // 4* 3, game_world.HEIGHT - 100, game_world.WIDTH // 2, game_world.HEIGHT // 4)

    def update(self):
        pass

class Rail():
    img = None
    def __init__(self):
        self.line = { 'back' : [[340, 530], [550, 530]], 'left' : [[0, 240], [350, 540]], 'right' : [[900, 240], [550, 540]]}
        if Rail.img == None:
            Rail.img = load_image('../resource/bowling_rail.png')

    def draw(self):
        # draw rail : WIDTH // 4 and HEIGHT // 2
        Rail.img.clip_draw(0, 0, 85, 208, game_world.WIDTH // 4, game_world.HEIGHT // 2, game_world.WIDTH // 2, game_world.HEIGHT)
        Rail.img.clip_composite_draw(0, 0, 85, 208, 0, 'h', game_world.WIDTH // 4 * 3, game_world.HEIGHT // 2, game_world.WIDTH // 2, game_world.HEIGHT)

    def update(self):
        pass

    def dead_line(self, ball):
        for where, loc in self.line.items():
            t = 0
            while t < 1.0:
                # 두 점의 점들을 구해서
                dx, dy = game_world.get_dots(loc[0], loc[1], t)
                # 그 점을 지나면 true
                if where == 'left':
                    if ball.x <= dx and ball.y >= dy:
                        return True
                else:
                    if ball.x >= dx and ball.y >= dy:
                        return True
                t += 0.1

        return False