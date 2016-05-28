# -*- coding: utf-8 -*-

class Gate:
    def __init__(self, t, b):
        self.top = int(t)
        self.bottom = int(b)

    @classmethod
    def fromNode(cls, node):
        return Gate(node.get('top'), node.get('bottom'))
