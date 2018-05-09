from game_board import GameBoard


class Minimax(object):
    """
    Implementation of MiniMax algorithm on current board
    """
    board = None
    disks = ["x", "o"]

    def __init__(self, board):
        # copy the board to self.board
        self.board = [x[:] for x in board]

    def bestMove(self, depth, gameBoard):

        for col in range(7):
            # if column col is a legal move...
            if self.is_legal_move(col, gameBoard.board):
                # make the move in column 'col' for curr_player
                temp = self.make_the_move(gameBoard.board, col, gameBoard.curr_player)
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
                if self.is_legal_move(col, gameBoard.board):
                    temp = self.make_the_move(gameBoard.board, col, gameBoard.curr_player)
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
                    if self.is_legal_move(col, flipped_board):
                        # make the move in column 'col' for curr_player
                        temp = self.make_the_move(flipped_board, col, gameBoard.curr_player)
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


    def is_legal_move(self, column, state):
        """ Boolean function to check if a move (column) is a legal move
        """

        for i in range(6):
            if state[i][column] == ' ':
                # once we find the first empty, we know it's a legal move
                return True

        # if we get here, the column is full
        return False

    def is_game_over(self, state):
        if self.check_for_streak(state, self.disks[0], 4) >= 1:
            return True
        elif self.check_for_streak(state, self.disks[1], 4) >= 1:
            return True
        else:
            return False

    def make_the_move(self, state, column, disk):
        """ Change a state object to reflect a player, denoted by disk,
            making a move at column 'column'

            Returns a copy of new state array with the added move
        """

        temp = [x[:] for x in state]
        for i in range(6):
            if temp[i][column] == ' ':
                temp[i][column] = disk
                return temp

    def calculate_board_value(self, board, disk):
        """ Simple heuristic to evaluate board configurations
            goodness = (current player's four-in-a-rows)*100000 + (current player's three-in-a-rows)*100 + (current player's two-in-a-rows)
            OR
            if the opponent has 1 or more four in a rows, then goodness = -100000
        """
        if disk == self.disks[0]:
            o_disk = self.disks[1]
        else:
            o_disk = self.disks[0]

        curr_fours = self.check_for_streak(board, disk, 4)
        curr_threes = self.check_for_streak(board, disk, 3)
        curr_twos = self.check_for_streak(board, disk, 2)

        opp_fours = self.check_for_streak(board, o_disk, 4)
        opp_threes = self.check_for_streak(board, o_disk, 3)
        opp_twos = self.check_for_streak(board, o_disk, 2)

        """
        (num of 4-in-a-rows)*99999 + (num of 3-in-a-rows)*100 + 
            (num of 2-in-a-rows)*10 - (num of opponent 4-in-a-rows)*99999 - (num of opponent
            3-in-a-rows)*100 - (num of opponent 2-in-a-rows)*10
        """

        # heuristic = (curr_fours)*99999 + (curr_threes)*100 + curr_twos * 10 - (opp_fours)*99999 - (opp_threes)*100 - (opp_twos)*10

        if opp_fours > 0:
            return -100000
        else:
            return curr_fours * 100000 + curr_threes * 100 + curr_twos
        # return heuristic

    def check_for_streak(self, board, disk, streak):
        count = 0
        # for each piece in the board...
        for i in range(6):
            for j in range(7):
                # ...that is of the disk we're looking for...
                if board[i][j].lower() == disk.lower():
                    # check if a vertical streak starts at (i, j)
                    count += self.check_vertical_streak(i, j, board, streak)

                    # check if a horizontal four-in-a-row starts at (i, j)
                    count += self.check_horizontal_streak(i, j, board, streak)

                    # check if a diagonal (either way) four-in-a-row starts at (i, j)
                    count += self.check_diagonal_streak(i, j, board, streak)
        # return the sum of streaks of length 'streak'
        return count

    def check_vertical_streak(self, row, col, board, streak):
        in_a_row_count = 0
        for i in range(row, 6):
            if board[i][col].lower() == board[row][col].lower():
                in_a_row_count += 1
            else:
                break

        if in_a_row_count >= streak:
            return 1
        else:
            return 0

    def check_horizontal_streak(self, row, col, board, streak):
        in_a_row_count = 0
        for j in range(col, 7):
            if board[row][j].lower() == board[row][col].lower():
                in_a_row_count += 1
            else:
                break

        if in_a_row_count >= streak:
            return 1
        else:
            return 0

    def check_diagonal_streak(self, row, col, board, streak):

        total = 0
        # check for diagonals with positive slope
        in_a_row_count = 0
        j = col
        for i in range(row, 6):
            if j > 6:
                break
            elif board[i][j].lower() == board[row][col].lower():
                in_a_row_count += 1
            else:
                break
            j += 1  # increment column when row is incremented

        if in_a_row_count >= streak:
            total += 1

        # check for diagonals with negative slope
        in_a_row_count = 0
        j = col
        for i in range(row, -1, -1):
            if j > 6:
                break
            elif board[i][j].lower() == board[row][col].lower():
                in_a_row_count += 1
            else:
                break
            j += 1  # increment column when row is incremented

        if in_a_row_count >= streak:
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
            if self.is_legal_move(i, boardInstance.board):
                temp = self.make_the_move(boardInstance.board, i, boardInstance.curr_player)
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
                    if self.is_legal_move(i, flipped_board):
                        last_move = i
                        temp = self.make_the_move(flipped_board, i, boardInstance.curr_player)
                        newBoard = GameBoard(boardInstance.opp_player, boardInstance.curr_player,
                                             boardInstance.opp_player_flip,
                                             boardInstance.curr_player_flip - 1, last_move, temp)
                        newBoard.set_move_type(2)
                        newBoard.set_selected_move(i)# 2 --> flip first then move
                        boardInstance.add_instance(newBoard)

        # legal_moves_with_move_first_then_flip

        if boardInstance.curr_player_flip > 0:
            for col in range(7):
                if self.is_legal_move(col, boardInstance.board):
                    temp = self.make_the_move(boardInstance.board, col, boardInstance.curr_player)
                    flipped_board = self.flip_the_board(temp)
                    if not self.are_boards_same(temp, flipped_board):
                        last_move = 'flip'
                        newBoard = GameBoard(boardInstance.opp_player, boardInstance.curr_player,
                                             boardInstance.opp_player_flip,
                                             boardInstance.curr_player_flip - 1, last_move, temp)
                        newBoard.set_move_type(3)
                        newBoard.set_selected_move(col)# 3 --> move first then flip
                        boardInstance.add_instance(newBoard)

        if depth == 0 or len(boardInstance.instances) == 0 or self.is_game_over(boardInstance.board):
            # return the heuristic value of node
            return self.calculate_board_value(boardInstance.board, boardInstance.curr_player)

        alpha = -99999999
        for child in boardInstance.instances:
            if child is None:
                print("child == None (search)")
            tmp_alpha = -self.iterative_search(depth - 1, child)
            child.set_alpha_value(tmp_alpha)
            alpha = max(alpha, tmp_alpha)
        return alpha
