from pico2d import *
import math

class Mario:
    def __init__(self):
        self.image = load_image('Mario.png')
        self.frame = 1;
        self.start = 32;
        self.x = 300; self.y = 90

    def draw(self):
        self.image.clip_draw(self.start + self.frame * 15, 34, 16, 16, self.x, self.y, 48, 48)

    def move(self):
        self.x += 5
        self.frame = (self.frame + 1) % 3

def handle_events():
    global Play
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            Play = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            Play = False


open_canvas()

mario = Mario()

Play = True

while Play:
    handle_events()

    mario.move()

    clear_canvas()

    mario.draw()

    update_canvas()

    delay(0.1)
