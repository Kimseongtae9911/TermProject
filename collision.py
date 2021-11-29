import server
import game_world
from Mushroom import Mushroom
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
        pass
    # 마리오가 땅에서 이동할때 충돌체크
    elif server.mario.cur_state == Character.RunState or server.mario.cur_state == Character.DashState or server.mario.cur_state == Character.AccState:
        # 오른쪽으로 이동할때
        if right_a + 1 >= left_2 and left_a <= right_2 and (server.mymap.tile1[checkx2][checky1] != 0 and server.mymap.tile1[checkx2][checky1] != 1 and
        server.mymap.tile1[checkx2][checky1] != 9 and server.mymap.tile1[checkx2][checky1] != 10 and server.mymap.tile1[checkx2][checky1] != 11 and
        server.mymap.tile1[checkx2][checky1] != 12 and server.mymap.tile1[checkx2][checky1] != -1) and server.mario.dir == 1:
            server.mario.x = pico2d.clamp(left_2 - server.mario.mariosizex // 2 - 1, server.mario.x, left_2 - server.mario.mariosizex // 2 - 1)
            return 1
        # 왼쪽으로 이동할때
        elif left_a <= right_1 and right_a >= right_1 and (server.mymap.tile1[checkx1][checky1] != 0 and server.mymap.tile1[checkx1][checky1] != 1 and
        server.mymap.tile1[checkx1][checky1] != 9 and server.mymap.tile1[checkx1][checky1] != 10 and server.mymap.tile1[checkx1][checky1] != 11 and
        server.mymap.tile1[checkx1][checky1] != 12 and server.mymap.tile1[checkx1][checky1] != -1):
            # print(server.mymap.tile1[checkx1][checky1])
            server.mario.x = pico2d.clamp(right_1 + server.mario.mariosizex // 2 + 1, server.mario.x, right_1 + server.mario.mariosizex // 2 + 1)
            return 2

    return 0

def collide_base(a, b):
    left_a, bottom_a, right_a, top_a = a.get_Check_Box()
    for j in range(0, 254):
        left_b, bottom_b, right_b, top_b = b.get_Check_Box(1, j)
        left_c, bottom_c, right_c, top_c = b.get_Check_Box(1, j + 1)
        if bottom_a == top_b and server.mymap.tile1[j][1] == 0 and left_a + 10 > left_b and right_a < right_b:
            return True
        elif bottom_a == top_b and server.mymap.tile1[j][1] == 0 and server.mymap.tile1[j+1][1] == 0 and left_a + 10 > left_b and right_a < right_c:
            return True

    return False


def collide_ques(a, b): # 5, 9
    left_a, bottom_a, right_a, top_a = a.get_Check_Box()
    for j in range(0, 254):
        left_b, bottom_b, right_b, top_b = b.get_Check_Box(5, j)
        left_c, bottom_c, right_c, top_c = b.get_Check_Box(9, j)
        if top_a + 10>= bottom_b and bottom_a <= bottom_b and server.mymap.tile1[j][5] == 6 and ((right_a > left_b and left_a < right_b) or (left_a < right_b and right_a > left_b)):
            server.mymap.tile1[j][5] = 8
            if j == 16:
                mushroom = Mushroom(j * 50 + 25, 300)
                game_world.add_object(mushroom, 1)
            return 1
        elif top_a >= bottom_c and bottom_a <= bottom_c and server.mymap.tile1[j][9] == 6 and ((right_a > left_c and left_a < right_c) or (left_a < right_c and right_a > left_c)):
            return 1
        elif bottom_a <= top_b and bottom_a >= bottom_b and server.mymap.tile1[j][5] == 6 and ((right_a > left_b and left_a < right_b) or (left_a < right_b and right_a > left_b)):
            print("Collide")
            return 2
        elif bottom_a <= top_c and bottom_a >= bottom_c and server.mymap.tile1[j][9] == 6 and ((right_a > left_c and left_a < right_c)  or (left_a < right_c and right_a > left_c)):
            print("Collide")
            return 2
    return 0
