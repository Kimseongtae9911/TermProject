from pico2d import *
import game_framework
import main_state

SCREENW = 1280; SCREENH = 800

open_canvas(SCREENW, SCREENH)
game_framework(main_state)
close_canvas()
