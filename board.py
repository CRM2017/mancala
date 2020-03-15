from termcolor import cprint

RED_HOLES = [0, 1, 2, 3, 10, 11, 13, 14, 15, 22, 23]
RED_MANCALA = [0, 12]
BLUE_MANCALA = [6, 18]
BLUE_HOLES = [4, 5, 6, 7, 8, 9, 16, 17, 19, 20, 21]
N = 4

# When start to move, return the next index of pit
def next_index(index, clockwise=True):
    if clockwise:
        index += 1
        if index > 23:
            index = 0
    else:
        index -= 1
        if index < 0:
            index = 23
    return index


# return adjacent horizontal and vertical holes
def adjacent_holes_indices(index):
    if index == 3:
        return [9, 4, 21]
    elif index == 4:
        return [3]
    elif index == 9:
        return [3, 10, 15]
    elif index == 10:
        return [9]
    elif index == 15:
        return [21, 9, 16]
    elif index == 16:
        return [4]
    elif index == 21:
        return [22, 15, 3]
    elif index == 22:
        return [21, 15, 3]


class Board:
    def __init__(self, board=None):
        if board is not None:
            self.board = board[:]
        else:
            self.board = [0, N, N, N, N, N, 0, N, N, N, N, N, 0, N, N, N, N, N, 0, N, N, N, N, N]

    def display(self):
        '''
        Board View:                     Index
                0                         6
              4   4                     5   7
              4   4                     4   8
          4 4 4   4 4 4           1  2  3   9  10 11
        0               0       0                    12
          4 4 4   4 4 4           23 22 21  15 14 13
              4   4                     20  16
              4   4                     19  17
                0                         18
        '''
        cprint(' '*8 + str(self.board[6]), 'blue', attrs=['bold'])
        cprint(' '*6 + str(self.board[5]) + '   ' + str(self.board[7]), 'blue')
        cprint(' '*6 + str(self.board[4]) + '   ' + str(self.board[8]), 'blue')

        cprint('  ' + str(self.board[1]) + ' ' + str(self.board[2]) + ' ' + str(self.board[3]), 'red', end='   ')
        cprint(str(self.board[9]), 'blue', end=' ')
        cprint(str(self.board[10]) + ' ' + str(self.board[11]), 'red')

        cprint(str(self.board[0]) + ' ' * 15 + str(self.board[12]), 'red', attrs=['bold'])

        cprint('  ' + str(self.board[23]) + ' ' + str(self.board[22]), 'red', end=' ')
        cprint(str(self.board[21]), 'blue', end='   ')
        cprint(str(self.board[15]) + ' ' + str(self.board[14]) + ' ' + str(self.board[13]), 'red')

        cprint(' '*6 + str(self.board[20]) + '   ' + str(self.board[16]), 'blue')
        cprint(' '*6 + str(self.board[19]) + '   ' + str(self.board[17]), 'blue')
        cprint(' '*8 + str(self.board[18]), 'blue', attrs=['bold'])

    def red_moves(self, index, clockwise=True, skip_opponent_mancala=False):
        play_again = False
        obtain_adjacent = None
        board = self.board[:]
        #  grab stones
        number_of_stones = self.board[index]
        board[index] = 0
        while number_of_stones > 0:
            number_of_stones -= 1
            index = next_index(index, clockwise)
            if index in BLUE_MANCALA:
                # Skip over the blue’s Mancala.
                if skip_opponent_mancala:
                    index += 1
                    board[index] += 1
                # place them directly in his Mancalas
                else:
                    # Place a stone in his opponent’s Mancala,
                    board[index] += 1
                    # take at most 2 stones from the opponent’s Mancala
                    if board[index] >= 2:
                        board[index] -= 2
                        # place them in his Mancalas.
                        board[0] += 2
                    else:
                        board[index] -= 1
                        board[0] += 1
            # if the red player drops a stone the last stone
            elif number_of_stones == 0:
                if index in RED_MANCALA:
                    play_again = True
                # if red player drops a stone into a hole that was previously empty and is on his side
                elif index in RED_HOLES and board[index] == 0:
                    adjacent_holes_list = adjacent_holes_indices(index)
                    obtain_adjacent = adjacent_holes_list
                board[index] += 1
            else:
                board[index] += 1
        return board, play_again, obtain_adjacent

    def blue_moves(self, index, clockwise=True, skip_opponent_mancala=False):
        board = self.board[:]
        play_again = False
        obtain_adjacent = None
        #  grab stones
        number_of_stones = board[index]
        board[index] = 0
        while number_of_stones > 0:
            number_of_stones -= 1
            index = next_index(index, clockwise)
            if index in RED_MANCALA:
                # Skip over the Red’s Mancala.
                if skip_opponent_mancala:
                    index += 1
                    board[index] += 1
                # place them directly in his Mancalas
                else:
                    # Place a stone in his opponent’s Mancala,
                    board[index] += 1
                    # take at most 2 stones from the opponent’s Mancala
                    if board[index] >= 2:
                        board[index] -= 2
                        # place them in his's Mancalas.
                        board[6] += 2
                    else:
                        board[index] -= 1
                        board[6] += 1
            # if the blue player drops a stone into his own Mancala, and it was the
            # last stone in his hand, he gets to play again
            elif number_of_stones == 0:
                if index in BLUE_MANCALA:
                    play_again = True
                # if blue player drops a stone into a hole that was previously empty and is on his side
                elif index in BLUE_HOLES and board[index] == 0:
                    adjacent_holes_list = adjacent_holes_indices(index)
                    obtain_adjacent = adjacent_holes_list
                board[index] += 1
            else:
                board[index] += 1
        return board, play_again, obtain_adjacent

    def run_move(self, board):
        self.board = board
