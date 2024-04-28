"""

Python file that contains the class 
that creates the game of connect 4.
Connect 4 is 1v1 game where players
take turns dropping a colored disc
into a nxm grid. The first player
to get 4 of their colored discs in
a row wins the game. The game is played 
in a pygame window.
The row can be up or down, left or right, or diagonally.
The window is composed of the grid and above the grid
lies the player's disc that is to be dropped into the grid.
When the move moves the mouse over the grid, the disc follows.
"""
import pygame 
import numpy as np
pygame.init()

class Game:
    def __init__(self, rows=6, cols=7, cell=100):
        self.rows = rows
        self.cols = cols
        self.cell_width = cell
        self.cell_height = cell
        self.disc_radius = self.cell_width // 2 - 5
        self.top_bar = self.disc_radius * 2
        self.window_width = self.cols * self.cell_width
        self.window_height = self.rows * self.cell_height + self.top_bar
        self.grid = np.zeros((self.rows, self.cols), dtype=int)
        self.turn = 1 # player 1 starts. player 1 is 1 and player 2 is 2
        self.player1_color = (255, 0, 0)
        self.player2_color = (255, 255, 0)
        self.disc_color = self.player1_color if self.turn == 1 else self.player2_color
        self.grid_color = (0, 0, 255)
        self.empty_color = (0, 0, 0)
        self.grid_width = 5
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        
        self.grid_height = self.window_height - self.top_bar
        self.winner = 0


    def draw_grid(self):
        # draw grid. So first draw rectangles and then draw circles
        self.window.fill(self.empty_color)
        for i in range(self.rows):
            for j in range(self.cols):
                pygame.draw.rect(self.window, self.grid_color, (j * self.cell_width, i * self.cell_height + self.top_bar, self.cell_width, self.cell_height))
                if self.grid[i][j] == 1:
                    pygame.draw.circle(self.window, self.player1_color, (j * self.cell_width + self.cell_width // 2, i * self.cell_height + self.cell_height // 2 + self.top_bar), self.disc_radius)
                elif self.grid[i][j] == 2:
                    pygame.draw.circle(self.window, self.player2_color, (j * self.cell_width + self.cell_width // 2, i * self.cell_height + self.cell_height // 2 + self.top_bar), self.disc_radius)
                else:
                    pygame.draw.circle(self.window, self.empty_color, (j * self.cell_width + self.cell_width // 2, i * self.cell_height + self.cell_height // 2 + self.top_bar), self.disc_radius)

    def change_turn(self):
        self.turn = 1 if self.turn == 2 else 2
        self.disc_color = self.player1_color if self.turn == 1 else self.player2_color

    def draw_disc(self):
        pygame.draw.circle(self.window, self.disc_color, (pygame.mouse.get_pos()[0], self.disc_radius), self.disc_radius)

    def drop_disc(self, col):
        for i in range(self.rows - 1, -1, -1):
            if self.grid[i][col] == 0:
                self.grid[i][col] = self.turn
                return True
        return False

    def check_winner(self):
        # Check horizontal
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1] - 3):
                if np.all(self.grid[i, j:j+4] == self.grid[i, j]) and self.grid[i, j] != 0:
                    self.winner = self.grid[i, j]

        # Check vertical
        for i in range(self.grid.shape[0] - 3):
            for j in range(self.grid.shape[1]):
                if np.all(self.grid[i:i+4, j] == self.grid[i, j]) and self.grid[i, j] != 0:
                    self.winner = self.grid[i, j]

        # Check diagonal
        for i in range(self.grid.shape[0] - 3):
            for j in range(self.grid.shape[1] - 3):
                if np.all(np.diag(self.grid[i:i+4, j:j+4]) == self.grid[i, j]) and self.grid[i, j] != 0:
                    self.winner = self.grid[i, j]
                
        for i in range(3, self.grid.shape[0]):
            for j in range(self.grid.shape[1] - 3):
                if np.all(np.diag(np.flipud(self.grid[i-3:i+1, j:j+4])) == self.grid[i, j]) and self.grid[i, j] != 0:
                    self.winner = self.grid[i, j]

        
    def draw_winner(self):
        # Create a font that fits the top bar and display the text where lies the top bar
        
        font = pygame.font.SysFont("Arial", self.top_bar)
        text = font.render(f"Player {self.winner} wins!", True, (255, 255, 255))
        self.window.blit(text, (0, 0))

    def play(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEMOTION and not self.winner:
                    self.draw_grid()
                    self.draw_disc()
                if event.type == pygame.MOUSEBUTTONDOWN and not self.winner:
                    col = pygame.mouse.get_pos()[0] // self.cell_width
                    if self.drop_disc(col):
                        self.draw_grid()
                        self.check_winner()
                        if self.winner:
                            print(f"Player {self.winner} wins!")
                            #running = False
                        self.change_turn()
            if self.winner:
                self.draw_winner()
            pygame.display.update()
        pygame.quit()