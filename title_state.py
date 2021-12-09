import random
import json
import os

from pico2d import *
import game_framework
import loading_state
import server

name = "TitleState"
SCREENW = 1280; SCREENH = 800
image = None
image2 = None
timer = 1000

def enter():
    server.bgm = load_music('Resource\Sound\Mario_Song.mp3')
    server.bgm.set_volume(10)
    server.bgm.repeat_play()
    global image, image2, timer
    image = load_image('Resource\Title.png')
    image2 = load_image('Resource\PRESS_TITLE.png')


def exit():
    global image, image2
    del image
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
            elif event.key == SDLK_RETURN:
                game_framework.change_state(loading_state)


def update():
    global timer
    if timer > 0:
        timer -= 2
    elif timer <= 0:
        timer = 1000
    pass

def draw():
    global image
    clear_canvas()
    image.clip_draw(0, 0, 964, 664, SCREENW // 2, SCREENH // 2, SCREENW, SCREENH)
    if timer > 500:
        image2.draw(SCREENW // 2, 300)
    update_canvas()







