import random
import json
import os

import Character
from Character import *
from pico2d import *
import game_framework
import game_world
import server

from Character import Mario
from MakeMap import Map
from Goomba import Goomba
name = "MainState"

def enter():
    server.mario = Mario()
    server.mymap = Map()
    server.goomba = Goomba(1200, 325)
    game_world.add_object(server.mymap, 0)
    game_world.add_object(server.mario, 2)
    game_world.add_object(server.goomba, 1)


def exit():
    game_world.clear()


def pause():
    pass


def resume():
    # server.mario = Mario()
    # server.mymap = Map()
    # server.goomba = Goomba()
    # game_world.add_object(server.mymap, 0)
    # game_world.add_object(server.mario, 2)
    # game_world.add_object(server.goomba, 1)
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
        else:
            server.mario.handle_event(event)

def update():
    for game_object in game_world.all_objects():
        game_object.update()


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()







