from pico2d import *
import MakeMap as mymap
import Character as Mario
import math

mariodir = 0
mariorun = False
mariojump = False
jumpcnt = 0
SCREENW = 1280; SCREENH = 800

def handle_events():
    global Play
    global mariodir
    global mariorun
    global mariojump
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            Play = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                Play = False
            elif event.key == SDLK_LEFT:
                mariodir = 2
            elif event.key == SDLK_RIGHT:
                mariodir = 1
            elif event.key == SDLK_DOWN:
                pass
            elif event.key == SDLK_UP:
                pass
            elif event.key == SDLK_SPACE:
                mariodir = 3
                pass
            elif event.key == SDLK_LSHIFT:
                mario.frame = 0
                mariorun = True
            elif event.key == SDLK_SPACE:
                mariojump = True
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_LEFT:
                mariodir = 0
            elif event.key == SDLK_RIGHT:
                mariodir = 0
            elif event.key == SDLK_LSHIFT:
                mariorun = False

def jump():
    global mariojump
    global mariodir
    global jumpcnt

    # 점프할때 마리오 시작위치를 넘겨주고 값이 변경되면 안됨
    x1, y1 = mario.x, mario.y
    x2, y2 = mario.x + 20, mario.y + 20
    x3, y3 = mario.x + 40, mario.y

    t = jumpcnt / 100
    mario.x = (2 * t ** 2 - 3 * t + 1) * x1 + (-4 * t ** 2 + 4 * t) * x2 + (2 * t ** 2 - t) * x3
    mario.y = (2 * t ** 2 - 3 * t + 1) * y1 + (-4 * t ** 2 + 4 * t) * y2 + (2 * t ** 2 - t) * y3

    if jumpcnt == 100:
        mariojump = False
        mariodir = 0
    else:
        jumpcnt += 1

open_canvas(SCREENW, SCREENH)

mario = Mario.Mario()
gamemap = mymap.Map()

Play = True

while Play:
    handle_events()

    clear_canvas()

    gamemap.draw(1)
    if mariodir == 1:
        if mariorun:
            mario.move_right()
            mario.move_right()
        else:
            mario.move_right()
        mario.right_move_draw()

    elif mariodir == 2:
        if mariorun:
            mario.move_left()
            mario.move_left()
        else:
            mario.move_left()
        mario.left_move_draw()

    elif mariodir == 3:
        jump()
        mario.jump_draw()

    else:
        mario.idle_draw()
    update_canvas()

    delay(0.1)
