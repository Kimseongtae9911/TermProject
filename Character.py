from pico2d import *
import game_world
import game_framework

SCREENW = 1280
mariosizex = 55
mariosizey = 55
startx = 0

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_MPM = (20 * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED = (RUN_SPEED_MPS * PIXEL_PER_METER)
DASH_SPEED = RUN_SPEED + 50
JUMP_SPEED = RUN_SPEED + 10

TIMER_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIMER_PER_ACTION
FRAMES_PER_ACTION = 4

history = []

RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, \
    SHIFT_DOWN, SHIFT_UP, DEBUG_KEY, SPACE, STOP = range(9)

event_name = ['RIGHT_DOWN', 'LEFT_DOWN', 'RIGHT_UP', 'LEFT_UP',
    'SHIFT_DOWN', 'SHIFT_UP', 'DEBUG_KEY', 'SPACE', 'STOP']

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
        if mario.jump:
            if mario.y > 200:
                mario.jumpdir = -1
            elif mario.y <= 50:
                mario.jumpdir = 0
                mario.y = 50

            mario.y += (mario.jumpdir * JUMP_SPEED) * game_framework.frame_time


    def draw(mario):
        if mario.dir == 1:
            if mario.jump:
                mario.start = 16 * 7
                mario.image.clip_draw(mario.start, 34, 16, 16, mario.x, mario.y, mariosizex, mariosizey)
            else:
                mario.start = 0
                mario.image.clip_draw(mario.start, 34, 16, 16, mario.x, mario.y, mariosizex, mariosizey)
        else:
            if mario.jump:
                mario.start = 16 * 7
                mario.l_image.clip_draw(mario.start, 0, 16, 16, mario.x, mario.y, mariosizex, mariosizey)
            else:
                mario.start = 0
                mario.l_image.clip_draw(mario.start, 34, 16, 16, mario.x, mario.y, mariosizex, mariosizey)


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
        mario.dir = clamp(-1, mario.velocity, 1)
        if mario.acc == 0 and event != SHIFT_UP:
            mario.acc = mario.velocity

    def exit(mario, event):
        if event == SPACE:
            mario.jump = True
        pass

    def do(mario):
        mario.frame = (mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        mario.x += (mario.velocity - mario.acc) * game_framework.frame_time
        if mario.dir == 1:
            if mario.acc > 0:
                mario.acc -= 500 * game_framework.frame_time
            elif mario.acc < 0:
                mario.acc = 0
        else:
            if mario.acc < 0:
                mario.acc += 500 * game_framework.frame_time
            elif mario.acc > 0:
                mario.acc = 0
        mario.x = clamp(25, mario.x, 1600 - 25)

    def draw(mario):
        if mario.dir == 1:
            mario.start = 32
            mario.image.clip_draw(mario.start + (int(mario.frame)) * 15, 34, 16, 16, mario.x, mario.y, mariosizex, mariosizey)
        else:
            mario.start = 32
            mario.l_image.clip_draw(mario.start + (int(mario.frame)) * 15, 34, 16, 16, mario.x, mario.y, mariosizex, mariosizey)


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
        mario.frame = (mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        mario.x += (mario.velocity - mario.acc) * game_framework.frame_time
        if mario.velocity > 0:
            if mario.acc > 0:
                mario.acc -= 500 * game_framework.frame_time
            else:
                mario.acc = 0
        elif mario.velocity < 0:
            if mario.acc < 0:
                mario.acc += 500 * game_framework.frame_time
            else:
                mario.acc = 0
        mario.x = clamp(25, mario.x, 1600 - 25)

    def draw(mario):
        if mario.dir == 1:
            mario.start = 32
            mario.image.clip_draw(mario.start + (int(mario.frame)) * 15, 34, 16, 16, mario.x, mario.y, mariosizex, mariosizey)
        else:
            mario.start = 32
            mario.l_image.clip_draw(mario.start + (int(mario.frame)) * 15, 34, 16, 16, mario.x, mario.y, mariosizex, mariosizey)


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
        mario.x = clamp(25, mario.x, 1600 - 25)

    def draw(mario):
        if mario.dir == 1:
            mario.start = 16 * 6
            mario.image.clip_draw(mario.start, 34, 15, 16, mario.x, mario.y, mariosizex, mariosizey)
        else:
            mario.start = 16 * 6
            mario.l_image.clip_draw(mario.start, 34, 16, 16, mario.x, mario.y, mariosizex, mariosizey)


next_state_table = {
    DashState: {SHIFT_UP: RunState, SHIFT_DOWN: DashState,
                RIGHT_DOWN: DashState, LEFT_DOWN: DashState, LEFT_UP: AccState, RIGHT_UP: AccState,
                SPACE: DashState},
    IdleState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState,
                SHIFT_DOWN: IdleState, SHIFT_UP: IdleState, SPACE: IdleState},
    RunState: {RIGHT_UP: AccState, LEFT_UP: AccState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,
               SHIFT_DOWN: DashState, SHIFT_UP: RunState, SPACE: RunState,
               STOP: IdleState},
    AccState: {RIGHT_UP: AccState, LEFT_UP: AccState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState,
               SHIFT_DOWN: AccState, SHIFT_UP: AccState, STOP: IdleState, SPACE: AccState
    }
}


class Mario:
    image = None

    def __init__(self):
        self.image = load_image('Resource\Mario.png')
        self.l_image = load_image('Resource\Mario_left.png')
        self.x, self.y = 300, 125
        self.frame = 1
        self.dir = 1
        self.velocity = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        self.acc = 0.0
        self.jump = False
        self.jumpdir = 0

        self.start = 0
        self.startx = 0
        self.marioRight = True
        self.marioLeft = True
        self.jumpdir = False; self.jumpstart = 0; self.jumping = False

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

    def draw(self):
        self.cur_state.draw(self)
        debug_print('Velocity : ' + str(self.velocity) + '  ACC : ' + str(self.acc) + '  Dir: ' + str(self.dir))

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            if DEBUG_KEY == key_event:
                print(history[-10:])
            else:
                self.add_event(key_event)

    def Rjump_draw(self):
        self.start = 16 * 7
        self.image.clip_draw(self.start, 34, 16, 16, self.x, self.y, mariosizex, mariosizey)

    def Ljump_draw(self):
        self.start = 16 * 7
        self.l_image.clip_draw(self.start, 0, 16, 16, self.x, self.y, mariosizex, mariosizey)

    def jump_left(self):
        if self.jumping == False and self.jumpstart == 0:
            self.jumpstart = self.y
            self.jumpdir = True
            self.jumping = True
        else:
            if self.jumping:
                if self.jumpdir:
                    self.y += 25
                    self.x -= 20
                    if self.y - self.jumpstart >= 105:
                        self.jumpdir = False
                else:
                    self.y -= 25
                    self.x -= 20
                    if self.y <= self.jumpstart:
                        self.y = self.jumpstart
                        self.jumpstart = 0
                        self.jumping = False
        return self.jumping

    def jump_right(self):
        if self.jumping == False and self.jumpstart == 0:
            self.jumpstart = self.y
            self.jumpdir = True
            self.jumping = True
        else:
            if self.jumping:
                if self.jumpdir:
                    self.y += 25
                    self.x += 20
                    if self.y - self.jumpstart >= 105:
                        self.jumpdir = False
                else:
                    self.y -= 25
                    self.x += 20
                    if self.y <= self.jumpstart:
                        self.y = self.jumpstart
                        self.jumpstart = 0
                        self.jumping = False
        return self.jumping

    def idle_jump(self):
        if self.jumpstart == 0 and self.jumping == False:
            self.jumpstart = self.y
            self.jumpdir = True
            self.jumping = True
        if self.jumping:
            if self.jumpdir:
                self.y += 25
                if self.y - self.jumpstart >= 105:
                    self.jumpdir = False
            else:
                self.y -= 25
                if self.y <= self.jumpstart:
                    self.y = self.jumpstart
                    self.jumpstart = 0
                    self.jumping = False
        return self.jumping

    def map_pos(self):
        return startx

    def get_marioPos(self):
        return self.x, self.y