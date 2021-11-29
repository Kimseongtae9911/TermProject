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

            # 첫번째맵 함수로 빼든지 깔끔하게 수정필요
            for i in range(0, 16):
                for j in range(0, 255):
                    if i == 0 or i == 1:
                        if j == 70 or j == 71 or j == 87 or j == 88 or j == 89 or j == 154 or j == 155:
                            Map.tile1[j][i] = 0  # Sky
                        else:
                            Map.tile1[j][i] = 1  # Base
                    elif i == 2:
                        if j == 0 or j == 49 or j == 98 or j == 194:  # Big Mountain
                            for a in range(j, j + 5):
                                for b in range(i, i + 3):
                                    Map.tile1[a][b] = -1
                            Map.tile1[j][i] = 10

                        elif j == 11 or j == 60 or j == 72 or j == 91 or j == 109:  # 3Grass
                            for a in range(j, j + 5):
                                Map.tile1[a][i] = -1
                            Map.tile1[j][i] = 12

                        elif j == 16 or j == 66 or j == 114 or j == 146 or j == 162 or j == 214:  # Small Mountain
                            for a in range(j, j + 3):
                                for b in range(i, i + 2):
                                    Map.tile1[a][b] = -1
                            Map.tile1[j][i] = 9

                        elif j == 24 or j == 121 or j == 169:  # 1Grass
                            for a in range(j, j + 3):
                                Map.tile1[a][i] = -1
                            Map.tile1[j][i] = 11

                        elif j == 29 or j == 39 or j == 47 or j == 58 or j == 165 or j == 181:
                            Map.tile1[j][i] = 2  # PipeBL
                        elif j == 30 or j == 40 or j == 48 or j == 59 or j == 166 or j == 182:
                            Map.tile1[j][i] = 3  # PipeBR

                        elif (j in range(136, 136 + 4)) or (j in range(142, 142 + 4)) or (j in range(149, 149 + 5)) or (j in range(156, 156+4))\
                                or (j in range(183, 183 + 9)): # block
                            Map.tile1[j][i] = 8

                    elif i == 3:
                        if j == 29 or j == 165 or j == 181:
                            Map.tile1[j][i] = 4  # PipeHL
                        elif j == 30 or j == 166 or j == 182:
                            Map.tile1[j][i] = 5  # PipeHR
                        elif j == 39 or j == 47 or j == 58:
                            Map.tile1[j][i] = 2  # PipeBL
                        elif j == 40 or j == 48 or j == 59:
                            Map.tile1[j][i] = 3  # PipeBR
                        elif (j in range(137, 137+3)) or (j in range(142, 142+3)) or (j in range(150, 150+4)) or (j in range(156, 156+3))\
                                or (j in range(184, 184 + 8)): # block
                            Map.tile1[j][i] = 8

                    elif i == 4:
                        if j == 39:  # PipeHL
                            Map.tile1[j][i] = 4
                        elif j == 40:  # PipeHR
                            Map.tile1[j][i] = 5
                        elif j == 47 or j == 58:
                            Map.tile1[j][i] = 2
                        elif j == 48 or j == 59:
                            Map.tile1[j][i] = 3
                        elif (j in range(138, 138+2)) or (j in range(142, 142+2)) or (j in range(151, 151+3)) or (j in range(156, 156+2))\
                                or (j in range(185, 185 + 7)): # block
                            Map.tile1[j][i] = 8

                    elif i == 5:
                        if j == 16 or j == 22 or j == 24 or j == 79 or j == 108 or j == 111 or j == 114 or j == 172:  # questiontile
                            Map.tile1[j][i] = 6
                        elif j == 21 or j == 23 or j == 25 or j == 78 or j == 80 or j == 96 or j == 102 or j == 103 or j == 120\
                                or j == 131 or j == 132 or j == 170 or j == 171 or j == 173:  # brick
                            Map.tile1[j][i] = 7
                        elif j == 47 or j == 58:
                            Map.tile1[j][i] = 4
                        elif j == 48 or j == 59:
                            Map.tile1[j][i] = 5
                        elif j == 139 or j == 142 or j == 152 or j == 153 or j == 156 or (j in range(186, 186 + 6)): # block
                            Map.tile1[j][i] = 8

                    elif i == 6:
                        if (j in range(187, 187 + 5)): # block
                            Map.tile1[j][i] = 8
                    elif i == 7:
                        if (j in range(188, 188 + 4)): # block
                            Map.tile1[j][i] = 8
                    elif i == 8:
                        if (j in range(189, 189 + 3)): # block
                            Map.tile1[j][i] = 8
                    elif i == 9:
                        if j == 23 or j == 96 or j == 111 or j == 131 or j == 132:  # questiontile
                            Map.tile1[j][i] = 6
                        elif (j in range(81, 89 + 1)) or (j in range(93, 95 + 1) or (j in range(123, 123+3)) or j == 130 or j == 133):  # brick
                            Map.tile1[j][i] = 7
                        elif j == 190 or j == 191: # block
                            Map.tile1[j][i] = 8
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


