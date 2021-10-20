from pico2d import *
SCREENW = 1280

startx = 0

class Mario:
    def __init__(self):
        self.image = load_image('Mario.png')
        self.frame = 1
        self.start = 0
        self.x = 300; self.y = 90
        self.startx = 0

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
        global startx
        if self.x >= SCREENW / 2:
            self.startx += 5
            startx = self.startx
        else:
            self.x += 5
        self.frame = (self.frame + 1) % 4

    def move_left(self):
        self.x -=5
        self.frame = (self.frame + 1) % 4

