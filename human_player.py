from utility import Utility

class HumanPlayer():
    """
    This is the class for Human Player. Based on the number of flip available it collects input from the user and
    sends to ConniptionBoardGame class
    """
    type = None  # possible types are "Human" and "AI"
    name = None
    disk = None
    flip = None

    def __init__(self, name, disk, flip):
        self.type = "Human"
        self.name = name
        self.disk = disk
        self.flip = flip

    def move(self, state, curr_player_flip, opp_player_flip, last_move):
        print("{0}'s turn.  {0} is {1}".format(self.name, self.disk))
        # make a copy of the current board
        copy_board = Utility.copy_the_board(state)
        flip_number = self.flip

        # check if player has flip remained
        if flip_number > 0:
            # check if the last move is flip or not
            if last_move != 'flip':

                choice, temp_board, flip_number = self.choose_flip_option(copy_board, flip_number)

                if choice:
                    column, temp_board = self.choose_column(temp_board, self.disk)

                    if flip_number > 0:
                        choice, temp_board, flip_number = self.choose_flip_option(temp_board, flip_number)

                        if choice:
                            return column, 4
                        else:
                            return column, 2
                    else:
                        print(self.name + " has used all the flips.")
                        return column, 2
                else:
                    column, temp_board = self.choose_column(copy_board, self.disk)
                    choice, temp_board, flip_number = self.choose_flip_option(temp_board, flip_number)

                    if choice:
                        return column, 3
                    else:
                        return column, 1

            else:
                print("As the opponent's last move was a flip you can't choose a flip now.")
                column, temp_board = self.choose_column(copy_board, self.disk)
                choice, temp_board, flip_number = self.choose_flip_option(temp_board, flip_number)

                if choice:
                    return column, 3
                else:
                    return column, 1

        else:
            print(self.name + " has used up all the flips. No flip available.")
            column, temp_board = self.choose_column(copy_board, self.disk)
            return column, 1


    def choose_column(self, board, disc):
        """
        Gives user option to choose his move by take input the number of cloumn
        :param board: Current Board
        :param disc: Current player's disk
        :return: User move and the new board after the move
        """
        column = None
        while column == None:
            try:
                choice = int(input("Enter a move (by column number): ")) - 1
                if 0 <= choice <= 6:
                    if self.check_choice_validity(choice, board):
                        column = choice
                    else:
                        print("Invalid choice. The column is full. Please select other column.")
                else:
                    print("Invalid choice, try again")
            except ValueError:
                print("Invalid choice, try again")
                column = None

        print("Current Board: \n")
        temp_board = Utility.make_temp_move(column, board, disc)
        Utility.print_the_board(temp_board)

        return column, temp_board

    def choose_flip_option(self, temp_board, flip_number):
        """
        Ask user where he likes to flip the board
        :param temp_board: Current Game Board
        :param flip_number: Number of available flip now
        :return: User flip choice, new board after flip (if user flips it) and available flip number now
        """
        while True:
            flip_choice = input("Do you want to flip the board(yes/no): ")

            if flip_choice.lower() == 'yes' or flip_choice.lower() == 'y':
                flip_number -= 1
                print("%s is using a flip." % self.name)
                print("After flipping, the board: \n")
                flipped_board = Utility.flip_the_board(temp_board)
                Utility.print_the_board(flipped_board)

                return True, flipped_board, flip_number

            elif flip_choice.lower() == 'no' or flip_choice.lower() == 'n':
                return False, temp_board, flip_number
            else:
                print("Invalid choice, try again")

    def check_choice_validity(self, choice, board):
        for i in range(6):
            if board[i][choice] == ' ':
                return True
        return False

