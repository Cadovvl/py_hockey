# -*- coding: utf-8 -*-

from config import *

import sys
from game import *
import time
import test_sets
from optparse import OptionParser
from config import *

parser = OptionParser()
parser.add_option("-t", "--from-tests", dest="test_name",
                  help="development or testing", metavar="{testing, dev}")

(options, args) = parser.parse_args()


"""
***************************************
###  eof initialization of players  ###
***************************************
"""

clock = pygame.time.Clock()


# -------- Основной цикл программы -----------

pygame.time.set_timer(pygame.QUIT, 300000)
startTime = time.time()

forceQuit = False

def print_error_result(is_left_team):
    screen.blit(tech_error_logo, final_logo_pos)
    score_string = "<== Technical Error from This Team" if is_left_team \
        else "Technical Error from This Team ==>"
    score_label = font_tech.render(score_string, 1, color_tech)
    screen.blit(score_label, final_score_pos)
    pygame.display.flip()

    time.sleep(3)

def print_score(score_string):
    screen.blit(final_logo, final_logo_pos)
    score_label = font_tech.render(score_string, 1, color_tech)
    screen.blit(score_label, final_score_pos)
    pygame.display.flip()

if options.test_name:
    ts = test_sets.GLOBAL_TEST_SET[options.test_name]
    cfg = ts.to_strings()
    game = Game(cfg[0], cfg[1], cfg[2])
else:
    game = Game.from_files()

while True:
    while not game.is_paused():
        # ОБРАБОТКА ВСЕХ СОБЫТИЙ ДОЛЖНА БЫТЬ ПОД ЭТИМ КОММЕНТАРИЕМ
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                game.pause()
                forceQuit = True

        # ОБРАБОТКА ВСЕХ СОБЫТИЙ ДОЛЖНА НАХОДИТЬСЯ НАД ЭТИМ КОММЕНТАРИЕМ

        # ВСЯ ИГРОВАЯ ЛОГИКА ДОЛЖНА НАХОДИТЬСЯ ПОД ЭТИМ КОММЕНТАРИЕМ

        game.step()

        # ВСЯ ИГРОВАЯ ЛОГИКА ДОЛЖНА НАХОДИТЬСЯ НАД ЭТИМ КОММЕНТАРИЕМ


        # ВЕСЬ КОД ДЛЯ РИСОВАНИЯ ДОЛЖЕН НАХОДИТЬСЯ ПОД ЭТИМ КОММЕНТАРИЕМ

        #    screen.fill(white)
        screen.blit(bg_image, [0, 0])

        # Отрисовка игроков

        game.display(screen)

        # Вывести сделанную картинку на экран в точке (250, 250)
        #text = font.render("{0} {1}".format(score[0],score[1]),True,font_color)
        #screen.blit(text, [0,0])

        # ВЕСЬ КОД ДЛЯ РИСОВАНИЯ ДОЛЖЕН НАХОДИТЬСЯ НАД ЭТИМ КОММЕНТАРИЕМ

        time_string = "{0:02}:{1:02}".format(time.localtime(time.time() - startTime).tm_min,
                                             time.localtime(time.time() - startTime).tm_sec)
        time_label = font_score.render(time_string, 1, color_score)

        score_label = font_score.render(game.get_score_string(), 1, color_score)
        screen.blit(score_label, score_label_pos)
        screen.blit(time_label, time_label_pos)

        pygame.display.flip()
        # Ограничить до 20 кадров в секунду
        clock.tick(time_tick)
    if game.is_game_ended(forceQuit):
        if game.is_technical_issue():
            print_error_result(game.is_left_technical_issue())
        else:
            print_score(game.get_score_string())
        break
    game.refresh()
    print_score(game.get_score_string())
    time.sleep(score_print_delay)

game.print_debug_info()
time.sleep(score_print_delay)

pygame.quit()
