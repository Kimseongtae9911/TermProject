from pico2d import *

SCREENW = 1280; SCREENH = 800
ratio = 237 / SCREENH
width = round(SCREENW * ratio)

class Map:
    def __init__(self):
        self.image1 = load_image('Map1_Fix1.png')
        self.image2 = load_image('Map1_Fix1.png')
        self.image3 = load_image('Map1_Fix1.png')
        self.camerax = 0;
        pass

    def draw(self, i):
        if i == 1:
            self.image1.clip_draw(self.camerax, 0, width, 237, SCREENW / 2, SCREENH / 2, SCREENW, SCREENH)
        elif i == 2:
            self.image1.clip_draw(self.camerax, 0, width, 237, SCREENW / 2, SCREENH / 2, SCREENW, SCREENH)
            pass
        else:
            self.image1.clip_draw(self.camerax, 0, width, 237, SCREENW / 2, SCREENH / 2, SCREENW, SCREENH)
            pass

    def Rightupdate(self, x):
        if x + width >= 3375:
            self.camerax = 3375 - width
        else:
            self.camerax = x

    def Leftupdate(self, x):
        if x < 0:
            return
        self.camerax = x