# -*- coding: utf-8 -*-
"""
Created on Mon May 19 21:33:29 2014

@author: pasukhov
"""

import math
import random


def solve(a, b, c, flag=True):
    if abs(a) <= 0.00001 and abs(b) > 0.000001:
        return c / b
    D = b ** 2 - 4.0 * a * c
    if D < 0:
        print a, b, c
        return None
    if flag:
        return (-1.0 * b + math.sqrt(D)) / (2.0 * a)
    else:
        return (-1.0 * b - math.sqrt(D)) / (2.0 * a)


def nextCircleCoordinate(x1, y1, x2, y2, flag=True):  # second is ball
    x0 = x2 - x1
    y0 = y2 - y1

    if x0 == 0:
        xk = math.sin(math.pi / 2.0 - math.acos(5.0 / abs(y0))) * 10.0
        yk = math.cos(math.pi / 2.0 - math.acos(5.0 / abs(y0))) * 10.0
        if (y1 <= y2) ^ flag:
            xk = -xk
        if (x1 >= x2) ^ flag:
            yk = -yk
    else:
        a = x0 ** 2 + y0 ** 2
        xk = solve(a, -100 * x0, 2500.0 - 100.0 * y0 ** 2, (y1 > y2) ^ flag)
        yk = solve(a, -100 * y0, 2500.0 - 100.0 * x0 ** 2, (x1 < x2) ^ flag)
        if xk == None or yk == None:
            print 'None'
            print (x1, y1), (x2, y2), (x0, y0)
            return (x2, y2)
    return (xk + x1, yk + y1 )


class P1:
    def move(self, board, gate, index, side, balls, your_team, enemy_team):
        gate = [gate.top, gate.bottom]
        lu = [board.left, board.top]
        rb = [board.right, board.bottom]

        your_position_x = your_team[index][0]
        your_position_y = your_team[index][1]
        gy = (gate[0] + gate[1]) / 2.0
        gx = rb[0]
        if side == 1:
            gx = lu[0]
        v1x = your_position_x - gx
        v1y = your_position_y - gy
        v2x = balls[0][0] - gx
        v2y = balls[0][1] + 40 - gy
        v3x = balls[0][0] - gx
        v3y = balls[0][1] - 40 - gy
        vty = balls[0][1] - gy

        speed = (balls[0][0] - your_position_x, balls[0][1] - your_position_y)
        if (( your_position_x - balls[0][0]) ** 2 + ( your_position_y - balls[0][1]) ** 2   ) < 100:
            speed = (gx - your_position_x, gy - your_position_y)
            alpha = 10.0 / max(abs(speed[0]), abs(speed[1]))
            speed = (alpha * speed[0], alpha * speed[1])
            return speed

        if ((v1x * v2y - v2x * v1y) * ((v1x * v3y - v3x * v1y)) < 0 and (balls[0][0] - your_position_x) * (
                    0.5 - side) > 0) or (
                        ( your_position_x - balls[0][0]) ** 2 + ( your_position_y - balls[0][1]) ** 2   ) > 3500:
            alpha = 10.0 / max(abs(speed[0]), abs(speed[1]))
            speed = (alpha * speed[0], alpha * speed[1])
            return speed

        if (( your_position_x - balls[0][0]) ** 2 + ( your_position_y - balls[0][1]) ** 2   ) > 400:
            target = nextCircleCoordinate(your_position_x, your_position_y, balls[0][0], balls[0][1],
                                          v1x * vty - v1y * v2x > 0)
            speed = (target[0] - your_position_x, target[1] - your_position_y)
            alpha = 10.0 / max(abs(speed[0]), abs(speed[1]))
            speed = (alpha * speed[0], alpha * speed[1])
            if speed[0] + your_position_x > rb[0] or speed[0] + your_position_x < lu[0]:
                speed = (speed[0], (speed[1] / abs(speed[1])) * 10.0)
            if speed[1] + your_position_y > rb[1] or speed[1] + your_position_y < lu[1]:
                speed = ( (speed[0] / abs(speed[0])) * 10.0, speed[1])

            return (speed[0] + random.random() * 2 - 1.0, speed[1] + random.random() * 2 - 1.0)
        else:
            return (0, 0)


class P2:
    def move(self, board, gate, index, side, balls, your_team, enemy_team):
        gate = [gate.top, gate.bottom]
        lu = [board.left, board.top]
        rb = [board.right, board.bottom]
        your_position_x = your_team[index][0]
        your_position_y = your_team[index][1]
        gy = (gate[0] + gate[1]) / 2.0
        gx = rb[0]
        if side == 1:
            gx = lu[0]
        v1x = your_position_x - gx
        v1y = your_position_y - gy
        v2x = balls[0][0] - gx
        v2y = balls[0][1] + 30 - gy
        v3x = balls[0][0] - gx
        v3y = balls[0][1] - 30 - gy
        vty = balls[0][1] - gy

        speed = (balls[0][0] - your_position_x, balls[0][1] - your_position_y)
        if (( your_position_x - balls[0][0]) ** 2 + ( your_position_y - balls[0][1]) ** 2   ) < 100:
            speed = (gx - your_position_x, gy - your_position_y)
            alpha = 10.0 / max(abs(speed[0]), abs(speed[1]))
            speed = (alpha * speed[0], alpha * speed[1])
            return speed

        if ((v1x * v2y - v2x * v1y) * ((v1x * v3y - v3x * v1y)) < 0 and (balls[0][0] - your_position_x) * (
                    0.5 - side) > 0 ) or (
                        ( your_position_x - balls[0][0]) ** 2 + ( your_position_y - balls[0][1]) ** 2   ) > 30000:
            alpha = 10.0 / max(abs(speed[0]), abs(speed[1]))
            speed = (alpha * speed[0], alpha * speed[1])
            return speed

        if (( your_position_x - balls[0][0]) ** 2 + ( your_position_y - balls[0][1]) ** 2   ) > 400:
            target = nextCircleCoordinate(your_position_x, your_position_y, balls[0][0], balls[0][1],
                                          v1x * vty - v1y * v2x > 0)
            speed = (target[0] - your_position_x, target[1] - your_position_y)
            alpha = 10.0 / max(abs(speed[0]), abs(speed[1]))
            speed = (alpha * speed[0], alpha * speed[1])
            if speed[0] + your_position_x > rb[0] or speed[0] + your_position_x < lu[0]:
                speed = (speed[0], (speed[1] / abs(speed[1])) * 10.0)
            if speed[1] + your_position_y > rb[1] or speed[1] + your_position_y < lu[1]:
                speed = ( (speed[0] / abs(speed[0])) * 10.0, speed[1])

            return (speed[0] + random.random() * 2 - 1.0, speed[1] + random.random() * 2 - 1.0)
        else:
            return (0, 0)


class P3:
    def move(self, board, gate, index, side, balls, your_team, enemy_team):
        gate = [gate.top, gate.bottom]
        lu = [board.left, board.top]
        rb = [board.right, board.bottom]
        your_position_x = your_team[index][0]
        your_position_y = your_team[index][1]
        gy = (gate[0] + gate[1]) / 2.0
        gx = rb[0]
        if side == 1:
            gx = lu[0]

        tx, ty = enemy_team[0][0], enemy_team[0][1]

        for i in enemy_team:
            if (tx - gx) ** 2 + (ty - gy) ** 2 > (i[0] - gx) ** 2 + (i[1] - gy) ** 2:
                tx = i[0]
                ty = i[1]
        if ((tx - your_position_x) ** 2 + (ty - your_position_y) ** 2) > 20000:
            speed = ((tx - your_position_x), (ty - your_position_y))
            return speed
        if (your_position_x - tx) * (your_position_x - gx) < 0:
            speed = ((tx - your_position_x), (ty - your_position_y))
            alpha = 10.0 / max(abs(speed[0]), abs(speed[1]))
            speed = (alpha * speed[0], alpha * speed[1])
            return speed
        if (tx - your_position_x) ** 2 + (ty - your_position_y) ** 2 > 200:
            target = nextCircleCoordinate(your_position_x, your_position_y, tx, ty,
                                          (tx - gx) * (your_position_y - gy) - (your_position_x - gx) * (ty - gy) > 0)
            speed = (target[0] - your_position_x, target[1] - your_position_y)
            alpha = 10.0 / max(abs(speed[0]), abs(speed[1]))
            speed = (alpha * speed[0], alpha * speed[1])
            if speed[0] + your_position_x > rb[0] or speed[0] + your_position_x < lu[0]:
                speed = (speed[0], (speed[1] / abs(speed[1])) * 10.0)
            if speed[1] + your_position_y > rb[1] or speed[1] + your_position_y < lu[1]:
                speed = ((speed[0] / abs(speed[0])) * 10.0, speed[1])

            return (speed[0] + random.random() * 2 - 1.0, speed[1] + random.random() * 2 - 1.0)
        else:
            return (0, 0)


class P4:
    def move(self, board, gate, index, side, balls, your_team, enemy_team):
        gate = [gate.top, gate.bottom]
        lu = [board.left, board.top]
        rb = [board.right, board.bottom]
        your_position_x = your_team[index][0]
        your_position_y = your_team[index][1]
        gy = (gate[0] + gate[1]) / 2.0
        gx = lu[0] + 10
        if side == 1:
            gx = rb[0] - 10

        target = ( (balls[0][0] + gx * 9.0) / 10.0,
                   (balls[0][1] + gy * 9.0) / 10.0 )

        b = (target[0] - gx) ** 2 + (target[1] - gy) ** 2
        if b < 10000 and b > 2:
            alpha = 100.0 / math.sqrt(b + 0.1)
            target = ((target[0] - gx) * alpha + gx, (target[1] - gy) * alpha + gy)

        return ( target[0] - your_position_x, target[1] - your_position_y)


  
