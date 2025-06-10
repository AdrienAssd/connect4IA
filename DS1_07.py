import math
import random
import time

ROW_COUNT = 6
COLUMN_COUNT = 12

PLAYER = 0
AI = 1

PLAYER_PIECE = ' X'
AI_PIECE = ' O'

MAX_PIECES = 21

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    flipped_board = board[::-1]
    for row in flipped_board:
        print(row)

def winning_move(board, piece):
    # Vérification des alignements horizontaux
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    # Vérification des alignements verticaux
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    # Vérification des diagonales positives
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
    # Vérification des diagonales négatives
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
    return False

def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    valid_locations.sort(key=lambda x: abs(COLUMN_COUNT // 2 - x))
    return valid_locations

def score_position(board, piece):
    score = 0
    opponent_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    # Score pour la colonne centrale
    center_array = [board[r][COLUMN_COUNT // 2] for r in range(ROW_COUNT)]
    score += center_array.count(piece) * 3

    # Score pour les alignements horizontaux
    for r in range(ROW_COUNT):
        row_array = board[r]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c+4]
            score += evaluate_window(window, piece)

    # Score pour les alignements verticaux
    for c in range(COLUMN_COUNT):
        col_array = [board[r][c] for r in range(ROW_COUNT)]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r+4]
            score += evaluate_window(window, piece)

    # Score pour les diagonales positives
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r+i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    # Score pour les diagonales négatives
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r+3-i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score

def evaluate_window(window, piece):
    score = 0
    opponent_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    if window.count(opponent_piece) == 3 and window.count(0) == 1:
        score -= 4

    return score

def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or (len(get_valid_locations(board)) == 0)

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, math.inf)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -math.inf)
            else:
                return (None, 0)
        else:
            return (None, score_position(board, AI_PIECE))

    if maximizingPlayer:
        value = -math.inf
        column = valid_locations[0]

        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = [row[:] for row in board]
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]

            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)

            if alpha >= beta:
                break
        return column, value

    else:
        value = math.inf
        column = valid_locations[0]

        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = [row[:] for row in board]
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]

            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)

            if alpha >= beta:
                break
        return column, value

def IA_Decision(board):
    start_time = time.time()
    best_col = None
    best_score = -math.inf

    valid_cols = get_valid_locations(board)
    nb_coups = len(valid_cols)

    if nb_coups > 10:
        depth = 5
    elif nb_coups > 7:
        depth = 6
    elif nb_coups > 4:
        depth = 7
    else:
        depth = 8

    for col in valid_cols:
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, PLAYER_PIECE)
        if winning_move(board, PLAYER_PIECE):
            board[row][col] = 0
            return col
        board[row][col] = 0

    for col in valid_cols:
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, AI_PIECE)
        if winning_move(board, AI_PIECE):
            board[row][col] = 0
            return col
        board[row][col] = 0

    for col in valid_cols:
        if time.time() - start_time >= 9.5:
            print("Temps limite dépassé ! L'IA joue le meilleur coup trouvé.")
            break

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)
            score = minimax(board, depth-1, -math.inf, math.inf, False)[1]
            board[row][col] = 0

            if score > best_score:
                best_score = score
                best_col = col

    if best_col is None:
        best_col = random.choice(valid_cols)

    return best_col

def Terminal_Test(board):
    if winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE):
        return True

    total_pieces = sum(row.count(PLAYER_PIECE) + row.count(AI_PIECE) for row in board)
    if total_pieces >= ROW_COUNT * COLUMN_COUNT:
        return True

    if len(get_valid_locations(board)) == 0:
        return True

    return False

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0