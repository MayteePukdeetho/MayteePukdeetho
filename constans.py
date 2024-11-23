#This is to make the sudoku_frontend look nicer.
import pygame
pygame.init()
SCREEN_WIDTH = 720
SCREEN_HEIGHT = 720
SIDE_BAR = (SCREEN_WIDTH-SCREEN_WIDTH/10,0,SCREEN_WIDTH/10,SCREEN_HEIGHT)
BOTTOM_BAR = (0,SCREEN_HEIGHT-SCREEN_HEIGHT/10, SCREEN_WIDTH, SCREEN_HEIGHT/10)
#font we will use in the boxes
box_font = pygame.font.SysFont(None, (int((SCREEN_HEIGHT/9))))
MAIN_SCREEN_BG = (200, 200, 200)