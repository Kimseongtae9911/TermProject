import server
import game_world
from Mushroom import Mushroom


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_Check_Box()
    if(b == server.mymap):
        for i in range(0, 16):
            for j in range(0, 255):
                left_b, bottom_b, right_b, top_b = b.get_Check_Box(i, j)
    else:
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
        if bottom_a + 2 == top_b and server.mymap.tile1[j][1] == 0 and left_a + 10 > left_b and right_a < right_b:
            return True
        elif bottom_a + 2 == top_b and server.mymap.tile1[j][1] == 0 and server.mymap.tile1[j+1][1] == 0 and left_a + 10 > left_b and right_a < right_c:
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


def collide_block(a, b):
    left_a, bottom_a, right_a, top_a = a.get_Check_Box()
    for j in range(0, 254):
        left_b, bottom_b, right_b, top_b = b.get_Check_Box(5, j)
        left_c, bottom_c, right_c, top_c = b.get_Check_Box(9, j)
        if top_a + 10 >= bottom_b and bottom_a <= bottom_b and server.mymap.tile1[j][5] == 8 and ((right_a > left_b and left_a < right_b) or (left_a < right_b and right_a > left_b)):
            return True
        elif top_a >= bottom_c and bottom_a <= bottom_c and server.mymap.tile1[j][9] == 8 and ((right_a > left_c and left_a < right_c) or (left_a < right_c and right_a > left_c)):
            return True

    return False


def collide_brick(a, b):
    left_a, bottom_a, right_a, top_a = a.get_Check_Box()
    for j in range(0, 254):
        left_b, bottom_b, right_b, top_b = b.get_Check_Box(5, j)
        left_c, bottom_c, right_c, top_c = b.get_Check_Box(9, j)
        if top_a + 10 >= bottom_b and bottom_a <= bottom_b and server.mymap.tile1[j][5] == 7 and ((right_a > left_b and left_a < right_b) or (left_a < right_b and right_a > left_b)):
            return True
        elif top_a >= bottom_c and bottom_a <= bottom_c and server.mymap.tile1[j][9] == 7 and ((right_a > left_c and left_a < right_c) or (left_a < right_c and right_a > left_c)):
            return True

    return False
