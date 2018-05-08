from conniptionboardgame import ConniptionBoardGame


def main():
    """
    Initialize Game Board and Player Settings. start_new_game restarts the game from beginning
    """
    conniption = ConniptionBoardGame()
    player1 = conniption.players[0]
    player2 = conniption.players[1]

    score_board = [0, 0, 0]  # [player1 wins, player2 wins, ties]
    count = 1

    while count < 101:
        conniption.print_current_board()
        while not conniption.is_game_finished:
            conniption.choose_next_move()

        conniption.identify_connecting_fours()
        conniption.print_final_board()

        if conniption.winner is None:
            score_board[2] += 1

        elif conniption.winner == player1:
            score_board[0] += 1

        elif conniption.winner == player2:
            score_board[1] += 1

        print_score_board(player1, player2, score_board)
        count += 1

        conniption.start_new_game()


def print_score_board(player1, player2, win_counts):
    print("\n")
    print("{0}: {1} wins, {2}: {3} wins, {4} ties".format(player1.name,
                                                          win_counts[0], player2.name, win_counts[1], win_counts[2]))
    print("\n")


if __name__ == "__main__":
    main()