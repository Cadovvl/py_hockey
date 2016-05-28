# -*- coding: utf-8 -*-
"""
Created on Tue Apr 08 00:56:59 2014

@author: pasukhov
"""

import pygame
from pygame.locals import *
import random
import time

from config import *


class Obj(object):
    centerx = 20.0
    centery = 20.0
    R = 10.0
    pic = None

    def __init__(self, pos, size, pic):
        self.R = size
        self.centerx, self.centery = tuple(pos)
        self.pic = pic

    def display(self, screen):
        screen.blit(self.pic,
                    ((self.centerx - self.R, self.centery - self.R), (self.centerx + self.R, self.centery + self.R)))


class Ball(Obj):
    vx = 0.0
    vy = 0.0
    maxvx = 20.0
    maxvy = 20.0

    def __init__(self, pos, size, pic, maxvx=20.0, maxvy=20.0):
        Obj.__init__(self, pos, size, pic)
        self.maxvx = maxvx
        self.maxvy = maxvy

    def cannon(self, vx, vy):
        if (self.vx * vx + self.vy * vy <= 0):
            self.vx = -self.vx
            self.vy = -self.vy
        self.vx = self.vx + 2 * vx
        self.vy = self.vy + 2 * vy
        self.vx = min(self.vx, self.maxvx)
        self.vy = min(self.vy, self.maxvy)
        self.vx = max(self.vx, -self.maxvx)
        self.vy = max(self.vy, -self.maxvy)

    def on_move(self):
        self.centerx += self.vx
        self.centery += self.vy
        self.vx = self.vx * 0.95
        self.vy = self.vy * 0.95


class Logic:
    a = (0, 0)

    def move(self, board, gate, index, side, balls, your_team, enemy_team):
        b = random.randint(1, 1000)
        if b < 150:
            x = random.randint(-10, 10)
            y = random.randint(-10, 10)
            self.a = (x, y)
            return self.a
        else:
            return self.a

class Player(Obj):
    vx = 0.0
    vy = 0.0
    maxvx = 10.0
    maxvy = 10.0
    name = "NoName"
    logic = None

    def __init__(self, pos, size, pic, move_logic, name="NoName", maxvx=10.0, maxvy=10.0):
        Obj.__init__(self, pos, size, pic)
        self.logic = move_logic
        self.maxvx = maxvx
        self.maxvy = maxvy
        self.name = name

    def cannon(self, vx, vy):
        self.vx = vx
        self.vy = vy
        self.vx = min(self.vx, self.maxvx)
        self.vy = min(self.vy, self.maxvy)
        self.vx = max(self.vx, -self.maxvx)
        self.vy = max(self.vy, -self.maxvy)

    def move(self, vx, vy):
        self.vx = vx
        self.vy = vy
        self.vx = min(self.vx, self.maxvx)
        self.vy = min(self.vy, self.maxvy)
        self.vx = max(self.vx, -self.maxvx)
        self.vy = max(self.vy, -self.maxvy)

    def on_move(self):
        self.centerx += self.vx
        self.centery += self.vy

    def display(self, screen):
        label = font_name.render(self.name, 1, color_name)
        screen.blit(label, (self.centerx - self.R, self.centery - self.R - 10))
        Obj.display(self, screen)

    

