import copy

ROWS = 6
COLS = 12
ALIGN = 4

class Puissance4:
    def __init__(self, board=None):
        if board:
            self.board = copy.deepcopy(board)
        else:
            self.board = [[0 for _ in range(COLS)] for _ in range(ROWS)]

    def drop_piece(self, col, player):
        for row in reversed(range(ROWS)):
            if self.board[row][col] == 0:
                self.board[row][col] = player
                return True
        return False

    def available_actions(self):
        return [col for col in range(COLS) if self.board[0][col] == 0]

    def is_terminal(self):
        return check_winner(self.board) != 0 or all(self.board[0][col] != 0 for col in range(COLS))

    def display(self):
        for row in self.board:
            print("| " + " | ".join(" " if cell == 0 else ("X" if cell == 1 else "O") for cell in row) + " |")
        print("-" * (4 * COLS + 1))
        print("  " + "   ".join(str(i) for i in range(COLS)))


def check_winner(board):
    for row in range(ROWS):
        for col in range(COLS):
            player = board[row][col]
            if player == 0:
                continue
            for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                if all(
                        0 <= row + dr * i < ROWS and
                        0 <= col + dc * i < COLS and
                        board[row + dr * i][col + dc * i] == player
                        for i in range(ALIGN)
                ):
                    return player
    return 0


def evaluate_line(line, player, opponent):
    if opponent in line and player in line:
        return 0
    count_player = line.count(player)
    count_opponent = line.count(opponent)
    if count_player == 4:
        return 1000
    elif count_player == 3:
        return 50
    elif count_player == 2:
        return 10
    elif count_player == 1:
        return 1
    elif count_opponent == 4:
        return -1000
    return 0


def heuristic(board, player):
    opponent = -player
    score = 0
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for row in range(ROWS):
        for col in range(COLS):
            for dr, dc in directions:
                line = []
                for i in range(ALIGN):
                    r, c = row + dr * i, col + dc * i
                    if 0 <= r < ROWS and 0 <= c < COLS:
                        line.append(board[r][c])
                if len(line) == ALIGN:
                    score += evaluate_line(line, player, opponent)
    return score


def alpha_beta_search(state, player, max_depth):
    def max_value(state, alpha, beta, depth):
        if state.is_terminal() or depth == 0:
            return heuristic(state.board, player)
        v = float('-inf')
        for col in state.available_actions():
            new_state = Puissance4(state.board)
            new_state.drop_piece(col, player)
            v = max(v, min_value(new_state, alpha, beta, depth - 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        opponent = -player
        if state.is_terminal() or depth == 0:
            return heuristic(state.board, player)
        v = float('inf')
        for col in state.available_actions():
            new_state = Puissance4(state.board)
            new_state.drop_piece(col, opponent)
            v = min(v, max_value(new_state, alpha, beta, depth - 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    best_score = float('-inf')
    best_action = None
    alpha = float('-inf')
    beta = float('inf')
    for col in state.available_actions():
        new_state = Puissance4(state.board)
        new_state.drop_piece(col, player)
        score = min_value(new_state, alpha, beta, max_depth - 1)
        if score > best_score:
            best_score = score
            best_action = col
        alpha = max(alpha, score)
    return best_action


# Fonction qui sera appelée pour que l'IA joue
def IA_Decision(board, player=1, max_depth=5):
    state = Puissance4(board)
    return alpha_beta_search(state, player, max_depth)

def main():
    print("Bienvenue dans Puissance 4 !")
    choix = input("Qui commence ? (1 = Humain, 2 = IA) : ")
    humain = 1 if choix == "1" else -1
    ia = -humain
    game = Puissance4()  # Crée un seul objet jeu
    joueur = humain if choix == "1" else ia

    while True:
        game.display()
        if check_winner(game.board):
            gagnant = "Humain" if check_winner(game.board) == humain else "IA"
            print(f"{gagnant} a gagné !")
            break
        if all(game.board[0][col] != 0 for col in range(COLS)):
            print("Match nul !")
            break

        if joueur == humain:
            try:
                col = int(input("Votre coup (0-{}): ".format(COLS - 1)))
                if col not in range(COLS) or game.board[0][col] != 0:
                    print("Colonne invalide, réessayez.")
                    continue
            except ValueError:
                print("Entrée invalide, réessayez.")
                continue
            game.drop_piece(col, humain)
        else:
            print("L'IA réfléchit...")
            col = IA_Decision(game.board, ia)
            game.drop_piece(col, ia)
            print(f"L'IA joue en colonne {col}")

        joueur = -joueur

if __name__ == "__main__":
    main()

