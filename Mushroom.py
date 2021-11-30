from pico2d import *
import Character
import MakeMap

import game_world
import game_framework
import main_state
import collision
import server
import math

SCREENW = 1280

PIXEL_PER_METER = (15.0 / 0.3)
MOVE_SPEED_MPM = (6 * 1000.0 / 60.0)
MOVE_SPEED_MPS = (MOVE_SPEED_MPM / 60.0)
MOVE_SPEED = (MOVE_SPEED_MPS * PIXEL_PER_METER)

history = []

RIGHT, LEFT, IDLE = range(3)

event_name = ['RIGHT', 'LEFT', 'IDLE']

key_event_table = {
}

class IdleState:
    def enter(mushroom, event):
        pass

    def exit(mushroom, event):
        pass

    def do(mushroom):
        if mushroom.drawy < 16:
            mushroom.drawy += 16 * game_framework.frame_time
            mushroom.y += 25 * game_framework.frame_time
        else:
            mushroom.drawy = int(mushroom.drawy)
            mushroom.y = int(mushroom.y)
            mushroom.add_event(RIGHT)

        if mushroom.x < 25:
            game_world.remove_object(mushroom)

        mushroom.camerax = server.mario.get_MapX()

    def draw(mushroom):
        mushroom.mushroom.clip_draw(0, 16 - int(mushroom.drawy), 16, int(mushroom.drawy), mushroom.x - mushroom.camerax, mushroom.y,
                                    mushroom.sizex, mushroom.sizey - (16 - int(mushroom.drawy)) * 3)


class Move_RState:
    def enter(mushroom, event):
        pass

    def exit(mushroom, event):
        pass

    def do(mushroom):
        mushroom.camerax = server.mario.get_MapX()
        mushroom.x += MOVE_SPEED * game_framework.frame_time
        tempx, tempy = (mushroom.x - mushroom.camerax - 25) // 50, math.ceil((mushroom.y - 25) / 50)

        if MakeMap.Map.tile[int(tempx)][(tempy) - 1] == 0:
            mushroom.y -= (MOVE_SPEED + 100) * game_framework.frame_time

        if mushroom.x < 25:
            game_world.remove_object(mushroom)

    def draw(mushroom):
        mushroom.mushroom.clip_draw(0, 16 - int(mushroom.drawy), 16, int(mushroom.drawy), mushroom.x - mushroom.camerax, mushroom.y, mushroom.sizex, mushroom.sizey)


class Move_LState:
    def enter(mushroom, event):
        pass

    def exit(mushroom, event):
        pass

    def do(mushroom):
        mushroom.x -= MOVE_SPEED * game_framework.frame_time

        if mushroom.x < 25:
            game_world.remove_object(mushroom)

        mushroom.camerax = server.mario.get_MapX()

    def draw(mushroom):
        if mushroom.dir == 1:
            mushroom.mushroom.clip_draw(0, 16 - int(mushroom.drawy), 16, int(mushroom.drawy),
                                        mushroom.x - mushroom.camerax, mushroom.y,
                                        mushroom.sizex, mushroom.sizey)


next_state_table = {
    IdleState: {RIGHT: Move_RState, LEFT: Move_LState, IDLE: IdleState},

    Move_LState: {RIGHT: Move_RState, LEFT: Move_LState, IDLE: IdleState},

    Move_RState: {RIGHT: Move_RState, LEFT: Move_LState, IDLE: IdleState}
}

class Mushroom:
    image = None
    def __init__(self, x, y):
        if Mushroom.image == None:
            self.mushroom = load_image('Resource\Mushroom.png')
        self.camerax = server.mario.get_MapX()
        self.x, self.y = x + self.camerax, y
        self.drawy = 0
        self.sizex, self.sizey = 50, 50
        self.velocity = 300
        self.event_que = []
        self.cur_state = IdleState
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
            if server.mario.cur_life < 2:
                server.mario.cur_life += 1

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

    def get_Check_Box(self):
        return self.x - self.sizex // 2 - self.camerax, self.y - self.sizey // 2, self.x + (self.sizex // 2) - self.camerax, self.y + self.sizey // 2