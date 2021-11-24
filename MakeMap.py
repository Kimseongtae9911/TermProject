from pico2d import *
from Character import *
import server

SCREENW = 1280; SCREENH = 800
ratio = 237 / SCREENH
width = round(SCREENW * ratio)

class Map:
    image2 = None
    tile1 = [[0 for _ in range(16)] for _ in range(255)]
    num = 1
    blocksize = 50
    camerax = 0
    def __init__(self):
        if(Map.image2 == None):
            Map.image2 = load_image('Resource\Map2.png')
            Map.image3 = load_image('Resource\Map3.png')
            Map.Basetile = load_image('Resource\Tile\Basetile.png')
            Map.Skytile = load_image('Resource\Tile\sky(16x16).png')
            Map.PipeHLtile = load_image('Resource\Tile\pipeHL.png')
            Map.PipeHRtile = load_image('Resource\Tile\pipeHR.png')
            Map.PipeBLtile = load_image('Resource\Tile\pipeBL.png')
            Map.PipeBRtile = load_image('Resource\Tile\pipeBR.png')
            Map.BigMountain = load_image('Resource\Tile\mountain(80x48).png')
            Map.SmallMountain = load_image('Resource\Tile\mountain(48x32).png')
            Map.Grass1 = load_image('Resource\Tile\grass(48x16).png')
            Map.Grass3 = load_image('Resource\Tile\grass(80x16).png')
            Map.Qtile = load_image('Resource\Tile\questiontile.png')
            Map.Btile = load_image('Resource\Tile\Bricktile.png')
            Map.Bltile = load_image('Resource\Tile\Blocktile.png')
            for i in range(0, 16):
                for j in range(0, 255):
                    if i == 0 or i == 1:
                        if j == 70 or j == 71 or j == 87 or j == 88 or j == 89 or j == 154 or j == 155:
                            Map.tile1[j][i] = 0  # Sky
                        else:
                            Map.tile1[j][i] = 1  # Base
                    elif i == 2:
                        if j == 0 or j == 49:  # Big Mountain
                            for a in range(j, j + 5):
                                for b in range(i, i + 3):
                                    Map.tile1[a][b] = -1
                            Map.tile1[j][i] = 10

                        elif j == 11 or j == 60 or j == 72:  # 3Grass
                            for a in range(j, j + 5):
                                Map.tile1[a][i] = -1
                            Map.tile1[j][i] = 12

                        elif j == 16 or j == 66:  # Small Mountain
                            for a in range(j, j + 3):
                                for b in range(i, i + 2):
                                    Map.tile1[a][b] = -1
                            Map.tile1[j][i] = 9

                        elif j == 24:  # 1Grass
                            for a in range(j, j + 3):
                                Map.tile1[a][i] = -1
                            Map.tile1[j][i] = 11

                        elif j == 29 or j == 39 or j == 47 or j == 58:
                            Map.tile1[j][i] = 2  # PipeBL
                        elif j == 30 or j == 40 or j == 48 or j == 59:
                            Map.tile1[j][i] = 3  # PipeBR
                    elif i == 3:
                        if j == 29:
                            Map.tile1[j][i] = 4  # PipeHL
                        elif j == 30:
                            Map.tile1[j][i] = 5  # PipeHR
                        elif j == 39 or j == 47 or j == 58:
                            Map.tile1[j][i] = 2  # PipeBL
                        elif j == 40 or j == 48 or j == 59:
                            Map.tile1[j][i] = 3  # PipeBR
                    elif i == 4:
                        if j == 39:  # PipeHL
                            Map.tile1[j][i] = 4
                        elif j == 40:  # PipeHR
                            Map.tile1[j][i] = 5
                        elif j == 47 or j == 58:
                            Map.tile1[j][i] = 2
                        elif j == 48 or j == 59:
                            Map.tile1[j][i] = 3
                    elif i == 5:
                        if j == 16 or j == 22 or j == 24:  # questiontile
                            Map.tile1[j][i] = 6
                        elif j == 21 or j == 23 or j == 25:  # brick
                            Map.tile1[j][i] = 7
                        elif j == 47 or j == 58:
                            Map.tile1[j][i] = 4
                        elif j == 48 or j == 59:
                            Map.tile1[j][i] = 5
                    elif i == 9:
                        if j == 23:  # questiontile
                            Map.tile1[j][i] = 6
        self.camerax = 0
        pass

    def draw(self):
        if Map.num == 1:
            self.num = 1
            for i in range(0, 16):
                for j in range(0, 255):
                    if Map.tile1[j][i] == 1 and i != 1:
                        self.Basetile.clip_draw(0, 0, 16, 32,
                                                (j * self.blocksize) + (self.blocksize // 2) - self.camerax,
                                                i * self.blocksize + self.blocksize, self.blocksize, self.blocksize * 2)
                    elif Map.tile1[j][i] == 2:
                        self.PipeBLtile.clip_draw(0, 0, 16, 16,
                                                  (j * self.blocksize) + (self.blocksize // 2) - self.camerax,
                                                  i * self.blocksize + (self.blocksize // 2), self.blocksize,
                                                  self.blocksize)
                    elif Map.tile1[j][i] == 3:
                        self.PipeBRtile.clip_draw(0, 0, 16, 16,
                                                  (j * self.blocksize) + (self.blocksize // 2) - self.camerax,
                                                  i * self.blocksize + (self.blocksize // 2), self.blocksize,
                                                  self.blocksize)
                    elif Map.tile1[j][i] == 4:
                        self.PipeHLtile.clip_draw(0, 0, 16, 16,
                                                  (j * self.blocksize) + (self.blocksize // 2) - self.camerax,
                                                  i * self.blocksize + (self.blocksize // 2), self.blocksize,
                                                  self.blocksize)
                    elif Map.tile1[j][i] == 5:
                        self.PipeHRtile.clip_draw(0, 0, 16, 16,
                                                  (j * self.blocksize) + (self.blocksize // 2) - self.camerax,
                                                  i * self.blocksize + (self.blocksize // 2), self.blocksize,
                                                  self.blocksize)
                    elif Map.tile1[j][i] == 6:
                        self.Qtile.clip_draw(0, 0, 16, 16,
                                                  (j * self.blocksize) + (self.blocksize // 2) - self.camerax,
                                                  i * self.blocksize + (self.blocksize // 2), self.blocksize,
                                                  self.blocksize)
                    elif Map.tile1[j][i] == 7:
                        self.Btile.clip_draw(0, 0, 16, 16,
                                                  (j * self.blocksize) + (self.blocksize // 2) - self.camerax,
                                                  i * self.blocksize + (self.blocksize // 2), self.blocksize,
                                                  self.blocksize)
                    elif Map.tile1[j][i] == 8:
                        self.Bltile.clip_draw(0, 0, 16, 16,
                                             (j * self.blocksize) + (self.blocksize // 2) - self.camerax,
                                             i * self.blocksize + (self.blocksize // 2), self.blocksize,
                                             self.blocksize)
                    elif Map.tile1[j][i] == 9:
                        self.SmallMountain.clip_draw(0, 0, 48, 32,
                                                   (j * self.blocksize) + ((self.blocksize * 3) // 2) - self.camerax,
                                                   i * self.blocksize + ((self.blocksize * 2) // 2), self.blocksize * 3,
                                                   self.blocksize * 2)
                    elif Map.tile1[j][i] == 10:
                        self.BigMountain.clip_draw(0, 0, 80, 48,
                                                   (j * self.blocksize) + ((self.blocksize * 5) // 2) - self.camerax,
                                                   i * self.blocksize + ((self.blocksize * 3) // 2), self.blocksize * 5,
                                                   self.blocksize * 3)
                    elif Map.tile1[j][i] == 11:
                        self.Grass1.clip_draw(0, 0, 48, 16,
                                                   (j * self.blocksize) + ((self.blocksize * 3) // 2) - self.camerax,
                                                   i * self.blocksize + ((self.blocksize) // 2), self.blocksize * 3,
                                                   self.blocksize)
                    elif Map.tile1[j][i] == 12:
                        self.Grass3.clip_draw(0, 0, 80, 16,
                                                   (j * self.blocksize) + ((self.blocksize * 5) // 2) - self.camerax,
                                                   i * self.blocksize + ((self.blocksize) // 2), self.blocksize * 5,
                                                   self.blocksize)
                    elif Map.tile1[j][i] == 0:
                        self.Skytile.clip_draw(0, 0, 16, 16,
                                               (j * self.blocksize) + (self.blocksize // 2) - self.camerax,
                                               i * self.blocksize + (self.blocksize // 2), self.blocksize,
                                               self.blocksize)

        elif Map.num == 2:
            self.num = 2
            self.image2.clip_draw(self.camerax, 0, width, 237, SCREENW / 2, SCREENH / 2, SCREENW, SCREENH)
            pass
        else:
            self.num = 3
            self.image3.clip_draw(self.camerax, 0, width, 237, SCREENW / 2, SCREENH / 2, SCREENW, SCREENH)
            pass

        draw_rectangle(*self.get_Check_Box(1, 0))
        for i in range(0, 16):
            for j in range(0, 254):
                 if Map.tile1[j][i] == 6:
                    draw_rectangle(*self.get_Check_Box(i, j))

    def update(self):
        if server.mario.get_marioPos() == SCREENW - 300:
            self.camerax = int(server.mario.get_MapX())
        elif server.mario.get_marioPos() == 200:
            self.camerax = int(server.mario.get_MapX())

    def get_Check_Box(self, i, j):
        return (j * self.blocksize) - self.camerax, i * self.blocksize, \
               (j * self.blocksize) + self.blocksize - self.camerax, i * self.blocksize + self.blocksize


