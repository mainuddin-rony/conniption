class GameBoard():
    curr_player = None
    opp_player = None
    curr_player_flip = None
    opp_player_flip = None
    last_move = None
    board = None
    alpha = None
    selected_move = None
    instances = None
    move_type = None
    
    def __init__(self, curr_player=None, opp_player=None, curr_player_flip=None, opp_player_flip=None, last_move=None,
                 board=None):
        self.curr_player = curr_player
        self.opp_player = opp_player
        self.curr_player_flip = curr_player_flip
        self.opp_player_flip = opp_player_flip
        self.last_move = last_move
        self.board = board
        self.instances = []

    def set_alpha_value(self, value):
        self.alpha = value

    def set_selected_move(self, move):
        self.selected_move = move

    def add_instance(self, boardObj):
        self.instances.append(boardObj)

    def set_move_type(self, move_type):
        self.move_type = move_type
