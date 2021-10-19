from pico2d import *

mushsizex = mushsizey = 50
rocketsizex = 50; rocketsizey = 30
class Mushroom:
    def __init__(self):
        self.image = load_image('MushroomMonster.png')
        self.frame = 0
        self.x = 800; self.y = 125
    def draw_mush(self):
        self.image.clip_draw(self.frame * 17, 0, 17, 16, self.x, self.y, mushsizex, mushsizey)

    def move_mush(self):
        self.x += 5;
        self.frame = (self.frame + 1) % 2

class Rocket:
    def __init__(self):
        self.rocket = load_image('RocketMonster.png')
        self.frame = 0
        self.x = 0;
        self.y = 0

    def draw_rocket(self):
        if self.y != 0:
            self.rocket.clip_draw(0, 0, 16, 16, self.x, self.y, rocketsizex, rocketsizey)
        else:
            return

    def generate_rocket(self, x, y):
        if self.y == 0:
            self.y = y
            self.x = x + round(1280 * 237 / 800)
            return True

    def move_rocket(self):
        if self.y != 0:
            self.x -= 10
        if self.x <= 0:
            self.x = self.y = 0