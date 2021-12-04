from pico2d import *
from Character import *
import server

SCREENW = 1280; SCREENH = 800
ratio = 237 / SCREENH
width = round(SCREENW * ratio)

class Map:
    image = None
    def __init__(self):
        if(Map.image == None):
            Map.Basetile = load_image('Resource\Tile\Basetile.png')
            Map.image = [load_image('Resource\Tile\Tile%d.png' % x) for x in range(8)]
            Map.S_image = [load_image('Resource\Tile\STile%d.png' % x) for x in range(2)]
            Map.B_image = [load_image('Resource\Tile\BTile%d.png' % x) for x in range(2)]

        self.tile = [[0 for _ in range(16)] for _ in range(255)]
        self.num = 1
        self.blocksize = 50
        # 첫번째맵 함수로 빼든지 깔끔하게 수정필요
        for i in range(0, 16):
                for j in range(0, 255):
                    if i == 0 or i == 1:
                        if j == 70 or j == 71 or j == 87 or j == 88 or j == 89 or j == 154 or j == 155:
                            self.tile[j][i] = 0  # Sky
                        else:
                            self.tile[j][i] = 8  # Base
                    elif i == 2:
                        if j == 0 or j == 49 or j == 98 or j == 194:  # Big Mountain
                            for a in range(j, j + 5):
                                for b in range(i, i + 3):
                                    self.tile[a][b] = -1
                            self.tile[j][i] = 10

                        elif j == 11 or j == 60 or j == 72 or j == 91 or j == 109:  # 3Grass
                            for a in range(j, j + 5):
                                self.tile[a][i] = -1
                            self.tile[j][i] = 12

                        elif j == 16 or j == 66 or j == 114 or j == 146 or j == 162 or j == 214:  # Small Mountain
                            for a in range(j, j + 3):
                                for b in range(i, i + 2):
                                    self.tile[a][b] = -1
                            self.tile[j][i] = 9

                        elif j == 24 or j == 121 or j == 169:  # 1Grass
                            for a in range(j, j + 3):
                                self.tile[a][i] = -1
                            self.tile[j][i] = 11

                        elif j == 29 or j == 39 or j == 47 or j == 58 or j == 165 or j == 181:
                            self.tile[j][i] = 1  # PipeBL
                        elif j == 30 or j == 40 or j == 48 or j == 59 or j == 166 or j == 182:
                            self.tile[j][i] = 2  # PipeBR

                        elif (j in range(136, 136 + 4)) or (j in range(142, 142 + 4)) or (j in range(149, 149 + 5)) or (j in range(156, 156+4))\
                                or (j in range(183, 183 + 9)): # block
                            self.tile[j][i] = 7

                    elif i == 3:
                        if j == 29 or j == 165 or j == 181:
                            self.tile[j][i] = 3  # PipeHL
                        elif j == 30 or j == 166 or j == 182:
                            self.tile[j][i] = 4  # PipeHR
                        elif j == 39 or j == 47 or j == 58:
                            self.tile[j][i] = 1  # PipeBL
                        elif j == 40 or j == 48 or j == 59:
                            self.tile[j][i] = 2  # PipeBR
                        elif (j in range(137, 137+3)) or (j in range(142, 142+3)) or (j in range(150, 150+4)) or (j in range(156, 156+3))\
                                or (j in range(184, 184 + 8)): # block
                            self.tile[j][i] = 7

                    elif i == 4:
                        if j == 39:  # PipeHL
                            self.tile[j][i] = 3
                        elif j == 40:  # PipeHR
                            self.tile[j][i] = 4
                        elif j == 47 or j == 58:
                            self.tile[j][i] = 1
                        elif j == 48 or j == 59:
                            self.tile[j][i] = 2
                        elif (j in range(138, 138+2)) or (j in range(142, 142+2)) or (j in range(151, 151+3)) or (j in range(156, 156+2))\
                                or (j in range(185, 185 + 7)): # block
                            self.tile[j][i] = 7

                    elif i == 5:
                        if j == 16 or j == 22 or j == 24 or j == 79 or j == 108 or j == 111 or j == 114 or j == 172:  # questiontile
                            self.tile[j][i] = 5
                        elif j == 21 or j == 23 or j == 25 or j == 78 or j == 80 or j == 96 or j == 102 or j == 103 or j == 120\
                                or j == 131 or j == 132 or j == 170 or j == 171 or j == 173:  # brick
                            self.tile[j][i] = 6
                        elif j == 47 or j == 58: # PipeHL
                            self.tile[j][i] = 3
                        elif j == 48 or j == 59: # PipeHR
                            self.tile[j][i] = 4
                        elif j == 139 or j == 142 or j == 152 or j == 153 or j == 156 or (j in range(186, 186 + 6)): # block
                            self.tile[j][i] = 7

                    elif i == 6:
                        if (j in range(187, 187 + 5)): # block
                            self.tile[j][i] = 7
                    elif i == 7:
                        if (j in range(188, 188 + 4)): # block
                            self.tile[j][i] = 7
                    elif i == 8:
                        if (j in range(189, 189 + 3)): # block
                            self.tile[j][i] = 7
                    elif i == 9:
                        if j == 23 or j == 96 or j == 111 or j == 131 or j == 132:  # questiontile
                            self.tile[j][i] = 5
                        elif (j in range(81, 89 + 1)) or (j in range(93, 95 + 1) or (j in range(123, 123+3)) or j == 130 or j == 133):  # brick
                            self.tile[j][i] = 6
                        elif j == 190 or j == 191: # block
                            self.tile[j][i] = 7
        self.camerax = 0

        for j in range(0, 255):
            for i in range(0, 16):
                print(self.tile[j][i], end='')
                if i != 15:
                    print(",", end='')
            print()
    def draw(self):
        if self.num == 1:
            self.num = 1
            for i in range(0, 16):
                for j in range(0, 255):
                    if self.tile[j][i] in range(0, 8):
                        Map.image[self.tile[j][i]].clip_draw(0, 0, 16, 16,
                                                  (j * self.blocksize) + (self.blocksize // 2) - self.camerax,
                                                  i * self.blocksize + (self.blocksize // 2), self.blocksize,
                                                  self.blocksize)
                    elif self.tile[j][i] == 8 and i != 1:
                        Map.Basetile.clip_draw(0, 0, 16, 32,
                                                (j * self.blocksize) + (self.blocksize // 2) - self.camerax,
                                                i * self.blocksize + self.blocksize, self.blocksize, self.blocksize * 2)
                    elif self.tile[j][i] == 9:
                        Map.S_image[0].clip_draw(0, 0, 48, 32,
                                                     (j * self.blocksize) + ((self.blocksize * 3) // 2) - self.camerax,
                                                     i * self.blocksize + ((self.blocksize * 2) // 2),
                                                     self.blocksize * 3,
                                                     self.blocksize * 2)
                    elif self.tile[j][i] == 10:
                        Map.B_image[0].clip_draw(0, 0, 80, 48,
                                                   (j * self.blocksize) + ((self.blocksize * 5) // 2) - self.camerax,
                                                   i * self.blocksize + ((self.blocksize * 3) // 2), self.blocksize * 5,
                                                   self.blocksize * 3)
                    elif self.tile[j][i] == 11:
                        Map.S_image[1].clip_draw(0, 0, 48, 16,
                                              (j * self.blocksize) + ((self.blocksize * 3) // 2) - self.camerax,
                                              i * self.blocksize + ((self.blocksize) // 2), self.blocksize * 3,
                                              self.blocksize)
                    elif self.tile[j][i] == 12:
                        Map.B_image[1].clip_draw(0, 0, 80, 16,
                                              (j * self.blocksize) + ((self.blocksize * 5) // 2) - self.camerax,
                                              i * self.blocksize + ((self.blocksize) // 2), self.blocksize * 5,
                                              self.blocksize)

        # draw_rectangle(*self.get_Check_Box(8, 0))
        for i in range(0, 16):
            for j in range(0, 254):
                 if self.tile[j][i] == 5:
                    draw_rectangle(*self.get_Check_Box(i, j))

    def update(self):
        if server.mario.get_marioPos() == SCREENW - 300:
            self.camerax = int(server.mario.get_MapX())
        elif server.mario.get_marioPos() == 200:
            self.camerax = int(server.mario.get_MapX())

    def get_Check_Box(self, i, j):
        return (j * self.blocksize) - self.camerax, i * self.blocksize, \
               (j * self.blocksize) + self.blocksize - self.camerax, i * self.blocksize + self.blocksize

    def __getstate__(self):
        state = {'num': self.num, 'tile': self.tile, 'camerax': self.camerax}
        return state


    def __setstate__(self, state):
        self.__init__()
        self.__dict__.update(state)

