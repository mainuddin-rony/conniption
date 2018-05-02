from conniptionboardgame import ConniptionBoardGame


def main():
    conniption = ConniptionBoardGame()
    player1 = conniption.players[0]
    player2 = conniption.players[1]

    score_board = [0, 0, 0]  # [p1 wins, p2 wins, ties]
    count = 1

    while count < 21:
        conniption.printState()
        while not conniption.finished:
            conniption.nextMove()

        conniption.findFours()
        conniption.print_final_board()

        if conniption.winner == None:
            score_board[2] += 1

        elif conniption.winner == player1:
            score_board[0] += 1

        elif conniption.winner == player2:
            score_board[1] += 1

        printStats(player1, player2, score_board)
        count += 1

        conniption.newGame()


def printStats(player1, player2, win_counts):
    print("\n")
    print("{0}: {1} wins, {2}: {3} wins, {4} ties".format(player1.name,
                                                          win_counts[0], player2.name, win_counts[1], win_counts[2]))
    print("\n")


if __name__ == "__main__":  # Default "main method" idiom.
    main()