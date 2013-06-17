import pygame
import sys
from pygame.locals import *
from math import pi
import math
pygame.init()
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
KINDA_GREEN = (0, 180, 0)
WINDOWHEIGHT = 1200
WINDOWLENGTH = 700
POINTRADIUS = 3
NUMBER_OF_POINTS = 21
DISTANCE_BETWEEN_POINTS = 15
mousex = 0
mousey = 0
DISPLAYSURF = pygame.display.set_mode((WINDOWHEIGHT, WINDOWLENGTH), 0, 32)
DISPLAYSURF.fill(BLACK)
pygame.display.set_caption('THE GAME!')


def main():
    global all_points_centers, all_points, prctective_area_of_points
    global first_point, prctective_area_of_lines, all_lines_ends, all_lines
    all_points_centers = []
    all_points = []
    prctective_area_of_points = []
    prctective_area_of_lines = []
    all_lines = []
    all_lines_ends = []



    first_point = (None, None)
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
                            forbiden_lines = visual_forbiden_area(all_points_centers, (mousex, mousey))
                            for i in forbiden_lines:
                                if i[0] == None:
                                    pass
                                else:
                                    p1_x = i[0][0]
                                    p1_y = i[0][1]
                                    p2_x = i[1][0]
                                    p2_y = i[1][1]
                                    new_b = i[2]
                                    draw_point(mousex, mousey)
                                    draw_line(DISPLAYSURF, RED, (p1_x,p1_y+new_b) , (p2_x,p2_y+new_b), 1)
                                    draw_line(DISPLAYSURF, RED, (p1_x,p1_y-new_b) , (p2_x,p2_y-new_b), 1)
                                
                    else:
                        draw_point(mousex, mousey)

                pygame.display.update()
    while True:  # main game loop
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                terminate()
            elif event.type == MOUSEBUTTONUP:
                    mousex, mousey = (event.pos[0], event.pos[1])
                    if IfPointAtClick(mousex, mousey) and CAN_WE_LINE:
                        second_point = IfPointAtClickReturn(mousex, mousey)
                        draw_line(
                            DISPLAYSURF, GREEN, first_point, second_point, 5)
                        second_point = False
                    if IfPointAtClick(mousex, mousey) and CAN_WE_LINE:
                        CAN_WE_LINE = False
                    elif IfPointAtClick(mousex, mousey):
                        first_point = IfPointAtClickReturn(mousex, mousey)
                        CAN_WE_LINE = True
        pygame.display.update()


def IfPointAreaAtClick(mousex, mousey):
    for i in prctective_area_of_points:
            if i.collidepoint(mousex, mousey):
                return True
    return False


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


def draw_point(mousex, mousey):
    all_points_centers.append((mousex, mousey))
    all_points.append(pygame.draw.circle(
        DISPLAYSURF, GREEN, (mousex, mousey), POINTRADIUS, 0))
    prctective_area_of_points.append(pygame.draw.ellipse(
        DISPLAYSURF, GREEN, [mousex - 15, mousey - 15, 30, 30], 1))
    return pygame.draw.circle(DISPLAYSURF, GREEN, (mousex, mousey), POINTRADIUS, 0)




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


def draw_line(surf, color, point1, point2, thickness):
    all_lines_ends.append((point1, point2))
    all_lines.append(pygame.draw.line(
        DISPLAYSURF, GREEN, point1, point2, thickness))
    return pygame.draw.line(DISPLAYSURF, GREEN, point1, point2, thickness)


def caluclate_line_by_2_points(point1, point2):
    if point1[0] == point2[0]:
        return 0, point1[1]
    a = (point1[1] - point2[1]) / (point1[0] - point2[0])
    b = point1[1] - point1[0] * a
    return a, b


def dist_between_point_and_line(point1, point2, point3):
    lineeq = caluclate_line_by_2_points(point1, point2)
    return round(abs((lineeq[0] * point3[0] - point3[1] + lineeq[1]) / (((lineeq[0]) ** 2 + 1) ** 0.5)))


def compare_all_points_with_new_one(all_points_centers, new_point_center):
    n = len(all_points_centers)
    for i in range(n):
        for j in range(i + 1, n):
            if dist_between_point_and_line(all_points_centers[i], all_points_centers[j], new_point_center) < DISTANCE_BETWEEN_POINTS:
                return True
    return False

def visual_forbiden_area(all_points_centers, new_point_center):
    n = len(all_points_centers)
    for i in range(n):
        for j in range(i + 1, n):
            the_dist = DISTANCE_BETWEEN_POINTS
            a, b = caluclate_line_by_2_points(all_points_centers[i], all_points_centers[j])
            if a != 0 :
                new_b = ((the_dist/a)**2 + the_dist ** 2)**0.5
                yield all_points_centers[i], all_points_centers[j], new_b
            yield None, None, None
def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()

