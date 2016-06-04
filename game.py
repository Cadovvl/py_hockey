# -*- coding: utf-8 -*-

import game_objects
from board import Board
from gate import Gate
import copy
import xml.etree.ElementTree as ET
import random
import config

class Game:

    @classmethod
    def from_files(cls, conf_filename="./game_config.xml",
                   t1_conf_filename="./first_team_config.xml",
                   t2_conf_filename="./second_team_config.xml"):
        return Game(open(conf_filename, 'r').read(),
            open(t1_conf_filename, 'r').read(),
            open(t2_conf_filename, 'r').read())

    def __init__(self, conf_str, team1_conf, team2_conf):
        self._score = [0, 0]
        self._is_paused = False
        self._exceptional_type_problem_happened = [False, False]

        self._croot = ET.fromstring(conf_str)
        self._t1_croot = ET.fromstring(team1_conf)
        self._t2_croot = ET.fromstring(team2_conf)

        self._board = Board.fromNode(self._croot.find('board'))
        self._gate = Gate.fromNode(self._croot.find('gate'))


        self._max_score = [int(self._croot.find('max_score').get('left')),
                             int(self._croot.find('max_score').get('right'))]

        self._balls_init = []
        self._team_players1 = []
        self._team_players2 = []


        for ball in self._croot.findall('./balls/ball'):
            bi = "self._balls_init.append(game_objects.Ball([" + \
                  ball.get('x') + "," + \
                  ball.get('y') + "]," + \
                  ball.get('r') + " , game_objects.ball_skin))"
            exec (bi)

        self._player_deviation = int(self._croot.find('player_deviation').text)


        t1_filename = self._t1_croot.find('file_name').text
        exec ("import " + t1_filename)
        for pl in self._t1_croot.findall('./players/player'):
            comm = "self._team_players1.append(game_objects.Player([" + \
                   pl.get('x') + "," + \
                   pl.get('y') + "]," + \
                   pl.get('r') + " , game_objects.first_team_skin, " + \
                   t1_filename + "." + pl.get('logic') + "() , '" + \
                   pl.get('name') + \
                   "'))"
            exec (comm)

        t2_filename = self._t2_croot.find('file_name').text
        exec ("import " + t2_filename)
        for pl in self._t2_croot.findall('./players/player'):
            comm = "self._team_players2.append(game_objects.Player([" + \
                   pl.get('x') + "," + \
                   pl.get('y') + "]," + \
                   pl.get('r') + " , game_objects.second_team_skin, " + \
                   t2_filename + "." + pl.get('logic') + "() , '" + \
                   pl.get('name') + \
                   "'))"
            exec (comm)

        self.refresh()

    def step(self):
        # player's moves

        if self._is_paused:
            return

        self._ask_moves()

        # event analize
        self._on_player_game()
        self._on_player_fight()

        self._on_victory()

        self._on_board_playres(self.t1)
        self._on_board_playres(self.t2)

        # don't reverse ball, if there was a goal
        if not self._is_paused:
            self._on_board_objects()

        self._move()

    def _on_victory(self):
        for i in self.balls:
            if i.centerx + i.vx <= self._board.left and i.vx < 0 and \
                                    self._gate.top < i.centery < self._gate.bottom:
                self._is_paused = True
                self._score[1] += 1
            if i.centerx + i.vx >= self._board.right and i.vx > 0 and \
                                    self._gate.top < i.centery < self._gate.bottom:
                self._is_paused = True
                self._score[0] += 1

    def _ask_team_moves(self, team, tn):
        count = 0
        for j in team:
            try:
                ball_positions = [(i.centerx, i.centery) for i in self.balls]
                team1_positions = [(i.centerx, i.centery) for i in self.t1]
                team2_positions = [(i.centerx, i.centery) for i in self.t2]
                poss = (team1_positions, team2_positions)
                r = j.logic.move(copy.copy(self._board), copy.copy(self._gate), count, tn, ball_positions, poss[tn],
                                 poss[1-tn])
                j.move(r[0], r[1])
            except Exception as e:
                print "Error while getting move"
                print e.message
                self._exceptional_type_problem_happened[tn] = True
                self._is_paused = True
            count += 1
    def _ask_moves(self):
        self._ask_team_moves(self.t1, 0)
        self._ask_team_moves(self.t2, 1)



    def _on_board_objects(self):
        for i in self.balls:
            if i.centerx + i.vx < self._board.left or i.centerx + i.vx > self._board.right:
                i.vx = -i.vx
            if i.centery + i.vy < self._board.top or i.centery + i.vy > self._board.bottom:
                i.vy = -i.vy

    def _on_board_playres(self, t):
        for i in t:
            if (i.centerx + i.vx < self._board.left and i.vx < 0) or \
                    (i.centerx + i.vx > self._board.right and i.vx > 0):
                i.vx = 0
            if (i.centery + i.vy < self._board.top and i.vy < 0) or \
                    (i.centery + i.vy > self._board.bottom and i.vy > 0):
                i.vy = 0

    def _on_player_game(self):
        for i in self.balls:
            for j in self.t1:
                if (j.centerx + j.vx - i.centerx)**2 + (j.centery + j.vy - i.centery)**2 <= (i.R + j.R)**2:
                    i.cannon(j.vx, j.vy)
            for j in self.t2:
                if (j.centerx + j.vx - i.centerx)**2 + (j.centery + j.vy - i.centery)**2 <= (i.R + j.R)**2:
                    i.cannon(j.vx, j.vy)

    def _on_player_fight(self):
            for j in self.t1:
                for i in self.t2:
                    if (j.centerx + j.vx - i.centerx - i.vx)**2 + (j.centery + j.vy - i.centery - i.vx)**2 <= \
                                    (i.R + j.R)**2:
                        vx, vy = i.vx, i.vy
                        i.cannon(j.vx, j.vy)
                        j.cannon(vx, vy)

    def _move(self):
        for i in self.t1:
            i.on_move()
        for i in self.t2:
            i.on_move()
        for i in self.balls:
            i.on_move()

    def get_score(self):
        return copy.copy(self._score)

    def get_score_string(self):
        return config.score_pattern.format(self._score[0], self._score[1])

    def is_paused(self):
        return True if self._is_paused else False

    def pause(self):
        self._is_paused = True

    def refresh(self):
        self._is_paused = False

        self.t1 = [copy.copy(i) for i in self._team_players1]
        self.t2 = [copy.copy(i) for i in self._team_players2]
        self.balls = [copy.copy(i) for i in self._balls_init]

        for i in self.t1:
            i.centerx += random.randint(-self._player_deviation, self._player_deviation)
            i.centery += random.randint(-self._player_deviation, self._player_deviation)
        for i in self.t2:
            i.centerx += random.randint(-self._player_deviation, self._player_deviation)
            i.centery += random.randint(-self._player_deviation, self._player_deviation)

    def is_technical_issue(self):
        if self._exceptional_type_problem_happened[0] or self._exceptional_type_problem_happened[1]:
            return True
        return False

    def is_left_technical_issue(self):
        return True if self._exceptional_type_problem_happened[0] else False


    def is_game_ended(self, forceQuit):
        if self._exceptional_type_problem_happened[0] or self._exceptional_type_problem_happened[1]:
            return True
        elif forceQuit:
            self._is_paused = True
            return True
        if self._score[0] >= self._max_score[0] or self._score[1] >= self._max_score[1]:
            return True
        return False


    def display(self, screen):
        # Отрисовка игроков
        for i in self.t1:
            i.display(screen)
        for i in self.t2:
            i.display(screen)

        # Отрисовка мяча
        for i in self.balls:
            i.display(screen)

    def print_debug_info(self):
        print "score:", self._score
        print "PI:", self._exceptional_type_problem_happened

