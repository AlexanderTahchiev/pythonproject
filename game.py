import pygame
import sys
from pygame.locals import *
from math import pi
import math


def menu():
    return sys.path.append('~/mypy/proect/menu_key/menu.py')

pygame.init()


class Colors:

    """klas za cvetovete"""
    YELLOW = (255, 255, 0)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    KINDA_GREEN = (0, 180, 0)
    RED = (255, 0, 0)


WINDOWHEIGHT = 1200
WINDOWLENGTH = 800
POINTRADIUS = 3

NUMBER_OF_POINTS = 5
DISTANCE_FROM_POINT = 5

mousex = 0
mousey = 0

DISPLAYSURF = pygame.display.set_mode((WINDOWHEIGHT, WINDOWLENGTH), 0, 32)
DISPLAYSURF.fill(Colors.BLACK)
pygame.display.set_caption('THE GAME!')


class AI:

    def __init__(self, name, turn, points, pos):
        self.turn = turn
        self.points = points
        self.name = name
        self.pos = pos


class Point:
    pass


class Line:
    pass


class Player:

    """Vsichko nujna informacia koqto trqbva da se sledi za igracha
    na tozi etap """

    def __init__(self, name, turn, points, pos):
        self.turn = turn
        self.points = points
        self.name = name
        self.pos = pos
    old_points = 0
    number_of_drawen_points = 0

    def get_points(self):
        return self.points

    def moi_red_li_e(self):
        return self.turn

    def return_all_lines(self, last_line_ends):
        all_line_from_point = []
        for i in all_lines_ends:
            if i[0] == last_line_ends[0] or i[1] == last_line_ends[0]:
                all_line_from_point.append(i)
        return all_line_from_point

    def in_event_of_point(self, other, last_line_ends):
        point1 = last_line_ends[0]
        point2 = last_line_ends[1]
        number_of_made_points = 0
        all_returned_lines = self.return_all_lines(last_line_ends)
        if tuple(last_line_ends) in all_lines_ends:
            return
        for i in all_returned_lines:
            if (i[0], point2) in all_lines_ends:
                number_of_made_points = number_of_made_points + 1
        if number_of_made_points == 0 and len(last_line_ends) == 2:
            self.turn = not self.turn
            other.turn = not other.turn
        else:
            if number_of_made_points > 2:
                self.points = self.points + 2
            else:
                self.points = self.points + number_of_made_points

    def display_turn(self):
        if self.moi_red_li_e():
            clear_turn = pygame.draw.polygon(DISPLAYSURF, Colors.RED, [
                                             (450 - 20, 10 - 5), (450 + 120, 10 - 5), (450 + 120, 10 + 20), (450 - 20, 10 + 20)])
            number_of_drawen_points = len(all_points)
            whos_turn = myfont.render(self.name + " turn", 1, Colors.YELLOW)
            return DISPLAYSURF.blit(whos_turn, (450, 10))

    def display_points(self):
        poin = myfont.render(str(self.points), 1, Colors.YELLOW)
        if self.old_points < self.points:

            pygame.draw.polygon(DISPLAYSURF, Colors.BLACK, [(self.pos[0] - 7, self.pos[1] - 7), (
                self.pos[0] + 20, self.pos[1] - 7), (self.pos[0] + 20, self.pos[1] + 20), (self.pos[0] - 7, self.pos[1] + 20)])

            self.old_points = self.points
        return DISPLAYSURF.blit(poin, self.pos)

    def get_stats(self):
        print(self.name, ":", self.points, " ", self.turn)

myfont = pygame.font.SysFont("Comic Sans MS", 25)
Pl1 = myfont.render("Player1:", 1, Colors.YELLOW)
Pl2 = myfont.render("Player2:", 1, Colors.YELLOW)
DISPLAYSURF.blit(Pl1, (20, 10))
DISPLAYSURF.blit(Pl2, (135, 10))


Player1 = Player("Player1", True, 0, (100, 10))
Player2 = Player("Player2", False, 0, (230, 10))


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
    # pygame.display.toggle_fullscreen()

    CAN_WE_LINE = False
    while len(all_points_centers) < NUMBER_OF_POINTS:
        """Purviq cikul dokato se napravqt n na broi tochki"""
        Player1.display_turn()
        Player2.display_turn()
        for event in pygame.event.get():
            Player1.display_points()
            Player2.display_points()
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                terminate()
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = (event.pos[0], event.pos[1])
                if IfPointAreaAtClick(mousex, mousey) or mousey < 35:
                    pass
                elif len(all_points_centers) > 1:
                    if compare_all_points_with_new_one(all_points_centers, (mousex, mousey)):
                        pass
                    else:
                        draw_point(mousex, mousey, Colors.GREEN)
                        Player1.turn = not Player1.turn
                        Player2.turn = not Player2.turn
                        Player1.display_turn()
                        Player2.display_turn()
                else:
                    draw_point(mousex, mousey, Colors.GREEN)
                    Player1.turn = not Player1.turn
                    Player2.turn = not Player2.turn
                    Player1.display_turn()
                    Player2.display_turn()
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
        """cikul do kogato se stigne kraq na igrata"""
        for event in pygame.event.get():
            Player1.display_points()
            Player2.display_points()
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                terminate()

            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = (event.pos[0], event.pos[1])
                if IfPointAtClick(mousex, mousey) and CAN_WE_LINE:
                    last_line_ends.append(IfPointAtClickReturn(mousex, mousey))
                    if can_we_lineup(last_line_ends):
                        add_forbiden_points(last_line_ends)
                        second_point = IfPointAtClickReturn(mousex, mousey)
                        draw_point(
                            first_point[0], first_point[1], Colors.GREEN)
                        print(tuple(last_line_ends), all_lines_ends)
                        if Player1.moi_red_li_e():
                            Player1.in_event_of_point(Player2, last_line_ends)
                        else:
                            Player2.in_event_of_point(Player1, last_line_ends)
                        print(Player1.turn)
                        print(Player2.turn)
                        Player1.get_stats()
                        Player2.get_stats()
                        draw_line(
                            DISPLAYSURF, Colors.GREEN, first_point, second_point, 5)
                        Player2.display_turn()
                        Player1.display_turn()
                        second_point = False
                    elif not can_we_lineup(last_line_ends):
                        draw_point(
                            first_point[0], first_point[1], Colors.GREEN)
                        second_point = False
                if IfPointAtClick(mousex, mousey) and CAN_WE_LINE:
                    CAN_WE_LINE = False
                    last_line_ends = []

                elif IfPointAtClick(mousex, mousey):
                    last_line_ends.append(IfPointAtClickReturn(mousex, mousey))
                    first_point = IfPointAtClickReturn(mousex, mousey)
                    draw_point(first_point[0], first_point[1], Colors.RED)
                    CAN_WE_LINE = True

            if not did_it_end():
                if Player1.get_points() > Player2.get_points():
                    winner = myfont.render("Player1 won", 1, Colors.YELLOW)
                    DISPLAYSURF.blit(winner, (WINDOWHEIGHT - 100,  10))
                    print("Player1 won")
                elif Player1.get_points() < Player2.get_points():
                    winner = myfont.render("Player2 won", 1, Colors.YELLOW)
                    DISPLAYSURF.blit(winner, (WINDOWHEIGHT - 150,  10))
                    print("Player2 won")
                else:
                    winner = myfont.render("Draw", 1, Colors.YELLOW)
                    DISPLAYSURF.blit(winner, (WINDOWHEIGHT - 150,  10))
                    print("Draw")
        pygame.display.update()


def IfPointAtClick(mousex, mousey):
    """ako e cuknata tochka vrushta True"""
    for i in prctective_area_of_points:
        if i.collidepoint(mousex, mousey):
            for j in all_points_centers:
                if i.collidepoint(j):
                    return True
    return False


def IfPointAtClickReturn(mousex, mousey):
    """ako e cuknata tochka vrushta cukanata tochka"""
    for i in prctective_area_of_points:
        if i.collidepoint(mousex, mousey):
            for j in all_points_centers:
                if i.collidepoint(j):
                    return j


def draw_point(mousex, mousey, color):
    """risuva tochka"""
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

# construktori


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

# zapisva q po dvata nachina (A,B), (B,A)


def draw_line(surf, color, point1, point2, thickness, ):
    """risuva prava i dobavq nqkoi neini harekteristiki v struturi ot danni"""
    if (point1, point2) in all_lines_ends:
        pass
    elif point1 == point2:
        pass
    else:
        all_lines_ends.append((point1, point2))
        all_lines_ends.append((point2, point1))
        all_lines.append(pygame.draw.line(
            DISPLAYSURF, Colors.GREEN, point1, point2, thickness))
        return pygame.draw.line(DISPLAYSURF, color, point1, point2, thickness)


# nad tezi dam islq

def caluclate_line_by_2_points(point1, point2):
    """namira naklona i konstanta kum dadena prava"""
    if point1[0] == point2[0]:
        return 0, point1[1]
    a = (point1[1] - point2[1]) / (point1[0] - point2[0])
    b = point1[1] - point1[0] * a
    return a, b


def add_forbiden_points(last_line_ends):
    """sprqmo poslednata prava 
    preglejda vsichki tochki 
    i dobavq v rechnika na zabranenite tochki sprqmo nqkoq tochka"""
    point1 = last_line_ends[0]
    point2 = last_line_ends[1]
    pot_line = caluclate_line_by_2_points(point1, point2)
    if point1 == point2:
        pass
    else:
        for i in all_points_centers:
            for j in all_points_centers:
                rand_line = caluclate_line_by_2_points(i, j)
                if i == j or i in last_line_ends or j in last_line_ends:
                    pass
                elif i in last_line_ends and j not in last_line_ends:
                    pass
                elif j in last_line_ends and i not in last_line_ends:
                    pass
                elif pot_line[0] * i[0] + pot_line[1] < i[1] and pot_line[0] * j[0] + pot_line[1] < j[1]:
                    pass
                elif pot_line[0] * i[0] + pot_line[1] >= i[1] and pot_line[0] * j[0] + pot_line[1] >= j[1]:
                    pass

                elif rand_line[0] * point1[0] + rand_line[1] < point1[1] and rand_line[0] * point2[0] + rand_line[1] < point2[1]:
                    pass
                elif rand_line[0] * point1[0] + rand_line[1] > point1[1] and rand_line[0] * point2[0] + rand_line[1] > point2[1]:
                    pass
                else:
                    point_key1 = dict_of_canters_points[i]
                    point_key2 = dict_of_canters_points[j]
                    map_between_point_forbpoints[
                        point_key1].append(dict_of_canters_points[j])
                    map_between_point_forbpoints[
                        point_key2].append(dict_of_canters_points[i])
                    map_between_point_forbpoints[point_key2] = list(
                        set(map_between_point_forbpoints[point_key2]))
                    map_between_point_forbpoints[point_key1] = list(
                        set(map_between_point_forbpoints[point_key1]))


def ispnt_underorabove(line, point):
    """v koq poluravnina e dadena tochka sprqmo dadena prava"""
    if line[0] * point[0] + line[1] < point[1]:
        return 1
    elif line[0] * point[0] + line[1] > point[1]:
        return 2
    else:
        return 0


def can_we_lineup(last_line_ends):
    """dali novata prava ne presicha veche sushtestvuvashta"""
    point1 = last_line_ends[0]
    point2 = last_line_ends[1]
    p1 = dict_of_canters_points[point1]
    p2 = dict_of_canters_points[point2]
    if point1 == point2:
        return False
    if last_line_ends in all_lines_ends:
        return False
    if p2 in map_between_point_forbpoints[dict_of_canters_points[point1]]:
        return False
    if p1 in map_between_point_forbpoints[dict_of_canters_points[point2]]:
        return False
    return True


# tezi sa samo vuv purviq while


def IfPointAreaAtClick(mousex, mousey):
    """dali krukcheto okolo tochkata e clicknato"""
    for i in prctective_area_of_points:
        if i.collidepoint(mousex, mousey):
            return True
    return False


def dist_between_point_and_line(point1, point2, point3):
    """presmqta raztoqnieto ot tochka do prava"""
    lineeq = caluclate_line_by_2_points(point1, point2)
    return round(abs((lineeq[0] * point3[0] - point3[1] + lineeq[1]) / (((lineeq[0]) ** 2 + 1) ** 0.5)))


def compare_all_points_with_new_one(all_points_centers, new_point_center):
    """ proverqva dali novo napravenata 
    tochka leji na edna prava sus sushtestvuvashtite tochki"""
    n = len(all_points_centers)
    for i in range(n):
        for j in range(i + 1, n):
            if dist_between_point_and_line(all_points_centers[i], all_points_centers[j], new_point_center) < DISTANCE_FROM_POINT:
                return True
    return False


def did_it_end():
    """dali e krai na igrata"""
    for i in all_points_centers:
        for j in all_points_centers:
            the_line = (i, j)
            if i == j:
                pass
            elif can_we_lineup(the_line):
                return True
    return False


def IfLineAtClick(mousex, mousey):
    """ako shtqh da razhirqvam tva shteshe da iam smisul"""
    for i in prctective_area_of_lines:

        if i.collidepoint(mousex, mousey):
            return True
    return False


def PointVector(point):
    """ako shtqh da razhirqvam tva shteshe da iam smisul"""
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
