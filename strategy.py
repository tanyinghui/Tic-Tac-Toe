import random
import numpy as np

class Strategy:
    def __init__(self):
        self.pc = -1 # initialise as O 
        self.user = 1 # initialise as X
        self.board = np.zeros((3, 3), dtype=int)

    def first_move(self):
        (self.pc, self.user) = (self.user, self.pc) # exchange side

    def update_board(self, board):
        self.board = board

    def check_status(self):
        (i, j) = self.check_if_pc_can_win() if all(self.check_if_pc_can_win()) else self.check_if_user_can_win()
        if i is None:
            return self.position_win_in_next_move()
        return (i, j)

    def check_winning_status(self, target):
        # Check Rows and Columns
        for i in range(3):
            if np.count_nonzero(self.board[i,:] == target) == 2 and 0 in self.board[i,:]:
                return (i, list(self.board[i,:]).index(0))
            elif np.count_nonzero(self.board[:,i] == target) == 2 and 0 in self.board[:,i]:
                return (list(self.board[:,i]).index(0), i)
        
        flip_matrix = np.fliplr(self.board)
        # Check diagonal
        if np.count_nonzero(self.board.diagonal() == target) == 2 and 0 in self.board.diagonal():
            index = list(self.board.diagonal()).index(0)
            return (index, index)
        elif np.count_nonzero(flip_matrix.diagonal() == target) == 2 and 0 in flip_matrix.diagonal():
            index = list(flip_matrix.diagonal()).index(0)
            if index == 1:
                return (index, index)
            elif index == 0:
                return (index, 2)
            elif index == 2:
                return (index, 0)
        return (None, None)

    def check_if_pc_can_win(self):
        return self.check_winning_status(self.pc)

    def check_if_user_can_win(self):
        return self.check_winning_status(self.user)

    def position_win_in_next_move(self):
        (row, column) = np.where(self.board == 0)
        if len(row) == 1:
            return (row[0], column[0])
        i = random.randint(0, len(row)-1)
        return (row[i], column[i])