
import random

#global variables
MINIMUM_SIZE = 5
MAXIMUM_SIZE = 10
###################### Functions ##########################
#save
def save_game(BOARD, MINES, size):
    try:
        with open("gamesave.txt", "w") as save:
            save.write(str(size) + '\n')
            for row in range(size):
                for col in range(size):
                    save.write(str(BOARD[row][col]))
                save.write('\n')
            for row in range(size):
                for col in range(size):
                    save.write(str(MINES[row][col]))
                save.write('\n')
    except:
        print("Sorry, something went wrong, couldn't save the game. Please try again.")
        quit()

#load saved game
def load_game():
    x = -1
    size = 0
    board = []
    mines = []
    #goes through file and finds other pieces
    with open("gamesave.txt", "r") as load:
        for line in load:
            if x == -1:
                size = int(line)
                x +=1
            elif x < size:
                board.append(list(line.rstrip()))
                x +=1
            else:
                mines.append(list(line.rstrip()))
    return (board, mines, size)
                
def create_blank_board(size):
    #generate blank board to be used
    blank_board = [['*' for i in range(size)] for i in range(size)]
    return blank_board

#generates mines 
def create_mines(size):
    i = 0
    number_of_mines = size - 1
    temp_board = create_blank_board(size)

    #generate mine board
    while i != number_of_mines:
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        if temp_board[x][y] != 'X':
            temp_board[x][y] = 'X'
            i += 1
        else:
            continue
    return temp_board

#prints the board
def display_board(BOARD, size):
    toplabel = '  '
        
    for i in range(size):
        toplabel = toplabel + str(i) + ' '
    print(toplabel)
        
    i = 0
    for row in BOARD:
        print(i, *row, ' ')
        i += 1

#check for mines next to move
def mine_check(col, row, MINES, size):
    mines = 0
    try:
        #checks the top
        if MINES[row - 1][col] == 'X' and row + 1 > -1:
            mines += 1
    except:
        pass
    try:
        #checks the bottom 
        if MINES[row + 1][col] == 'X' and row + 1 < (size - 1):
            mines += 1
    except:
        pass
    try:
        #checks the left side
        if MINES[row][col - 1] == 'X' and col - 1 > -1:
            mines += 1
    except:
        pass
    try:
        #checks the right side
        if MINES[row][col + 1] == 'X' and col + 1 < (size - 1):
            mines += 1
    except:
        pass
    try:
        #checks top right
        if MINES[row - 1][col + 1] == 'X' and (row - 1 > -1 and col + 1 < (size - 1)):
            mines += 1
    except:
        pass
    try:
        #checks bottom right
        if MINES[row + 1][col + 1] == 'X' and (row + 1 < (size - 1) and col + 1 < (size - 1)):
            mines += 1
    except:
        pass
    try:
        #checks top left
        if MINES[row - 1][col - 1] == 'X' and (row - 1 > -1 and col - 1 > -1):
            mines += 1
    except:
        pass
    try:
        #check bottom left
        if MINES[row + 1][col - 1] == 'X' and (row + 1 < (size - 1) and col - 1 > -1):
            mines += 1
    except:
        pass
    return int(mines)

def place_move(col, row, BOARD, MINES, size):
    BOARD[int(row)][int(col)] = mine_check(int(col), int(row), MINES, size)
    return BOARD

def not_a_mine(col, row, MINES):
    if MINES[int(row)][int(col)] != 'X':
        return True
    else:
        return False

def game_won_decider(moves, size):
    temp = (size * size) - (size - 1)
    if moves == temp:
        return True
    else:
        return False

#play the game
def play_game(BOARD, MINES, size):
    not_dead = True
    game_won = False
    move_count = 0

    while not_dead and not game_won:
        #option to play, save or quit
        print("What would you like to do?:")
        print(" 1: choose a cell")
        print(" 2: save and quit(so you can come back again)")
        print(" 3: quit without saving")
        print("--------------------------------------------------")
        option = input("?: ")

        #perform option
        if option == '1':
            pass
        elif option == '2':
            save_game(BOARD, MINES, size)
            quit()
        elif option == '3':
            quit()
        else:
            print("Error, choose a correct option.")
            continue
        #displays board and collects user inputs
        display_board(BOARD, size)
        try:
            row = input("Pick a row: ")
            col = input("Pick a column: ")
            BOARD = place_move(col, row, BOARD, MINES, size)
            display_board(BOARD, size)
        except:
            print("invalid, Try agian.")
            continue
        
        if not not_a_mine(col, row, MINES):
            not_dead = False
        move_count += 1
        #print("Nice pick, keep going!")
        #print("-----------------------")
        if game_won_decider(move_count, size):
            break

    #game over depending on win or loss
    if not_dead:
        print("Congrats! You won the game! Thanks for playing.")
    else:
        print("Noo, you found a bomb, sorry! Try again, maybe you'll win:)")
        print("----------------------------------------------------------")
        try:
            x = input("Please press a button to exit the game.")
            quit
        except:
            quit
        
################################ Main ################################
def main():
    #initial prompt
    print("Hello, Welcome to Minesweeper v1.")
    print("---------------------------------")
 
    while True:
        #collect user preference
        print("You can either start a new game or continue from a save game?")
        print(" 1: Start a new game")
        print(" 2: Continue a saved game")
        print("--------------------------------------------------------------")
        temp = input("?: ")
        option = int(temp)
        if option == 1 or option == 2:
            break
        else:
            print("Please press either 1 or 2")
    if option == 1:
        #collect board size
        while True:
            try:
                boardSize = input("What size board would you like to play on(5-10): ")
                board_size = int(boardSize)
                
                #error check
                if board_size < MINIMUM_SIZE or board_size > MAXIMUM_SIZE:
                    print("Error, Please enter a number between 5 and 10.")
                    continue
                else:
                    break
            except ValueError:
                print("Please enter a number")

        #passes size into function
        BOARD = create_blank_board(board_size)
        MINES = create_mines(board_size)
        display_board(BOARD, board_size)

        #play game
        play_game(BOARD, MINES, board_size)
        
    elif option == 2:
        #calls function
        try:
            BOARD, MINES, board_size = load_game()
        except:
            print("Seems like there's no saved file. Try starting a new game and save it.")
            main()
        #generates board
        display_board(BOARD, board_size)
        #play game
        play_game(BOARD, MINES, board_size)
main()