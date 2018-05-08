from human_player import HumanPlayer
from ai_player import AIPlayer
from random_player import RandomPlayer
from utility import Utility


class ConniptionBoardGame(object):
    """ Game object that holds state of game board and game values
    """
    board = None
    round = None
    game = None
    is_game_finished = None
    winner = None
    whose_turn = None
    players = [None, None]
    disks = ["x", "o"]
    MAX_FLIP = 4
    last_move = None

    def __init__(self):
        self.round = 1
        self.game = 1
        self.is_game_finished = False
        self.winner = None
        self.last_move = None

        # ======================== Take Information from User =========================== #
        print("Welcome to Conniption Board Game")
        print("Should Player 1 be a Human/AI/Random?")
        while self.players[0] == None:
            choice = str(input("Type 'H'/'A'/'R': "))
            if choice.lower() == "human" or choice.lower() == "h":
                name = str(input("What is Player 1's name? "))
                self.players[0] = HumanPlayer(name, self.disks[0], self.MAX_FLIP) # Initializes a Human type player
            elif choice.lower() == "ai" or choice.lower() == "a":
                name = str(input("What is Player 1's name? "))
                depth = 3
                self.players[0] = AIPlayer(name, self.disks[0], self.MAX_FLIP, depth + 1)  # Initializes an AI type player
            elif choice.lower() == "random" or choice.lower() == "r":
                name = str(input("What is Player 1's name? "))
                self.players[0] = RandomPlayer(name, self.disks[0], self.MAX_FLIP) # Initializes a Random Player
            else:
                print("Invalid choice, please try again")
        print("{0} will be {1}".format(self.players[0].name, self.disks[0]))

        print("Should Player 2 be a Human/AI/Random?")
        while self.players[1] == None:
            choice = str(input("Type 'H'/'A'/'R': "))
            if choice.lower() == "human" or choice.lower() == "h":
                name = str(input("What is Player 2's name? "))
                self.players[1] = HumanPlayer(name, self.disks[1], self.MAX_FLIP)
            elif choice.lower() == "ai" or choice.lower() == "a":
                name = str(input("What is Player 2's name? "))
                depth = 3
                self.players[1] = AIPlayer(name, self.disks[1], self.MAX_FLIP, depth + 1)
            elif choice.lower() == "random" or choice.lower() == "r":
                name = str(input("What is Player 2's name? "))
                self.players[1] = RandomPlayer(name, self.disks[1], self.MAX_FLIP)
            else:
                print("Invalid choice, please try again")
        print("{0} will be {1}".format(self.players[1].name, self.disks[1]))



        # x always goes first
        self.whose_turn = self.players[0]
        self.create_the_board()

        # creating a conniption Game Board with 6 rows and 7 columns

    def create_the_board(self):
        self.board = []
        for i in range(6):
            self.board.append([])
            for j in range(7):
                self.board[i].append(' ')

    def start_new_game(self):
        """ Reset The Game Variables
        """
        self.round = 1
        self.game += 1
        self.is_game_finished = False
        self.winner = None
        self.last_move = None


        self.whose_turn = self.players[0]
        self.players[0].flip = 4
        self.players[1].flip = 4

        self.create_the_board()

    def switch_players_turn(self):
        """
        Switches players turn after each round
        :return: Object of next players
        """
        if self.whose_turn == self.players[0]:
            self.whose_turn = self.players[1]
        else:
            self.whose_turn = self.players[0]

        # increment the round number
        self.round += 1

    def choose_next_move(self):
        """
        This function defines what should be the next move of the players. Depending on the move and move type
        it changes the board accordingly.
        """
        player = self.whose_turn

        if self.whose_turn == self.players[0]:
            curr_player_flip = self.players[0].flip
            opp_player_flip = self.players[1].flip
        else:
            opp_player_flip = self.players[0].flip
            curr_player_flip = self.players[1].flip

        # there are only 42 legal places on the board, so after 42 moves, no legal move available
        if self.round > 42:
            self.is_game_finished = True
            return

        # move is the column that player want's to play
        # move type defines whether move includes any flip before or/and after the move

        move, move_type = player.move(self.board, curr_player_flip, opp_player_flip, self.last_move)

        # only move, no flip
        if move_type == 1:
            print("Selected move by %s at this round: Column %d" % (player.name, move + 1))
            print("Final Board after this round: ")
            print("Flip remains for %s is %d: " % (player.name, player.flip))
            self.last_move = move
            for i in range(6):
                if self.board[i][move] == ' ':
                    self.board[i][move] = player.color
                    Utility.print_the_board(self.board)
                    self.switch_players_turn()
                    self.is_there_any_connecting_four()
                    self.print_current_board()
                    return

        # First a flip and then move (Flip + column Number)
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
                    self.switch_players_turn()
                    self.is_there_any_connecting_four()
                    self.print_current_board()
                    return

        # First a move and then flip (column Number + Flip)
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
                    self.switch_players_turn()
                    self.is_there_any_connecting_four()
                    self.print_current_board()
                    return

        # Flip before and after a move (Flip + column Number + Flip)
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
                    self.switch_players_turn()
                    self.is_there_any_connecting_four()
                    self.print_current_board()
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

    def is_there_any_connecting_four(self):
        for i in range(6):
            for j in range(7):
                if self.board[i][j] != ' ':
                    # check if a vertical four-in-a-row starts at (i, j)
                    if self.any_connecting_four_vertically(i, j):
                        self.is_game_finished = True
                        return

                    # check if a horizontal four-in-a-row starts at (i, j)
                    if self.any_connecting_four_horizontally(i, j):
                        self.is_game_finished = True
                        return

                    # check if a diagonal (either way) four-in-a-row starts at (i, j)
                    diagonal_fours, slope = self.any_connecting_four_diagonally(i, j)
                    if diagonal_fours:
                        self.is_game_finished = True
                        return

    def identify_connecting_fours(self):
        for i in range(6):
            for j in range(7):
                if self.board[i][j] != ' ':
                    if self.any_connecting_four_vertically(i, j):
                        self.highlight_connecting_disks(i, j, 'vertical')

                    if self.any_connecting_four_horizontally(i, j):
                        self.highlight_connecting_disks(i, j, 'horizontal')

                    diagonal_fours, slope = self.any_connecting_four_diagonally(i, j)
                    if diagonal_fours:
                        self.highlight_connecting_disks(i, j, 'diagonal', slope)

    def any_connecting_four_vertically(self, row, col):
        """
        Check if there are four same disks vertically
        :param row: row number of the board
        :param col: column number of the board
        :return: True if there any connecting four
        """
        four_in_a_row = False
        in_a_row_count = 0

        for i in range(row, 6):
            if self.board[i][col].lower() == self.board[row][col].lower():
                in_a_row_count += 1
            else:
                break

        if in_a_row_count >= 4:
            four_in_a_row = True
            if self.players[0].color.lower() == self.board[row][col].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        return four_in_a_row

    def any_connecting_four_horizontally(self, row, col):
        """
        Check if there are four same disks horizontally
        :param row: row number of the board
        :param col: column number of the board
        :return: True if there any connecting four
        """
        four_in_a_row = False
        in_a_row_count = 0

        for j in range(col, 7):
            if self.board[row][j].lower() == self.board[row][col].lower():
                in_a_row_count += 1
            else:
                break

        if in_a_row_count >= 4:
            four_in_a_row = True
            if self.players[0].color.lower() == self.board[row][col].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        return four_in_a_row

    def any_connecting_four_diagonally(self, row, col):
        """
        Check if there are four same disks diagonally
        :param row: row number of the board
        :param col: column number of the board
        :return: True if there any connecting four
        """
        four_in_a_row = False
        count = 0
        slope = None

        # check for diagonals with positive slope
        in_a_row_count = 0
        j = col
        for i in range(row, 6):
            if j > 6:
                break
            elif self.board[i][j].lower() == self.board[row][col].lower():
                in_a_row_count += 1
            else:
                break
            j += 1  # increment column when row is incremented

        if in_a_row_count >= 4:
            count += 1
            slope = 'positive'
            if self.players[0].color.lower() == self.board[row][col].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        # check for diagonals with negative slope
        in_a_row_count = 0
        j = col
        for i in range(row, -1, -1):
            if j > 6:
                break
            elif self.board[i][j].lower() == self.board[row][col].lower():
                in_a_row_count += 1
            else:
                break
            j += 1  # increment column when row is decremented

        if in_a_row_count >= 4:
            count += 1
            slope = 'negative'
            if self.players[0].color.lower() == self.board[row][col].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        if count > 0:
            four_in_a_row = True
        if count == 2:
            slope = 'both'
        return four_in_a_row, slope



    def highlight_connecting_disks(self, row, col, direction, slope=None):
        """
        Highlights connecting four disks by converting them upper character
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

    def print_current_board(self):
        """
        Print the current Game board showing the disk positions
        :return:
        """
        if not self.is_game_finished:
            print("  ====== Game: %d, Round: %d ====== " % (self.game, self.round))

        for i in range(5, -1, -1):
            print("\t", end="")
            for j in range(7):
                print("| " + str(self.board[i][j]), end=" ")
            print("|")
        print("\t  _   _   _   _   _   _   _ ")
        print("\t  1   2   3   4   5   6   7 ")

        if self.is_game_finished:
            print("Game Over!")
            if self.winner != None:
                print(str(self.winner.name) + " is the winner\n")
            else:
                print("Game was a draw\n")

    def print_final_board(self):
        """
        Print the current Game board showing the disk positions after each round
        :return:
        """
        for i in range(5, -1, -1):
            print("\t", end="")
            for j in range(7):
                print("| " + str(self.board[i][j]), end=" ")
            print("|")
        print("\t  _   _   _   _   _   _   _ ")
        print("\t  1   2   3   4   5   6   7 ")