import os


def verticalCheck(row, col, board):
    # print("checking vert")
    fourInARow = False
    consecutiveCount = 0

    for i in range(row, 6):
        if board[i][col].lower() == board[row][col].lower():
            consecutiveCount += 1
        else:
            break

    if consecutiveCount >= 4:
        fourInARow = True

    return fourInARow


def horizontalCheck(row, col, board):
    fourInARow = False
    consecutiveCount = 0

    for j in range(col, 7):
        if board[row][j].lower() == board[row][col].lower():
            consecutiveCount += 1
        else:
            break

    if consecutiveCount >= 4:
        fourInARow = True
    return fourInARow


def diagonalCheck(row, col, board):
    fourInARow = False
    count = 0
    slope = None

    # check for diagonals with positive slope
    consecutiveCount = 0
    j = col
    for i in range(row, 6):
        if j > 6:
            break
        elif board[i][j].lower() == board[row][col].lower():
            consecutiveCount += 1
        else:
            break
        j += 1  # increment column when row is incremented

    if consecutiveCount >= 4:
        count += 1
        slope = 'positive'

    # check for diagonals with negative slope
    consecutiveCount = 0
    j = col
    for i in range(row, -1, -1):
        if j > 6:
            break
        elif board[i][j].lower() == board[row][col].lower():
            consecutiveCount += 1
        else:
            break
        j += 1  # increment column when row is decremented

    if consecutiveCount >= 4:
        count += 1
        slope = 'negative'

    if count > 0:
        fourInARow = True
    if count == 2:
        slope = 'both'
    return fourInARow, slope


def verticalCheck_3(row, col, board):
    # print("checking vert")
    fourInARow = False
    consecutiveCount = 0

    for i in range(row, 6):
        if board[i][col].lower() == board[row][col].lower():
            consecutiveCount += 1
        else:
            break

    if consecutiveCount == 3:
        fourInARow = True

    return fourInARow


def horizontalCheck_3(row, col, board):
    fourInARow = False
    consecutiveCount = 0

    for j in range(col, 7):
        if board[row][j].lower() == board[row][col].lower():
            consecutiveCount += 1
        else:
            break

    if consecutiveCount == 3:
        fourInARow = True
    return fourInARow


def diagonalCheck_3(row, col, board):
    fourInARow = False
    count = 0
    slope = None

    # check for diagonals with positive slope
    consecutiveCount = 0
    j = col
    for i in range(row, 6):
        if j > 6:
            break
        elif board[i][j].lower() == board[row][col].lower():
            consecutiveCount += 1
        else:
            break
        j += 1  # increment column when row is incremented

    if consecutiveCount == 3:
        count += 1
        slope = 'positive'

    # check for diagonals with negative slope
    consecutiveCount = 0
    j = col
    for i in range(row, -1, -1):
        if j > 6:
            break
        elif board[i][j].lower() == board[row][col].lower():
            consecutiveCount += 1
        else:
            break
        j += 1  # increment column when row is decremented

    if consecutiveCount == 3:
        count += 1
        slope = 'negative'

    if count > 0:
        fourInARow = True
    if count == 2:
        slope = 'both'
    return fourInARow, slope


class Utility():
    @classmethod
    def flip_the_board(cls, state):
        keys = [i for i in range(7)]
        elem = dict.fromkeys(keys, 0)
        for i in range(6):
            for j in range(7):
                if state[i][j] != ' ':
                    elem[j] += 1

        board = []
        for i in range(6):
            board.append([])
            for j in range(7):
                board[i].append(' ')

        for i in range(6):
            for j in range(7):
                if state[i][j] != ' ':
                    new_row = elem[j] - i - 1
                    board[new_row][j] = state[i][j]

        return board

    @classmethod
    def print_the_board(cls, board):
        # os.system(['clear', 'cls'][os.name == 'nt'])
        for i in range(5, -1, -1):
            print("\t", end="")
            for j in range(7):
                print("| " + str(board[i][j]), end=" ")
            print("|")
        print("\t  _   _   _   _   _   _   _ ")
        print("\t  1   2   3   4   5   6   7 ")

    @classmethod
    def make_temp_move(cls, column, board, color):
        for i in range(6):
            if board[i][column] == ' ':
                board[i][column] = color
                break

        return board

    @classmethod
    def copy_the_board(cls, state):
        board = []
        for i in range(6):
            board.append([])
            for j in range(7):
                board[i].append(' ')

        for i in range(6):
            for j in range(7):
                if state[i][j] != " ":
                    board[i][j] = state[i][j]
        return board

    @classmethod
    def checkForConsecutives(cls, board):
        # for each piece in the board...
        finished = False
        for i in range(6):
            for j in range(7):
                if board[i][j] != ' ':
                    # check if a vertical four-in-a-row starts at (i, j)
                    if verticalCheck(i, j, board):
                        finished = True
                        return finished

                    # check if a horizontal four-in-a-row starts at (i, j)
                    if horizontalCheck(i, j, board):
                        finished = True
                        return finished

                    # check if a diagonal (either way) four-in-a-row starts at (i, j)
                    # also, get the slope of the four if there is one
                    diag_fours, slope = diagonalCheck(i, j, board)
                    if diag_fours:
                        # print(slope)
                        finished = True
                        return finished
        return finished

    @classmethod
    def checkForConsecutives_3(cls, board):
        finished = False
        col = None

        for i in range(6):
            for j in range(7):
                if board[i][j] != ' ':
                    # check if a vertical four-in-a-row starts at (i, j)
                    if verticalCheck_3(i, j, board):
                        finished = True
                        return finished, j

                    # check if a horizontal four-in-a-row starts at (i, j)
                    if horizontalCheck_3(i, j, board):
                        finished = True
                        return finished, j

                    # check if a diagonal (either way) four-in-a-row starts at (i, j)
                    # also, get the slope of the four if there is one
                    diag_fours, slope = diagonalCheck_3(i, j, board)
                    if diag_fours:
                        # print(slope)
                        finished = True
                        return finished, j
        return finished, col