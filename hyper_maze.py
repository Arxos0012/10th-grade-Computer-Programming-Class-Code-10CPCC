from random import *

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

room = "R"
door = "D"
wall = " "
hall = "H"

class Maze():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.miners = []
        self.maze = self.generate_maze()
        self.display()

    def debug_display(self, m):
        line = ""
        print "*"*(self.width+2)
        for row in m:
            line += "*"
            for col in row:
                line += col
            line += "*"
            print line
            line = ""
        print "*"*(self.width+2)

    def display(self):
        line = ""
        print "*"*(self.width+2)
        for row in self.maze:
            line += "*"
            for col in row:
                line += col
            line += "*"
            print line
            line = ""
        print "*"*(self.width+2)

    def generate_maze(self):
        grid =[[wall for i in range(self.width)] for j in range(self.height)]

        self.miners.append(Miner(self.width/2, self.height/2, grid, 0, 1, .5))
        #x, y, grid, death_rate, spawn_rate, room_rate, direction
        i = 0
        while len(self.miners) > 0:
            for miner in self.miners:
                miner.die(grid)
                if miner.is_dead:
                    self.miners.remove(miner)
                new_miner = miner.spawn(grid)
                if new_miner:
                    self.miners.append(new_miner)
                grid = miner.dig(grid)
                grid = miner.dig_room(grid)
                if i % 5 == 0:
                    self.debug_display(grid)
                i += 1
        return grid

class Miner():
    def __init__(self, x, y, grid, death_rate, spawn_rate, room_rate, direction = None):
        self.x = x
        self.y = y
        self.grid = grid
        self.death_rate = death_rate
        self.spawn_rate = spawn_rate
        self.room_rate = room_rate
        self.is_dead = False
        if not direction:
            self.direction = choice([UP, DOWN, LEFT, RIGHT])
        else:
            self.direction = direction
        self.grid[y][x] = hall

    def dig(self, grid):
        self.grid = grid
        if self.direction == UP:
            if self.y == 0:
                self.is_dead = True
                return self.grid
            target = [self.y - 1, self.x]
            if self.is_safe(target):
                self.grid[target[0]][target[1]] = hall
                self.y -= 1
                return self.grid
            self.is_dead = True
            return self.grid
        elif self.direction == DOWN:
            if self.y == len(self.grid) - 1:
                self.is_dead = True
                return self.grid
            target = [self.y + 1, self.x]
            if self.is_safe(target):
                self.grid[target[0]][target[1]] = hall
                self.y += 1
                return self.grid
            self.is_dead = True
            return self.grid
        elif self.direction == LEFT:
            if self.x == 0:
                self.is_dead = True
                return self.grid
            target = [self.y, self.x - 1]
            if self.is_safe(target):
                self.grid[target[0]][target[1]] = hall
                self.x -= 1
                return self.grid
            self.is_dead = True
            return self.grid
        else:
            if self.x == len(self.grid[0])-1:
                self.is_dead = True
                return self.grid
            target = [self.y, self.x + 1]
            if self.is_safe(target):
                self.grid[target[0]][target[1]] = hall
                self.x += 1
                return self.grid
            self.is_dead = True
            return self.grid

    def dig_room(self, grid):
        self.grid = grid
        if random() < self.room_rate:
            width, height = 5, 5
            if self.direction == UP or self.direction == DOWN:
                left_room = [[y for y in range(self.y-height/2, self.y+height/2)], [x for x in range(self.x-width, self.x)]]
                right_room = [[y for y in range(self.y-height/2, self.y+height/2)], [x for x in range(self.x + 1, self.x + (width-1))]]
                if self.x < width:
                    for y in right_room[0]:
                        for x in right_room[1]:
                            if not self.is_safe([y, x]):
                                return self.grid
                    for y in right_room[0]:
                        for x in right_room[1]:
                            self.grid[y][x] = wall
                    self.grid[self.y][self.x + 1] = door
                    return self.grid
                elif self.x > len(grid[0]) - (width+1):
                    for y in left_room[0]:
                        for x in left_room[1]:
                            if not self.is_safe([y, x]):
                                return self.grid
                    for y in left_room[0]:
                        for x in left_room[1]:
                            self.grid[y][x] = wall
                    self.grid[self.y][self.x - 1] = door
                    return self.grid
                else:
                    rooms = [left_room, right_room]
                    for i in range(2):
                        for y in rooms[i][0]:
                            for x in rooms[i][1]:
                                if not self.is_safe([y, x]):
                                     continue
                        for y in rooms[i][0]:
                            for x in rooms[i][1]:
                                self.grid[y][x] = wall
                        if i % 2 == 0:
                            self.grid[self.y][self.x - 1] = door
                            return self.grid
                        else:
                            self.grid[self.y][self.x + 1] = door
                            return self.grid
            else:
                up_room = [[y for y in range(self.y-height, self.y)], [x for x in range(self.x-width/2, self.x+width/2)]]
                down_room = [[y for y in range(self.y+1, self.y+(height-1))], [x for x in range(self.x-width/2, self.x+width/2)]]
                if self.y < height:
                    for y in down_room[0]:
                        for x in down_room[1]:
                            if not self.is_safe([y, x]):
                                return self.grid
                    for y in down_room[0]:
                        for x in down_room[1]:
                            self.grid[y][x] = wall
                    self.grid[self.y + 1][self.x] = door
                    return self.grid
                elif self.y > len(grid) - (height+1):
                    for y in up_room[0]:
                        for x in up_room[1]:
                            if not self.is_safe([y, x]):
                                return self.grid
                    for y in up_room[0]:
                        for x in up_room[1]:
                            self.grid[y][x] = wall
                    self.grid[self.y - 1][self.x] = door
                    return self.grid
                else:
                    rooms = [up_room, down_room]
                    for i in range(2):
                        for y in rooms[i][0]:
                            for x in rooms[i][1]:
                                if not self.is_safe([y, x]):
                                     continue
                        for y in rooms[i][0]:
                            for x in rooms[i][1]:
                                self.grid[y][x] = wall
                        if i % 2 == 0:
                            self.grid[self.y - 1][self.x] = door
                            return self.grid
                        else:
                            self.grid[self.y + 1][self.x] = door
                            return self.grid
        return self.grid

    def spawn(self, grid):
        self.grid = grid
        if random() < self.spawn_rate:
            if self.direction == UP or self.direction == DOWN:
                target_left, target_right = [self.y, self.x - 1], [self.y, self.x + 1]
                if self.is_safe(target_left):
                    return Miner(self.x, self.y, self.grid, self.death_rate, self.spawn_rate, self.room_rate, LEFT)
                if self.is_safe(target_right):
                    return Miner(self.x, self.y, self.grid, self.death_rate, self.spawn_rate, self.room_rate, RIGHT)
            else:
                target_up, target_down = [self.y - 1, self.x], [self.y + 1, self.y]
                if self.is_safe(target_up):
                    return Miner(self.x, self.y, self.grid, self.death_rate, self.spawn_rate, self.room_rate, UP)
                if self.is_safe(target_down):
                    return Miner(self.x, self.y, self.grid, self.death_rate, self.spawn_rate, self.room_rate, RIGHT)

    def die(self, grid):
        self.grid = grid
        if random() < self.death_rate:
            self.is_dead = True

    def is_safe(self, target):
        y, x = target[0], target[1]
        try:
            if self.direction == UP:
                if self.x == 0:
                    if self.grid[y][x] == wall and self.grid[y-1][x] == wall and self.grid[y-1][x+1] == wall:
                        return True
                    return False
                elif self.x == len(self.grid[0])-1:
                    if self.grid[y][x] == wall and self.grid[y-1][x] == wall and self.grid[y-1][x+1] == wall:
                        return True
                    return False
                else:
                    if self.grid[y][x] == wall and self.grid[y-1][x] == wall and self.grid[y-1][x-1] == wall and self.grid[y-1][x+1] == wall:
                        return True
                    return False
            elif self.direction == DOWN:
                if self.x == 0:
                    if self.grid[y][x] == wall and self.grid[y+1][x] == wall and self.grid[y+1][x+1] == wall:
                        return True
                    return False
                elif self.x == len(self.grid[0])-1:
                    if self.grid[y][x] == wall and self.grid[y+1][x] == wall and self.grid[y+1][x+1] == wall:
                        return True
                    return False
                else:
                    if self.grid[y][x] == wall and self.grid[y+1][x] == wall and self.grid[y+1][x-1] == wall and self.grid[y+1][x+1] == wall:
                        return True
                    return False
            elif self.direction == LEFT:
                if self.y == 0:
                    if self.grid[y][x] == wall and self.grid[y][x-1] == wall and self.grid[y+1][x-1] == wall:
                        return True
                    return False
                elif self.y == len(self.grid)-1:
                    if self.grid[y][x] == wall and self.grid[y][x-1] == wall and self.grid[y-1][x-1] == wall:
                        return True
                    return False
                else:
                    if self.grid[y][x] == wall and self.grid[y][x-1] == wall and self.grid[y-1][x-1] == wall and self.grid[y+1][x-1] == wall:
                        return True
                    return False
            else:
                if self.y == 0:
                    if self.grid[y][x] == wall and self.grid[y][x+1] == wall and self.grid[y+1][x+1] == wall:
                        return True
                    return False
                elif self.y == len(self.grid)-1:
                    if self.grid[y][x] == wall and self.grid[y][x+1] == wall and self.grid[y-1][x+1] == wall:
                        return True
                    return False
                else:
                    if self.grid[y][x] == wall and self.grid[y][x+1] == wall and self.grid[y-1][x+1] == wall and self.grid[y+1][x+1] == wall:
                        return True
                    return False
        except Exception:
            return True

maze = Maze(15,15)
