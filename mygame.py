import game_framework
import pico2d

import main_state

SCREENW = 1280; SCREENH = 800

pico2d.open_canvas(SCREENW, SCREENH)
game_framework.play(main_state)
pico2d.close_canvas()
