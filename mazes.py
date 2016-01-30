from random import choice, uniform, randint

NORTH,EAST,SOUTH,WEST = 0,1,2,3

class Node(object):

    def __init__(self):
        self.neighbors = [None for i in xrange(4)]
        self.open = [False for i in xrange(4)]
        self.visited = False

    def set_neighbor(self, node, direction):
        self.neighbors[direction] = node
        node.neighbors[(direction+2)%4] = self

    def connect(self, node):
        if node not in self.neighbors: return
        direction = self.neighbors.index(node)
        self.open[direction] = True
        node.open[(direction+2)%4] = True

def blank_grid(width, height):
    grid = [[Node() for i in xrange(width)] for j in xrange(height)]
    for row in xrange(0,height):
        for col in xrange(0,width):
            if row-1 >= 0:
                grid[row][col].set_neighbor(grid[row-1][col],NORTH)
            if col-1 >= 0:
                grid[row][col].set_neighbor(grid[row][col-1],WEST)
    return grid

def growing_tree_maze(width,height):
    grid = blank_grid(width,height)
    active = []

    x, y = randint(0,width-1), randint(0,height-1)
    active.append(grid[x][y])

    while active != []:
        node = choice(active)
        #Change the starting node for each time to change the method of generation

        node.visited = True
        good_neighbors = [n for n in node.neighbors if n != None and n.visited == False]
        if good_neighbors == []:
            active.remove(node)
        else:
            x = choice(good_neighbors)
            node.connect(x)
            active.append(x)
            x.visited = True
    return grid

def display(grid):
    out = ""
    for row in grid:
        for node in row:
            if node.open[NORTH]:
                out += "* "
            else:
                out += "**"
        out += "*\n"
        for node in row:
            if node.open[WEST]:
                out += "  "
            else:
                out += "| "
        out += "|\n"
    for node in grid[0]:
        out += "**"
    out += "*"
    print out

display(growing_tree_maze(10,10))
