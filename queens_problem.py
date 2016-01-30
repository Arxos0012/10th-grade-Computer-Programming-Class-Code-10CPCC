def q_problem(n, r = 0, board=None):
    solutions = 0
    if not board:
        board = [["" for x in range(n)] for y in range(n)]
    if is_solved(n, board):
        return 1
    elif is_filled(board):
        return 0
    for x in range(n):
        copy = [[col for col in row] for row in board]
        if not add_queen(r+1, x, copy):
            continue
        solutions += q_problem(n, r+1, copy)
    return solutions
        
def is_filled(board):
    cells = len(board)**2
    taken = 0
    for y in range(len(board)):
        for x in range(len(board)):
            if board[y][x] != "":
                taken != 1
    if taken == cells:
        return True
    return False

def is_solved(n, board):
    queens = 0
    dangers = 0
    
    for y in range(n):
        for x in range(n):
            if board[y][x] == "Q":
                queens += 1
            if board[y][x] == "X":
                dangers += 1
    if queens == n and dangers == (n**2)-n:
        return True

def add_queen(row, col, board):
    if row >= len(board) and board[row][col] != "":
        return False
    board[row][col] = "Q"
    for y in range(len(board)):
        for x in range(len(board)):
            if board[y][x] != 'Q' and (y == row or x == col):
                board[y][x] = "X"
            elif board[y][x] != 'Q' and x != col and abs(float(y-row)/(x-col)) == 1:
                board[y][x] = "X"
    return True
