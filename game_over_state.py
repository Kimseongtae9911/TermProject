import random
import json
import os
import csv

from pico2d import *
import game_framework
import loading_state
import server

name = "Game_Over_State"
SCREENW = 1280; SCREENH = 800
image = None
image2 = None
press = None

def enter():
    global image, image2, press
    image = load_image('Resource\Game_over.png')
    image2 = load_image('Resource\Clear.png')
    press = load_image('Resource\Press_N.png')
    hide_cursor()
    hide_lattice()


def exit():
    global image, press, image2
    del image
    del press
    del image2


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
            elif event.key == SDLK_n:
                game_framework.change_state(loading_state)
                server.mario.life = 3
                server.stage = 1


def update():
    pass


def draw():
    clear_canvas()
    if server.clear:
        image2.clip_draw(0, 0, 258, 235, SCREENW // 2, SCREENH // 2, SCREENW, SCREENH)
    else:
        image.clip_draw(0, 0, 258, 235, SCREENW // 2, SCREENH // 2, SCREENW, SCREENH)
    press.clip_draw(0, 0, 423, 57, SCREENW // 2, 100)
    update_canvas()







