from minimax import Minimax
from utility import Utility

class AIPlayer():
    """ AIPlayer object that extends Player
            The AI algorithm is minimax, the difficulty parameter is the depth to which
            the search tree is expanded.
        """

    difficulty = None
    flip = None

    def __init__(self, name, color, flip, difficulty=5):
        self.type = "AI"
        self.name = name
        self.color = color
        self.difficulty = difficulty
        self.flip = flip

    def move(self, state, curr_player_flip, opp_player_flip, last_move):
        print("{0}'s turn.  {0} is {1}".format(self.name, self.color))

        # sleeping for about 1 second makes it looks like he's thinking
        # time.sleep(random.randrange(8, 17, 1)/10.0)
        # return random.randint(0, 6)

        m = Minimax(state)
        best_move, value, move_type = m.bestMove(self.difficulty, state, self.color, curr_player_flip, opp_player_flip, last_move)
        copy_state = Utility.copy_the_board(state)
        jitbo = False
        if move_type == 1:
            tmp = Utility.make_temp_move(best_move, copy_state, self.color)
            if Utility.checkForConsecutives(tmp):
                jitbo = True
        if move_type == 2:
            tmp = Utility.flip_the_board(state)
            tmp = Utility.make_temp_move(best_move, tmp, self.color)
            if Utility.checkForConsecutives(tmp):
                jitbo = True

        if move_type == 3:
            tmp = Utility.make_temp_move(best_move, copy_state, self.color)
            tmp = Utility.flip_the_board(tmp)
            if Utility.checkForConsecutives(tmp):
                jitbo = True

        if jitbo:
            return best_move, move_type
        else:
            tmp_flip = Utility.flip_the_board(copy_state)
            b4_has_3, col = Utility.checkForConsecutives_3(copy_state)
            if b4_has_3:
                return col, 2
            af_has_3, col = Utility.checkForConsecutives_3(tmp_flip)
            if af_has_3:
                return col, 1
            return best_move, move_type

