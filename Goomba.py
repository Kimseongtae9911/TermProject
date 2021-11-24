from pico2d import *
import Character
import MakeMap

import game_world
import game_framework
import server
import collision
import math

SCREENW = 1280

PIXEL_PER_METER = (15.0 / 0.3)
MOVE_SPEED_MPM = (6 * 1000.0 / 60.0)
MOVE_SPEED_MPS = (MOVE_SPEED_MPM / 60.0)
MOVE_SPEED = (MOVE_SPEED_MPS * PIXEL_PER_METER)

TIMER_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIMER_PER_ACTION
FRAMES_PER_ACTION = 2

history = []

RIGHT, LEFT = range(2)

event_name = ['RIGHT', 'LEFT']

key_event_table = {
}


class Move_RState:
    def enter(Goomba, event):
        pass

    def exit(Goomba, event):
        pass

    def do(Goomba):
        Goomba.camerax = Character.get_Map()
        Goomba.x += MOVE_SPEED * game_framework.frame_time
        Goomba.frame = (Goomba.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        tempx, tempy = (Goomba.x - Goomba.camerax - 25) // 50, math.ceil((Goomba.y - 25) / 50)

        if MakeMap.Map.tile1[int(tempx)][(tempy) - 1] == 0:
            Goomba.y -= (MOVE_SPEED + 100) * game_framework.frame_time

        if Goomba.x < 25:
            game_world.remove_object(Goomba)

    def draw(Goomba):
        Goomba.image.clip_draw(int(Goomba.frame) * 16, 0, 16, 16, Goomba.x - Goomba.camerax, Goomba.y, Goomba.sizex, Goomba.sizey)


class Move_LState:
    def enter(Goomba, event):
        pass

    def exit(Goomba, event):
        pass

    def do(Goomba):
        Goomba.x -= MOVE_SPEED * game_framework.frame_time
        Goomba.frame = (Goomba.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2

        if Goomba.x < 25:
            game_world.remove_object(Goomba)

        Goomba.camerax = Character.get_Map()

    def draw(Goomba):
        if Goomba.dir == 1:
            Goomba.image.clip_draw(int(Goomba.frame) * 16, 0, 16, 16, Goomba.x - Goomba.camerax, Goomba.y,  Goomba.sizex, Goomba.sizey)


next_state_table = {
    Move_LState: {RIGHT: Move_RState, LEFT: Move_LState},

    Move_RState: {RIGHT: Move_RState, LEFT: Move_LState}
}

class Goomba:
    image = None
    def __init__(self, x, y):
        if Goomba.image == None:
            self.image = load_image('Resource\MushroomMonster.png')
        self.camerax = Character.get_Map()
        self.x, self.y = x + self.camerax, y
        self.frame = 0
        self.sizex, self.sizey = 50, 50
        self.velocity = 300
        self.event_que = []
        self.cur_state = Move_RState
        self.cur_state.enter(self, None)

    def draw(self):
        self.cur_state.draw(self)
        draw_rectangle(*self.get_Check_Box())

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            try:
                history.append((self.cur_state.__name__, event_name[event]))
                self.cur_state = next_state_table[self.cur_state][event]
            except:
                print('State: ', self.cur_state.__name__ + 'Event: ', event_name[event])
                exit(-1)

            self.cur_state.enter(self, event)

        if collision.collide(server.mario, self):
            game_world.remove_object(self)
            if server.mario.cur_life >= 2:
                server.mario.cur_life -= 1
            elif server.mario.cur_life <= 1:
                server.mario.cur_life -= 1
                server.mario.add_event(10)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

    def get_Check_Box(self):
        return self.x - self.sizex // 2 - self.camerax, self.y - self.sizey // 2, self.x + (self.sizex // 2) - self.camerax, self.y + self.sizey // 2