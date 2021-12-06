from pico2d import *

import game_world
import server
import collision
import game_framework


class Flower:
    image = None
    def __init__(self, x, y):
        if Flower.image == None:
            Flower.image = load_image('Resource\Flower.png')
        self.camerax = server.mario.get_MapX()
        self.x, self.y = x + self.camerax, y
        self.flowersize = 50
        self.drawy = 0

    def draw(self):
        draw_rectangle(*self.get_Check_Box())
        Flower.image.clip_draw(0, 16 - int(self.drawy), 16, int(self.drawy), self.x - self.camerax, self.y, self.flowersize, self.flowersize - (16 - int(self.drawy)) * 3)

    def update(self):

        if self.drawy < 16:
            self.drawy += 16 * game_framework.frame_time
            self.y += 25 * game_framework.frame_time
        else:
            self.drawy = int(self.drawy)
            self.y = int(self.y)

        if collision.collide(server.mario, self):
            game_world.remove_object(self)
            server.mario.cur_life = 3

        self.camerax = server.mario.get_MapX()

    def get_Check_Box(self):
        return self.x - self.flowersize // 2 - self.camerax, self.y - self.flowersize // 2, self.x + (self.flowersize // 2) - self.camerax, self.y + self.flowersize // 2

    def __getstate__(self):
        state = {'x': self.x, 'y': self.y, 'camerax': self.camerax}
        return state

    def __setstate__(self, state):
        self.__init__()
        self.__dict__.update(state)