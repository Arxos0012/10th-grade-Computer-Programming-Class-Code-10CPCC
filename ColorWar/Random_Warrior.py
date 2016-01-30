from ColorWar import *
from random import choice

class Rando(Player):

    def go(self):
        legal = self.legal_moves()
        return choice(legal)
