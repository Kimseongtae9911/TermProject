from pico2d import *

SCREENW = 1280; SCREENH = 800
ratio = 237 / SCREENH
width = round(SCREENW * ratio)

class Map:
    image1 = None
    tile1 = [[0 for col in range(10)] for row in range(255)]
    def __init__(self):
        if(Map.image1 == None):
            Map.image1 = load_image('Resource\Map1_Fix1.png')
            Map.image2 = load_image('Resource\Map2.png')
            Map.image3 = load_image('Resource\Map3.png')
            Map.Basetile = load_image('Resource\Basetile.png')
            for i in range(0, 10):
                for j in range(0, 255):
                    if i == 0 or i == 1:
                        if j == 70 or 71 or 87 or 88 or 89 or 154 or 155:
                            Map.tile1[j][i] = 0
                        else:
                            Map.tile1[j][i] = 1
        self.camerax = 0
        self.i = 0
        pass

    def draw(self, i):
        if i == 1:
            self.i = 1
            # self.image1.clip_draw(self.camerax, 0, width, 237, SCREENW / 2, SCREENH / 2, SCREENW, SCREENH)
            for i in range(0, 10):
                for j in range(0, 255):
                    if Map.tile1[j][i] == 1:
                        self.Basetile.clip_draw(0, 0, 15, 16, j * 15, i * 16, 50, 50)
        elif i == 2:
            self.i = 2
            self.image1.clip_draw(self.camerax, 0, width, 237, SCREENW / 2, SCREENH / 2, SCREENW, SCREENH)
            pass
        else:
            self.i = 3
            self.image1.clip_draw(self.camerax, 0, width, 237, SCREENW / 2, SCREENH / 2, SCREENW, SCREENH)
            pass

    def get_camera(self, x, startx):
        if self.i == 1:
            if x >= (SCREENW / 2) and (SCREENW / 2 + startx + x) <= 3375:
                self.camerax = startx

        elif self.i == 2:

            if x >= (SCREENW / 2) and (SCREENW / 2 + startx + x) <= 2624:
                self.camerax = startx

        else:
            if x >= (SCREENW / 2) and (SCREENW / 2 + startx + x) <= 2560:
                self.camerax = startx

