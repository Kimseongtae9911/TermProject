from pico2d import *
import MakeMap as mymap
import Character as Mario
import math

mariodir = 0
mariorun = False
mariojump = False
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
                if mariojump:
                    mariodir = 3
                else:
                    mariodir = 2
            elif event.key == SDLK_RIGHT:
                if mariojump:
                    mariodir = 4
                else:
                    mariodir = 1
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
            elif event.key == SDLK_RIGHT:
                if not mariojump:
                    mariodir = 0
            elif event.key == SDLK_LSHIFT:
                mariorun = False


open_canvas(SCREENW, SCREENH)

mario = Mario.Mario()
gamemap = mymap.Map()

Play = True

while Play:
    handle_events()

    clear_canvas()

    gamemap.draw(1)
    if mariodir == 1:
        gamemap.Rightupdate(mario.map_pos())
        if mariorun:
            mario.move_right()
            mario.move_right()
        else:
            mario.move_right()
        mario.right_move_draw()

    elif mariodir == 2:
        gamemap.Leftupdate(mario.map_pos())
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
       mario.jump_draw()

    elif mariodir == 4:
        if not mario.jump_right():
            mariojump = False
            mariodir = 1
        mario.jump_draw()

    elif mariodir == 5:
        if not mario.idle_jump():
            mariojump = False
            mariodir = 0
        mario.jump_draw()

    else:
        mario.idle_draw()
    update_canvas()

    delay(0.1)
