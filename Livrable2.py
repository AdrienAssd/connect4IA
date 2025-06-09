from main import *

def IA_Decision(board):
    """
    Fonction qui décide de l'action à jouer pour l'IA.
    Prend en paramètre une matrice de 6 lignes * 12 colonnes.
    Retourne le numéro de colonne à jouer.
    """
    depth = 6  # Profondeur de recherche pour l'algorithme Minimax
    best_col = None
    best_score = -math.inf

    # Parcourt les colonnes valides pour trouver le meilleur coup
    for col in get_valid_locations(board):
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, 1)  # L'IA est le joueur 1
        score = minimax(board, depth-1, -math.inf, math.inf, False)[1]
        board[row][col] = 0  # Annule le coup

        # Met à jour le meilleur coup
        if score > best_score:
            best_score = score
            best_col = col

    return best_col

def Terminal_Test(board):
    """
    Vérifie si le jeu est terminé.
    Retourne True si le jeu est fini (victoire ou match nul), sinon False.
    """
    if winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE):
        return True

    if len(get_valid_locations(board)) == 0:
        return True

    return False

if __name__ == "__main__":
    board = create_board()
    print_board(board)