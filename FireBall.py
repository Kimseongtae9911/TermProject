from pico2d import *

import collision
import game_framework
import game_world
import server

class FireBall:
    image = None

    def __init__(self, x, y, dir):
        if FireBall.image == None:
            FireBall.image = load_image('Resource\Fire_ball.png')
        self.x, self.y, self.dir = x, y, dir
        self.size = 32

    def draw(self):
        FireBall.image.clip_draw(0, 0, 16, 16, self.x, self.y, self.size, self.size)

    def update(self):
        self.x += self.dir * 700 * game_framework.frame_time

        if self.x < 25 or self.x > 1280 - 25:
            game_world.remove_object(self)

        if collision.collide(self, server.rocket):
            game_world.remove_object(self)
            game_world.remove_object(server.rocket)
        # elif collision.collide(self, server.goomba):
        #     game_world.remove_object(self)
        #     game_world.remove_object(server.goomba)

    def get_Check_Box(self):
        return self.x - self.size // 2, self.y - self.size // 2, self.x + (self.size // 2), self.y + self.size // 2

    def __getstate__(self):
        state = {'x': self.x, 'y': self.y, 'dir': self.dir}

        return state

    def __setstate__(self, state):
        self.__init__()
        self.__dict__.update(state)