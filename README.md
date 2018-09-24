# Conniption AI Game
This project requires to build us an AI based game of conniption (Classical version of Connect Four). Using Minimax algorithm, I implemented the strategy to choose the next move based on a heuristic. The short description of the different classes of the code and evaluation function are provided below.

# Requirements
This program needs python 3 to run.

# Game Description
You need to run main.py for starting the game. It prompts users to create 2 players of types either Human, Random or AI. It also asks for name the player. For random and AI type player it chooses its move internally but for Human type player it prompts user to input his/her move. Based on the flipping rule and flipping availability it also asks for whether user wants to flip the board. User should provide ‘yes’ or ‘no’ as the answer. After each move, it checks for connecting four disks, highlights them (by making the disk character capital letter) if there any and finishes the game. It asks the user whether she wants to play next game and continues accordingly.

# Code Description
This project has 8 classes. 
Main.py: It is the main class of the project. It starts the game and keeps the result as the game progresses. 

Conniptionboardgame.py: It prompts the user for player information and initializes the board and  player objects according to the information. It also keeps track who is the current player, what was the last move, who is the winner, is the game finished etc. Based on the move chosen by the players and flip choice, it changes the board and displays it. It also contains the function for checking the connecting four disks vertically, horizontally or diagonally.

Ai_palyer.py: It creates an AI type player object. Based on the current status of the board and other player information, it chooses the next move using minimax algorithm and then returns the move and flipping choice to Conniptionboardgame.py

Human_player.py: It creates a human type player object and prompts for user input of next move and flipping choice. After each move (column choice or flip) it changes the board accordingly to helps the player understand the current situation of the game. It also controls user of choosing flipping option ( like is  the player has any flip left, or is the last move of the opponent player a flip).

Random_player.py: This class is for creating random type player object. It chooses it column moves randomly (chooses among 1 to 7 randomly). It also chooses its flipping option randomly. But to maintain a minimum standard flipping, I generated a weighted list of flipping option ( 70% no flip, 15% flip + column move and 15% column move + flip) and it chooses the flipping option randomly from this list. 

Game_board.py: This class keeps track of the status of the current board and instance of this class is provided as an input for minimax algorithm. It also has a list to store the other game board instances which is generated from this game board considering all the moves possible up to certain depth.

Minmax.py: This class contains the implementation of the minimax algorithm. It creates all the possible valid moves iteratively up to certain depth (I used depth 3) based on the current status of the board and players (like who is the current player, how many flip she has, what was the last ove etc) and stored the board’s value returned by an evaluation function. For expanding the nodes, I only considers 3 types of move - column move only, flip + column move, and column move + flip. I didn’t consider flip + column move + flip combination but it can take this combination as an input from other players. After judging the all child nodes value, it chooses the best move. To calculate the board value it also has a function which considers the number of streaks of length k. 

Utility.py: It contains some utility functions like copy the game board, flipping the board etc.

# Choosing Heuristic for Minimax
I tried with couple of heuristics for the minimax algorithm. With trial and error, I finally came up with two heuristics which produced primarily a good  result. 
Heuristic 1: (4-in-a-rows of X)*99999 + (3-in-a-rows of X)*100 + (2-in-a-rows of X)*10 - (4-in-a-rows of O)*99999 - (3-in-a-rows of O)*100 - (2-in-a-rows of O)*10
Heuristic 2: (four-in-a-rows for X)*100000 + (three-in-a-rows for X)*100 + (two-in-a-rows for X) Or if the opponent has 1 or more four in a rows, then return -100000

I played the AI player against a random player 100 times when my AI went first, and also 100 times when it went later with both the heuristics.
After observing the playing behaviour of the AI player with heuristic 1, I found that it didn’t defend when the opponent has 3 disks in a row and opponent can make it four in a streak at next move. So, I needed a better strategy to prevent this and came up with the second heuristic which performed better when the AI went second. The main idea behind this strategy to assign a greater negative value to show the higher advantage of the opponent at the current situation. To assure that it also holds the performance when it goes first like the previous heuristic, I ran the play 100 times more and it won all the games. That’s why my final version of the game chooses second heuristic.
