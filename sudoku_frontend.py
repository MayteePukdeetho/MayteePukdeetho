#import needed modules
import pygame, sys
from sudoku_generator import *
from GUI_LESS import *
from constans import *

#setup pygame modules
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #creates a 720 by 720 screen
pygame.display.set_caption("Sudoku") # the white bar ontop of the thingy says Sudoku now.
game_state = "title"
setup = 1
#checks if a certain box is clicked. Parameters are the x and y coordinateds of mouse click and
#all boxes on screen. Maybe not the best implementation. returns the boxes index.
def check_if_clicked(x,y,boxes):
    #print(x,y)
    for index, box in enumerate(boxes):
        box_coords = pygame.Rect(box)
        #after 2 hours of uh, not knowing this exists, it does.
        #this checks if it was clicked or not. fun.
        if box_coords.collidepoint(x,y):
            print(f"box using {box} at {index} was clicked.")
            return index

#pro tip, theres a little > you can use to collapse the thingy.
def draw_title_screen():
    #list of we want to be interactable with textboxes on the title screen.
    boxes = []
    #sets up the background
    screen.fill((10, 10, 10))
    #Set up Fonts to be used.
    title_font = pygame.font.SysFont("comicsans", 100)
    option_select_font = pygame.font.Font(None, 50)
    textbox_font = pygame.font.SysFont(None, 35)
    #Set up a surfaces to be applied to a textbox
    title_surface = title_font.render("Sudoku", True, (60,70,100))
    option_select_surface = option_select_font.render("Select your difficulty", True, (60,70,100))
    textbox_easy_surface = textbox_font.render("easy", True, (0,255,0))
    textbox_medium_surface = textbox_font.render("medium", True, (0,0,255))
    textbox_hard_surface = textbox_font.render("hard", True, (255,0,0))
    #sets up a textboxs (in paranthese is the position)
    title_rect = title_surface.get_rect(center = (360, 100))
    option_rect = option_select_surface.get_rect(center = (360, 360))
    textbox_easy_rect = textbox_easy_surface.get_rect(center = (180, 500))
    textbox_medium_rect = textbox_medium_surface.get_rect(center = (360, 500))
    textbox_hard_rect = textbox_hard_surface.get_rect(center = (540, 500))
    # these are the boxes we want to interact with on the title screen
    boxes.append(textbox_easy_rect)
    boxes.append(textbox_medium_rect)
    boxes.append(textbox_hard_rect)
    #actually draws the surface in the textbox
    screen.blit(title_surface, title_rect)
    screen.blit(option_select_surface, option_rect)
    #to make the buttons look fancy, we will draw rectangles behind them.
    #(what we are drawing on, color, position and dimentions, line thickness)
    pygame.draw.rect(screen, (255,255,255), textbox_easy_rect)
    pygame.draw.rect(screen, (255,255,255), textbox_medium_rect)
    pygame.draw.rect(screen, (255,255,255), textbox_hard_rect)
    screen.blit(textbox_easy_surface, textbox_easy_rect)
    screen.blit(textbox_medium_surface, textbox_medium_rect)
    screen.blit(textbox_hard_surface, textbox_hard_rect)
    #this is what we will be checking with.
    return boxes




def draw_main_screen():
    screen.fill(MAIN_SCREEN_BG)
    #lets draw the grid (10X10)
    for num in range(1, 10):
        #vertical lines
        pygame.draw.line(screen,(0,0,0),(num*SCREEN_WIDTH/10,0),(num*SCREEN_WIDTH/10,720), 10)
        #horizontal lines
        pygame.draw.line(screen, (0, 0, 0), (0, num * SCREEN_HEIGHT / 10), (720, num * SCREEN_HEIGHT / 10), 10)
    #fill the unused space with black boxes
    pygame.draw.rect(screen, (0,0,0), (SIDE_BAR))
    pygame.draw.rect(screen,(0,0,0),(BOTTOM_BAR))
    #print the numbers
    for row in range(0,9):
        for col in range(0,9):
            current_num = given_board.board[row][col]
            #hide the 0 numbers
            if current_num == 0:
                current_num_surface = box_font.render(f"{current_num}", True, (MAIN_SCREEN_BG))
            else:
                current_num_surface = box_font.render(f"{current_num}", True, (60,70,100))
            current_num_rect = current_num_surface.get_rect(topleft = ((row)*SCREEN_WIDTH/10+SCREEN_WIDTH/35,(col)*SCREEN_HEIGHT/10+SCREEN_HEIGHT/50))
            #parse
            screen.blit(current_num_surface, current_num_rect)
    pygame.display.flip()

while True:
    #watch for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            #
        if event.type == pygame.MOUSEBUTTONDOWN:
            #title logic
            if game_state == "title":
                x, y = event.pos
                print(x, y)
                # this gets the (x, y coordinates of the top left of the rectangle and the width, height)
                # (x,y, width, height)
                # the bottom right coordinates should be the  x + width, y + height
                #comments are holdover from learning
                # test = (pygame.Rect(textbox_easy_rect))
                difficulty = check_if_clicked(x, y, boxes)
                if difficulty != None:
                    game_state = "main"

            #main logic
            if game_state == "main":
                pass

    if game_state == "title":
        boxes = draw_title_screen()
    if game_state == "main":
        if setup == 1:
            #setting up sudoku boards for the frontend
            the_boards = sudoku_setup(difficulty)
            given_board = the_boards[0]
            solved_board = the_boards[1]
            solved_board.print_board()
            print("AHHHHHHHHHHHHHHHHHH")
            given_board.print_board()
            draw_main_screen()
            setup = 0



    pygame.display.flip()