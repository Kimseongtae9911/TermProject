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
            Map.image = [load_image('Resource\Tile\Tile%d.png' % x) for x in range(12)] #0Sky, 1PipeBL, 2PiprBR, 3PipeHL, 4PipeHR, 5ques, 6brick, 7block, 16LeafL, 17LeafM, 18LeafR, 19Tree
            Map.S_image = [load_image('Resource\Tile\STile%d.png' % x) for x in range(2)] #9Mountain, #11 1Grass
            Map.B_image = [load_image('Resource\Tile\BTile%d.png' % x) for x in range(2)] #10Mountain #12 3frass
            Map.F_image = [load_image('Resource\Tile\Flag%d.png' % x) for x in range(2)] #13Flag #14Flag
            Map.castle = load_image('Resource\Tile\Castle.png') #15Castle
        self.tile = [[0 for _ in range(16)] for _ in range(255)]
        self.num = 1
        self.blocksize = 50
        self.camerax = 0
        # 첫번째맵 함수로 빼든지 깔끔하게 수정필요

        # for i in range(0, 16):
        #     for j in range(0, 255):
        #         self.tile[j][i] = 0
        #
        # for i in range(0, 16):
        #     for j in range(0, 255):
        #        if i == 0:
        #             if j == 0:
        #                 for a in range(j, j+16):
        #                     self.tile[a][i] = 8; self.tile[a][i+1] = 8
        #             elif j == 127:
        #                 for a in range(j, j+40):
        #                     self.tile[a][i] = 8; self.tile[a][i+1] = 8
        #             elif j in [19, 20, 25, 26, 27, 28, 29, 30, 33, 36, 37, 38, 41, 42, 43, 44, 45, 51, 52, 60, 61, 62, 66, 67, 68,71,77,78,79,80,99,100,105,106,107,108,109,110,114,117,118,123,124]:
        #                 self.tile[j][i] = 19
        #        elif i == 1:
        #             if j in [19, 20, 25, 26, 27, 28, 29, 30, 33, 36, 37, 38, 41, 42, 43, 44, 45,71,77,78,79,80,99,100,105,106,107,108,109,110,117,118,123,124]:
        #                 self.tile[j][i] = 19
        #             elif j in [50,59,65,113]:
        #                 self.tile[j][i] = 16
        #             elif j in [51,52,60,61,62,66,67,68,114]:
        #                 self.tile[j][i] = 17
        #             elif j in [53,63,69,115]:
        #                 self.tile[j][i] = 18
        #        elif i == 2:
        #             if j == 0 or j == 153:
        #                 for a in range(j, j +5):
        #                     for b in range(i, i+5):
        #                         self.tile[a][b] = -1
        #                 self.tile[j][i] = 15
        #             elif j in [136,137,138,139,140,141]:
        #                 self.tile[j][i] = 7
        #             elif j in [18, 32]:
        #                 self.tile[j][i] = 16
        #             elif j in [19, 20, 33]:
        #                 self.tile[j][i] = 17
        #             elif j in [21, 34]:
        #                 self.tile[j][i] = 18
        #             elif j in [25, 26, 27, 28, 29, 30, 36, 37, 38, 41, 42, 43, 44, 45,61,62,71,77,78,79,80,99,100,105,106,107,108,109,110,117,118,123,124]:
        #                 self.tile[j][i] = 19
        #             elif j == 150:
        #                 for a in range(i, i+11):
        #                     self.tile[j][a] = -2
        #                 self.tile[j][i] = 13
        #             elif j == 156:
        #                 self.tile[j][i] = -3
        #        elif i == 3:
        #             if j in [25, 26, 27, 28, 29, 30, 36, 37, 38, 41, 42, 43, 44, 45,61,62,71,77,78,79,80,105,106,107,108,109,110,117,118,123,124]:
        #                 self.tile[j][i] = 19
        #             elif j in [98]:
        #                 self.tile[j][i] = 16
        #             elif j in [99,100]:
        #                 self.tile[j][i] = 17
        #             elif j in [101]:
        #                 self.tile[j][i] = 18
        #             elif j in [136,137,138,139,140,141]:
        #                 self.tile[j][i] = 7
        #        elif i == 4:
        #            if j in [25, 26, 27, 28, 29, 30, 36, 37, 38, 41, 42, 43, 44, 45,61,62,71,77,78,79,80,105,106,107,108,109,110,117,118,123,124]:
        #                self.tile[j][i] = 19
        #            elif j == 59:
        #                self.tile[j][i] = 5
        #            elif j in [136, 137, 138, 139, 140, 141]:
        #                self.tile[j][i] = 7
        #        elif i == 5:
        #            if j in [36, 37, 38, 41, 42, 43, 44, 45,61,62,77,78,79,80,105,106,107,108,109,110]:
        #                self.tile[j][i] = 19
        #            elif j in [24,70,116,122]:
        #                self.tile[j][i] = 16
        #            elif j in [25,26,27,28,29,30,71,117,118,123,124]:
        #                self.tile[j][i] = 17
        #            elif j in [31,72,119,125]:
        #                self.tile[j][i] = 18
        #            elif j in [94,95,96,136, 137, 138, 139, 140, 141]:
        #                self.tile[j][i] = 7
        #        elif i == 6:
        #            if j in [27,28,29,41,42,43,44,45,61,62,77,78,79,80,105,106,107,108,109,110]:
        #                self.tile[j][i] = 19
        #            elif j in [35]:
        #                self.tile[j][i] = 16
        #            elif j in [36,37,38]:
        #                self.tile[j][i] = 17
        #            elif j in [39]:
        #                self.tile[j][i] = 18
        #            elif j in [86,87,88,138, 139, 140, 141]:
        #                self.tile[j][i] = 7
        #        elif i == 7:
        #            if j in [27,28,29,41,42,43,44,45,61,62,77,78,79,80]:
        #                self.tile[j][i] = 19
        #            elif j in [104]:
        #                self.tile[j][i] = 16
        #            elif j in [105,106,107,108,109,110]:
        #                self.tile[j][i] = 17
        #            elif j in [111]:
        #                self.tile[j][i] = 18
        #            elif j in [138,139,140,141]:
        #                self.tile[j][i] = 7
        #        elif i == 8:
        #            if j in [27,28,29,41,42,43,44,45,61,62]:
        #                self.tile[j][i] = 19
        #            elif j in [76]:
        #                self.tile[j][i] = 16
        #            elif j in [77,78,79,80]:
        #                self.tile[j][i] = 17
        #            elif j in [81]:
        #                self.tile[j][i] = 18
        #            elif j in [140, 141]:
        #                self.tile[j][i] = 7
        #        elif i == 9:
        #            if j in [26,60]:
        #                self.tile[j][i] = 16
        #            elif j in [27,28,29,61,62]:
        #                self.tile[j][i] = 17
        #            elif j in [30,63]:
        #                self.tile[j][i] = 18
        #            elif j in [41,42,43,44,45]:
        #                self.tile[j][i] = 19
        #            elif j in [140, 141]:
        #                self.tile[j][i] = 7
        #        elif i == 10:
        #            if j in [40]:
        #                self.tile[j][i] = 16
        #            elif j in [41,42,43,44,45]:
        #                self.tile[j][i] = 17
        #            elif j == 46:
        #                self.tile[j][i] = 18
        #        elif i == 11:
        #            if j == 149:
        #                self.tile[j][i] = 14
        # for j in range(0, 255):
        #     for i in range(0, 16):
        #         print(self.tile[j][i])

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
                    elif self.tile[j][i] in range(16, 20):
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

