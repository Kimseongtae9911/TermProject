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
            Map.Basetile = load_image('Resource\Tile\Basetile.png') #8 Base
            Map.image = [load_image('Resource\Tile\Tile%d.png' % x) for x in range(20)] #0Sky, 1PipeBL, 2PiprBR, 3PipeHL, 4PipeHR, 5ques, 6brick, 7block, 16LeafL, 17LeafM, 18LeafR, 19Tree,
            # 20CastleBrick# , 21magmaL, 22magmaH, 23CastleBlock, 24Bridge1, 25Bridge2, 26Axe, 27Dark
            Map.S_image = [load_image('Resource\Tile\STile%d.png' % x) for x in range(2)] #9Mountain, #11 1Grass
            Map.B_image = [load_image('Resource\Tile\BTile%d.png' % x) for x in range(2)] #10Mountain #12 3frass
            Map.F_image = [load_image('Resource\Tile\Flag%d.png' % x) for x in range(2)] #13Flag #14Flag
            Map.castle = load_image('Resource\Tile\Castle.png') #15Castle
        self.tile = [[0 for _ in range(16)] for _ in range(255)]
        self.num = 1
        self.blocksize = 50
        self.camerax = 0

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
                    elif self.tile[j][i] in range(16, 28):
                        Map.image[self.tile[j][i] - 8].clip_draw(0, 0, 16, 16,
                                                             (j * self.blocksize) + (
                                                                         self.blocksize // 2) - self.camerax,
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
                    elif self.tile[j][i] == 13:
                        Map.F_image[0].clip_draw(0, 0, 16, 176, (j * self.blocksize) + ((self.blocksize) // 2) - self.camerax,
                                              i * self.blocksize + ((self.blocksize * 11) // 2), self.blocksize,
                                              self.blocksize * 11)
                    elif self.tile[j][i] == 14:
                        Map.F_image[1].clip_draw(0, 0, 24, 16, (j * self.blocksize) + (self.blocksize // 2) - self.camerax,
                                              i * self.blocksize + ((self.blocksize) // 2), self.blocksize * 1.5,
                                              self.blocksize)
                    elif self.tile[j][i] == 15:
                        Map.castle.clip_draw(0, 0, 80, 80, (j * self.blocksize) + ((self.blocksize * 5) // 2) - self.camerax,
                                              i * self.blocksize + ((self.blocksize * 5) // 2), self.blocksize * 5,
                                              self.blocksize * 5)

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

