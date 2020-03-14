import random
from board import Board, RED_HOLES, RED_MANCALA, BLUE_MANCALA, BLUE_HOLES, N

# BOARD = Board(N)

# TODO: def heuristics1()

# TODO: def heuristics2()

# TODO: MiniMax():
# TODO: Alpha_Beta():
# TODO: calculate_point():


def payoff(board, move, player):
    new_board = Board(board)
    if player == 'red':
        # new_board.red_moves(move, clockwise=True)
        return (board[0] + board[12]) - (board[6] + board[18])
    else:
        return (board[6] + board[18]) - (board[0] + board[12])


def is_game_over(board):
    # there is any stones in red holes or blue hole, return False (game is not over)
    if any(board[1:4] + board[10:12] + board[13:16] + board[22:24]) or \
            any(board[4:6] + board[7:10] + board[16:18] + board[19:22]):
        return False
    else:
        return True


def get_available_moves(board, player):
    moves = []
    if player == 'red':
        for hole in RED_HOLES:
            if board[hole] != 0:
                moves.append(hole)
    else:
        for hole in BLUE_HOLES:
            if board[hole] != 0:
                moves.append(hole)
    return moves


def mini_max(depth, board, player):
    if depth > 5 or is_game_over(board):

    if player == 'red':
        best_value = -10 * N
        max_moves = get_available_moves(board, 'red')
        if max_moves == []:
            val = mini_max(depth+1, board, 'blue')
            if val > best_value:
                best_value = val
        for move in max_moves:
            val = mini_max(depth+1, board, (move, board, 1, True))

# def if_pass_opponent_mancala(board, move):
#     if move > 0:
#         if


def run_game():
    board = Board(N)
    board.display()
    first_player =  random.choice(random.choice(['red', 'blue']))
    while not is_game_over(board):
        # 1: clockwise move hole 1,  -1 counterclockwise move hole 1
        move = int(input('Please choose a hole and a direction to move: {}'.format(get_available_moves(board, 'red'))))
        if move > 0:
            board.red_moves(index=move)
        else:
            board.red_moves(index=move, clockwise=False)