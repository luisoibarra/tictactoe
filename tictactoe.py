"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    return X if len([x for i in range(len(board)) for x in board[i] if x == EMPTY]) % 2 == 1 else O 


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return set((i,j) for i in range(len(board)) for j in range(len(board[i])) if board[i][j] == EMPTY)


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] != EMPTY:
        raise Exception("Invalid movement. Trying to make a move into a non empty square")
    
    board = [x.copy() for x in board]
    
    board[action[0]][action[1]] = player(board)
    
    return board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    def check_if_player_won(player):
        # Row check
        for r in board:
            if all(x == player for x in r):
                return True
        # Column check
        for j in range(len(board[0])): 
            if all(x == player for x in [board[i][j] for i in range(len(board))]):
                return True
        # Diagonal check
        if all(x == player for x in [board[i][i] for i in range(len(board))]) or \
           all(x == player for x in [board[len(board)-1-i][i] for i in range(len(board))]):
            return True
        return False
    
    X_won = check_if_player_won(X)
    if X_won:
        return X
    
    O_won = check_if_player_won(O)
    if O_won:
        return O
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    return len([x for r in board for x in r if x == EMPTY]) == 0


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    player_winner = winner(board)
    if player_winner == X:
        return 1
    if player_winner == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    current_player = player(board)
    
    def minimax_value(board, is_max):
        if terminal(board):
            return (utility(board), None)
        value = -float('inf') if is_max else float('inf')
        action = None
        for a in actions(board):
            new_value,_ = minimax_value(result(board, a), not is_max)
            if is_max and value < new_value:
                value = new_value
                action = a
            elif not is_max and value > new_value:
                value = new_value
                action = a
        return (value, action)
    
    def alpha_beta_value(board, is_max, alpha, beta):
        if terminal(board):
            return (utility(board), None)
        value = -float('inf') if is_max else float('inf')
        action = None
        for a in actions(board):
            new_value,_ = alpha_beta_value(result(board, a), not is_max, alpha, beta)
            
            if is_max and value < new_value:
                value = new_value
                action = a
            elif not is_max and value > new_value:
                value = new_value
                action = a
            
            if is_max and new_value >= beta:
                break
            if not is_max and new_value <= alpha:
                break
            
            if is_max:
                alpha = max(alpha, new_value)
            else:
                beta = min(beta, new_value)
                
                
        return (value, action)
    
    # return minimax_value(board, current_player == X)[1]
    return alpha_beta_value(board, current_player == X, -float('inf'), float('inf'))[1]
        
