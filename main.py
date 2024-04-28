"""

Entry point of the game. It creates a 
Game object and calls the play method to start the game.

"""

import pygame
from Game.game import Game

def main():
    # to do : argparse the number of cols and rows and why not the size of the window
    Connect4 = Game()
    Connect4.play()

if __name__ == "__main__":
    main()