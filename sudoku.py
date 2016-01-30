from copy import deepcopy

easy ='''003020600
900305001
001806400
008102900
700000008
006708200
002609500
800203009
005010300'''
def read_puzzle(puzzle_txt):
    pzzl = []
    if isinstance(puzzle_txt, str):
        pzzl = puzzle_txt.split()
        pzzl = [[range(1,len(row)+1) if char == "0" else [int(char)] for char in row] for row in pzzl]
    else:
        pzzl = puzzle_txt
    for y in range(len(pzzl)):
        for x in range(len(pzzl[0])):
            if len(pzzl[y][x]) > 1:
                bad = []
                for elem in pzzl[y][x]:
                    if elem in get_row(pzzl, y) + get_col(pzzl, x) + get_block(pzzl, y, x):
                        bad.append(elem)
                for elem in bad:
                    pzzl[y][x].remove(elem)
    return pzzl


def get_row(pzzl, y):
    return [elem[0] for elem in pzzl[y] if len(elem) == 1]

def get_col(pzzl, x):
    return [row[x][0] for row in pzzl if len(row[x]) == 1]

def get_block(pzzl, y, x):
    a, b = y, x
    while a % 3 != 0:
        a -= 1
    while b % 3 != 0:
        b -= 1
    block, out = [row[b:b+3] for row in pzzl[a:a+3]], []
    for row in block:
        for cell in row:
            out.append(cell)
    return [elem[0] for elem in out if len(elem) == 1]

def get_row_pos(pzzl, y, x):
    unknowns = [elem for elem in pzzl[y][:x] if len(elem) > 1] + [elem for elem in pzzl[y][x+1:] if len(elem) > 1]
    out = []
    for unknown in unknowns:
        for elem in unknown:
            out.append(elem)
    return out

def get_col_pos(pzzl, y, x):
    unknowns = [row[x] for row in pzzl[:y] if len(row[x]) > 1] + [row[x] for row in pzzl[y+1:] if len(row[x]) > 1]
    out = []
    for unknown in unknowns:
        for elem in unknown:
            out.append(elem)
    return out

def get_block_pos(pzzl, y, x):
    a, b = y, x
    while a % 3 != 0:
        a -= 1
    while b % 3 != 0:
        b -= 1
    unknowns, out = [], []
    for i in range(a, a+3):
        for j in range(b, b+3):
            if i == y and j == b:
                continue
            if len(pzzl[i][j]) > 1:
                unknowns.append(pzzl[i][j])           
    for unknown in unknowns:
        for elem in unknown:
            out.append(elem)
    return out


    
def stringify(puzzle):
    out = ""
    for row in puzzle:
        for col in row:
            if len(col) > 1:
                out += "0"
            else:
                out += str(col[0])
        out += "\n"
    return out

def is_solved(puzzle):
    for y in range(len(puzzle)):
        for x in range(len(puzzle[0])):
            if len(puzzle[y][x]) > 1:
                return False
    return True

def solve(puzzle):
    rp = read_puzzle(puzzle)
    while not is_solved(rp):
        for y in range(len(rp)):
            for x in range(len(rp[0])):
                if len(rp[y][x]) > 1:
                    for elem in rp[y][x]:
                        if elem not in get_row_pos(rp, y, x) + get_col_pos(rp, y, x) + get_block_pos(rp, y, x):
                            rp[y][x] = [elem]
                rp = read_puzzle(rp)
    return stringify(rp)
