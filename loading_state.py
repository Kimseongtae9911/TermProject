import random
import json
import os
import csv

from pico2d import *
import game_framework
import game_world
import main_state
import game_over_state
import server
from Character import Mario
from MakeMap import Map
from Goomba import Goomba
from Rocket import Rocket
from Mushroom import Mushroom

name = "LoadingState"
SCREENW = 1280; SCREENH = 800
image = None
numbers = None
press = None
timer = 1000


def enter():
    global image, numbers, timer, press
    game_world.clear()
    server.goombas.clear()
    if server.mario == None:
        server.mario = Mario()
    if server.mymap == None:
        server.mymap = Map()
    image = load_image('Resource\loading.png')
    numbers = load_image('Resource\_Number.png')
    press = load_image('Resource\Press_L.png')
    hide_cursor()
    hide_lattice()
    if server.mario.life == 0:
        game_framework.change_state(game_over_state)

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
            elif event.key == SDLK_l:
                load_saved_world()

def create_new_world():
    server.mario = Mario()
    server.mymap = Map()
    game_world.add_object(server.mymap, 0)
    game_world.add_object(server.mario, 1)

    cnti = 0
    cntj = 0
    if server.stage == 1:
        with open('map_data1.txt', 'rt') as f:
            while True:
                c = f.readline()
                if c == '':
                    break
                temp = int(c)
                server.mymap.tile[cntj][cnti] = temp
                cnti += 1
                if cnti == 16:
                    cnti = 0
                    cntj += 1
    elif server.stage == 2:
        with open('map_data2.txt', 'rt') as f:
            while True:
                c = f.readline()
                if c == '':
                    break
                temp = int(c)
                server.mymap.tile[cntj][cnti] = temp
                cnti += 1
                if cnti == 16:
                    cnti = 0
                    cntj += 1
    elif server.stage == 3:
        with open('map_data3.txt', 'rt') as f:
            while True:
                c = f.readline()
                if c == '':
                    break
                temp = int(c)
                server.mymap.tile[cntj][cnti] = temp
                cnti += 1
                if cnti == 16:
                    cnti = 0
                    cntj += 1


def load_saved_world():
    game_world.load()

    for o in game_world.all_objects():
        if isinstance(o, Mario):
            server.mario = o
        elif isinstance(o, Map):
            server.mymap = o
        elif isinstance(o, Goomba):
            server.goombas.append(o)
        elif isinstance(o, Rocket):
            server.rockets = o
        elif isinstance(o, Mushroom):
            server.mushroom = o
    if server.mymap.tile[0][2] == 0:
        server.stage = 1
    elif server.mymap.tile[0][2] == 15:
        server.stage = 2
    else:
        server.stage = 3
    game_framework.change_state(main_state)

def update():
    global timer
    if timer > 0:
        timer -= 1

    if timer <= 0:
        timer = 1000
        temp_life = server.mario.life
        create_new_world()
        server.mario.life = temp_life
        game_framework.change_state(main_state)


def draw():
    global image
    clear_canvas()
    image.clip_draw(0, 0, 964, 664, SCREENW // 2, SCREENH // 2, SCREENW, SCREENH)

    numbers.clip_draw(server.stage * 9, 0, 9, 8, SCREENW // 2 + 50, SCREENH // 2 + 130, 50, 50)
    numbers.clip_draw(server.stage * 9, 0, 9, 8, SCREENW // 2 + 100, SCREENH // 2 + 360, 50, 50)
    numbers.clip_draw(server.mario.life * 9, 0, 9, 8, SCREENW // 2 + 50, SCREENH // 2 + 15, 50, 50)
    press.clip_draw(0, 0, 300, 57, SCREENW // 2, 200)
    update_canvas()







