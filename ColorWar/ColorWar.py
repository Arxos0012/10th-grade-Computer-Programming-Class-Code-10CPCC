from random import randint
from copy import copy
import time

VERBOSE = True

class Player(object):

    def __init__(self, name):
        '''
        Creates a new Player object with a given name.
        '''
        self.name = name
        self._game = None
        self._count = 1

    def set_coords(self,row, col):
        '''
        Sets the initial coordinates of the Player.
        DO NOT CALL THIS FUNCTION EVER.
        '''
        self._coords = (row,col)

    def get_score(self):
        '''
        Returns my score - the percentage of squares that I control.
        '''
        return self._game.score(self)

    def get_team_score(self):
        '''
        Returns the sum score of the players on my team.
        (In a 1v1 game, this will be the same as get_score()
        '''
        return self._game.team_score(self)

    def get_enemy_score(self):
        '''
        Returns the sum score of the players not on my team.
        In a 1v1 game, this will be the score of my opponent.
        '''
        return self._game.enemy_score(self)

    def my_row(self):
        '''
        Returns the index of my starting row.
        '''
        return self._coords[0]

    def my_col(self):
        '''
        Returns the index of my starting column.
        '''
        return self._coords[1]

    def my_coord(self):
        '''
        Returns my starting location as a tuple in the form (row, col)
        '''
        return copy(self._coords)

    def enemy_coord(self):
        '''
        Returns a list of tuples representing starting locations for all players that are not
        me or my allies.
        '''
        teams = self._game.get_enemy_teams(self)
        coords = []
        for team in teams:
            for player in team:
                coords.append(player.my_coord())
        return coords[0]

    def rows(self):
        '''
        Returns the number of rows on the board.
        '''
        return self._game.rows()

    def cols(self):
        '''
        Returns the number of columns on the board.
        '''
        return self._game.cols()

    def colors(self):
        '''
        Returns the total number of colors available.
        (If there are 4 colors available, they will be numbered
        0,1,2 and 3.
        '''
        return self._game.colors()

    def get_color(self, row, col):
        '''
        Returns the color at a given location on the board.
        '''
        return self._game.get_color(row,col)

    def legal_moves(self):
        '''
        Returns a list of colors that would be legal choices
        for your upcoming move.
        '''
        out = range(self.colors())
        for player in self._game.players:
            color = self.get_color(player.my_row(),player.my_col())
            if color in out:
                out.remove(color)
        return out

    def go(self):
        '''
        Returns the color to which you would like to switch your territory.
        THIS is the only function that you are allowed to override.
        It is also the only one that you are required to override.
        '''
        pass
    
class Game(object):

    def __init__(self, rows, cols, colors, *players):
        '''
        Creates a new Game. Parameters specify the number of
        rows, columns and colors. The two players are passed in as well.
        '''
        self.board = Board(rows, cols, colors)
        players = list(players)
        self.players = players
        if len(self.players) == 4:
            self.teams = [players[:2],players[2:]]
            self.players = [players[0],players[2],players[1],players[3]]
        else:
            self.teams = [[p] for p in self.players]
        players[0]._coords = (0,0)
        players[1]._coords = (rows-1, cols-1)
        if len(players) > 2:
            players[2]._coords = (0, cols-1)
            players[3]._coords = (rows-1, 0)
        for p in self.players:
            p._game = self

    def __str__(self):
        out = str(self.board) + "\n"
        for p in self.players:
            out += "{}: {:.3%}\n".format(p.name, self.score(p))
        return out

    def rows(self):
        '''
        Returns the number of rows on the board.
        '''
        return self.board.rows()

    def cols(self):
        '''
        Returns the number of columns on the board.
        '''
        return self.board.cols()

    def get_color(self, row, col):
        '''
        Returns the color of a given square as an integer.
        '''
        return self.board.get_color(row, col)

    def colors(self):
        '''
        Returns the number of possible colors.
        '''
        return self.board.colors

    def get_adjacent(self, row, col):
        '''
        Returns a list of all adjacent coordinates to a given square.
        (Returns a list of tuples)
        '''
        out = []
        for i in xrange(-1,2):
            for j in xrange(-1,2):
                if (i != 0 and j != 0) or (i == 0 and j == 0):
                    continue
                if self.board.is_valid(row+i, col+j):
                    out.append((row+i, col+j))
        return out

    def player_turn(self, player):
        '''
        Makes a turn for a given player. Checks for errors and illegal moves.
        '''
        move = -1
        #try:
        move = player.go()
        #except:
            #return -1
        if move not in player.legal_moves():
            return -1
        return move

    def play(self):
        '''
        Plays a full game of Color War until a player either captures
        50% of territory or makes an illegal move and thus surrenders.
        '''
        self.setup_log("colorwar_{}.cw".format(int(time.time())))
        turn = 0
        winner = None
        while not winner:
            self.log_turn()
            player = self.players[turn]
            if VERBOSE:
                print "{}'s turn:".format(player.name)
                print self
            move = self.player_turn(player)
            if move < 0:
                if VERBOSE: print self
                winner = self.players[(turn+1)%2]
                break
            player._count = self.board.flood_fill(player.my_row(), player.my_col(), move)
            if self.team_score(player) >= 0.5:
                if VERBOSE: print self
                winner = player
                break
            turn = (turn+1)%len(self.players)
        if VERBOSE: print self
        self.log_turn()
        self.log.flush()
        self.log.close()

    def score(self, player):
        '''
        Calculates a given player's score.
        '''
        denom = self.rows() * self.cols()
        num = 0
        color = self.get_color(player.my_row(), player.my_col())
        visited = []
        frontier = [(player.my_row(), player.my_col())]
        while len(frontier) > 0:
            curr = frontier.pop()
            num += 1
            visited.append(curr)
            adj = self.get_adjacent(curr[0],curr[1])
            for location in adj:
                if location in visited or location in frontier:
                    continue
                if self.get_color(location[0], location[1]) != color:
                    continue
                frontier.append(location)
        return float(num)/denom

    def get_team(self, player):
        for team in self.teams:
            if player in team:
                return team

    def get_enemies(self, player):
        enemies = []
        for team in self.teams:
            if player not in team:
                enemies.append(team)
        return enemies

    def team_score(self, player):
        team = self.get_team(player)
        return sum([self.score(p) for p in team])

    def enemy_score(self, player):
        team = get_enemies(player)
        return sum([self.score(p) for p in team])

    def setup_log(self, filename):
        f = open(filename, 'w')
        out = "{},{},{}\n".format(self.rows(), self.cols(), self.colors())
        f.write(out)
        self.log = f

    def log_turn(self):
        out = ""
        for row in xrange(self.rows()):
            for col in xrange(self.cols()):
                out += "{},".format(self.get_color(row,col))
        for team in self.teams:
            out += "{},".format(self.team_score(team[0]))
        out += "\n"
        self.log.write(out)

class Board(object):

    def __init__(self, rows, cols, colors):
        self.board = [[randint(0,colors-1) for i in xrange(cols)] for j in xrange(rows)]
        self.colors = colors

    def __str__(self):
        return "\n".join([" ".join(str(val) for val in row) for row in self.board])

    def rows(self,):
        return len(self.board)

    def cols(self):
        return len(self.board[0])

    def get_color(self, row, col):
        return self.board[row][col]

    def is_valid(self, row, col):
        return 0 <= row < self.rows() and 0 <= col < self.cols()

    def flood_fill(self, row, col, color):
        start_color = self.get_color(row,col)
        visited = []
        frontier = [(row,col)]
        n = 0
        while len(frontier) > 0:
            coord = frontier.pop()
            visited.append(coord)
            curr_color = self.get_color(*coord)
            if curr_color != start_color:
                continue
            self.board[coord[0]][coord[1]] = color
            n += 1
            neighbors = [(coord[0]+r,coord[1]+c) for r in range(-1,2) for c in range(-1,2) if (r == 0 or c == 0) and r != c]
            neighbors = [val for val in neighbors if self.is_valid(*val)]
            for val in neighbors:
                if val not in visited and self.is_valid(*val):
                    frontier.append(val)
        return n
