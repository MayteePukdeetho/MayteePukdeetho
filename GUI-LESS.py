from sudoku_generator import *
import copy
#used for creating another board
def greeting_screen():
    print("Welcome to Sudoku!")
    choice = int(input("Choose your difficulty. \n[1 for Easy], [2 for Medium], [3 for Hard] "))
    return choice
#given board is what we will compare to solved board so to compare between the two.
def sudoku_setup(choice):
    print(choice)
    if choice == 1:
        solved_board = SudokuGenerator(9,30)
        given_board = SudokuGenerator(9,30)
    elif choice == 2:
        solved_board = SudokuGenerator(9,40)
        given_board = SudokuGenerator(9,40)
    elif choice == 3:
        solved_board = SudokuGenerator(9,50)
        given_board = SudokuGenerator(9,50)
    solved_board.fill_values()
    #deepcopy lets me copy the actual list, not just the refrence
    given_board.board = copy.deepcopy(solved_board.get_board())
    given_board.remove_cells(given_board.removed_cells)
    return [given_board, solved_board]

#checking if all cells are filled and finalized
def Board_Full(given_board, list_of_erasable_cells):
    if list_of_erasable_cells != []:
        return False
    for row in range(0,9):
        for col in range(0,9):
            if given_board.board[row][col] == 0:
                return False
    return True

#checks if there is a winner
def check_if_winner(given_board, solved_board):
    for row in range(0,9):
        for col in range(0,9):
            if given_board.board[row][col] != solved_board.board[row][col]:
                return False
    return True



#game_over_screen
def game_over(the_result):
    if the_result == 0:
        print("Congratulations, you won!")
    elif the_result == -1:
       print("Thanks for playing!")
    elif the_result == 1:
        print("Sorry, you lost")
    else:
        pass
    play_on = int(input("Press 1 to play again. "))
    if play_on == 1:
        the_boards = sudoku_setup(greeting_screen())
        given_board = the_boards[0]
        solved_board = the_boards[1]
        Sudoku_Game(given_board, solved_board)
    else:
        exit()
#how we will track the cells we can erase, and what we can't.
def erasable_cells(resseted_board):
    list_of_erasable_cells = []
    list_of_unerasable_cells = []
    for row in range(0,9):
        for col in range(0,9):
            if resseted_board[row][col] == 0:
                list_of_erasable_cells.append((row,col))
            else:
                list_of_unerasable_cells.append((row,col))

    return list_of_erasable_cells, list_of_unerasable_cells

#it comes up enough to warrant it's own function.
def select_a_row_and_column(given_board):
    selected_row = input("Select what row you want to select: ")
    selected_col = input("Select what column you want to select: ")
    if selected_row.isdigit() == False or selected_col.isdigit() == False or selected_col == '9' or selected_row == '9':
        print("Invalid input, try again.")
        select_a_row_and_column(given_board)
    else:
        return int(selected_row), int(selected_col)

#prints board, where, finalized numbers are bolded, sketched numbers are normal,
#and unerasable numbers are in italics.
def print_fancy_board(given_board, list_of_erasable_cells, list_of_unerasable_cells, list_of_finalized_cells):
    for row in range(0,9):
        print(" ")
        for col in range(0,9):
            if (row, col) in list_of_finalized_cells:
                #asci markdown codes or whatever can make it bold or something like that.
                print(f"\033[1m{given_board.board[row][col]}\033[0m", end=" ")
            if (row, col) in list_of_unerasable_cells:
                print(f"\033[3m{given_board.board[row][col]}\033[0m", end=" ")
            if (row, col) in list_of_erasable_cells:
                print(given_board.board[row][col], end=" ")
    print("\n")



def Sudoku_Game(given_board, solved_board):
    #for the reset function
    resetted_board = copy.deepcopy(given_board.get_board())
    Game_Over = False
    #Keeps track of what type of cells are what type of cells.
    list_of_erasable_cells, list_of_unerasable_cells = erasable_cells(resetted_board)
    list_of_finalized_cells = []


#this is really messy i need to fix this
    def menu(given_board):
        print("Choose your option:")
        #printing out the menu for the first time
        selection = int(input("1. Sketch in a cell \n2. Display the board \n3. Reset the board \n4. Exit\n5. Cheat (For Developers Only!)\n6. Erase a Cell.\n7. Finalize a Cell. "))
        #sketching in a cell, this...
        if selection == 1:
            #prompts the user to select a cell
            selected_row, selected_col = select_a_row_and_column(given_board)
            #invalid selection, send back to menu.
            if given_board.board[selected_row][selected_col] != 0:
                print("The cell you selected is already filled!")
                menu(given_board)
                #valid selection, but a number is already there (not 0).
                if (selected_row, selected_col) in list_of_erasable_cells:
                    #asking are you sure?
                    choice = int(input("This cell is able to be overwritten. Do you want to overwrite it? [1 for yes]"))
                    #user confirms.
                    if choice == 1:
                        #asks what number the cell will be filled in with.
                        selected_num = int(input("What number do you want to fill the cell in with? [0 to cancel selection] "))
                        #user cancels the selection.
                        if selected_num == 0:
                            #back to the menu!
                            menu(given_board)
                        #sketches in the number.
                        given_board.board[selected_row][selected_col] = selected_num
                #back to the menu.
                menu(given_board)
            #it's the same thing from above. theres probably a way to do this better. (sketch in function?)
            selected_num = int(input("What number do you want to fill the cell in with? [0 to cancel selection] "))
            if selected_num == 0:
                #he cancelled it.
                menu(given_board)
            #sketches in the number, again.
            given_board.board[selected_row][selected_col] = selected_num
            print("Cell sketched successfully!")
            menu(given_board)

        if selection == 2:
            #uses the lists from before to print out the board.
            print_fancy_board(given_board, list_of_erasable_cells, list_of_unerasable_cells, list_of_finalized_cells)
            menu(given_board)
        if selection == 3:
            #resets every finalized cell.
            are_you_sure= int(input("Are you sure? Input 1 to confirm."))
            if are_you_sure == 1:
                #go through every finalized cell, and replace that with 0. then clear finalized cell list.
                #also, since all of these cells can be erased now, add them to the erasable cells list.
                for pair in list_of_finalized_cells:
                    row = pair[0]
                    col = pair[1]
                    given_board.board[row][col] = 0
                    list_of_erasable_cells.append((row,col))
                list_of_finalized_cells.clear()

                menu(given_board)
        if selection == 4:
            #quits out the game.
            return game_over(-1)
        #for testing purposes only
        if selection == 5:
            #go through each cell and make it so it matches the correct solution, and adding it to
            #the finalized cell list, except for the bottom right cell. Useful for testing.
            for row in range(0,9):
                for col in range(0,9):
                    if given_board.board[row][col] == 0:
                        given_board.board[row][col] = solved_board.board[row][col]
                        list_of_finalized_cells.append((row,col))
                        list_of_erasable_cells.remove((row,col))
            given_board.board[8][8] = 0
            list_of_finalized_cells.pop()
            list_of_erasable_cells.append((8,8))
            print(f"The final number is: {solved_board.board[8][8]}")
            menu(given_board)
        #Erases a cell.
        if selection == 6:
            selected_row, selected_col = select_a_row_and_column(given_board)
            #checks if the cell is in the erasable cell list.
            if (selected_row, selected_col) not in list_of_erasable_cells:
                #it's not.
                print("Invalid cell selection!")
                menu(given_board)

            else:
                #it is. Maybe I should prompt user for if they're sure.
                choice = int(input(f"Are you sure you want to erase cell in row:{selected_row} col:{selected_col}? [1 for yes]"))
                if choice == 1:
                    given_board.board[selected_row][selected_col] = 0
                    print("Cell erased successfully!")
                    menu(given_board)
                else:
                    menu(given_board)
        if selection == 7:
            #finalizes a cell, making it being unable to erased, but making it be able to submit for grading
            selected_row, selected_col = select_a_row_and_column(given_board)
            #make sure it's valid.
            if (selected_row, selected_col) not in list_of_erasable_cells or given_board.board[selected_row][selected_col] == 0:
                print("Invalid cell selection!")
                menu(given_board)
            else:
                choice = int(input("Are you sure you want to finalize this cell? [1 for yes] "))
                if choice == 1:
                    #Finalizes the cell.
                    list_of_finalized_cells.append((selected_row,selected_col))
                    list_of_erasable_cells.remove((selected_row,selected_col))
                    print("Cell finalized successfully!")
                    #Check if the board is full.
                    Full = Board_Full(given_board, list_of_erasable_cells)
                    if Full == False:
                        menu(given_board)
                    if Full == True:
                        #Did you do it correctly?
                        winner = check_if_winner(given_board, solved_board)
                        if winner == True:

                            return game_over(0)
                        else:
                            return game_over(1)
                    #Boards not full.
                    menu(given_board)
                else:
                    menu(given_board)


#uh, main gameplay loop I guess. I forgot this was here.
    while not Game_Over:
        print("This is your board!")
        given_board.print_board()
        the_result = menu(given_board)
        game_over(the_result)
        Game_Over = True
#checks if there is a winner

#This is how we setup our boards.
if __name__ == "__main__":
    the_boards = sudoku_setup(greeting_screen())
    given_board = the_boards[0]
    solved_board = the_boards[1]
    Sudoku_Game(given_board, solved_board)

