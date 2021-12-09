import random
import json
import os

from pico2d import *
import game_framework
import game_world
import server

from Character import Mario
from MakeMap import Map
from Goomba import Goomba
from Boss import Boss
name = "MainState"

def enter():
    if server.mario == None:
        server.mario = Mario()
        game_world.add_object(server.mario, 2)
    if server.mymap == None:
        server.mymap = Map()
        game_world.add_object(server.mymap, 0)
    if server.stage == 1:
        server.goombas.append(Goomba(1200, 325))
        server.goombas.append(Goomba(1700, 325))
        server.goombas.append(Goomba(8500, 125))
        game_world.add_objects(server.goombas, 1)
    elif server.stage == 3:
        server.boss = Boss()
        game_world.add_object(server.boss, 1)

def exit():
    game_world.clear()


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_s:
            game_world.save()
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







