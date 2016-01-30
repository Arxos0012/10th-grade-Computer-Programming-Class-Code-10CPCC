from ColorWar import *
from Random_Warrior import *
from random import *

class Warrior(Player):

    def __init__(self, name):
        '''
        self.plays solely exist to facilitate first action on first move
        '''
        super(self.__class__, self).__init__(name)
        self.plays = 0
        
    def go(self):
        '''
        Sets opponent coordinates on the grid as a variable of the class,
        sets variables for my color and the opponent color, then
        returns a desired color based on a minimax algorithm
        '''
        self.opponent_coord = (self.rows()-self.my_row()-1, self.cols()-self.my_col()-1)
    
        my_color = self.get_color(self.my_row(), self.my_col())
        op_color = self.get_color(self.opponent_coord[0], self.opponent_coord[1])

        grid  = [[self.get_color(y,x) for x in range(self.cols())] for y in range(self.rows())]

        if self.plays < 1:
            self.plays += 1
            return self.minimax(grid, range(self.colors()), my_color, op_color, True)[1]
        return self.minimax(grid, range(self.colors()), my_color, op_color)[1]
                
    def get_neighbors(self, cell):
        '''
        Returns a list of neighboring cells to a give cell in the grid.
        Each cell is represented as a tuple of row and column coordinates.
        '''
        neighbors = []
        if cell[0] - 1 >= 0:
            neighbors.append((cell[0]-1, cell[1]))
        if cell[0] + 1 < self.rows():
            neighbors.append((cell[0]+1, cell[1]))
        if cell[1] - 1 >= 0:
            neighbors.append((cell[0], cell[1]-1))
        if cell[1] + 1 < self.cols():
            neighbors.append((cell[0], cell[1]+1))
        return neighbors

    def minimax(self, grid, colors, my_color, op_color, is_start = False, rec = 3):
        '''
        Our minimax implementation for ColorWar simulates three recursive steps
        of a game where the opponent wants to choose the possiblities that
        minimizes the amount of the board I gain and I want to maximize it.
        '''
        if is_start:
            choices = [self.get_color(neighbor[0],neighbor[1])for neighbor in self.get_neighbors((self.my_row(), self.my_col()))]
        else:
            choices = [elem for elem in colors]
            if my_color in choices:
                choices.remove(my_color)
            if op_color in choices:
                choices.remove(op_color)
        
        if rec == 0 :
            #return percentage of board under possesion after three recurives steps
            region = [(self.my_row(), self.my_col())]
            for cell in region:
                neighbors = self.get_neighbors(cell)
                for neighbor in neighbors:
                    if grid[neighbor[0]][neighbor[1]] == my_color and neighbor not in region:
                        region.append(neighbor)
            out = len(region)/float(self.rows()*self.cols())
            return (out, my_color)
        if rec % 2 == 1:
            #return the max value
            pos = {choice: self.minimax(self.flood_fill(grid, (self.my_row(), self.my_col()), my_color, choice), colors, choice, op_color, False, rec-1)[0] for choice in choices}
            maxi = float('-inf')
            out = 0
            for p in pos:
                if pos[p] > maxi:
                    maxi = pos[p]
                    out = p
            return (maxi, out)
        else:
            #return the minimum value
            pos = {choice: self.minimax(self.flood_fill(grid, self.opponent_coord, op_color, choice), colors, my_color, choice, False, rec-1)[0] for choice in choices}
            mini = float('inf')
            out = 0
            for p in pos:
                if pos[p] < mini:
                    mini = pos[p]
                    out = p
            return (mini, out)

    def flood_fill(self, grid, coord, color, new_color):
        '''
        Flood fills the region of a given player give its coordinates, its
        current color and the new color it will swap to.
        '''
        region = [coord]
        copy = [[cell for cell in row] for row in grid]

        for cell in region:
            neighbors = self.get_neighbors(cell)
            for neighbor in neighbors:
                if grid[neighbor[0]][neighbor[1]] == color and neighbor not in region:
                    region.append(neighbor)
        for cell in region:
            copy[cell[0]][cell[1]] = new_color
        return copy
