import pygame
import sys
from pygame.locals import *
from math import pi
import math

pygame.init()
pygame.display.set_caption('THE GAME!')


class Colors:
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    KINDA_GREEN = (0, 180, 0)


class Point():
    x_of_ellipse = 30
    y_of_ellipse = 30
    ellipse_center_margin_x = x_of_ellipse / 2
    ellipse_center_margin_y = y_of_ellipse / 2 

    def __init__(self, pointradius, color ):
        self.color = color
        self.pointradius = pointradius

    def draw_point(self):
        mousex = self.pointradius[0]
        mousey = self.pointradius[1]
        all_points_centers.append((mousex, mousey))
        all_points.append(pygame.draw.circle(
            DISPLAYSURF, 
            self.color, 
            (mousex, mousey), 
            POINTRADIUS, 
            0))
        prctective_area_of_points.append(
            pygame.draw.ellipse(
            DISPLAYSURF, self.color, 
            [mousex - self.ellipse_center_margin_x, 
            mousey - self.ellipse_center_margin_y, 
            self.x_of_ellipse, 
            self.x_of_ellipse
            ], 
            1))

    def draw_point_no_copy(self):
        mousex = self.pointradius[0]
        mousey = self.pointradius[1]
        pygame.draw.circle(
            DISPLAYSURF, 
            self.color, 
            (mousex, mousey), 
            POINTRADIUS, 
            0)
        pygame.draw.ellipse(
            DISPLAYSURF, self.color, 
            [mousex - self.ellipse_center_margin_x, 
            mousey - self.ellipse_center_margin_y, 
            self.x_of_ellipse, 
            self.x_of_ellipse
            ], 
            1)

NUMBER_OF_POINTS = 7
POINTRADIUS = 3
DISTANCE_FROM_POINT = 10


WINDOWHEIGHT = 1200
WINDOWLENGTH = 700
DISPLAYSURF = pygame.display.set_mode((WINDOWHEIGHT, WINDOWLENGTH), 0, 32)
DISPLAYSURF.fill(Colors.BLACK)


def main():
    global all_points_centers, all_points, prctective_area_of_points

    global first_point, all_lines_ends, all_lines

    all_points_centers = []
    all_points = []
    prctective_area_of_points = []

    all_lines = []
    all_lines_ends = []

    first_point = (None, None)

    dict_of_all_lines = {}
    CAN_WE_LINE = False
    while len(all_points_centers) < NUMBER_OF_POINTS:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                terminate()
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = (event.pos[0], event.pos[1])
                if IfPointAreaAtClick(mousex, mousey):
                    pass
                    if compare_all_points_with_new_one(all_points_centers, (mousex, mousey)):
                        pass
                else:
                    momentpoint = Point((mousex, mousey), Colors.GREEN)
                    momentpoint.draw_point()
            pygame.display.update()

    dict_of_points = all_points_centers_in_dict(all_points_centers, {})
    print(dict_of_points)
    print(prctective_area_of_points)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                terminate()
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = (event.pos[0], event.pos[1])
                if IfPointAtClick(mousex, mousey) and CAN_WE_LINE:
                    momentpoint = Point((first_point[0], first_point[1]), Colors.GREEN)
                    momentpoint.draw_point_no_copy()
                    second_point = IfPointAtClickReturn(mousex, mousey)
                    draw_line(DISPLAYSURF, Colors.GREEN, first_point, second_point, 5)
                    add_line_ends_in_dict((first_point, second_point), dict_of_all_lines)
                    print(all_points_centers)
                    print(dict_of_all_lines)
                    second_point = False
                if IfPointAtClick(mousex, mousey) and CAN_WE_LINE:
                    CAN_WE_LINE = False
                elif IfPointAtClick(mousex, mousey):
                    first_point = IfPointAtClickReturn(mousex, mousey)
                    momentpoint = Point((first_point[0], first_point[1]), Colors.RED)
                    momentpoint.draw_point_no_copy()
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




def draw_line(surf, color, point1, point2, thickness):
    all_lines_ends.append((point1, point2))
    all_lines.append(pygame.draw.line(
        DISPLAYSURF, Colors.GREEN, point1, point2, thickness))
    return pygame.draw.line(DISPLAYSURF, Colors.GREEN, point1, point2, thickness)


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
            if dist_between_point_and_line(all_points_centers[i], all_points_centers[j], new_point_center) < DISTANCE_FROM_POINT:
                return True
    return False

def all_points_centers_in_dict(all_points_centers, the_dict):
    for i in range(NUMBER_OF_POINTS):
        the_dict[i] = all_points_centers[i]
    return the_dict

def add_line_ends_in_dict(line_ends, the_dict):
    for i in range(round((NUMBER_OF_POINTS*(NUMBER_OF_POINTS-1))/2 + 3)):
        the_dict[i] = line_ends
        yield the_dict


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
