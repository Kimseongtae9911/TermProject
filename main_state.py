import random
import json
import os

from Character import *
from pico2d import *
import game_framework
import game_world

from Character import Mario
from MakeMap import Map
from Rocket import Rocket

name = "MainState"

mario = None
mymap = None


def enter():
    global mario, mymap
    mario = Mario()
    mymap = Map()
    game_world.add_object(mymap, 0)
    game_world.add_object(mario, 2)


def exit():
    global mario, mymap
    del mario
    del mymap
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
        else:
            mario.handle_event(event)


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_Check_Box()
    if(b == mymap):
        for i in range(0, 16):
            for j in range(0, 255):
                left_b, bottom_b, right_b, top_b = b.get_Check_Box(i, j)
    else:
        left_b, bottom_b, right_b, top_b = b.get_Check_Box()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


def collide_map(a, b):
    left_a, bottom_a, right_a, top_a = a.get_Check_Box()
    for j in range(0, 254):
        left_b, bottom_b, right_b, top_b = b.get_Check_Box(1, j)
        left_c, bottom_c, right_c, top_c = b.get_Check_Box(1, j + 1)
        if bottom_a + 2 >= top_b and Map.tile1[j][1] == 0 and left_a + 10 > left_b and right_a < right_b:
            return True
        elif bottom_a + 2 >= top_b and Map.tile1[j][1] == 0 and Map.tile1[j+1][1] == 0 and left_a + 10 > left_b and right_a < right_c:
            return True

    return False


def update():
    global mario, mymap
    for game_object in game_world.all_objects():
        if game_object == mymap:
            game_object.update(mario)
        else:
            game_object.update()

        if collide(mario, game_object):
            if game_object != mario:
                game_world.remove_object(game_object)


    if(collide_map(mario, mymap)):
        mario.add_event(9)

def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()







