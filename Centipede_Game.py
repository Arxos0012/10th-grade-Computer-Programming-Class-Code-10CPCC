#The Centipede Game
from random import shuffle, randint
from itertools import combinations
from copy import deepcopy
from sys import maxint

class Player(object):

    def __init__(self, name):
        self.name = name
        self.game = None #IF YOU ACCESS GAME YOU ARE CHEATING
        self.id = randint(-maxint,maxint) #IF YOU CHANGE YOUR ID YOU ARE CHEATING

    def __str__(self):
        return self.name

    def go(self):
        '''
        Return True if take the big pot and False if you pass the pots
        '''
        pass

    def start(self):
        '''
        Called automatically before each game
        '''
        pass

    def end(self):
        '''
        Called automatically at the end of each game, after points are awarded.
        '''
        pass

    #ALL FUNCTIONS AFTER THIS POINT SHOULD NOT BE OVERRIDDEN.
    def get_pot_size(self):
        '''
        Returns the current pot amounts, in the form (small pot, large pot)
        '''
        return tuple(self.game.pot)

    def opponent_id(self):
        '''
        Returns the ID number of your current opponent
        '''
        for p in self.game.players:
            if p != self:
                return p.id

    def my_id(self):
        '''
        Returns your ID number
        '''
        return self.id

    def get_scores(self):
        '''
        Returns a dictionary of ID numbers to scores.
        To look up your own score, you should call self.get_scores()[self.my_id()]
        '''
        return self.game.get_scores()

    def get_rounds_left(self):
        '''
        Returns the number of rounds yet to be played
        '''
        return self.game.max_rounds - self.game.round_number

class Game(object):

    def __init__(self, max_rounds, p0, p1, tournament = None):
        '''
        Creates a new game. Will be played to max_rounds rounds.
        '''
        self.max_rounds = max_rounds
        self.players = [p0, p1]
        for player in self.players:
            player.game = self
        self.tournament = tournament
        self.score = {p.id:0 for p in self.players}
        self.pot = [1,4]
        self.round_number = 0

    def give_points(self, player, points):
        '''
        Awards some number of points to a given player
        '''
        self.score[player.id] += points
        if self.tournament:
            self.tournament.score[player.id] += points

    def get_scores(self):
        '''
        Returns a dictionary of player IDs to scores. (To be passed along to the players)
        '''
        if self.tournament:
            return deepcopy(self.tournament.score)
        return deepcopy(self.score)

    def play(self):
        '''
        Plays out the game between the two players.
        '''
        self.pot = [1,4]
        self.round_number = 0
        shuffle(self.players)
        for player in self.players:
            try:
                player.start()
            except:
                print "Unexpected error in start():", sys.exc_info()[0]
        while self.round_number < self.max_rounds:
            curr = self.players[self.round_number%2]
            other = self.players[(self.round_number+1)%2]
            move = False
            try:
                move = curr.go()
            except:
                print "Unexpected error in go():", sys.exc_info()[0]
            if move:
                self.give_points(other,self.pot[0])
                self.give_points(curr,self.pot[1])
                for p in self.players:
                    try:
                        p.end()
                    except:
                        print "Unexpected error in end():", sys.exc_info()[0]
                return self.score
            self.round_number += 1
            if self.round_number < self.max_rounds:
                for i in xrange(len(self.pot)):
                    self.pot[i] *= 2
        for p in self.players:
            self.give_points(p, sum(self.pot)/2)
        for p in self.players:
            try:
                p.end()
            except:
                print "Unexpected error in end():", sys.exc_info()[0]
        return self.score

class Tournament(object):

    def __init__(self, max_rounds, n_repetitions, *players):
        '''
        Create a new tournament. Max_rounds refers to the
        maximum length of a game. n_repetitions is the number of
        times each player will play each other player.
        '''
        self.max_rounds = max_rounds
        self.n_repetitions = n_repetitions
        self.players = list(players)
        self.id_to_name = {p.id: p.name for p in self.players}
        self.score = {p.id:0 for p in self.players}

    def play(self):
        '''
        Plays the tournament, with each player playing each other player n_repetitions times.
        '''
        matches = list(combinations(self.players,2))
        games_played = {p:0 for p in self.players}
        matches_played = {m:0 for m in matches}
        while len(matches) > 0:
            shuffle(self.players)
            curr = min(matches, key = lambda x : games_played[x[0]]+games_played[x[1]])
            g = Game(self.max_rounds, curr[0], curr[1], self)
            g.play()
            for p in curr:
                games_played[p] += 1
            matches_played[curr] += 1
            if matches_played[curr] >= self.n_repetitions:
                matches.remove(curr)
        ordered_scores = sorted(self.score.items(), key = lambda x:x[1], reverse=True)
        for player in ordered_scores:
            print (self.id_to_name[player[0]]+":").ljust(15,'.')+"{:,}".format(player[1])

class Human(Player):

    def go(self):
        print "*"*10
        print "{}'s turn.".format(self.name)
        print "The big pot has ${0[1]}.\nThe small pot has ${0[0]}".format(self.get_pot_size())
        print "There are at most {} rounds left.".format(self.get_rounds_left())
        scores = self.get_scores()
        print "You have ${}, and your opponent has ${}.".format(scores[self.my_id()],scores[self.opponent_id()])
        print "Do you keep the pot or pass the pot? (enter 'keep' or 'pass')"
        val = raw_input().strip().lower()
        while val not in ["keep","pass"]:
            print "Invalid input. Try again."
            val = raw_input().strip().lower()
        return val == "keep"
