import random


class RandomPlayer():
    type = None  # possible types are "Human" and "AI"
    name = None
    disk = None
    flip = None

    def __init__(self, name, disk, flip):
        self.type = "Random"
        self.name = name
        self.disk = disk
        self.flip = flip

    def move(self, state, curr_player, opp_player, last_move):
        print("{0}'s turn.  {0} is {1}".format(self.name, self.disk))
        column = None
        flip_list = [1] * 70 + [2] * 15 + [3] * 15 # weighted flip choice list
        condition = True

        while condition:
            flip_choice = random.choice(flip_list)
            if last_move == 'flip' and flip_choice == 2:
                condition = True
            else:
                condition = False

        if flip_choice == 1 or self.flip <= 0:
            while column is None:
                choice = random.randint(0, 6)
                if self.isLegalMove(choice, state):
                    column = choice
            return column, 1

        else:
            if flip_choice == 2:
                temp_board = self.flip_the_board(state)
                while column is None:
                    choice = random.randint(0,6)
                    if self.isLegalMove(choice, temp_board):
                        column = choice
                return column, flip_choice

            if flip_choice == 3:
                while column is None:
                    choice = random.randint(0,6)
                    if self.isLegalMove(choice, state):
                        column = choice
                return column, flip_choice


    def isLegalMove(self, column, state):
        """ Boolean function to check if a move (column) is a legal move
        """
        for i in range(6):
            if state[i][column] == ' ':
                # once we find the first empty, we know it's a legal move
                return True

        # if we get here, the column is full
        return False

    def flip_the_board(self, state):
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
