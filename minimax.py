import random
from game_board import GameBoard

class Minimax(object):
    """ Minimax object that takes a current connect four board state
    """

    board = None
    colors = ["x", "o"]

    def __init__(self, board):
        # copy the board to self.board
        self.board = [x[:] for x in board]

    def bestMove(self, depth, gameBoard):

        for col in range(7):
            # if column i is a legal move...
            if self.isLegalMove(col, gameBoard.board):
                # make the move in column 'col' for curr_player
                temp = self.makeMove(gameBoard.board, col, gameBoard.curr_player)
                gameBoard.set_selected_move(col)
                tmp_last_move = col
                boardInstance = GameBoard(gameBoard.opp_player, gameBoard.curr_player, gameBoard.opp_player_flip, gameBoard.curr_player_flip, tmp_last_move, temp)

                alpha = -self.iterative_search(depth - 1, boardInstance)
                boardInstance.set_alpha_value(alpha)
                boardInstance.set_move_type(1)
                boardInstance.set_selected_move(col)
                gameBoard.add_instance(boardInstance)

        # legal_moves_with_move_first_then_Flip

        if gameBoard.curr_player_flip > 0:
            for col in range(7):
                if self.isLegalMove(col, gameBoard.board):
                    temp = self.makeMove(gameBoard.board, col, gameBoard.curr_player)
                    tmp_last_move = 'flip'
                    flipped_board = self.flip_the_board(temp)
                    if not self.are_boards_same(temp, flipped_board):
                        boardInstance = GameBoard(gameBoard.opp_player, gameBoard.curr_player,
                                                  gameBoard.opp_player_flip, gameBoard.curr_player_flip - 1, tmp_last_move,
                                                  flipped_board)

                        alpha = -self.iterative_search(depth - 1, boardInstance)
                        boardInstance.set_alpha_value(alpha)
                        boardInstance.set_move_type(3)
                        boardInstance.set_selected_move(col)
                        gameBoard.add_instance(boardInstance)

        # legal_moves_with_flip_first_then_move

        if gameBoard.curr_player_flip > 0 and gameBoard.last_move != 'flip':
            flipped_board = self.flip_the_board(gameBoard.board)
            if not self.are_boards_same(gameBoard.board, flipped_board):
                for col in range(7):
                    # if column i is a legal move...
                    if self.isLegalMove(col, flipped_board):
                        # make the move in column 'col' for curr_player
                        temp = self.makeMove(flipped_board, col, gameBoard.curr_player)
                        tmp_last_move = col

                        boardInstance = GameBoard(gameBoard.opp_player, gameBoard.curr_player,
                                                  gameBoard.opp_player_flip, gameBoard.curr_player_flip - 1,
                                                  tmp_last_move,
                                                  temp)

                        alpha = -self.iterative_search(depth - 1, boardInstance)
                        boardInstance.set_alpha_value(alpha)
                        boardInstance.set_move_type(2)
                        boardInstance.set_selected_move(col)
                        gameBoard.add_instance(boardInstance)



        best_alpha = -99999999
        best_move = None
        move_type = None  # 1 for move only, 2 for flip first then move and 3 for move first then flip

        for instance in gameBoard.instances:
            if instance.alpha >= best_alpha:
                best_alpha = instance.alpha
                best_move = instance.selected_move
                move_type = instance.move_type

        return best_move, best_alpha, move_type

    def search(self, depth, state, curr_player, curr_player_flip, opp_player_flip, last_move):
        """ Searches the tree at depth 'depth'
            By default, the state is the board, and curr_player is whomever
            called this search

            Returns the alpha value
        """

        # enumerate all legal moves from this state

        # legal_moves_without_any_flip
        legal_moves = []
        for i in range(7):
            # if column i is a legal move...
            if self.isLegalMove(i, state):
                # make the move in column i for curr_player
                temp = self.makeMove(state, i, curr_player)
                legal_moves.append(temp)

        # legal_moves_with_flip_first_then_move
        legal_moves_with_flip_first = []
        if curr_player_flip > 0 and last_move != 'flip':
            flipped_board = self.flip_the_board(state)
            if not self.are_boards_same(state, flipped_board):
                for i in range(7):
                    # if column i is a legal move...
                    if self.isLegalMove(i, flipped_board):
                        # make the move in column i for curr_player
                        temp = self.makeMove(flipped_board, i, curr_player)
                        legal_moves_with_flip_first.append(temp)

        # legal_moves_with_move_first_then_flip
        legal_moves_with_flip_last = []
        if curr_player_flip > 0:
            for col in range(7):
                if self.isLegalMove(col, state):
                    temp = self.makeMove(state, col, curr_player)
                    flipped_board = self.flip_the_board(temp)
                    if not self.are_boards_same(temp, flipped_board):
                        legal_moves_with_flip_last.append(flipped_board)

        # legal_moves_with_flip_move_flip = []
        # if curr_player_flip > 1 and last_move != 'flip':
        #     flipped_board = self.flip_the_board(state)
        #     if not self.are_boards_same(state, flipped_board):
        #         for i in range(7):
        #             # if column i is a legal move...
        #             if self.isLegalMove(i, flipped_board):
        #                 # make the move in column i for curr_player
        #                 temp = self.makeMove(flipped_board, i, curr_player)
        #                 temp_flip = self.flip_the_board(temp)
        #                 if not self.are_boards_same(state, temp_flip):
        #                     legal_moves_with_flip_move_flip.append(temp_flip)

        # if this node (state) is a terminal node or depth == 0...
        if depth == 0 or (len(legal_moves) == 0 and len(legal_moves_with_flip_last) == 0 and len(
                legal_moves_with_flip_first) == 0) or self.gameIsOver(
                state):
            # return the heuristic value of node
            return self.value(state, curr_player)

        # determine opponent's color
        if curr_player == self.colors[0]:
            opp_player = self.colors[1]
        else:
            opp_player = self.colors[0]

        alpha = -99999999
        for child in legal_moves:
            if child is None:
                print("child == None (search)")
            tmp_last_move = 'col'
            alpha = max(alpha,
                        -self.search(depth - 1, child, opp_player, opp_player_flip, curr_player_flip, tmp_last_move))

        if len(legal_moves_with_flip_first) > 0:
            for child in legal_moves_with_flip_first:
                if child is None:
                    print("child == None (search)")
                tmp_last_move = 'col'
                alpha = max(alpha, -self.search(depth - 1, child, opp_player, opp_player_flip, curr_player_flip - 1,
                                                tmp_last_move))

        if len(legal_moves_with_flip_last) > 0:
            for child in legal_moves_with_flip_last:
                if child is None:
                    print("child == None (search)")
                tmp_last_move = 'flip'
                alpha = max(alpha, -self.search(depth - 1, child, opp_player, opp_player_flip, curr_player_flip - 1,
                                                tmp_last_move))

        # if len(legal_moves_with_flip_move_flip) > 0:
        #     for child in legal_moves_with_flip_move_flip:
        #         if child is None:
        #             print("child == None (search)")
        #         tmp_last_move = 'flip'
        #         alpha = max(alpha, -self.search(depth - 1, child, opp_player, opp_player_flip, curr_player_flip - 2,
        #                                         tmp_last_move))
        return alpha

    def isLegalMove(self, column, state):
        """ Boolean function to check if a move (column) is a legal move
        """

        for i in range(6):
            if state[i][column] == ' ':
                # once we find the first empty, we know it's a legal move
                return True

        # if we get here, the column is full
        return False

    def gameIsOver(self, state):
        if self.checkForStreak(state, self.colors[0], 4) >= 1:
            return True
        elif self.checkForStreak(state, self.colors[1], 4) >= 1:
            return True
        else:
            return False

    def makeMove(self, state, column, color):
        """ Change a state object to reflect a player, denoted by color,
            making a move at column 'column'

            Returns a copy of new state array with the added move
        """

        temp = [x[:] for x in state]
        for i in range(6):
            if temp[i][column] == ' ':
                temp[i][column] = color
                return temp

    def value(self, state, color):
        """ Simple heuristic to evaluate board configurations
            Heuristic is (num of 4-in-a-rows)*99999 + (num of 3-in-a-rows)*100 + 
            (num of 2-in-a-rows)*10 - (num of opponent 4-in-a-rows)*99999 - (num of opponent
            3-in-a-rows)*100 - (num of opponent 2-in-a-rows)*10
        """
        if color == self.colors[0]:
            o_color = self.colors[1]
        else:
            o_color = self.colors[0]

        my_fours = self.checkForStreak(state, color, 4)
        my_threes = self.checkForStreak(state, color, 3)
        my_twos = self.checkForStreak(state, color, 2)
        opp_fours = self.checkForStreak(state, o_color, 4)
        # opp_threes = self.checkForStreak(state, o_color, 3)
        # opp_twos = self.checkForStreak(state, o_color, 2)
        if opp_fours > 0:
            return -100000
        else:
            return my_fours * 100000 + my_threes * 100 + my_twos

    def checkForStreak(self, state, color, streak):
        count = 0
        # for each piece in the board...
        for i in range(6):
            for j in range(7):
                # ...that is of the color we're looking for...
                if state[i][j].lower() == color.lower():
                    # check if a vertical streak starts at (i, j)
                    count += self.verticalStreak(i, j, state, streak)

                    # check if a horizontal four-in-a-row starts at (i, j)
                    count += self.horizontalStreak(i, j, state, streak)

                    # check if a diagonal (either way) four-in-a-row starts at (i, j)
                    count += self.diagonalCheck(i, j, state, streak)
        # return the sum of streaks of length 'streak'
        return count

    def verticalStreak(self, row, col, state, streak):
        consecutiveCount = 0
        for i in range(row, 6):
            if state[i][col].lower() == state[row][col].lower():
                consecutiveCount += 1
            else:
                break

        if consecutiveCount >= streak:
            return 1
        else:
            return 0

    def horizontalStreak(self, row, col, state, streak):
        consecutiveCount = 0
        for j in range(col, 7):
            if state[row][j].lower() == state[row][col].lower():
                consecutiveCount += 1
            else:
                break

        if consecutiveCount >= streak:
            return 1
        else:
            return 0

    def diagonalCheck(self, row, col, state, streak):

        total = 0
        # check for diagonals with positive slope
        consecutiveCount = 0
        j = col
        for i in range(row, 6):
            if j > 6:
                break
            elif state[i][j].lower() == state[row][col].lower():
                consecutiveCount += 1
            else:
                break
            j += 1  # increment column when row is incremented

        if consecutiveCount >= streak:
            total += 1

        # check for diagonals with negative slope
        consecutiveCount = 0
        j = col
        for i in range(row, -1, -1):
            if j > 6:
                break
            elif state[i][j].lower() == state[row][col].lower():
                consecutiveCount += 1
            else:
                break
            j += 1  # increment column when row is incremented

        if consecutiveCount >= streak:
            total += 1

        return total

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

    def are_boards_same(self, state, flipped_board):
        for i in range(6):
            for j in range(7):
                if state[i][j] != flipped_board[i][j]:
                    return False

        return True

    def iterative_search(self, depth, boardInstance):
        for i in range(7):
            if self.isLegalMove(i, boardInstance.board):
                temp = self.makeMove(boardInstance.board, i, boardInstance.curr_player)
                last_move = i
                newBoard = GameBoard(boardInstance.opp_player, boardInstance.curr_player, boardInstance.opp_player_flip,
                                     boardInstance.curr_player_flip, last_move, temp)
                newBoard.set_move_type(1)
                newBoard.set_selected_move(i)
                boardInstance.add_instance(newBoard)

        # legal_moves_with_flip_first_then_move

        if boardInstance.curr_player_flip > 0 and boardInstance.last_move != 'flip':
            flipped_board = self.flip_the_board(boardInstance.board)
            if not self.are_boards_same(boardInstance.board, flipped_board):
                for i in range(7):
                    if self.isLegalMove(i, flipped_board):
                        last_move = i
                        temp = self.makeMove(flipped_board, i, boardInstance.curr_player)
                        newBoard = GameBoard(boardInstance.opp_player, boardInstance.curr_player,
                                             boardInstance.opp_player_flip,
                                             boardInstance.curr_player_flip - 1, last_move, temp)
                        newBoard.set_move_type(2)
                        newBoard.set_selected_move(i)# 2 --> flip first then move
                        boardInstance.add_instance(newBoard)

        # legal_moves_with_move_first_then_flip

        if boardInstance.curr_player_flip > 0:
            for col in range(7):
                if self.isLegalMove(col, boardInstance.board):
                    temp = self.makeMove(boardInstance.board, col, boardInstance.curr_player)
                    flipped_board = self.flip_the_board(temp)
                    if not self.are_boards_same(temp, flipped_board):
                        last_move = 'flip'
                        newBoard = GameBoard(boardInstance.opp_player, boardInstance.curr_player,
                                             boardInstance.opp_player_flip,
                                             boardInstance.curr_player_flip - 1, last_move, temp)
                        newBoard.set_move_type(3)
                        newBoard.set_selected_move(col)# 3 --> move first then flip
                        boardInstance.add_instance(newBoard)

        if depth == 0 or len(boardInstance.instances) == 0 or self.gameIsOver(boardInstance.board):
            # return the heuristic value of node
            return self.value(boardInstance.board, boardInstance.curr_player)


        alpha = -99999999
        for child in boardInstance.instances:
            if child is None:
                print("child == None (search)")
            tmp_alpha = -self.iterative_search(depth - 1, child)
            child.set_alpha_value(tmp_alpha)
            alpha = max(alpha, tmp_alpha)
        return alpha
