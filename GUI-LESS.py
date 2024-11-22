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


#game_over_screen
def game_over(the_result):
    if the_result == 0:
        print("Congratulations, you won!")
        Continue = int(input("Play again? [1 for yes]"))
    if the_result == -1:
        Continue = int(input(("Thanks for playing! [1 to try again]")))
    if the_result == 1:
        print("Sorry, you lost")
        Continue = int(input("Play again? [1 for yes]"))
    if Continue == 1:
        the_boards = sudoku_setup(greeting_screen())
        given_board = the_boards[0]
        solved_board = the_boards[1]
        Sudoku_Game(given_board, solved_board)
    else:
        pass



def Sudoku_Game(given_board, solved_board):
    #for the reset function
    resetted_board = copy.deepcopy(given_board.get_board())
    Game_Over = False

#this is really messy i need to fix this
    def menu(given_board):
        print("Choose your option:")
        selection = int(input("1. Fill in a cell \n2. Display the board \n3. Reset the board \n4. Exit\n"))
        if selection == 1:
            selected_row = int(input("Select what row you want to select: "))
            selected_col = int(input("Select what column you want to select: "))
            if given_board.board[selected_row][selected_col] != 0:
                print("The cell you selected is already filled!")
                menu(given_board)
            selected_num = int(input("What number do you want to fill the cell in with? [0 to cancel selection]"))
            if selected_num == 0:
                pass #implement menu function
            given_board.board[selected_row][selected_col] = selected_num
            print("Cell filled successfully!")
            #checking if all cells are filled
            def Board_Full(given_board):
                for row in range(0,8):
                    for col in range(0,8):
                        if given_board.board[row][col] == 0:
                            return False
                return True
            Full = Board_Full(given_board)
            if Full == False:
                menu(given_board)
            if Full == True:
                Winner = check_if_winner(given_board,solved_board)
                if Winner == True:
                    return 0
                else:
                    return 1

        if selection == 2:
            given_board.print_board()
            menu(given_board)
        if selection == 3:
            are_you_sure= int(input("Are you sure? Input 1 to confirm."))
            if are_you_sure == 1:
                given_board.board = resetted_board
                menu(given_board)
        if selection == 4:
            return -1
    while not Game_Over:
        print("This is your board!")
        given_board.print_board()
        the_result = menu(given_board)
        game_over(the_result)
        Game_Over = True
#checks if there is a winner
def check_if_winner(given_board, solved_board):
    for row in range(0,8):
        for col in range(0,8):
            if given_board.board[row][col] != solved_board.board[row][col]:
                return False
    return True

if __name__ == "__main__":
    the_boards = sudoku_setup(greeting_screen())
    given_board = the_boards[0]
    solved_board = the_boards[1]
    Sudoku_Game(given_board, solved_board)

