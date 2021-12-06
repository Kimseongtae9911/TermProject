import server
import game_world
from Mushroom import Mushroom
from Flower import Flower
import Character
import pico2d


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_Check_Box()
    left_b, bottom_b, right_b, top_b = b.get_Check_Box()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


def collide_base(a, b):
    left_a, bottom_a, right_a, top_a = a.get_Check_Box()
    for j in range(0, 254):
        left_b, bottom_b, right_b, top_b = b.get_Check_Box(1, j)
        left_c, bottom_c, right_c, top_c = b.get_Check_Box(1, j + 1)
        if bottom_a == top_b and server.mymap.tile[j][1] == 0 and left_a + 10 > left_b and right_a < right_b:
            return True
        elif bottom_a == top_b and server.mymap.tile[j][1] == 0 and server.mymap.tile[j+1][1] == 0 and left_a + 10 > left_b and right_a < right_c:
            return True

    return False


def collide_mario(a):
    left_a, bottom_a, right_a, top_a = a.get_Check_Box()

    checkx1 = int((left_a + server.mario.mapx) // 50)
    checkx2 = int((right_a + server.mario.mapx) // 50)
    checky1 = int(bottom_a // 50)
    checky2 = int(top_a // 50)

    left_1, bottom_1, right_1, top_1 = server.mymap.get_Check_Box(checky1, checkx1)
    left_2, bottom_2, right_2, top_2 = server.mymap.get_Check_Box(checky1, checkx2)
    left_3, bottom_3, right_3, top_3 = server.mymap.get_Check_Box(checky2, checkx1)
    left_4, bottom_4, right_4, top_4 = server.mymap.get_Check_Box(checky2, checkx2)

    if server.mario.cur_state == Character.JumpState:
        # 블럭의 윗부분과 마리오의 아래부분 충돌체크
        #아래 오른블럭과 체크
        if bottom_a <= top_2 and top_a >= top_2 and right_a >= left_2 and right_a <= right_2 and (server.mymap.tile[checkx2][checky1] != 0 and server.mymap.tile[checkx2][checky1] != 8 and
        server.mymap.tile[checkx2][checky1] != 9 and server.mymap.tile[checkx2][checky1] != 10 and server.mymap.tile[checkx2][checky1] != 11 and
        server.mymap.tile[checkx2][checky1] != 12 and server.mymap.tile[checkx2][checky1] != -1) and server.mario.jumpdir == -1:
            if server.mario.jumpdir == -1:
                server.mario.add_event(8)
                server.mario.jump = False
                server.mario.jumpdir = 1
            if server.mario.jump == False:
                server.mario.y = pico2d.clamp(top_1 + server.mymap.blocksize // 2, server.mario.y, top_1 + server.mymap.blocksize // 2)
            return 5
        # 아래 왼쪽블럭과 체크
        elif bottom_a <= top_1 and top_a >= top_1 and left_a >= left_1 and left_a <= right_1 and (server.mymap.tile[checkx1][checky1] != 0 and server.mymap.tile[checkx1][checky1] != 8 and
        server.mymap.tile[checkx1][checky1] != 9 and server.mymap.tile[checkx1][checky1] != 10 and server.mymap.tile[checkx1][checky1] != 11 and
        server.mymap.tile[checkx1][checky1] != 12 and server.mymap.tile[checkx1][checky1] != -1) and server.mario.jumpdir == -1:
            if server.mario.jumpdir == -1:
                server.mario.add_event(8)
                server.mario.jump = False
                server.mario.jumpdir = 1
            if server.mario.jump == False:
                server.mario.y = pico2d.clamp(top_1 + server.mymap.blocksize // 2, server.mario.y, top_1 + server.mymap.blocksize // 2)
            return 6
        # 위 왼쪽블럭과 체크
        elif top_a >= bottom_3 and bottom_a <= bottom_3 and left_a >= left_3 and left_a <= right_3 and (server.mymap.tile[checkx1][checky2] != 0 and server.mymap.tile[checkx1][checky2] != 8 and
        server.mymap.tile[checkx1][checky2] != 9 and server.mymap.tile[checkx1][checky2] != 10 and server.mymap.tile[checkx1][checky2] != 11 and
        server.mymap.tile[checkx1][checky2] != 12 and server.mymap.tile[checkx1][checky2] != -1):
            if server.mymap.tile[checkx1][checky2] == 5:
                if checkx1 == 16:
                    mushroom = Mushroom(checkx1 * server.mymap.blocksize + 25 - server.mario.mapx, (checky2 + 1) * server.mymap.blocksize)
                    game_world.add_object(mushroom, 1)
                elif checkx1 == 23:
                    print('Collide')
                    flower = Flower(checkx1 * server.mymap.blocksize + 25 - server.mario.mapx, (checky2 + 1) * server.mymap.blocksize)
                    game_world.add_object(flower, 1)
                server.mymap.tile[checkx1][checky2] = 7
            return 8
        # 위 오른블럭과 체크
        elif top_a >= bottom_4 and bottom_a <= bottom_4 and right_a >= left_4 and right_a <= right_4 and (server.mymap.tile[checkx2][checky2] != 0 and server.mymap.tile[checkx2][checky2] != 8 and
        server.mymap.tile[checkx2][checky2] != 9 and server.mymap.tile[checkx2][checky2] != 10 and server.mymap.tile[checkx2][checky2] != 11 and
        server.mymap.tile[checkx2][checky2] != 12 and server.mymap.tile[checkx2][checky2] != -1):
            if server.mymap.tile[checkx2][checky2] == 5:
                if checkx2 == 16:
                    mushroom = Mushroom(checkx2 * server.mymap.blocksize + 25 - server.mario.mapx, (checky2 + 1) * server.mymap.blocksize)
                    game_world.add_object(mushroom, 1)
                elif checkx2 == 23:
                    print('Collide')
                    flower = Flower(checkx2 * server.mymap.blocksize + 25 - server.mario.mapx, (checky2 + 1) * server.mymap.blocksize)
                    game_world.add_object(flower, 1)
                server.mymap.tile[checkx2][checky2] = 7
            return 8
        elif right_a + 1 >= left_2 and left_a <= right_2 and (server.mymap.tile[checkx2][checky1] != 0 and server.mymap.tile[checkx2][checky1] != 8 and
        server.mymap.tile[checkx2][checky1] != 9 and server.mymap.tile[checkx2][checky1] != 10 and server.mymap.tile[checkx2][checky1] != 11 and
        server.mymap.tile[checkx2][checky1] != 12 and server.mymap.tile[checkx2][checky1] != -1) and server.mario.dir == 1:
            server.mario.x = pico2d.clamp(left_2 - server.mario.mariosizex // 2 - 1, server.mario.x, left_2 - server.mario.mariosizex // 2 - 1)
            return 3

        # 왼쪽으로 이동할때
        elif left_a <= right_1 and right_a >= right_1 and (server.mymap.tile[checkx1][checky1] != 0 and server.mymap.tile[checkx1][checky1] != 8 and
        server.mymap.tile[checkx1][checky1] != 9 and server.mymap.tile[checkx1][checky1] != 10 and server.mymap.tile[checkx1][checky1] != 11 and
        server.mymap.tile[checkx1][checky1] != 12 and server.mymap.tile[checkx1][checky1] != -1):
            server.mario.x = pico2d.clamp(right_1 + server.mario.mariosizex // 2 + 1, server.mario.x, right_1 + server.mario.mariosizex // 2 + 1)
            return 3

    # 마리오가 땅에서 이동할때 충돌체크
    elif server.mario.cur_state == Character.RunState or server.mario.cur_state == Character.DashState or server.mario.cur_state == Character.AccState:
        # 오른쪽으로 이동할때
        if right_a + 1 >= left_2 and left_a <= right_2 and (server.mymap.tile[checkx2][checky1] != 0 and server.mymap.tile[checkx2][checky1] != 8 and
        server.mymap.tile[checkx2][checky1] != 9 and server.mymap.tile[checkx2][checky1] != 10 and server.mymap.tile[checkx2][checky1] != 11 and
        server.mymap.tile[checkx2][checky1] != 12 and server.mymap.tile[checkx2][checky1] != -1) and server.mario.dir == 1:
            server.mario.x = pico2d.clamp(left_2 - server.mario.mariosizex // 2 - 1, server.mario.x, left_2 - server.mario.mariosizex // 2 - 1)
            return 1
        # 왼쪽으로 이동할때
        elif left_a <= right_1 and right_a >= right_1 and (server.mymap.tile[checkx1][checky1] != 0 and server.mymap.tile[checkx1][checky1] != 8 and
        server.mymap.tile[checkx1][checky1] != 9 and server.mymap.tile[checkx1][checky1] != 10 and server.mymap.tile[checkx1][checky1] != 11 and
        server.mymap.tile[checkx1][checky1] != 12 and server.mymap.tile[checkx1][checky1] != -1):
            server.mario.x = pico2d.clamp(right_1 + server.mario.mariosizex // 2 + 1, server.mario.x, right_1 + server.mario.mariosizex // 2 + 1)
            return 2

        # 밑에 블럭이 없으면 떨어져야한다
        elif server.mymap.tile[checkx1][checky1 - 1] == 0 and server.mymap.tile[checkx2][checky1 - 1] == 0:
            server.mario.jumpdir = -1
            server.mario.add_event(7)
            return 7
    return 0
