import math

# ==========================================
# MODULE 1: AI PROBLEM FORMULATION & REPRESENTATION
# ==========================================
def print_board(board):
    print("\n")
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---|---|---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---|---|---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print("\n")

def check_winner(board):
    """Checks the current state space for terminal win conditions."""
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8], # Columns
        [0, 4, 8], [2, 4, 6]             # Diagonals
    ]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] != " ":
            return board[condition[0]]
    return None

def is_terminal(board):
    return check_winner(board) is not None or " " not in board

# ==========================================
# MODULE 3: CONSTRAINT SATISFACTION (CSP)
# ==========================================
def csp_get_legal_moves(board):
    """Hard Constraint: AI can only place markers on empty cells."""
    return [i for i, cell in enumerate(board) if cell == " "]

# ==========================================
# MODULE 4: SEQUENTIAL DECISION MAKING
# ==========================================
def evaluate_heuristic(board, ai_player, human_player):
    """Soft Constraints: Fallback preferences if depth limit is reached."""
    score = 0
    center = 4
    corners = [0, 2, 6, 8]
    
    if board[center] == ai_player: score += 10
    elif board[center] == human_player: score -= 10
        
    for corner in corners:
        if board[corner] == ai_player: score += 5
        elif board[corner] == human_player: score -= 5
            
    return score

# ==========================================
# MODULE 2: GRAPH SEARCH ALGORITHMS
# ==========================================
def minimax_alpha_beta(board, depth, alpha, beta, is_maximizing, ai_player, human_player):
    """Adversarial search to find the optimal path through the game tree."""
    winner = check_winner(board)
    
    # Terminal Test
    if winner == ai_player:
        return 100 + depth  # Prioritize faster wins
    elif winner == human_player:
        return -100 - depth # Delay unavoidable losses
    elif " " not in board:
        return 0            # Draw
        
    # Heuristic evaluation (used only if depth limit is hit)
    if depth == 0:
        return evaluate_heuristic(board, ai_player, human_player)

    legal_moves = csp_get_legal_moves(board)

    if is_maximizing:
        max_eval = -math.inf
        for move in legal_moves:
            board[move] = ai_player
            eval_score = minimax_alpha_beta(board, depth - 1, alpha, beta, False, ai_player, human_player)
            board[move] = " "
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break # Alpha-Beta Pruning
        return max_eval
    else:
        min_eval = math.inf
        for move in legal_moves:
            board[move] = human_player
            eval_score = minimax_alpha_beta(board, depth - 1, alpha, beta, True, ai_player, human_player)
            board[move] = " "
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break # Alpha-Beta Pruning
        return min_eval

# ==========================================
# MODULE 5: REASONING UNDER UNCERTAINTY
# ==========================================
class UncertaintyModel:
    def __init__(self):
        # To be unbeatable, the agent must assume maximum risk (uncertainty = 0).
        # It assumes the opponent will always play the absolute best move.
        self.assume_perfect_opponent = True 

    def get_search_depth(self, remaining_empty_cells):
        """
        By returning the exact number of empty cells, we force the AI to search 
        the entire remainder of the game tree. It will never stop calculating 
        until it sees the final outcome (Win/Draw), making it invincible.
        """
        return remaining_empty_cells

# ==========================================
# MODULE 6: INTEGRATED AI PIPELINE
# ==========================================
class IntegratedAIAgent:
    def __init__(self, ai_player="O", human_player="X"):
        self.board = [" "] * 9
        self.ai = ai_player
        self.human = human_player
        self.uncertainty_model = UncertaintyModel()

    def get_best_move(self):
        legal_moves = csp_get_legal_moves(self.board)
        if not legal_moves: return None

        best_score = -math.inf
        best_move = None
        
        # Module 5 guarantees we search all the way to the end of the game
        search_depth = self.uncertainty_model.get_search_depth(len(legal_moves))

        for move in legal_moves:
            self.board[move] = self.ai
            score = minimax_alpha_beta(
                self.board, search_depth, -math.inf, math.inf, False, self.ai, self.human
            )
            self.board[move] = " "

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def play(self):
        print("=== UNBEATABLE TIC-TAC-TOE AGENT (PROJECT 19) ===")
        print("Positions are 1-9 (Top-Left to Bottom-Right)")
        print_board(self.board)

        current_turn = "X" # Human goes first

        while not is_terminal(self.board):
            if current_turn == self.human:
                try:
                    move = int(input("Enter your move (1-9): ")) - 1
                except ValueError:
                    print("Invalid input.")
                    continue
                
                if move not in csp_get_legal_moves(self.board):
                    print("Constraint Violation: Cell is already occupied or invalid.")
                    continue
                
                self.board[move] = self.human
                current_turn = self.ai
            else:
                print("\nAI is calculating optimal move...")
                move = self.get_best_move()
                self.board[move] = self.ai
                print(f"AI plays position {move + 1}")
                current_turn = self.human

            print_board(self.board)

        winner = check_winner(self.board)
        if winner == self.ai:
            print("Output: AI Wins! (As mathematically expected).")
        elif winner == self.human:
            print("Output: Human Wins! (Error: This should be impossible).")
        else:
            print("Output: It's a Draw! You played a perfect game against the AI.")

if __name__ == "__main__":
    game = IntegratedAIAgent(ai_player="O", human_player="X")
    game.play()