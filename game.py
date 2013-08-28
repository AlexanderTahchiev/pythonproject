import pygame
import sys
from pygame.locals import *
from math import pi
import math
pygame.init()


class Colors:
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    KINDA_GREEN = (0, 180, 0)
    RED = (255, 0, 0)


WINDOWHEIGHT = 860
WINDOWLENGTH = 640
POINTRADIUS = 3

NUMBER_OF_POINTS = 6
DISTANCE_FROM_POINT = 10

mousex = 0
mousey = 0
DISPLAYSURF = pygame.display.set_mode((WINDOWHEIGHT, WINDOWLENGTH), 0, 32)
DISPLAYSURF.fill(Colors.BLACK)
pygame.display.set_caption('THE GAME!')
class cat:
    love = 1

def main():
    global all_points_centers, all_points, prctective_area_of_points, dict_of_canters_points
    global prctective_area_of_lines, all_lines_ends, all_lines, dict_of_points_centers
    global last_line_ends, map_between_point_forbpoints, dict_of_canters_points, dict_of_points_centers
    all_points_centers = []
    all_points = []
    prctective_area_of_points = []
    prctective_area_of_lines = []
    all_lines = []
    all_lines_ends = []
    dict_of_points_centers = dict()

    CAN_WE_LINE = False
    while len(all_points_centers) < NUMBER_OF_POINTS:
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                terminate()
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = (event.pos[0], event.pos[1])
                if IfPointAreaAtClick(mousex, mousey):
                    pass
                elif len(all_points_centers) > 1:
                    if compare_all_points_with_new_one(all_points_centers, (mousex, mousey)):
                        pass
                    else:
                        draw_point(mousex, mousey, Colors.GREEN)
                else:
                    draw_point(mousex, mousey, Colors.GREEN)

            pygame.display.update()

    dict_of_points_centers = creat_dict_of_points_centers(
        all_points_centers)[0]
    dict_of_canters_points = creat_dict_of_points_centers(
        all_points_centers)[1]
    map_between_point_forbpoints = making_dict_of_points_names()
    print("dict_of_points_centers", dict_of_points_centers)
    print("map_between_point_forbpoints", map_between_point_forbpoints)
    print("dict_of_canters_points", dict_of_canters_points)
    print("all_points_centers", all_points_centers)
    print("all_lines_ends", all_lines_ends)
    last_line_ends = []
    while True:  # main game loop
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                terminate()
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = (event.pos[0], event.pos[1])
                if IfPointAtClick(mousex, mousey) and CAN_WE_LINE:
                    last_line_ends.append(IfPointAtClickReturn(mousex, mousey))

                    if can_we_lineup(last_line_ends):
                        add_forbiden_points(last_line_ends)
                        second_point = IfPointAtClickReturn(mousex, mousey)
                        draw_point(first_point[0], first_point[1], Colors.GREEN)
                        draw_line(
                            DISPLAYSURF, Colors.GREEN, first_point, second_point, 5)
                        second_point = False
                    elif not can_we_lineup(last_line_ends):
                        draw_point(first_point[0], first_point[1], Colors.GREEN)
                        second_point = False
                    print("map_between_point_forbpoints", map_between_point_forbpoints)
                    print("all_lines_ends", all_lines_ends) 
                if IfPointAtClick(mousex, mousey) and CAN_WE_LINE:
                    CAN_WE_LINE = False
                    last_line_ends = []

                elif IfPointAtClick(mousex, mousey):
                    last_line_ends.append(IfPointAtClickReturn(mousex, mousey))
                    first_point = IfPointAtClickReturn(mousex, mousey)
                    draw_point(first_point[0], first_point[1], Colors.RED)
                    CAN_WE_LINE = True

        pygame.display.update()


def IfPointAtClick(mousex, mousey):
    for i in prctective_area_of_points:
        if i.collidepoint(mousex, mousey):
            for j in all_points_centers:
                if i.collidepoint(j):
                    return True
    return False


def IfPointAtClickReturn(mousex, mousey):
    for i in prctective_area_of_points:
        if i.collidepoint(mousex, mousey):
            for j in all_points_centers:
                if i.collidepoint(j):
                    return j


def draw_point(mousex, mousey, color):
    if (mousex, mousey) in all_points_centers:
        pygame.draw.circle(
            DISPLAYSURF, color, (mousex, mousey), POINTRADIUS, 0)
        prctective_area_of_points.append(pygame.draw.ellipse(
            DISPLAYSURF,
            color,
            [mousex - 15, mousey - 15, 30, 30],
            1))
    else:
        all_points_centers.append((mousex, mousey))
        all_points.append(pygame.draw.circle(
            DISPLAYSURF, color, (mousex, mousey), POINTRADIUS, 0))
        prctective_area_of_points.append(pygame.draw.ellipse(
            DISPLAYSURF,
            color,
            [mousex - 15, mousey - 15, 30, 30],
            1))

#construktori

def creat_dict_of_points_centers(all_points_centers):
    dict_of_points_centers = dict()
    dict_of_canters_points = {}
    j = 0
    for i in all_points_centers:
        dict_of_points_centers[j] = i
        dict_of_canters_points[i] = j
        j = j + 1
    return dict_of_points_centers, dict_of_canters_points


def making_dict_of_points_names():
    map_between_point_forbpoints = dict()
    for i in range(NUMBER_OF_POINTS):
        map_between_point_forbpoints[i] = [i]
    return map_between_point_forbpoints


def returned_points(mousex, mousey, dict_of_points_centers):
    return dict_of_canters_points[(mousex, mousey)]

#zapisva q po dvata nachina (A,B), (B,A)
def draw_line(surf, color, point1, point2, thickness, ):
    if (point1,point2) in all_lines_ends:
        pass
    elif point1==point2:
        pass
    else:
        all_lines_ends.append((point1, point2))
        all_lines_ends.append((point2, point1))
        all_lines.append(pygame.draw.line(
            DISPLAYSURF, Colors.GREEN, point1, point2, thickness))
        return pygame.draw.line(DISPLAYSURF, Colors.GREEN, point1, point2, thickness)


#nad tezi dam islq

def caluclate_line_by_2_points(point1, point2):
    if point1[0] == point2[0]:
        return 0, point1[1]
    a = (point1[1] - point2[1]) / (point1[0] - point2[0])
    b = point1[1] - point1[0] * a
    return a, b


def add_forbiden_points(last_line_ends):
    point1 = last_line_ends[0]
    point2 = last_line_ends[1]
    pot_line = caluclate_line_by_2_points(point1, point2)
    if point1 == point2:
        pass
    else:

        for i in all_points_centers:
            for j in all_points_centers:
                rand_line =  caluclate_line_by_2_points(i, j)              
                #ako sa v edna polu ravnina i po golemi ot pravata i
                if i == j or i in last_line_ends or j in last_line_ends:
                    pass
                elif i in last_line_ends and j not in last_line_ends:
                    pass
                elif j in last_line_ends and i not in last_line_ends:
                    pass
                elif pot_line[0]*i[0] + pot_line[1] < i[1] and pot_line[0]*j[0] + pot_line[1] < j[1]:
                    pass
                elif pot_line[0]*i[0] + pot_line[1] >= i[1] and pot_line[0]*j[0] + pot_line[1] >= j[1]:
                    pass

                elif rand_line[0]*point1[0] + rand_line[1] < point1[1] and rand_line[0]*point2[0] + rand_line[1] < point2[1]:
                    pass
                elif rand_line[0]*point1[0] + rand_line[1] > point1[1] and rand_line[0]*point2[0] + rand_line[1] > point2[1]:
                    pass
                else:
                    point_key1 = dict_of_canters_points[i]
                    point_key2 = dict_of_canters_points[j]
                    map_between_point_forbpoints[point_key1].append(dict_of_canters_points[j])
                    map_between_point_forbpoints[point_key2].append(dict_of_canters_points[i])
                    map_between_point_forbpoints[point_key2] = list(set(map_between_point_forbpoints[point_key2]))
                    map_between_point_forbpoints[point_key1] = list(set(map_between_point_forbpoints[point_key1]))


def calculate_line_value(a_b,point):
    return round(a_b[0]*point[0] + a_b[1])



def ispnt_underorabove(line, point):
    if line[0]*point[0] + line[1] < point[1]:
        return 1
    elif line[0]*point[0] + line[1] > point[1]:
        return 2
    else:
        return 0

def can_we_lineup(last_line_ends):
    point1 = last_line_ends[0]
    point2 = last_line_ends[1]
    p1 = dict_of_canters_points[point1]
    p2 = dict_of_canters_points[point2]
    if point1 == point2:
        return False
    if p2 in map_between_point_forbpoints[dict_of_canters_points[point1]]:
        return False
    if p1 in map_between_point_forbpoints[dict_of_canters_points[point2]]:
        return False
    return True


# tezi sa samo vuv purviq while


def IfPointAreaAtClick(mousex, mousey):
    for i in prctective_area_of_points:
        if i.collidepoint(mousex, mousey):
            return True
    return False




def dist_between_point_and_line(point1, point2, point3):
    lineeq = caluclate_line_by_2_points(point1, point2)
    return round(abs((lineeq[0] * point3[0] - point3[1] + lineeq[1]) / (((lineeq[0]) ** 2 + 1) ** 0.5)))


def compare_all_points_with_new_one(all_points_centers, new_point_center):
    n = len(all_points_centers)
    for i in range(n):
        for j in range(i + 1, n):
            if dist_between_point_and_line(all_points_centers[i], all_points_centers[j], new_point_center) < DISTANCE_FROM_POINT:
                return True
    return False



# tezi hich ne gi polzvam ma da sedqt
def IfLineAtClick(mousex, mousey):
    for i in prctective_area_of_lines:

        if i.collidepoint(mousex, mousey):
            return True
    return False


def PointVector(point):
    x = point[0]
    y = point[1]
    r = (x ** 2 + y ** 2) ** 0.5
    sin = y / r
    cos = x / r
    return cos, sin


def terminate():
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
