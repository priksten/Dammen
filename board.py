import pygame

class Board():

    def __init__(self, screen):
        self.board = []
        self.screen = screen
        self.width = 700
        self.height = 700
        self.rows = 10
        self.cols = 10
        self.square_size = 70
        

    def draw_board(self, screen):
        # screen.fill((244,164,96))
        pygame.draw.rect(screen, (244,164,95), pygame.Rect(30, 30, 60, 60))
        pygame.display.flip()
        # for row in range(self.rows):
        #    for col in range(row%2, self.rows, 2):
        #        pygame.draw.rect(screen, (205, 197, 191), self.rows*self.square_size, self.cols*self.square_size, self.square_size, self.square_size)
