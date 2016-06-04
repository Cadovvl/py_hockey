import random

class SampleStayLogic:
    def move(self, board, gate, index, side, balls, your_team, enemy_team):
        return (0, 0)

class SampleRandomLogic:
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

class MoveToBallLogic:
    def move(self, board, gate, index, side, balls, your_team, enemy_team):
        your_position = your_team[index]
        ball_position = balls[0]
        vec = (ball_position[0] - your_position[0], ball_position[1] - your_position[1])
        return vec

class StayLeftLogic:
    target_coord = (140, 349)
    def move(self, board, gate, index, side, balls, your_team, enemy_team):
        your_position = your_team[index]
        vec = (self.target_coord[0] - your_position[0], self.target_coord[1] - your_position[1])
        return vec
