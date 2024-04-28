"""

Entry point of the game. It creates a 
Game object and calls the play method to start the game.

"""

from Game.game import Game
import argparse




    

if __name__ == "__main__":
    # argparse the number of cols and rows
    parser = argparse.ArgumentParser(description="Connect 4 game")
    parser.add_argument("--rows", type=int, default=6, help="Number of rows in the grid")
    parser.add_argument("--cols", type=int, default=7, help="Number of cols in the grid")
    args = parser.parse_args()
    Connect4 = Game(args.rows, args.cols)
    Connect4.play()