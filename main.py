from pico2d import *
import MakeMap as mymap
import Character as Mario
import Monster
import Camera
import time

import math

mariodir = 0
mariorun = False
mariojump = False
idledir = 0
SCREENW = 1280; SCREENH = 800
begin = time.time()
def handle_events():
    global Play
    global mariodir
    global mariorun
    global mariojump
    global idledir
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            Play = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                Play = False
            elif event.key == SDLK_LEFT:
                if mariojump:
                    mariodir = 3
                    idledir = 1
                else:
                    mariodir = 2
                    idledir = 1
            elif event.key == SDLK_RIGHT:
                if mariojump:
                    mariodir = 4
                    idledir = 0
                else:
                    mariodir = 1
                    idledir = 0
            elif event.key == SDLK_DOWN:
                pass
            elif event.key == SDLK_UP:
                pass
            elif event.key == SDLK_SPACE:
                if mariodir == 2:
                    mariodir = 3
                    mariojump = True
                elif mariodir == 1:
                    mariodir = 4
                    mariojump = True
                else:
                    mariodir = 5
                    mariojump = True
                pass
            elif event.key == SDLK_LSHIFT:
                mario.frame = 0
                mariorun = True
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_LEFT:
                if not mariojump:
                    mariodir = 0
                    idledir = 1
            elif event.key == SDLK_RIGHT:
                if not mariojump:
                    mariodir = 0
                    idledir = 0
            elif event.key == SDLK_LSHIFT:
                mariorun = False

open_canvas(SCREENW, SCREENH)

mario = Mario.Mario()
gamemap = mymap.Map()
mush = Monster.Mushroom()
rockets = [Monster.Rocket() for i in range(5)]

Play = True

while Play:
    handle_events()

    result = round(time.time() - begin)
    if result % 5 == 0:
        for rocket in rockets:
            x, y = mario.get_marioPos()
            gen = rocket.generate_rocket(x, y)
            if gen: break

    clear_canvas()

    mariox, marioy = mario.get_marioPos()
    gamemap.get_camera(mariox, mario.map_pos())

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
       if not mario.jump_left():
           mariojump = False
           mariodir = 2
       mario.Ljump_draw()

    elif mariodir == 4:
        if not mario.jump_right():
            mariojump = False
            mariodir = 1
        mario.Rjump_draw()

    elif mariodir == 5:
        if not mario.idle_jump():
            mariojump = False
            mariodir = 0

        else:
            if idledir == 0:
                mario.Rjump_draw()
            else:
                mario.Ljump_draw()

    else:
        if idledir == 0:
            mario.Ridle_draw()
        else:
            mario.Lidle_draw()

    mush.move_mush()
    for roc in rockets:
        roc.move_rocket()

    mush.draw_mush()
    for roc in rockets:
        roc.draw_rocket()
    update_canvas()

    delay(0.1)
