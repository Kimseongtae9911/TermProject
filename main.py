from pico2d import *
import math

mariodir = 0
mariorun = False
mariojump = False

class Mario:
    def __init__(self):
        self.image = load_image('Mario.png')
        self.frame = 1
        self.start = 0
        self.x = 300; self.y = 90

    def right_move_draw(self):
        self.start = 32
        self.image.clip_draw(self.start + self.frame * 15, 34, 16, 16, self.x, self.y, 48, 48)

    def left_move_draw(self):
        self.start = 32
        self.image.clip_draw(self.start + self.frame * 15, 34, 16, 16, self.x, self.y, 48, 48)

    def idle_draw(self):
        self.start = 0
        self.image.clip_draw(self.start, 34, 16, 16, self.x, self.y, 48, 48)

    def jump_draw(self):
        self.start = 16 * 7
        self.image.clip_draw(self.start, 34, 16, 16, self.x, self.y, 48, 48)

    def move_right(self):
        self.x += 5
        self.frame = (self.frame + 1) % 4
    def move_left(self):
        self.x -=5
        self.frame = (self.frame + 1) % 4

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

    x1, y1 = mario.x, mario.y
    x2, y2 = mario.x + 20, mario.y + 20
    x3, y3 = mario.x + 40, mario.y

    for i in range(0, 100 + 1, 4):
        t = i / 100
        mario.x = (2 * t ** 2 - 3 * t + 1) * x1 + (-4 * t ** 2 + 4 * t) * x2 + (2 * t ** 2 - t) * x3
        mario.y = (2 * t ** 2 - 3 * t + 1) * y1 + (-4 * t ** 2 + 4 * t) * y2 + (2 * t ** 2 - t) * y3
    mariojump = False
    mariodir = 0

open_canvas()

mario = Mario()

Play = True

while Play:
    handle_events()

    clear_canvas()
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
