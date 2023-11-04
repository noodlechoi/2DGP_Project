from pico2d import load_image, clear_canvas, update_canvas, get_events, get_time
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT

import game_framework
import play_mode
from rail import Rail
from game_world import WIDTH, HEIGHT, isConflict

PIXEL_PER_METER = (10.0 / 0.3)
MOVE_SPEED_KMPH = 20.0
MOVE_SPEED_MPM = MOVE_SPEED_KMPH * 1000.0 / 60.0
MOVE_SPEED_MPS = MOVE_SPEED_MPM / 60.0
MOVE_SPEED_PPS = MOVE_SPEED_MPS * PIXEL_PER_METER

# 시간 당 프레임
TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5

FRAMES_PER_TIME = ACTION_PER_TIME * FRAMES_PER_ACTION

# 소닉 로고, 제목, 소닉 애니메이션, start_exit
location = [[225, 80], [470, 260], [450, 468], [460, 205]]

def init():
    global sonic_img, title_img, text_img
    global running
    global rail
    global x, y, padding
    global frame

    # 타이틀 소닉의 애니메이션을 위한 x축 패딩값
    padding = 0
    # 이미지에서의 소닉 값
    x = 95
    y = 130
    frame = 0

    rail = Rail()
    running = True
    # 소닉 이미지
    sonic_img = load_image('../resource/title_sonic(1).png')

    title_img = load_image('../resource/title_name.png')
    text_img = load_image('../resource/start_exit(1).png')


def finish():
    global sonic_img, rail
    del sonic_img
    del rail
    # del location

def update():
    pass

def draw():
    global x, y, padding, frame
    clear_canvas()

    # sonic
    # animation : 5
    # size = 95, 130
    # 프레임 크기 업데이트
    if frame >= 2.0:
        padding = -15
        x = 110
    else:
        padding = 0
        x = 95

    rail.draw()
    # title
    # width : 260, height : 155
    sonic_img.clip_draw(location[0][0], location[0][1], 260, 155, WIDTH // 2, HEIGHT // 3 * 2, WIDTH // 2, HEIGHT // 2)
    title_img.draw(location[2][0], location[2][1], 250, 80)

    # index 2~ : start : 675, x = 110
    # 프레임 = 한 액션 당 프레임 수 * 시간 당 액션 수 * 프레임 시간
    frame = (frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
    sonic_img.clip_draw(location[1][0] + (int(frame) * x) + padding, location[1][1], x, y, WIDTH // 2, HEIGHT // 4 * 3)

    text_img.draw(location[3][0], location[3][1], 300, 200)
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            # exit를 누르면 종료
            if isConflict([location[3][0], location[3][1] - 50], [200, 100], [event.x, HEIGHT - event.y]):
                game_framework.quit()
            # print(event.x, HEIGHT - event.y)
    pass