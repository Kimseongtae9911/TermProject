import random
import json
import os

from pico2d import *
import game_framework
import main_state
from Character import Mario
from MakeMap import Map

name = "LoadingState"
SCREENW = 1280; SCREENH = 800
image = None
numbers = None
timer = 1000


def enter():
    global image, numbers, timer
    image = load_image('Resource\loading.png')
    numbers = load_image('Resource\_Number.png')


def exit():
    global image, numbers
    del image
    del numbers


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()


def update():
    global timer
    if timer > 0:
        timer -= 1

    if timer <= 0:
        timer =1000
        game_framework.push_state(main_state)
    pass

def draw():
    global image
    clear_canvas()
    image.clip_draw(0, 0, 964, 664, SCREENW // 2, SCREENH // 2, SCREENW, SCREENH)

    numbers.clip_draw(Map.num * 9, 0, 9, 8, SCREENW // 2 + 50, SCREENH // 2 + 130, 50, 50)
    numbers.clip_draw(Map.num * 9, 0, 9, 8, SCREENW // 2 + 100, SCREENH // 2 + 360, 50, 50)
    numbers.clip_draw(Mario.life * 9, 0, 9, 8, SCREENW // 2 + 50, SCREENH // 2 + 15, 50, 50)
    update_canvas()







