from pico2d import *
import Character

import game_world
import game_framework

SCREENW = 1280

class Rocket:
    image = None
    def __init__(self, x = 1280, y = 100):
        if Rocket.image == None:
            self.rocket = load_image('Resource\RocketMonster.png')
        self.camerax = Character.get_Map()
        self.x, self.y = x + self.camerax, y
        self.rocketsizex, self.rocketsizey = 50, 30
        self.velocity = 300


    def draw(self):
        self.rocket.clip_draw(0, 0, 16, 16, self.x - self.camerax, self.y, self.rocketsizex, self.rocketsizey)
        draw_rectangle(*self.get_Check_Box())


    def update(self):
        self.x -= (self.velocity) * game_framework.frame_time
        if self.x < 25:
            game_world.remove_object(self)

        self.camerax = Character.get_Map()

    def get_Check_Box(self):
        return self.x - self.rocketsizex // 2, self.y - self.rocketsizey // 2, self.x + (self.rocketsizex // 2), self.y + self.rocketsizey // 2