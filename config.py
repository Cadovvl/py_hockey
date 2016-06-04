# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import xml.etree.ElementTree as ET

pygame.init()

config = ET.parse('./config.xml')
croot = config.getroot()

# Define some colors
for color in croot.findall('./colors/color'):
    exec (color.get('name') + " = ( " +
          color.get('r') + ", " +
          color.get('g') + ", " +
          color.get('b') + ")")

# define pygame fonts
for font in croot.findall('./fonts/font'):
    exec (font.get('name') + " = pygame.font.Font(pygame.font.match_font(pygame.font.get_fonts()[" +
          font.get('index') + "]), " +
          font.get('size') + ", bold=" +
          font.get('bold') + ")")

for image in croot.findall('./images/image'):
    exec (image.get('name') + " = pygame.image.load('" +
          image.text + "')")
    exec (image.get('name') + " = pygame.transform.scale(" +
          image.get('name') + ", (" +
          image.get('w') + ", " +
          image.get('h') + "))")

csize = croot.find('size')
size = [int(csize.get('w')), int(csize.get('h'))]  # 1180, 670

score_pattern = croot.find('score_pattern').text
screen = pygame.display.set_mode(size)

pygame.display.set_caption('I\'m PAVEEEEEEL')

bg_image = pygame.image.load(croot.find('background').text).convert()
bg_image = pygame.transform.scale(bg_image, tuple(size))

score_label_pos = (int(croot.find('score_label').get('x')), int(croot.find('score_label').get('y')))
time_label_pos = (int(croot.find('time_label').get('x')), int(croot.find('time_label').get('y')))
final_logo_pos = (int(croot.find('final_logo').get('x')), int(croot.find('final_logo').get('y')))
final_score_pos = (int(croot.find('final_score').get('x')), int(croot.find('final_score').get('y')))


time_tick = int(croot.find('time_tick').text)
score_print_delay = int(croot.find('score_print_delay').text)
vertical_shift = int(croot.find('name_vertical_shift').text)
