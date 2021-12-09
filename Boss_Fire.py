from pico2d import *

import collision
import game_framework
import game_world
import server

class FireB:
    image = None

    def __init__(self, x, y):
        if FireB.image == None:
            FireB.image = load_image('Resource\Boss_fire.png')
        self.x, self.y = x, y
        self.sizex = 75
        self.sizey = 25
        self.camerax = server.mario.get_MapX()

    def draw(self):
        FireB.image.clip_draw(0, 0, 24, 8, self.x - self.camerax, self.y, self.sizex, self.sizey)
        # draw_rectangle(*self.get_Check_Box())

    def update(self):
        self.camerax = server.mario.get_MapX()
        self.x -= 200 * game_framework.frame_time

        if self.y > server.mario.y:
            self.y -= 100 * game_framework.frame_time
        elif self.y < server.mario.y:
            self.y += 100 * game_framework.frame_time
        elif self.y == server.mario.y:
            self.y = server.mario.y

        if self.x < 25:
            game_world.remove_object(self)

        if collision.collide(server.mario, self):
            if server.mario.cur_life == 3:
                server.mario.sound_die()
            server.mario.cur_life = 1
            server.mario.life -= 1
            server.mario.add_event(10)



    def get_Check_Box(self):
        return self.x - self.camerax - self.sizex // 2, self.y - self.sizey // 2, self.x - self.camerax + (self.sizex // 2), self.y + self.sizey // 2

    def __getstate__(self):
        state = {'x': self.x, 'y': self.y}

        return state

    def __setstate__(self, state):
        self.__init__()
        self.__dict__.update(state)