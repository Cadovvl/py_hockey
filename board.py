# -*- coding: utf-8 -*-

class Board:
    def __init__(self, l, r, t, b):
        self.left = int(l)
        self.right = int(r)
        self.top = int(t)
        self.bottom = int(b)

    @classmethod
    def fromNode(cls, node):
        return Board(node.get('left'), node.get('right'), node.get('top'), node.get('bottom'))
