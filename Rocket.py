from pico2d import *
import Character

import game_world
import server
import collision
import game_framework

SCREENW = 1280

class Rocket:
    image = None
    def __init__(self, x = 1280, y = 100):
        if Rocket.image == None:
            self.rocket = load_image('Resource\RocketMonster.png')
        self.camerax = server.mario.get_MapX()
        self.x, self.y = x + self.camerax, y
        self.rocketsizex, self.rocketsizey = 50, 30
        self.velocity = 200


    def draw(self):
        self.rocket.clip_draw(0, 0, 16, 16, self.x - self.camerax, self.y, self.rocketsizex, self.rocketsizey)
        draw_rectangle(*self.get_Check_Box())


    def update(self):
        self.x -= (self.velocity) * game_framework.frame_time
        if self.x < 25:
            game_world.remove_object(self)

        if collision.collide(server.mario, self):
            game_world.remove_object(self)
            if server.mario.cur_life >= 2:
                server.mario.cur_life -= 1
            elif server.mario.cur_life == 1:
                server.mario.cur_life -= 1
                server.mario.add_event(10)
        self.camerax = server.mario.get_MapX()

    def get_Check_Box(self):
        return self.x - self.rocketsizex // 2 - self.camerax, self.y - self.rocketsizey // 2, self.x + (self.rocketsizex // 2) - self.camerax, self.y + self.rocketsizey // 2

    def __getstate__(self):
        state = {'x': self.x, 'y': self.y, 'camerax': self.camerax}
        return state

    def __setstate__(self, state):
        self.__init__()
        self.__dict__.update(state)