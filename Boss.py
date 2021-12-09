from pico2d import *
import time
import Character

import game_world
import server
import collision
import game_framework
import loading_state
import game_over_state
from Boss_Fire import FireB
SCREENW = 1280


PIXEL_PER_METER = (15.0 / 0.3)
RUN_SPEED_MPM = (25 * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED = (RUN_SPEED_MPS * PIXEL_PER_METER)
SPEED = RUN_SPEED - 300


TIMER_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIMER_PER_ACTION
FRAMES_PER_ACTION = 4

class Boss:
    image = None
    def __init__(self):
        if Boss.image == None:
            Boss.image = load_image('Resource\Boss.png')
        self.camerax = server.mario.get_MapX()
        self.x, self.y = 7150, 300
        self.size = 100
        self.life = 8
        self.frame = 0
        self.velocity = SPEED
        self.dir = -1
        self.timer = 300
        self.cleartimer = 50

    def draw(self):
        Boss.image.clip_draw(32 * int(self.frame), 0, 32, 32, self.x - self.camerax, self.y, self.size, self.size)
        # draw_rectangle(*self.get_Check_Box())


    def update(self):
        self.camerax = server.mario.get_MapX()
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        if self.dir == -1:
            self.x += int(self.velocity * game_framework.frame_time) * self.dir
        else:
            self.x += int(self.velocity * game_framework.frame_time) * self.dir

        if self.x < 7100:
            self.dir = 1
        elif self.x > 7200:
            self.dir = -1

        if self.life <= 0:
            self.camerax = 0
            server.clear = True
            server.mario.flag_sound.play()
            if self.cleartimer <= 0:
                game_world.remove_object(self)
                game_framework.change_state(game_over_state)

        if server.clear == True:
            self.cleartimer -= 1

        if server.mario.x + server.mario.mapx > 5000:
            self.timer -= 1

        if self.timer <= 0 and self.life > 0:
            self.fire_boss()
            self.timer = 300

        if collision.collide(server.mario, self):
            server.mario.cur_life = 0
            server.mario.life -= 1
            server.mario.sound_die()
            game_framework.change_state(loading_state)

    def get_Check_Box(self):
        return self.x - self.size // 2 - self.camerax, self.y - self.size // 2, self.x + (self.size // 2) - self.camerax, self.y + self.size // 2

    def __getstate__(self):
        state = {'x': self.x, 'y': self.y, 'camerax': self.camerax, 'life': self.life}
        return state

    def __setstate__(self, state):
        self.__init__()
        self.__dict__.update(state)

    def fire_boss(self):
        fire = FireB(self.x, self.y)
        game_world.add_object(fire, 1)