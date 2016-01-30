from random import *
from math import *

hall = "H"
wall = "|"
room = "R"
door = "D"

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

class Rogue_2014():

    def __init__(self, width, height, stats):
        self.miners = []
        self.width = width
        self.height = height
        self.map = self.generate_map(width, height, stats)

    def generate_map(self, width, height, stats):
        grid = [[wall for i in range(width)] for j in range(height)]

        self.miners.append(Miner(randint(0,width-1), randint(0,height-1), grid, stats))
        #x, y, death prob, spwan prob, room spawn prob, grid

        i = 0
        while len(self.miners) > 0:
            for miner in self.miners:
                grid = miner.die(grid)
                if miner.is_dead:
                    self.miners.remove(miner)
                grid = miner.dig(grid)
                grid = miner.dig_room(grid)
                new_miner = miner.spawn(grid)
                if new_miner != None:
                    self.miners.append(new_miner)
                '''
                if i % 5 == 0:
                    self.debug_display(grid)
                    print ""
                i += 1
                '''
                
        return grid

    def debug_display(self, m):
        line = ""
        for row in m:
            for col in row:
                line += col
            print line
            line = ""
            
    def display(self):
        print "Welcome to 'Rogue 2014'!"
        line = ""
        print "*"*(self.width + 2)
        for row in self.map:
            line += "*"
            for col in row:
                line += col
            line += "*"
            print line
            line = ""
        print "*"*(self.width + 2)

class Miner():

    def __init__(self, x, y, grid, stats, direction = None):
        self.grid = grid
        self.x = x
        self.y = y
        self.d_percent = stats[0]
        self.s_percent = stats[1]
        self.rs_percent = stats[2]
        self.is_dead = False
        if not direction:
            self.direction = randint(0,3)
        else:
            self.direction = direction
        self.grid[y][x] = hall

    def dig(self, grid):
        self.grid = grid
        try:
            if self.direction == UP: #up
                if self.y == 0:
                    self.is_dead = True
                    return self.grid
                try:
                    if self.x == len(grid[0])-1 and self.grid[self.y - 2][self.x] == wall and self.grid[self.y - 1][self.x - 1] in [wall, room, door]:
                        self.grid[self.y - 1][self.x] = hall
                        self.y -= 1
                    elif self.x == 0 and self.grid[self.y - 2][self.x] == wall and self.grid[self.y - 1][self.x + 1] in [wall, room, door]:
                        self.grid[self.y - 1][self.x] = hall
                        self.y -= 1
                    elif self.grid[self.y - 2][self.x] == wall and self.grid[self.y - 1][self.x - 1] in [wall, room, door] and self.grid[self.y - 1][self.x + 1] in [wall, room, door]:
                        self.grid[self.y - 1][self.x] = hall
                        self.y -= 1
                    else:
                        self.is_dead = True
                except Exception:
                    self.grid[self.y - 1][self.x] = hall
                    self.y -= 1
            elif self.direction == DOWN:   #down
                if self.y == len(grid)-1:
                    self.is_dead = True
                    return self.grid
                try:
                    if self.x == len(grid[0])-1 and self.grid[self.y + 2][self.x] == wall and self.grid[self.y + 1][self.x - 1] in [wall, room, door]:
                        self.grid[self.y + 1][self.x] = hall
                        self.y += 1
                    elif self.x == 0 and self.grid[self.y + 2][self.x] == wall and self.grid[self.y + 1][self.x + 1] in [wall, room, door]:
                        self.grid[self.y + 1][self.x] = hall
                        self.y += 1
                    elif self.grid[self.y + 2][self.x] == wall and self.grid[self.y + 1][self.x - 1] in [wall, room, door] and self.grid[self.y + 1][self.x + 1] in [wall, room, door]:
                        self.grid[self.y + 1][self.x] = hall
                        self.y += 1
                    else:
                        self.is_dead = True
                except Exception:
                    self.grid[self.y + 1][self.x] = hall
                    self.y += 1
            elif self.direction == LEFT:   #left
                if self.x == 0:
                    self.is_dead = True
                    return self.grid
                try:
                    if self.y == len(grid)-1 and self.grid[self.y][self.x - 2] == wall and self.grid[self.y - 1][self.x - 1] in [wall, room, door]:
                        self.grid[self.y][self.x - 1] = hall
                        self.x -= 1
                    elif self.y == 0 and self.grid[self.y + 2][self.x] == wall and self.grid[self.y + 1][self.x - 1] in [wall, room, door]:
                        self.grid[self.y][self.x - 1] = hall
                        self.x -= 1
                    elif self.grid[self.y][self.x - 2] == wall and self.grid[self.y - 1][self.x - 1] in [wall, room, door] and self.grid[self.y + 1][self.x - 1] in [wall, room, door]:
                        self.grid[self.y][self.x - 1] = hall
                        self.x -= 1
                    else:
                        self.is_dead = True
                except Exception:
                    self.grid[self.y][self.x - 1] = hall
                    self.x -= 1
            else:   #right
                if self.x == len(self.grid[0]) - 1:
                    self.is_dead = True
                    return self.grid
                try:
                    if self.y == len(grid)-1 and self.grid[self.y][self.x + 2] == wall and self.grid[self.y - 1][self.x + 1] in [wall, room, door]:
                        self.grid[self.y][self.x + 1] = hall
                        self.x += 1
                    elif self.y == 0 and self.grid[self.y][self.x + 2] == wall and self.grid[self.y + 1][self.x + 1] in [wall, room, door]:
                        self.grid[self.y][self.x + 1] = hall
                        self.x += 1
                    elif self.grid[self.y][self.x + 2] == wall and self.grid[self.y - 1][self.x + 1] in [wall, room, door] and self.grid[self.y + 1][self.x + 1] in [wall, room, door]:
                        self.grid[self.y][self.x + 1] = hall
                        self.x += 1
                    else:
                        self.is_dead = True
                except Exception:
                    self.grid[self.y][self.x + 1] = hall
                    self.x += 1
        except Exception:
            self.is_dead = True
        return self.grid

    def dig_room(self, grid):
        self.grid = grid
        draw = random()
        if draw < self.rs_percent:
            width = choice([x for x in range(2,7) if x % 2 == 1])
            height = choice([x for x in range(2,7) if x % 2 == 1])
            if self.direction == UP or self.direction == DOWN:
                try:
                    if self.y <= height/2 + 1 or len(grid) - (height/2+2) <= self.y:
                        return self.grid
                    if self.x <= width:
                        is_clear = True
                        lower, upper = self.x + 1, self.y + width + 2
                        for row in self.grid[self.y - (height/2+1) : self.y + (height/2+2)]:
                            for i in range(lower,upper):
                                if row[i]!= wall:
                                    is_clear = False
                        if is_clear:
                            upper -= 1
                            for row in self.grid[self.y - (height/2) : self.y + (height/2+1)]:
                                for i in range(lower,upper):
                                    row[i] = room
                            self.grid[self.y][self.x + 1] = door
                            return self.grid
                        return self.grid
                    elif len(grid[0]) - width <= self.x:
                        is_clear = True
                        lower, upper = self.x - (width+1), self.y
                        for row in self.grid[self.y - (height/2+1) : self.y + (height/2+2)]:
                            for i in range(lower,upper):
                                if row[i]!= wall:
                                    is_clear = False
                        if is_clear:
                            lower += 1
                            for row in self.grid[self.y - (height/2) : self.y + (height/2+1)]:
                                for i in range(lower,upper):
                                    row[i] = room
                            self.grid[self.y][self.x - 1] = door
                            return self.grid
                        return self.grid
                    else:
                        for x in range(2):
                            is_clear = True
                            if x == 0:
                                lower, upper = self.x + 1, self.y + width + 2
                            else:
                                lower, upper = self.x - (width+1), self.y
                            for row in self.grid[self.y - (height/2) : self.y + (height/2+1)]:
                                for i in range(lower, upper):
                                    if row[i] != wall:
                                        is_clear = False
                            if is_clear:
                                if x == 0:
                                    upper -= 1
                                else:
                                    lower += 1
                                for row in self.grid[self.y - (height/2) : self.y + (height/2+1)]:
                                    for i in range(lower, upper):
                                        row[i] = room
                                if x == 0:
                                    self.grid[self.y][self.x + 1] = door
                                    return self.grid
                                self.grid[self.y][self.x - 1] = door
                                return self.grid
                        return self.grid
                except Exception:
                    return self.grid
            else:
                try:
                    if self.x <= width/2 + 1 or len(grid[0]) - (width/2+2) <= self.x:
                        return self.grid
                    if self.y <= height:
                        is_clear = True
                        lower, upper = self.x - (width/2+1), self.x + (width/2+1)
                        for row in self.grid[self.y + 1 : self.y + (height-1)]:
                            for i in range(lower,upper):
                                if row[i]!= wall:
                                    is_clear = False
                        if is_clear:
                            lower += 1
                            upper -= 1
                            for row in self.grid[self.y + 1 : self.y + height]:
                                for i in range(lower,upper):
                                    row[i] = room
                            self.grid[self.y + 1][self.x] = door
                            return self.grid
                        return self.grid
                    elif len(grid) - height <= self.y:
                        is_clear = True
                        lower, upper = self.x - (width/2+1), self.x + (width/2+1)
                        for row in self.grid[self.y - (height+1) : self.y]:
                            for i in range(lower,upper):
                                if row[i]!= wall:
                                    is_clear = False
                        if is_clear:
                            lower += 1
                            upper -= 1
                            for row in self.grid[self.y - height : self.y]:
                                for i in range(lower,upper):
                                    row[i] = room
                            self.grid[self.y - 1][self.x] = door
                            return self.grid
                        return self.grid
                    else:
                        for x in range(2):
                            is_clear = True
                            lower, upper = self.x - (width/2+1), self.x + (width/2+1)
                            if x == 0:
                                for row in self.grid[self.y + 1 : self.y + height + 1]:
                                    for i in range(lower,upper):
                                        if row[i]!= wall:
                                            is_clear = False
                            else:
                                for row in self.grid[self.y - (height+1) : self.y]:
                                    for i in range(lower,upper):
                                        if row[i]!= wall:
                                            is_clear = False
                            for row in self.grid[self.y - (height/2) : self.y + (height/2+1)]:
                                for i in range(lower, upper):
                                    if row[i] != wall:
                                        is_clear = False
                            if is_clear:
                                lower += 1
                                upper -= 1
                                if x == 0:
                                    for row in self.grid[self.y + 1 : self.y + height]:
                                        for i in range(lower,upper):
                                            row[i] = room
                                    self.grid[self.y + 1][self.x] = door
                                    return self.grid
                                for row in self.grid[self.y - height : self.y]:
                                    for i in range(lower,upper):
                                        row[i] = room
                                self.grid[self.y - 1][self.x] = door
                                return self.grid
                        return self.grid
                except Exception:
                    return self.grid
        return self.grid

    def spawn(self, grid):
        self.grid = grid
        draw = random()
        if draw < self.s_percent:
            if (self.direction == UP or self.direction == DOWN) and self.grid:
                return Miner(self.x, self.y, self.grid, [self.d_percent, self.s_percent, self.rs_percent], choice([LEFT, RIGHT]))
            else:
                return Miner(self.x, self.y, self.grid, [self.d_percent, self.s_percent, self.rs_percent], choice([UP, DOWN]))

    def die(self,grid):
        self.grid = grid
        draw = random()
        if draw < self.d_percent:
            self.is_dead = True
            return self.grid
        return self.grid

game = Rogue_2014(30, 30, [.2, .5, .5])
counter = 0
for x in game.map:
    for y in x:
        if y == wall:
            counter += 1
wp = float(counter)/(game.width*game.height)
while wp < .4:
    game = Rogue_2014(30, 30, [.2, .5, .5])
    counter = 0
    for x in game.map:
        for y in x:
            if y == wall:
                counter += 1
    wp = float(counter)/(game.width*game.height)
game.display()
