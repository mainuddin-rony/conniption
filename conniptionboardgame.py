import os
from human_player import HumanPlayer
from ai_player import AIPlayer
from random_player import RandomPlayer
from utility import Utility

class ConniptionBoardGame(object):
    """ Game object that holds state of Connect 4 board and game values
    """

    board = None
    round = None
    game = None
    finished = None
    winner = None
    turn = None
    players = [None, None]
    colors = ["x", "o"]
    MAX_FLIP = 4
    last_move = None


    def __init__(self):
        self.round = 1
        self.game = 1
        self.finished = False
        self.winner = None
        self.last_move = None

        # do cross-platform clear screen
        # os.system(['clear', 'cls'][os.name == 'nt'])
        print("Welcome to Conniption Board Game")
        print("Should Player 1 be a Human/AI/Random?")
        while self.players[0] == None:
            choice = str(input("Type 'H'/'A'/'R': "))
            if choice.lower() == "human" or choice.lower() == "h":
                name = str(input("What is Player 1's name? "))
                self.players[0] = HumanPlayer(name, self.colors[0], self.MAX_FLIP)
            elif choice.lower() == "ai" or choice.lower() == "a":
                name = str(input("What is Player 1's name? "))
                diff = int(input("Enter difficulty for this AI (1 - 4) "))
                self.players[0] = AIPlayer(name, self.colors[0], self.MAX_FLIP, diff + 1)
            elif choice.lower() == "random" or choice.lower() == "r":
                name = str(input("What is Player 1's name? "))
                self.players[0] = RandomPlayer(name, self.colors[0], self.MAX_FLIP)
            else:
                print("Invalid choice, please try again")
        print("{0} will be {1}".format(self.players[0].name, self.colors[0]))

        print("Should Player 2 be a Human/AI/Random?")
        while self.players[1] == None:
            choice = str(input("Type 'H'/'A'/'R': "))
            if choice.lower() == "human" or choice.lower() == "h":
                name = str(input("What is Player 2's name? "))
                self.players[1] = HumanPlayer(name, self.colors[1], self.MAX_FLIP)
            elif choice.lower() == "ai" or choice.lower() == "a":
                name = str(input("What is Player 2's name? "))
                diff = int(input("Enter difficulty for this AI (1 - 4) "))
                self.players[1] = AIPlayer(name, self.colors[1], self.MAX_FLIP, diff + 1)
            elif choice.lower() == "random" or choice.lower() == "r":
                name = str(input("What is Player 2's name? "))
                self.players[1] = RandomPlayer(name, self.colors[1], self.MAX_FLIP)
            else:
                print("Invalid choice, please try again")
        print("{0} will be {1}".format(self.players[1].name, self.colors[1]))

        # x always goes first (arbitrary choice on my part)
        self.turn = self.players[0]

        self.board = []
        for i in range(6):
            self.board.append([])
            for j in range(7):
                self.board[i].append(' ')

    def newGame(self):
        """ Function to reset the game, but not the names or colors
        """
        self.round = 1
        self.game += 1
        self.finished = False
        self.winner = None
        self.last_move = None

        # x always goes first (arbitrary choice on my part)
        self.turn = self.players[0]
        self.players[0].flip = 4
        self.players[1].flip = 4

        self.board = []
        for i in range(6):
            self.board.append([])
            for j in range(7):
                self.board[i].append(' ')

    def switchTurn(self):
        if self.turn == self.players[0]:
            self.turn = self.players[1]
        else:
            self.turn = self.players[0]

        # increment the round
        self.round += 1

    def nextMove(self):
        player = self.turn

        if self.turn == self.players[0]:
            curr_player_flip = self.players[0].flip
            opp_player_flip = self.players[1].flip
        else:
            opp_player_flip = self.players[0].flip
            curr_player_flip = self.players[1].flip


        # there are only 42 legal places for pieces on the board
        # exactly one piece is added to the board each turn
        if self.round > 42:
            self.finished = True
            # this would be a stalemate :(
            return

        # move is the column that player want's to play
        move, move_type = player.move(self.board, curr_player_flip, opp_player_flip, self.last_move)

        if move_type == 1:
            print("Selected move by %s at this round: Column %d" % (player.name, move + 1))
            print("Final Board after this round: ")
            print("Flip remains for %s is %d: " % (player.name, player.flip))
            self.last_move = move
            for i in range(6):
                if self.board[i][move] == ' ':
                    self.board[i][move] = player.color
                    Utility.print_the_board(self.board)
                    self.switchTurn()
                    self.checkForFours()
                    self.printState()
                    return

        if move_type == 2:
            print("Selected move by %s at this round: Flip + Column %d" % (player.name, move + 1))
            print("Final Board after this round: ")
            self.board = self.flip_the_board(self.board)
            self.last_move = move
            player.flip -= 1
            print("Flip remains for %s is %d: " % (player.name, player.flip))
            for i in range(6):
                if self.board[i][move] == ' ':
                    self.board[i][move] = player.color
                    Utility.print_the_board(self.board)
                    self.switchTurn()
                    self.checkForFours()
                    self.printState()
                    return

        if move_type == 3:
            print("Selected move by %s at this round: Column %d + Flip" % (player.name, move + 1))
            print("Final Board after this round: ")
            player.flip -= 1
            self.last_move = 'flip'
            print("Flip remains for %s is %d: " % (player.name, player.flip))
            for i in range(6):
                if self.board[i][move] == ' ':
                    self.board[i][move] = player.color
                    self.board = self.flip_the_board(self.board)
                    Utility.print_the_board(self.board)
                    self.switchTurn()
                    self.checkForFours()
                    self.printState()
                    return

        if move_type == 4:
            print("Selected move by %s at this round: Flip + Column %d + Flip" % (player.name, move + 1))
            print("Final Board after this round: ")
            self.board = self.flip_the_board(self.board)
            self.last_move = 'flip'
            player.flip -= 2
            print("Flip remains for %s is %d: " % (player.name, player.flip))
            for i in range(6):
                if self.board[i][move] == ' ':
                    self.board[i][move] = player.color
                    self.board = self.flip_the_board(self.board)
                    Utility.print_the_board(self.board)
                    self.switchTurn()
                    self.checkForFours()
                    self.printState()
                    return

        print("Invalid move")
        return


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

    def checkForFours(self):
        # for each piece in the board...
        for i in range(6):
            for j in range(7):
                if self.board[i][j] != ' ':
                    # check if a vertical four-in-a-row starts at (i, j)
                    if self.verticalCheck(i, j):
                        self.finished = True
                        return

                    # check if a horizontal four-in-a-row starts at (i, j)
                    if self.horizontalCheck(i, j):
                        self.finished = True
                        return

                    # check if a diagonal (either way) four-in-a-row starts at (i, j)
                    # also, get the slope of the four if there is one
                    diag_fours, slope = self.diagonalCheck(i, j)
                    if diag_fours:
                        # print(slope)
                        self.finished = True
                        return

    def verticalCheck(self, row, col):
        # print("checking vert")
        fourInARow = False
        consecutiveCount = 0

        for i in range(row, 6):
            if self.board[i][col].lower() == self.board[row][col].lower():
                consecutiveCount += 1
            else:
                break

        if consecutiveCount >= 4:
            fourInARow = True
            if self.players[0].color.lower() == self.board[row][col].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        return fourInARow

    def horizontalCheck(self, row, col):
        fourInARow = False
        consecutiveCount = 0

        for j in range(col, 7):
            if self.board[row][j].lower() == self.board[row][col].lower():
                consecutiveCount += 1
            else:
                break

        if consecutiveCount >= 4:
            fourInARow = True
            if self.players[0].color.lower() == self.board[row][col].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        return fourInARow

    def diagonalCheck(self, row, col):
        fourInARow = False
        count = 0
        slope = None

        # check for diagonals with positive slope
        consecutiveCount = 0
        j = col
        for i in range(row, 6):
            if j > 6:
                break
            elif self.board[i][j].lower() == self.board[row][col].lower():
                consecutiveCount += 1
            else:
                break
            j += 1  # increment column when row is incremented

        if consecutiveCount >= 4:
            count += 1
            slope = 'positive'
            if self.players[0].color.lower() == self.board[row][col].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        # check for diagonals with negative slope
        consecutiveCount = 0
        j = col
        for i in range(row, -1, -1):
            if j > 6:
                break
            elif self.board[i][j].lower() == self.board[row][col].lower():
                consecutiveCount += 1
            else:
                break
            j += 1  # increment column when row is decremented

        if consecutiveCount >= 4:
            count += 1
            slope = 'negative'
            if self.players[0].color.lower() == self.board[row][col].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        if count > 0:
            fourInARow = True
        if count == 2:
            slope = 'both'
        return fourInARow, slope

    def findFours(self):
        """ Finds start i,j of four-in-a-row
            Calls highlightFours
        """

        for i in range(6):
            for j in range(7):
                if self.board[i][j] != ' ':
                    # check if a vertical four-in-a-row starts at (i, j)
                    if self.verticalCheck(i, j):
                        self.highlightFour(i, j, 'vertical')

                    # check if a horizontal four-in-a-row starts at (i, j)
                    if self.horizontalCheck(i, j):
                        self.highlightFour(i, j, 'horizontal')

                    # check if a diagonal (either way) four-in-a-row starts at (i, j)
                    # also, get the slope of the four if there is one
                    diag_fours, slope = self.diagonalCheck(i, j)
                    if diag_fours:
                        self.highlightFour(i, j, 'diagonal', slope)

    def highlightFour(self, row, col, direction, slope=None):
        """ This function enunciates four-in-a-rows by capitalizing
            the character for those pieces on the board
        """

        if direction == 'vertical':
            for i in range(4):
                self.board[row + i][col] = self.board[row + i][col].upper()

        elif direction == 'horizontal':
            for i in range(4):
                self.board[row][col + i] = self.board[row][col + i].upper()

        elif direction == 'diagonal':
            if slope == 'positive' or slope == 'both':
                for i in range(4):
                    self.board[row + i][col + i] = self.board[row + i][col + i].upper()

            elif slope == 'negative' or slope == 'both':
                for i in range(4):
                    self.board[row - i][col + i] = self.board[row - i][col + i].upper()

        else:
            print("Error - Cannot enunciate four-of-a-kind")

    def printState(self):
        # cross-platform clear screen
        # os.system(['clear', 'cls'][os.name == 'nt'])
        if not self.finished:
            print("  ====== Game: %d, Round: %d ====== " % (self.game, self.round))

        for i in range(5, -1, -1):
            print("\t", end="")
            for j in range(7):
                print("| " + str(self.board[i][j]), end=" ")
            print("|")
        print("\t  _   _   _   _   _   _   _ ")
        print("\t  1   2   3   4   5   6   7 ")

        if self.finished:
            print("Game Over!")
            if self.winner != None:
                print(str(self.winner.name) + " is the winner\n")
            else:
                print("Game was a draw\n")

    def print_final_board(self):
        for i in range(5, -1, -1):
            print("\t", end="")
            for j in range(7):
                print("| " + str(self.board[i][j]), end=" ")
            print("|")
        print("\t  _   _   _   _   _   _   _ ")
        print("\t  1   2   3   4   5   6   7 ")