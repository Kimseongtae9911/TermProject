from pico2d import *

mushsizex = mushsizey = 50


class Mushroom:
    image = None
    def __init__(self):
        if Mushroom.image == None:
            self.image = load_image('Resource\MushroomMonster.png')
        self.frame = 0
        self.x = 800; self.y = 125
    def draw_mush(self):
        self.image.clip_draw(self.frame * 17, 0, 17, 16, self.x, self.y, mushsizex, mushsizey)

    def move_mush(self):
        self.x += 5;
        self.frame = (self.frame + 1) % 2


