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
        for i in range(5, -1, -1):
            print("\t", end="")
            for j in range(7):
                print("| " + str(board[i][j]), end=" ")
            print("|")
        print("\t  _   _   _   _   _   _   _ ")
        print("\t  1   2   3   4   5   6   7 ")

    @classmethod
    def make_temp_move(cls, column, board, disk):
        for i in range(6):
            if board[i][column] == ' ':
                board[i][column] = disk
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
