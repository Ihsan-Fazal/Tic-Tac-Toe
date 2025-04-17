
import random
import time
from datetime import date, datetime
import mysql.connector
 
# initialising mySQL connection
mydb = mysql.connector.connect(host="localhost", user="root", password="ihsan")
mycursor = mydb.cursor()
 
 
class ImpVar:
    """stores important variables for use anywhere"""
 
    win_counter, loss_counter = 0, 0
    tied_counter, match_counter = 0, 0
    move_counter = None
    today = date.today()
    now = datetime.now()
    date = today.strftime("%d-%m-%y")
    time = now.strftime("%H:%M:%S")
    res_stmnt = None
 
 
def clean_slate(today, now):
    """resets all impvar values"""
    ImpVar.win_counter, ImpVar.loss_counter = 0, 0
    ImpVar.tied_counter, ImpVar.match_counter = 0, 0
    ImpVar.date = today.strftime("%d-%m-%y")
    ImpVar.time = now.strftime("%H:%M:%S")
 
 
def file_init():
    """first initialisation of record file"""
    f1 = open("RECORD.TXT", 'w')  # writes recent session's summary to file
    f1.write("~" * 30 + "\n")
    f1.close()
 
 
def data_check(dt_name, d_type):
    """used for checking if database or table exists"""
    flag = 0
    for x in mycursor:
        if x[0] == dt_name:
            flag = 1
    if flag == 0 and d_type == "D":
        mycursor.execute("create database data")
    if flag == 0 and d_type == "T":
        mycursor.execute("create table scores(sDate {1}, sTime {1}, sMatches {0}, sWins {0}, sLosses {0}, sTied {0})".format("int(3)", "varchar(20)"))
 
 
def display():
    """display mysql content"""
    db = mysql.connector.connect(host="localhost", user="root", password="ihsan", database="data")
    cursor = db.cursor()
    cursor.execute("select * from scores")
    results = cursor.fetchall()
    if len(results) == 0:
        print("Empty set!")
        return
    print()
    print("+----------+----------+----------------+------+--------+------+------+\n"
          "| Date     | Time     | Matches Played | Wins | Losses | Tied | Win% |\n"
          "+----------+----------+----------------+------+--------+------+------+")
    for i in results:
        win_percent = int(i[3]/i[2] * 100)
        i += (win_percent,)
        print("| {} | {} | {:<14} | {:<4} | {:<6} | {:<4} | {:<4} |".format(*i))
    print("+----------+----------+----------------+------+--------+------+------+")
 
 
def print_board(board):
    global a
    a = "  {1}  |  {2}  |  {3}  \n-----------------\n  {4}  |  {5}  |  {6}  \n-----------------\n  {7}  |  {8}  |  {9}  \n"
    print()
    print(a.format(*board))
 
 
def x_o_picker():
    while True:
        inpx = input("Please choose either X or O: ")
        if inpx in "xX1":
            print("X selected!")
            return "X"
        if inpx in "oO0":
            print("O selected!")
            return "O"
        else:
            print("Please input one of the specified options!")
 
 
def space_is_free(board, pos):
    return board[pos] == " "
 
 
def board_full(b):
    for i in range(1, 10):
        if b[i] == " ":
            return False
    else:
        return True
 
 
def insert_char(b, p, c):
    b[p] = c
 
 
def win_check(b, c):
    if ((b[1] == b[2] == b[3] == c) or
            (b[4] == b[5] == b[6] == c) or
            (b[7] == b[8] == b[9] == c) or
            (b[1] == b[4] == b[7] == c) or
            (b[2] == b[5] == b[8] == c) or
            (b[3] == b[6] == b[9] == c) or
            (b[1] == b[5] == b[9] == c) or
            (b[3] == b[5] == b[7] == c)):
        return True
    else:
        return False
 
 
def p_move(board, char):
    """player move code"""
    if board_full(board):
        return
 
    move = True
    while move:
 
        try:
            pos = int(input("Enter position (from 1 to 9): "))
            if 0 < pos < 10:
                while move:
                    if space_is_free(board, pos) is True:
                        insert_char(board, pos, char)
                        ImpVar.move_counter += 1
                        move = False
                    else:
                        print("Position is already occupied!\n")
                        break
 
            else:
                print("Please enter a valid number!\n")
 
        except ValueError:
            print("Enter a number!\n")
 
 
def comp_move(board, char):
    """ai code"""
    if board_full(board):
        return
 
    if char == "X":
        comp_char = "O"
    else:
        comp_char = "X"
        
    corner_list, edge_list = [], []
    possible_moves = []
    move = 0
    for i in range(1, len(board)):  # makes list of possible moves
        if board[i] == " ":
            possible_moves.append(i)
 
    for i in possible_moves:  # makes list of edges open
        if i in [2, 4, 6, 8]:
            edge_list.append(i)
 
    for i in possible_moves:  # makes list of corners open
        if i in [1, 3, 7, 9]:
            corner_list.append(i)
 
    # checks if win is possible or blocks opp. win
    for temp in [comp_char, char]:
        for i in possible_moves:
            board_copy = board.copy()
            board_copy[i] = temp
            if win_check(board_copy, temp) is True:
                move = i
                break
        else:
            continue
        break
    
    if move == 0:
 
        while True:
            next_move = random.random()  # decides next best move
            if next_move < 0.3 and len(edge_list) > 0:
                move = edge_list[random.randrange(0, len(edge_list))]
                break
            if 0.3 <= next_move <= 0.6:
                if 5 in possible_moves:
                    move = 5
                    break
                elif len(edge_list) > 0:
                    move = edge_list[random.randrange(0, len(edge_list))]  # change to corner-list and AI becomes harder
                    break
            if next_move > 0.6 and len(corner_list) > 0:
                move = corner_list[random.randrange(0, len(corner_list))]
                break
            if len(corner_list) == 0 and len(edge_list) == 0:
                if 5 in possible_moves:
                    move = 5
                break
                             
    insert_char(board, move, comp_char)
    ImpVar.move_counter += 1
    print("Computer placed \"{}\" at position {}".format(comp_char, move))
 
 
def play_again():
    while True:
        inpmain = input("Would you like to play again? (Y/N): ")
        if inpmain in ["Y", "y", "Yes", "yes"]:
            rep = 1
            break
        if inpmain in ["N", "n", "No", "no"]:
            rep = 0
            break
        else:
            print("Please enter a valid input!")
    return rep
 
 
def main():
    # first element is test as it allows us to follow 123 as the numbering system
    global board
    board = ["test", " ", " ", " ", " ", " ", " ", " ", " ", " "]
    # game_state 0 indicates comp win, 1 indicates player win and 2 indicates tie
    game_state = 2
    ImpVar.move_counter = 0  # countmoves
    char = x_o_picker()
 
    # X = player, O = comp
    if char == "X":
        print_board(board)
        while not (board_full(board)):
            if win_check(board, "O") is False:  # checks for computers win
                p_move(board, char)
                if win_check(board, char) is True:  # checks for players win
                    game_state = 1
                    break
                comp_move(board, char)
                print_board(board)
            else:
                game_state = 0
                break
 
    if char == "O":
        while not board_full(board):
            if win_check(board, char) is False:  # checks for players win
                comp_move(board, char)
                print_board(board)
                if win_check(board, "X") is True:  # checks for computers win
                    game_state = 0
                    break
                p_move(board, char)
            else:
                game_state = 1
                break
 
    # conclusion statement
    if game_state == 2:
        ImpVar.tied_counter += 1
        ImpVar.res_stmnt = "GAME TIED"
        print(ImpVar.res_stmnt)
 
    if game_state == 1:
        ImpVar.win_counter += 1
        print_board(board)
        ImpVar.res_stmnt = "PLAYER WINS!"
        print(ImpVar.res_stmnt)
 
    if game_state == 0:
        ImpVar.loss_counter += 1
        ImpVar.res_stmnt = "COMPUTER WINS!"
        print(ImpVar.res_stmnt + " Better luck next time!")
 
    ImpVar.match_counter += 1  # counts matches played
 
 
########################################################################################################################
# main program
mycursor.execute("show databases")
data_check("data", "D")  # checks if database is present
mycursor.execute("use data")
mycursor.execute("show tables")  # checks if table is present
data_check("scores", "T")
 
 
print("------------------------")
print("!WELCOME TO TIC TAC TOE!")
print("------------------------")
 
while True:
    clean_slate(ImpVar.today, ImpVar.now)
    print()
    print("-" * 28)
    print("1. START NEW GAME\n"
          "2. SHOW PREVIOUS SESSION SUMMARY\n"
          "3. SHOW ALL TIME SCORES\n"
          "4. HOW TO PLAY\n"
          "5. QUIT")
    print("-" * 28)
    ch = None
    try:
        ch = int(input("Enter Your Choice: "))
    except ValueError:
        print("Please enter a number!")
        continue
 
    if ch == 1:
        file_init()
        while True:
            print("-" * 28)
            main()
            print()
            time.sleep(1.5)
 
            f1 = open("RECORD.TXT", 'a')  # writes recent session's summary to file
            f1.write("{0} | Match Number: {1}\n".format(ImpVar.date, str(ImpVar.match_counter)))
            f1.write("Result: {}\n".format(ImpVar.res_stmnt))
            f1.write("Number of moves: {}\n".format(str(ImpVar.move_counter)))
            f1.write("~" * 30 + "\n")
 
            replay = play_again()  # asks user if they want to play again
 
            if replay == 1:
                continue
            if replay == 0:
                # inserting data into sql
                mycursor.execute("insert into scores values(\"{0}\", \"{1}\", \"{2}\", {3}, {4}, {5})".format(ImpVar.date,
                                                                                                          ImpVar.time,
                                                                                                          ImpVar.match_counter,
                                                                                                          ImpVar.win_counter,
                                                                                                          ImpVar.loss_counter,
                                                                                                          ImpVar.tied_counter))   
                mydb.commit()
 
                # inserting data into files
                f1 = open("RECORD.TXT", "a")
                f1.write("Total number of matches played: {}".format(str(ImpVar.match_counter)))
                break
 
    elif ch == 2:
        f1 = open("RECORD.TXT", 'r')
        r = f1.read()
        print("\n" + r)
        print(input("Press Enter to continue"), end="")
 
    elif ch == 3:
        display()
        print(input("Press Enter to continue"), end="")
 
    elif ch == 4:
        f2 = open("HOW.txt", 'r')
        r = f2.read()
        print(r)
        print(input("Press Enter to continue"), end="")
 
    elif ch == 5:
        for i in "Saving,.,.,.,\rSaved!".split(","):
            print(i, end="")
            time.sleep(0.4)
        break
 
    else:
        print("INVALID OPTION")

                                                      
















        
