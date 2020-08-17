import random
import numpy as np
import emoji as emj

from player import Player
from roles import Roles

O = emj.emojize(":o:", use_aliases=True)
X = emj.emojize(":x:", use_aliases=True)
vs = emj.emojize(":vs:", use_aliases=True)
pc = vs = emj.emojize(":computer:", use_aliases=True)
boardkey = {
    "1" : (0,0), "2": (0,1), "3": (0,2),
    "4" : (1,0), "5": (1,1), "6": (1,2),
    "7" : (2,0), "8": (2,1), "9": (2,2)
}
reference = {
    0: "  ",
    1: X,
    -1: O
}

class Board:
    def __init__(self):
        self.board = np.zeros((3, 3), dtype=int)
        self.winner = None
        self.choose_side()
        self.create_board()
        
    def create_board(self):
        print(f"Game board created: \n")
        i = 1
        while i < 10:
            if i != 1:
                print(f"----+----+----")
            print(f"  {i} |  {i+1} |  {i+2} ")
            i += 3
        
    def print_board(self):
        print(f"\nCurrent Game Board: \n")
        i, j = 0, 0
        while i < 3:
            if i != 0:
                print(f"----+----+----")
            print(f" {reference[self.board[i,j]]} | {reference[self.board[i,j+1]]} | {reference[self.board[i,j+2]]} ")
            i += 1
                
    def choose_side(self):
        while True:
            user_side = int(input(f"Plese choose your side: \n1: {X} (first player)\n2: {O} (second player)\n"))
            if user_side == 1:
                self.current_player = Roles.USER
                self.user = Player(1, X)
                self.pc = Player(-1, O)
                break
            elif user_side == 2:
                self.current_player = Roles.PC
                self.user = Player(-1, O)
                self.pc = Player(1, X)
                break
            else:
                print(f"Please enter 1 or 0.")
        print(f"\nUser: {self.user.emoji}  {vs}  PC: {self.pc.emoji}\n")
    
    def play_game(self):
        print(f"\nLet's start!")
        while self.winner is None:
            if self.current_player == Roles.PC:
                self.pc_move()
            elif self.current_player == Roles.USER:
                self.user_move()
            self.print_board()
            self.check_win()
            self.update_turns()
            if len(boardkey) == 0:
                print(f"\n {X} {O} DRAW MATCH!")
                return
        self.finished()

    def pc_move(self):
        print(f"\n{pc}'s turn")
        key = str(random.choice(list(boardkey.keys())))
        (i, j) = boardkey[key]
        self.board[i,j] = self.pc.side
        del boardkey[key]
        
    def user_move(self):
        key = self.input_movement()
        (i, j) = boardkey[key]
        self.board[i,j] = self.user.side
        del boardkey[key]

    def input_movement(self):
        while True:
            key = input("\nIt's your turn! Please select the position (1 - 9): ")
            if key not in boardkey.keys():
                print("Place is taken/ Index out of range")
                continue
            else:
                return key
    
    def update_turns(self):
        self.current_player = Roles.PC if self.current_player == Roles.USER else Roles.USER
        
    def check_win(self):
        # diagonal sum
        d1 = np.trace(self.board)
        d2 = np.trace(np.fliplr(self.board))
        # row and colum sum
        row = list(self.board.sum(axis=1))
        column = list(self.board.sum(axis=0))
        check_list = [d1, d2] + row + column
        if 3 in check_list or -3 in check_list:
            self.winner = self.current_player.name
            
    def finished(self):
        if self.winner == "USER":
            print(f"\nYou won! {self.user.emoji} is the WINNER!")
        else:
            print(f"\n{self.pc.emoji} is the WINNER!")