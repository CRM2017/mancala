import random
from board import Board, RED_HOLES, RED_MANCALA, BLUE_MANCALA, BLUE_HOLES, N



# TODO: def heuristics1()

# TODO: def heuristics2()

# TODO: MiniMax():
# TODO: Alpha_Beta():
# TODO: calculate_point():


def payoff(board, player):
    board = board.board
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


count = 0
def mini_max(depth, board, player):
    global count
    count +=1
    print(board.board, count)
    if depth > 2 or is_game_over(board.board):
        print("payoff:", payoff(board,player))
        return payoff(board,player), None
    if player == 'red':
        best_value = (-10 * N), None  # best_value (score, move)
        max_moves = get_available_moves(board.board, 'red')
        if max_moves == []:
            val = mini_max(depth+1, board, 'blue')
            if val > best_value:
                best_value = val, None
        for move in max_moves:
            cw_move_result = board.red_moves(index=move) # clockwise move
            ccw_move_result = board.red_moves(index=move, clockwise=False) # counter-clockwise move

            cw_val = mini_max(depth+1, Board(cw_move_result[0]), 'blue')
            ccw_val = mini_max(depth + 1, Board(ccw_move_result[0]), 'blue')
            best_value = max(cw_val[0], ccw_val[0], best_value[0]), move
        return best_value

    elif player == 'blue':
        best_value = (10 * N), None
        max_moves = get_available_moves(board.board, 'blue')
        if max_moves == []:
            val = mini_max(depth + 1, board, 'red')
            if val > best_value:
                best_value = val, None
        for move in max_moves:
            cw_move_result = board.red_moves(index=move)  # clockwise move
            ccw_move_result = board.red_moves(index=move, clockwise=False)  # counter-clockwise move
            cw_val = mini_max(depth + 1, Board(cw_move_result[0]), 'red')
            ccw_val = mini_max(depth + 1, Board(ccw_move_result[0]), 'red')
            best_value = max(cw_val[0], ccw_val[0], best_value[0]), move
        return best_value


# def if_pass_opponent_mancala(board, move):
#     if move > 0:
#         if


def run_game():
    board = Board()
    board.display()
    first_player = random.choice(random.choice(['red', 'blue']))
    while not is_game_over(board):
        if first_player == 'red':
            available_moves = get_available_moves(board, 'red')
            move = int(input('Please choose a hole to move: {}'.format(available_moves)))
            if move not in available_moves:
                print('Invalid move input: {}'.format(move))
                return
            direction = int(input('Please choose a direction to move: 1. clockwise 2. counterclockwise'))
            if direction == 1:
                direction = True
            elif direction == 2:
                direction = False
            else:
                print('Invalid direction input: {}'.format(dir))
                return
            move_result = board.red_moves(index=move, clockwise=dir)


BOARD = Board()
print(mini_max(0,board=BOARD, player='red'))