# Zhirnova
# Borisenko

import math

b_vx = 0
b_vy = 0

b_lx = 0
b_ly = 0

play_mode = 0

gate_y = 0
gate_x = 0


def getMaxVelocity(v):
    x = abs(v[0])
    y = abs(v[1])
    if (x == 0.0 and y == 0.0):
        return (0.0, 0.0)
    if (x == 0.0):
        return (0.0, 10.0 * y / v[1])
    if (y == 0.0):
        return (10.0 * x / v[0], 0.0)
    k = (10.0 / x) if (x > y) else (10.0 / y)
    return (k * v[0], k * v[1])


def getDist(x_1, y_1, x_2, y_2):
    dx = x_1 - x_2
    dy = y_1 - y_2
    return math.sqrt(dx * dx + dy * dy)


def getNorm(x, y):
    d = math.sqrt(x * x + y * y)
    if (d > 0):
        return (x / d, y / d)
    else:
        return (0.0, 0.0)


def calcGateTarget(lu, rb, gate, side, enemy_team):
    global gate_x, gate_y

    gate_x = lu[0] if side else rb[0]
    if getDist(gate_x, gate[0], enemy_team[3][0], enemy_team[3][1]) > getDist(gate_x, gate[1], enemy_team[3][0],
                                                                              enemy_team[3][1]):
        gate_y = gate[0]
    else:
        gate_y = gate[1]


def calcPlayMode(side):
    global play_mode

    if (play_mode > 0):
        play_mode = 1 if ((side - 0.5) * b_vx <= 0) else 2


class P1:
    def move(self, board, gate, index, side, balls, your_team, enemy_team):
        gate = [gate.top, gate.bottom]
        lu = [board.left, board.top]
        rb = [board.right, board.bottom]

        global b_vx, b_vy, b_lx, b_ly, play_mode

        if (b_lx != 0 and b_ly != 0):
            b_vx = balls[0][0] - b_lx
            b_vy = balls[0][1] - b_ly

        b_lx = balls[0][0]
        b_ly = balls[0][1]

        calcGateTarget(lu, rb, gate, side, enemy_team)

        calcPlayMode(side)

        my_x = your_team[index][0]
        my_y = your_team[index][1]

        if (getDist(my_x, my_y, balls[0][0], balls[0][1]) <= 50.0):
            if (getDist(my_x, my_y, balls[0][0], balls[0][1]) <= 20.0):
                if (play_mode == 0):
                    play_mode = 1
                    speed = getMaxVelocity(getNorm(gate_x - my_x, gate_y - my_y))
                else:
                    if (getDist(gate_x, gate_y, my_x, my_y) < 80.0):
                        speed = getMaxVelocity(getNorm(gate_x - my_x, gate_y - my_y))
                    else:
                        speed = getMaxVelocity(getNorm(your_team[1][0] - my_x, your_team[1][1] - my_y))
            else:
                if ((my_x - balls[0][0]) * (gate_x - balls[0][0]) + (my_y - balls[0][1]) * (gate_y - balls[0][1]) > 0):
                    if (((my_x - balls[0][0]) * b_vx + (my_y - balls[0][1]) * b_vy) > 0.6):
                        speed = getMaxVelocity(getNorm(b_vx, b_vy))
                    else:
                        if (((my_x - balls[0][0]) * -b_vy + (my_y - balls[0][1]) * b_vx) > 0.0):
                            speed = getMaxVelocity(getNorm(-b_vy, b_vx))
                        else:
                            speed = getMaxVelocity(getNorm(b_vy, -b_vx))
                else:
                    speed = getMaxVelocity(getNorm(balls[0][0] - my_x, balls[0][1] - my_y))
        else:
            if (play_mode == 2 and ((balls[0][0] - (lu[0] + (rb[0] - lu[0]) * (0.3 + side * 0.4))) * (side - 0.5) > 0)):
                speed = getMaxVelocity(getNorm(((lu[0] + rb[0]) / 2) - my_x, ((lu[1] + rb[1]) / 2) - my_y))
            else:
                if ((my_x - balls[0][0]) * (gate_x - balls[0][0]) + (my_y - balls[0][1]) * (gate_y - balls[0][1]) > 0):
                    v_1 = getNorm(-b_vy, b_vx)
                    v_2 = getNorm(b_vx, -b_vy)
                    if (getDist(my_x, my_y, balls[0][0] + 30.0 * v_1[0], balls[0][1] + 30.0 * v_1[1]) < getDist(my_x,
                                                                                                                my_y,
                                                                                                                balls[
                                                                                                                    0][
                                                                                                                    0] + 30.0 *
                                                                                                                    v_2[
                                                                                                                        0],
                                                                                                                balls[
                                                                                                                    0][
                                                                                                                    1] + 30.0 *
                                                                                                                    v_2[
                                                                                                                        1])):
                        speed = getMaxVelocity(
                            getNorm(balls[0][0] + 30.0 * v_1[0] - my_x, balls[0][1] + 30.0 * v_1[1] - my_y))
                    else:
                        speed = getMaxVelocity(
                            getNorm(balls[0][0] + 30.0 * v_2[0] - my_x, balls[0][1] + 30.0 * v_2[1] - my_y))
                else:
                    speed = getMaxVelocity(getNorm(balls[0][0] - my_x + 5 * b_vx, balls[0][1] - my_y + 5 * b_vy))

        return speed


class P2:
    def move(self, board, gate, index, side, balls, your_team, enemy_team):
        gate = [gate.top, gate.bottom]
        lu = [board.left, board.top]
        rb = [board.right, board.bottom]
        global b_vx, b_vy, b_lx, b_ly, play_mode

        calcPlayMode(side)

        my_x = your_team[index][0]
        my_y = your_team[index][1]

        if (getDist(my_x, my_y, balls[0][0], balls[0][1]) <= 20.0):
            if (play_mode == 0):
                play_mode = 1
                speed = getMaxVelocity(getNorm(gate_x - my_x, gate_y - my_y))
            else:
                if (getDist(gate_x, gate_y, my_x, my_y) < 160.0):
                    speed = getMaxVelocity(getNorm(gate_x - my_x, gate_y - my_y))
                else:
                    speed = getMaxVelocity(getNorm(your_team[0][0] - my_x, your_team[0][1] - my_y))
        else:
            if (play_mode == 2 and ((balls[0][0] - (lu[0] + (rb[0] - lu[0]) * (0.3 + side * 0.4))) * (side - 0.5) > 0)):
                speed = getMaxVelocity(getNorm(((lu[0] + rb[0]) / 2) - my_x, ((lu[1] + rb[1]) / 2) - my_y))
            else:
                speed = getMaxVelocity(getNorm(balls[0][0] - my_x + 5 * b_vx, balls[0][1] - my_y + 5 * b_vy))

        return speed


class P3:
    def move(self, board, gate, index, side, balls, your_team, enemy_team):
        gate = [gate.top, gate.bottom]
        lu = [board.left, board.top]
        rb = [board.right, board.bottom]
        global b_vx, b_vy, b_lx, b_ly, play_mode

        calcPlayMode(side)

        my_x = your_team[index][0]
        my_y = your_team[index][1]

        if (getDist(my_x, my_y, balls[0][0], balls[0][1]) <= 20.0):
            if (play_mode == 0):
                play_mode = 1
            speed = getMaxVelocity(getNorm(((lu[0] + rb[0]) / 2) - my_x, ((lu[1] + rb[1]) / 2) - my_y))
        else:
            if ((balls[0][0] - (lu[0] + rb[0]) / 2) * (side - 0.5) > 0):
                if (getDist(my_x, my_y, your_team[3][0], your_team[3][1]) > 40.0):
                    speed = getMaxVelocity(getNorm(balls[0][0] - my_x, balls[0][1] - my_y))
                else:
                    speed = (0, 0)
            else:
                speed = getMaxVelocity(
                    getNorm((lu[0] + (rb[0] - lu[0]) * (0.25 + side * 0.5)) - my_x, (balls[0][1] - my_y)))
        return speed

class P4:
    def move(self, board, gate, index, side, balls, your_team, enemy_team):
        gate = [gate.top, gate.bottom]
        lu = [board.left, board.top]
        rb = [board.right, board.bottom]
        global b_vx, b_vy, b_lx, b_ly, play_mode

        calcPlayMode(side)

        my_x = your_team[index][0]
        my_y = your_team[index][1]

        bx = lu[0] + (rb[0] - lu[0]) * side

        if (getDist(my_x, my_y, balls[0][0], balls[0][1]) <= 20.0):
            if (play_mode == 0):
                play_mode = 1
            speed = getMaxVelocity(getNorm(((lu[0] + rb[0]) / 2) - my_x, ((lu[1] + rb[1]) / 2) - my_y))
        else:
            if (play_mode == 2 or ((balls[0][0] - (lu[0] + (rb[0] - lu[0]) * (0.25 + side * 0.5))) * (side - 0.5) > 0)):
                by = balls[0][1] + (0.0 if b_vy == 0.0 else (b_vx / b_vy * (bx - balls[0][0])))

                by = max(gate[0], by)
                by = min(gate[1], by)
                speed = getMaxVelocity(getNorm(bx - my_x, by - my_y))

            else:
                speed = getNorm(bx - my_x, ((gate[0] + gate[1]) / 2) - my_y)

        return speed
