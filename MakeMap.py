from pico2d import *
import Character


SCREENW = 1280.0; SCREENH = 800
ratio = 237 / SCREENH
width = round(SCREENW * ratio)

class Map:
    def __init__(self):
        self.image1 = load_image('Map1_Fix1.png')
        self.image2 = load_image('Map1_Fix1.png')
        self.image3 = load_image('Map1_Fix1.png')
        pass

    def draw(self, i):
        if i == 1:
            self.image1.clip_draw(0, 0, width, 237, SCREENW / 2, SCREENH / 2, SCREENW, SCREENH)
        elif i == 2:
            self.image2.clip_image(0,0, SCREENW, SCREENH)
        else:
            self.image3.clip_image(0,0, SCREENW, SCREENH)

