from game_board import GameBoard
from minimax import Minimax

class AIPlayer():
    """
    Class for AI type player. AI Player chooses its next move based on MiniMax algorithm
    """
    depth = None
    flip = None

    def __init__(self, name, disk, flip, difficulty=3):
        self.type = "AI"
        self.name = name
        self.disk = disk
        self.depth = difficulty
        self.flip = flip

    def move(self, state, curr_player_flip, opp_player_flip, last_move):
        print("{0}'s turn.  {0} is {1}".format(self.name, self.disk))

        # Deciding who is the opponent player npw
        if self.dsik == 'x':
            opp_player = 'o'
        else:
            opp_player = 'x'

        m = Minimax(state)
        #creating a game board instance
        gameBoard = GameBoard(self.disk, opp_player, curr_player_flip, opp_player_flip, last_move, state)
        best_move, value, move_type = m.bestMove(self.depth, gameBoard)
        return best_move, move_type



