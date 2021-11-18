from pico2d import *
import game_world
import game_framework
import loading_state
import main_state
from Rocket import Rocket

SCREENW = 1280
mapx = 0

PIXEL_PER_METER = (15.0 / 0.3)
RUN_SPEED_MPM = (25 * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED = (RUN_SPEED_MPS * PIXEL_PER_METER)
DASH_SPEED = RUN_SPEED + 100
JUMP_SPEED = RUN_SPEED + 10

TIMER_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIMER_PER_ACTION
FRAMES_PER_ACTION = 4

history = []

RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, \
    SHIFT_DOWN, SHIFT_UP, DEBUG_KEY, SPACE, STOP, FALL, DIE, COLLIDE = range(12)

event_name = ['RIGHT_DOWN', 'LEFT_DOWN', 'RIGHT_UP', 'LEFT_UP',
    'SHIFT_DOWN', 'SHIFT_UP', 'DEBUG_KEY', 'SPACE', 'STOP', 'FALL', 'DIE', 'COLLIDE']

key_event_table = {
    (SDL_KEYDOWN, SDLK_SPACE): SPACE,
    (SDL_KEYDOWN, SDLK_v): DEBUG_KEY,

    (SDL_KEYDOWN, SDLK_LSHIFT): SHIFT_DOWN,
    (SDL_KEYDOWN, SDLK_RSHIFT): SHIFT_DOWN,
    (SDL_KEYUP, SDLK_LSHIFT): SHIFT_UP,
    (SDL_KEYUP, SDLK_RSHIFT): SHIFT_UP,

    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP
}

class IdleState:
    def enter(mario, event):
        if event == RIGHT_DOWN:
            mario.velocity += RUN_SPEED
        elif event == LEFT_DOWN:
            mario.velocity -= RUN_SPEED
        elif event == RIGHT_UP:
            mario.velocity -= RUN_SPEED
        elif event == LEFT_UP:
            mario.velocity += RUN_SPEED
        mario.acc = 0

    def exit(mario, event):
        if event == SPACE:
            mario.jump = True
        pass

    def do(mario):
        pass


    def draw(mario):
        if mario.dir == 1:
            if mario.cur_life <= 1:
                mario.start = 0
                mario.image.clip_draw(mario.start, 34, 16, 16, mario.x, mario.y, mario.mariosizex, mario.mariosizey)
            elif mario.cur_life == 2:
                mario.start = 0
                mario.image.clip_draw(mario.start, 0, 16, 32, mario.x, mario.y + mario.mariosizex // 2, mario.mariosizex, mario.mariosizey)
        else:
            if mario.cur_life <= 1:
                mario.start = 0
                mario.l_image.clip_draw(mario.start, 34, 16, 16, mario.x, mario.y, mario.mariosizex, mario.mariosizey)
            elif mario.cur_life == 2:
                mario.start = 0
                mario.l_image.clip_draw(mario.start, 0, 16, 32, mario.x, mario.y + mario.mariosizex // 2, mario.mariosizex, mario.mariosizey)


class RunState:
    def enter(mario, event):
        if event == RIGHT_DOWN:
            mario.velocity += RUN_SPEED
        elif event == LEFT_DOWN:
            mario.velocity -= RUN_SPEED
        elif event == RIGHT_UP:
            mario.velocity -= RUN_SPEED
        elif event == LEFT_UP:
            mario.velocity += RUN_SPEED
        if event != STOP:
            mario.dir = clamp(-1, mario.velocity, 1)
        if mario.acc == 0 and event != SHIFT_UP:
            mario.acc = mario.velocity

    def exit(mario, event):
        if event == SPACE:
            mario.jump = True
        pass

    def do(mario):
        global mapx
        if mario.velocity == 0:
            mario.add_event(STOP)

        mario.frame = (mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        mario.x += (mario.velocity - mario.acc) * game_framework.frame_time

        if mario.dir == 1:
            if mario.acc > 0:
                mario.acc -= 200 * game_framework.frame_time
            elif mario.acc < 0:
                mario.acc = 0
        else:
            if mario.acc < 0:
                mario.acc += 200 * game_framework.frame_time
            elif mario.acc > 0:
                mario.acc = 0

        if mario.x > SCREENW - 300:
            mario.mapx += (mario.x - (SCREENW - 300))
        elif mario.x < 200 and mario.mapx > 0:
            mario.mapx -= 200 - mario.x

        if mario.mapx > 0:
            mario.x = clamp(200, mario.x, SCREENW - 300)
        else:
            mario.x = clamp(int(mario.mariosizex / 2), mario.x, SCREENW - 300)


    def draw(mario):
        if mario.dir == 1:
            if mario.cur_life <= 1:
                mario.start = 32
                mario.image.clip_draw(mario.start + (int(mario.frame)) * 15, 34, 16, 16, mario.x, mario.y, mario.mariosizex, mario.mariosizey)
            elif mario.cur_life == 2:
                mario.start = 21
                mario.image.clip_draw(mario.start + (int(mario.frame)) * 21, 0, 16, 32, mario.x, mario.y + mario.mariosizex // 2, mario.mariosizex, mario.mariosizey)
        else:
            if mario.cur_life <= 1:
                mario.start = 32
                mario.l_image.clip_draw(mario.start + (int(mario.frame)) * 15, 34, 16, 16, mario.x, mario.y, mario.mariosizex, mario.mariosizey)
            elif mario.cur_life == 2:
                mario.start = 21
                mario.l_image.clip_draw(mario.start + (int(mario.frame)) * 21, 0, 16, 32, mario.x, mario.y + mario.mariosizex // 2, mario.mariosizex, mario.mariosizey)


class DashState:
    def enter(mario, event):
        if event == RIGHT_DOWN:
            mario.velocity += DASH_SPEED
        elif event == LEFT_DOWN:
            mario.velocity -= DASH_SPEED
        elif event == RIGHT_UP:
            mario.velocity -= DASH_SPEED
        elif event == LEFT_UP:
            mario.velocity += DASH_SPEED
        elif event == SHIFT_DOWN:
            if mario.velocity > 0:
                mario.velocity = DASH_SPEED
                mario.acc = (DASH_SPEED - RUN_SPEED)
            else:
                mario.velocity = -DASH_SPEED
                mario.acc = -(DASH_SPEED - RUN_SPEED)
        mario.dir = clamp(-1, mario.velocity, 1)

    def exit(mario, event):
        if event == SHIFT_UP:
            if mario.velocity > 0:
                mario.velocity = RUN_SPEED
            else:
                mario.velocity = -RUN_SPEED
        elif event == SPACE:
            mario.jump = True
        pass

    def do(mario):
        mario.frame = (mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * (game_framework.frame_time * 2)) % 4
        mario.x += (mario.velocity - mario.acc) * (game_framework.frame_time)
        if mario.velocity > 0:
            if mario.acc > 0:
                mario.acc -= 200 * game_framework.frame_time
            else:
                mario.acc = 0
        elif mario.velocity < 0:
            if mario.acc < 0:
                mario.acc += 200 * game_framework.frame_time
            else:
                mario.acc = 0

        if mario.x > SCREENW - 300:
            mario.mapx += (mario.x - (SCREENW - 300))
        elif mario.x < 200 and mario.mapx > 0:
            mario.mapx -= 200 - mario.x

        if mario.mapx > 0:
            mario.x = clamp(200, mario.x, SCREENW - 300)
        else:
            mario.x = clamp(int(mario.mariosizex / 2), mario.x, SCREENW - 300)

    def draw(mario):
        if mario.dir == 1:
            if mario.cur_life <= 1:
                mario.start = 32
                mario.image.clip_draw(mario.start + (int(mario.frame)) * 15, 34, 16, 16, mario.x, mario.y, mario.mariosizex, mario.mariosizey)
            elif mario.cur_life == 2:
                mario.start = 21
                mario.image.clip_draw(mario.start + (int(mario.frame)) * 21, 0, 16, 32, mario.x, mario.y + mario.mariosizex // 2, mario.mariosizex, mario.mariosizey)
        else:
            if mario.cur_life <= 1:
                mario.start = 32
                mario.l_image.clip_draw(mario.start + (int(mario.frame)) * 15, 34, 16, 16, mario.x, mario.y, mario.mariosizex, mario.mariosizey)
            elif mario.cur_life == 2:
                mario.start = 21
                mario.l_image.clip_draw(mario.start + (int(mario.frame)) * 21, 0, 16, 32, mario.x, mario.y + mario.mariosizex // 2, mario.mariosizex, mario.mariosizey)


class AccState:
    def enter(mario, event):
        if mario.velocity > 0:
            if mario.acc > 0:
                mario.add_event(STOP)
        elif mario.velocity < 0:
            if mario.acc < 0:
                mario.add_event(STOP)
        pass

    def exit(mario, event):
        mario.velocity = 0
        pass

    def do(mario):
        mario.frame = 7

        mario.x += (mario.velocity - mario.acc) * game_framework.frame_time
        if mario.dir == 1:
            if mario.acc < mario.velocity + 100:
                mario.acc += 500 * game_framework.frame_time
            elif mario.acc > mario.velocity + 100:
                mario.acc = mario.velocity = 0
                mario.add_event(STOP)
        else:
            if mario.acc > mario.velocity - 100:
                mario.acc -= 500 * game_framework.frame_time
            elif mario.acc < mario.velocity - 100:
                mario.acc = mario.velocity = 0
                mario.add_event(STOP)

        if mario.x > SCREENW - 300:
            mario.mapx += (mario.x - (SCREENW - 300))
        elif mario.x < 200 and mario.mapx > 0:
            mario.mapx -= 200 - mario.x

        if mario.mapx > 0:
            mario.x = clamp(200, mario.x, SCREENW - 300)
        else:
            mario.x = clamp(int(mario.mariosizex / 2), mario.x, SCREENW - 300)

    def draw(mario):
        if mario.dir == 1:
            if mario.cur_life <= 1:
                mario.start = 16 * 6
                mario.image.clip_draw(mario.start, 34, 15, 16, mario.x, mario.y, mario.mariosizex, mario.mariosizey)
            elif mario.cur_life == 2:
                mario.start = 21 * 5
                mario.image.clip_draw(mario.start, 0, 16, 32, mario.x, mario.y + mario.mariosizex // 2, mario.mariosizex, mario.mariosizey)
        else:
            if mario.cur_life <= 1:
                mario.start = 16 * 6
                mario.l_image.clip_draw(mario.start, 34, 16, 16, mario.x, mario.y, mario.mariosizex, mario.mariosizey)
            elif mario.cur_life == 2:
                mario.start = 21 * 5
                mario.l_image.clip_draw(mario.start, 0, 16, 32, mario.x, mario.y + mario.mariosizex // 2, mario.mariosizex, mario.mariosizey)


class JumpState:
    def enter(mario, event):
        if event == RIGHT_DOWN:
            mario.velocity += RUN_SPEED
        elif event == LEFT_DOWN:
            mario.velocity -= RUN_SPEED
        elif event == RIGHT_UP:
            mario.velocity -= RUN_SPEED
            if mario.velocity == 100:
                mario.velocity = 0
        elif event == LEFT_UP:
            mario.velocity += RUN_SPEED
            if mario.velocity == -100:
                mario.velocity = 0
        elif event == COLLIDE:
            mario.jumpdir = -1
        mario.dir = clamp(-1, mario.velocity, 1)

    def exit(mario, event):
        pass

    def do(mario):
        if mario.jump:
            if mario.y > 400:
                mario.jumpdir = -1
            elif mario.y < 125:
                mario.jumpdir = 0
                mario.y = 125
                mario.jump = False
                mario.add_event(STOP)

            elif mario.y == 125:
                mario.jumpdir = 1

            if mario.jumpdir == 1:
                mario.y += (mario.jumpdir * JUMP_SPEED) * (game_framework.frame_time * 1.5)
                mario.x += (mario.velocity - mario.acc) * game_framework.frame_time
            elif mario.jumpdir == -1:
                mario.y += (mario.jumpdir * JUMP_SPEED) * (game_framework.frame_time * 2)
                mario.x += (mario.velocity - mario.acc) * game_framework.frame_time

            if mario.x > SCREENW - 300:
                mario.mapx += (mario.x - (SCREENW - 300))
            elif mario.x < 200 and mario.mapx > 0:
                mario.mapx -= 200 - mario.x

            if mario.mapx > 0:
                mario.x = clamp(200, mario.x, SCREENW - 300)
            else:
                mario.x = clamp(int(mario.mariosizex / 2), mario.x, SCREENW - 300)

    def draw(mario):
        if mario.dir == 1:
            if mario.cur_life <= 1:
                mario.start = 16 * 7
                mario.image.clip_draw(mario.start, 34, 16, 16, mario.x, mario.y, mario.mariosizex, mario.mariosizey)
            elif mario.cur_life == 2:
                mario.start = 21 * 6
                mario.image.clip_draw(mario.start, 0, 16, 32, mario.x, mario.y + mario.mariosizex // 2, mario.mariosizex, mario.mariosizey)
        else:
            if mario.cur_life <= 1:
                mario.start = 16 * 7
                mario.l_image.clip_draw(mario.start, 34, 16, 16, mario.x, mario.y, mario.mariosizex, mario.mariosizey)
            elif mario.cur_life == 2:
                mario.start = 21 * 6
                mario.l_image.clip_draw(mario.start, 0, 16, 32, mario.x, mario.y + mario.mariosizex // 2, mario.mariosizex, mario.mariosizey)


class FallState:
    def enter(mario, event):
        pass

    def exit(mario, event):
        pass

    def do(mario):
        mario.y -= JUMP_SPEED * (game_framework.frame_time * 1.5)
        if mario.y <= 50:
            mario.add_event(DIE)
        pass


    def draw(mario):
        if mario.dir == 1:
            if mario.cur_life <= 1:
                mario.start = 16 * 7
                mario.image.clip_draw(mario.start, 34, 16, 16, mario.x, mario.y, mario.mariosizex, mario.mariosizey)
            elif mario.cur_life == 2:
                mario.start = 21 * 6
                mario.image.clip_draw(mario.start, 0, 16, 32, mario.x, mario.y + mario.mariosizex // 2,
                                      mario.mariosizex, mario.mariosizey)
        else:
            if mario.cur_life <= 1:
                mario.start = 16 * 7
                mario.l_image.clip_draw(mario.start, 34, 16, 16, mario.x, mario.y, mario.mariosizex, mario.mariosizey)
            elif mario.cur_life == 2:
                mario.start = 21 * 6
                mario.l_image.clip_draw(mario.start, 0, 16, 32, mario.x, mario.y + mario.mariosizex // 2,
                                        mario.mariosizex, mario.mariosizey)

class DieState:
    def enter(mario, event):
        mario.dir == 1
        mario.cur_life = 0
        if mario.y >= 150:
            mario.dir = -1

    def exit(mario, event):
        pass

    def do(mario):
        if mario.dir == 1:
            mario.y += 100 * (game_framework.frame_time)
        elif mario.dir == -1:
            mario.y -= JUMP_SPEED * (game_framework.frame_time)

        if mario.y >= 150:
            mario.dir = -1
        elif mario.y <= -50:
            mario.life -= 1
            # game_framework.change_state(loading_state)
            game_framework.push_state(loading_state)

    def draw(mario):
        if mario.cur_life <= 1:
            mario.start = 16
            mario.image.clip_draw(mario.start, 34, 16, 16, mario.x, mario.y, mario.mariosizex, mario.mariosizey)


next_state_table = {
    DashState: {SHIFT_UP: RunState, SHIFT_DOWN: DashState, RIGHT_DOWN: DashState, LEFT_DOWN: DashState,
                LEFT_UP: AccState, RIGHT_UP: AccState, SPACE: JumpState, FALL: FallState, DIE: DieState, STOP: IdleState},

    IdleState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState,
                SHIFT_DOWN: IdleState, SHIFT_UP: IdleState, SPACE: JumpState, FALL: FallState, DIE: DieState, STOP: IdleState},

    RunState: {RIGHT_UP: AccState, LEFT_UP: AccState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,
               SHIFT_DOWN: DashState, SHIFT_UP: RunState, SPACE: JumpState, STOP: IdleState, FALL: FallState, DIE: DieState},

    AccState: {RIGHT_UP: AccState, LEFT_UP: AccState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState,
               SHIFT_DOWN: AccState, SHIFT_UP: AccState, STOP: IdleState, SPACE: AccState, FALL: FallState, DIE: DieState},

    JumpState: {RIGHT_UP: JumpState, LEFT_UP: JumpState, RIGHT_DOWN: JumpState, LEFT_DOWN: JumpState,
               SHIFT_DOWN: JumpState, SHIFT_UP: JumpState, STOP: RunState, SPACE: JumpState, FALL: FallState, DIE: DieState,
                COLLIDE: JumpState},

    FallState: {RIGHT_UP: FallState, LEFT_UP: FallState, RIGHT_DOWN: FallState, LEFT_DOWN: FallState,
                SHIFT_DOWN: FallState, SHIFT_UP: FallState, SPACE: FallState, FALL: FallState, DIE: DieState, STOP: FallState},

    DieState: {RIGHT_UP: DieState, LEFT_UP: DieState, RIGHT_DOWN: DieState, LEFT_DOWN: DieState,
                SHIFT_DOWN: DieState, SHIFT_UP: DieState, SPACE: DieState, FALL: DieState, DIE: DieState, STOP: DieState, COLLIDE: DieState}
}


class Mario:
    image = None
    life = 3
    cur_life = 1
    jumpdir = 1
    def __init__(self):
        if Mario.image == None:
            Mario.image = load_image('Resource\Mario.png')
            Mario.l_image = load_image('Resource\Mario_left.png')
        self.x, self.y = 300, 125
        self.frame = 0
        self.dir = 1
        self.velocity = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        self.acc = 0.0
        self.jump = False
        self.mapx = 0
        self.mariosizex = self.mariosizey = 55
        self.timer = 500

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        global mapx
        if self.cur_life <= 1:
            self.mariosizex = 55; self.mariosizey = 55;
        elif self.cur_life >= 2:
            self.mariosizex = 55; self.mariosizey = 110;

        self.timer -= 5
        mapx = self.mapx
        if self.timer <= 0:
            rocket = Rocket(SCREENW, self.y)
            game_world.add_object(rocket, 1)
            self.timer = 500

        if self.cur_life == 0:
            print(self.life)
            self.add_event(DIE)


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

        if (main_state.collide_base(self, main_state.mymap)):
            self.add_event(9)
        elif (main_state.collide_ques(self, main_state.mymap)):
            self.add_event(11)
        elif (main_state.collide_block(self, main_state.mymap)):
            self.add_event(11)

    def draw(self):
        self.cur_state.draw(self)
        # draw_rectangle(*self.get_Check_Box())
        # debug_print('Velocity : ' + str(self.velocity) + '  cur_life : ' + str(self.cur_life) + '  Dir: ' + str(self.dir))

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            if DEBUG_KEY == key_event:
                print(history[-10:])
            else:
                self.add_event(key_event)

    def get_marioPos(self):
        return self.x

    def get_MapX(self):
        return self.mapx

    def get_Check_Box(self):
        if self.cur_life <= 1:
            return self.x - self.mariosizex // 2, self.y - self.mariosizey // 2, self.x + (self.mariosizex // 2), self.y + self.mariosizey // 2
        else:
            return self.x - self.mariosizex // 2, self.y - self.mariosizey // 4, self.x + (self.mariosizex // 2), self.y + self.mariosizex * 2

def get_Map():
    return mapx