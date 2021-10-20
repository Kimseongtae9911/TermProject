from pico2d import *
SCREENW = 1280
mariosizex = 55
mariosizey = 55
startx = 0

class Mario:
    def __init__(self):
        self.image = load_image('Mario.png')
        self.frame = 1
        self.start = 0
        self.x = 300; self.y = 125
        self.startx = 0
        self.marioRight = True
        self.marioLeft = True
        self.jumpdir = False; self.jumpstart = 0; self.jumping = False
    def right_move_draw(self):
        self.start = 32
        self.image.clip_draw(self.start + self.frame * 15, 34, 16, 16, self.x, self.y, mariosizex, mariosizey)

    def left_move_draw(self):
        self.start = 32
        self.image.clip_draw(self.start + self.frame * 15, 34, 16, 16, self.x, self.y, mariosizex, mariosizey)

    def idle_draw(self):
        self.start = 0
        self.image.clip_draw(self.start, 34, 16, 16, self.x, self.y, mariosizex, mariosizey)

    def jump_draw(self):
        self.start = 16 * 7
        self.image.clip_draw(self.start, 34, 16, 16, self.x, self.y, mariosizex, mariosizey)

    def move_right(self):
        global startx
        if self.x >= SCREENW / 2:
            self.marioRight = False
        else:
            self.marioRight = True
        if self.marioRight:
            self.x += 10
        else:
            self.startx += 10
            startx = self.startx

        self.frame = (self.frame + 1) % 4

    def move_left(self):
        global startx
        if startx != 0:
            self.marioLeft = False
        else:
            self.marioLeft = True
            startx = 0

        if self.marioLeft:
            self.x -= 10
        else:
            self.startx -= 10
            startx = self.startx

        self.frame = (self.frame + 1) % 4

    def jump_left(self):
        if self.jumping == False and self.jumpstart == 0:
            self.jumpstart = self.y
            self.jumpdir = True
            self.jumping = True
        else:
            if self.jumping:
                if self.jumpdir:
                    self.y += 25
                    self.x -= 10
                    if self.y - self.jumpstart >= 105:
                        self.jumpdir = False
                else:
                    self.y -= 25
                    self.x -= 10
                    if self.y <= self.jumpstart:
                        self.y = self.jumpstart
                        self.jumpstart = 0
                        self.jumping = False
        return self.jumping

    def jump_right(self):
        if self.jumping == False and self.jumpstart == 0:
            self.jumpstart = self.y
            self.jumpdir = True
            self.jumping = True
        else:
            if self.jumping:
                if self.jumpdir:
                    self.y += 25
                    self.x += 10
                    if self.y - self.jumpstart >= 105:
                        self.jumpdir = False
                else:
                    self.y -= 25
                    self.x += 10
                    if self.y <= self.jumpstart:
                        self.y = self.jumpstart
                        self.jumpstart = 0
                        self.jumping = False
        return self.jumping

    def idle_jump(self):
        if self.jumpstart == 0 and self.jumping == False:
            self.jumpstart = self.y
            self.jumpdir = True
            self.jumping = True
        if self.jumping:
            if self.jumpdir:
                self.y += 25
                if self.y - self.jumpstart >= 105:
                    self.jumpdir = False
            else:
                self.y -= 25
                if self.y <= self.jumpstart:
                    self.y = self.jumpstart
                    self.jumpstart = 0
                    self.jumping = False
        return self.jumping
    def map_pos(self):
        return startx

    def get_marioPos(self):
        return self.x, self.y