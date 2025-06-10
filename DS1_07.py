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



# Fonction pour placer une pièce dans une colonne donnée
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# Fonction pour vérifier si une colonne est valide pour placer une pièce
def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

# Fonction pour trouver la prochaine ligne ouverte dans une colonne donnée
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r
    return None  # <-- Ajoute ceci


# Fonction pour vérifier si un joueur a une combinaison gagnante
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

# Fonction pour obtenir une liste des colonnes valides pour placer une pièce
def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    # Priorise la colonne centrale et les colonnes adjacentes
    valid_locations.sort(key=lambda x: abs(COLUMN_COUNT // 2 - x))
    return valid_locations

# Fonction pour évaluer la position du plateau pour un joueur donné
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

# Fonction pour vérifier si le plateau est dans un état terminal (fin de jeu)
def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or (len(get_valid_locations(board)) == 0)

# Algorithme Minimax avec élagage Alpha-Beta pour trouver le meilleur coup
def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    # Cas de base : profondeur 0 ou état terminal
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, math.inf)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -math.inf)
            else:  # Match nul
                return (None, 0)
        else:  # Profondeur 0
            return (None, score_position(board, AI_PIECE))

    # Maximisation pour l'IA
    if maximizingPlayer:
        value = -math.inf
        column = valid_locations[0]

        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = [row[:] for row in board]  # Copie profonde du plateau
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]

            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)

            if alpha >= beta:
                break
        return column, value

    # Minimisation pour le joueur
    else:
        value = math.inf
        column = valid_locations[0]

        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = [row[:] for row in board]  # Copie profonde du plateau
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
    """
    Fonction qui décide de l'action à jouer pour l'IA.
    Prend en paramètre une matrice de 6 lignes * 12 colonnes.
    Retourne le numéro de colonne à jouer.
    """
    start_time = time.time()
    best_col = None
    best_score = -math.inf

    valid_cols = get_valid_locations(board)
    nb_coups = len(valid_cols)

    # Profondeur adaptative
    if nb_coups > 10:
        depth = 5
    elif nb_coups > 7:
        depth = 6
    elif nb_coups > 4:
        depth = 7
    else:
        depth = 8

    # 1. Vérifie si l'IA peut gagner au prochain coup
    for col in valid_cols:
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, AI_PIECE)
        if winning_move(board, AI_PIECE):
            board[row][col] = 0
            return col  # Priorité à la victoire
        board[row][col] = 0

    # 2. Vérifie si le joueur peut gagner au prochain coup, et bloque-le
    for col in valid_cols:
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, PLAYER_PIECE)
        if winning_move(board, PLAYER_PIECE):
            board[row][col] = 0
            return col  # Priorité au blocage
        board[row][col] = 0

    # 3. Sinon, joue le meilleur coup selon Minimax
    for col in valid_cols:
        if time.time() - start_time >= 9.5:  # Temps limite dépassé
            print("Temps limite dépassé ! L'IA joue le meilleur coup trouvé.")
            break

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)
            score = minimax(board, depth-1, -math.inf, math.inf, False)[1]
            board[row][col] = 0  # Annule le coup

            if score > best_score:
                best_score = score
                best_col = col

    # Si aucun coup n'a été trouvé (best_col == None), on choisit une colonne valide au hasard
    if best_col is None:
        best_col = random.choice(valid_cols)

    return best_col

def Terminal_Test(board):
    """
    Vérifie si le jeu est terminé.
    Retourne True si le jeu est fini (victoire, match nul ou plateau plein), sinon False.
    """
    if winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE):
        return True

    # Vérifie si toutes les cases du plateau sont remplies (42 pions utilisés)
    total_pieces = sum(row.count(PLAYER_PIECE) + row.count(AI_PIECE) for row in board)
    if total_pieces >= ROW_COUNT * COLUMN_COUNT:  # 6 * 12 = 42
        return True

    if len(get_valid_locations(board)) == 0:
        return True

    return False


    board = create_board()
    ai1_pieces_used = 0
    ai2_pieces_used = 0
    turn = random.choice([0, 1])  # IA1 ou IA2 commence
    game_over = False

    print("Début de la partie IA vs IA")
    print_board(board)
    print("\n")

    while not game_over:
        if ai1_pieces_used >= MAX_PIECES and ai2_pieces_used >= MAX_PIECES:
            print("Les deux IA ont utilisé toutes leurs pièces. Match nul !")
            break

        if turn == 0 and ai1_pieces_used < MAX_PIECES:
            print("IA 1 (X) joue...")
            start_time = time.time()
            col = IA_Decision(board)
            end_time = time.time()
            elapsed_time = end_time - start_time

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, PLAYER_PIECE)
                ai1_pieces_used += 1

                print(f"IA 1 a joué dans la colonne {col}. Temps écoulé : {elapsed_time:.2f} secondes.")
                print_board(board)
                print("\n")

                if winning_move(board, PLAYER_PIECE):
                    print("IA 1 (X) a gagné !")
                    game_over = True
                    break

        elif turn == 1 and ai2_pieces_used < MAX_PIECES:
            print("IA 2 (O) joue...")
            start_time = time.time()
            col = IA_Decision(board)
            end_time = time.time()
            elapsed_time = end_time - start_time

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)
                ai2_pieces_used += 1

                print(f"IA 2 a joué dans la colonne {col}. Temps écoulé : {elapsed_time:.2f} secondes.")
                print_board(board)
                print("\n")

                if winning_move(board, AI_PIECE):
                    print("IA 2 (O) a gagné !")
                    game_over = True
                    break

        if Terminal_Test(board):
            print("Match nul !")
            game_over = True
            break

        turn = 1 - turn  # Change de tour

