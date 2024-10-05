# ai.py

import copy
import math

class AI:
    def __init__(self, player_id, depth=6):
        self.player_id = player_id  # AI's store index (13)
        self.opponent_id = 6        # Player's store index (6)
        self.depth = depth

    def get_best_move(self, board):
        _, move = self.minimax(board, self.depth, -math.inf, math.inf, True)
        return move

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.is_game_over(board):
            return self.evaluate(board), None

        valid_moves = self.get_valid_moves(board, maximizing_player)

        if maximizing_player:
            max_eval = -math.inf
            best_move = None
            for move in valid_moves:
                new_board, extra_turn = self.make_move(board, move, maximizing_player)
                eval, _ = self.minimax(new_board, depth - 1 if not extra_turn else depth, alpha, beta, not extra_turn)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = math.inf
            best_move = None
            for move in valid_moves:
                new_board, extra_turn = self.make_move(board, move, maximizing_player)
                eval, _ = self.minimax(new_board, depth - 1 if not extra_turn else depth, alpha, beta, extra_turn)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def evaluate(self, board):
        return board[self.player_id] - board[self.opponent_id]

    def is_game_over(self, board):
        side1 = sum(board[0:6])
        side2 = sum(board[7:13])
        return side1 == 0 or side2 == 0

    def get_valid_moves(self, board, maximizing_player):
        if maximizing_player:
            return [i for i in range(7, 13) if board[i] > 0]
        else:
            return [i for i in range(0, 6) if board[i] > 0]

    def make_move(self, board, pit, maximizing_player):
        new_board = copy.deepcopy(board)
        stones = new_board[pit]
        new_board[pit] = 0
        current_pit = pit

        while stones > 0:
            current_pit = (current_pit + 1) % 14
            # Skip opponent's store
            if maximizing_player and current_pit == self.opponent_id:
                continue
            if not maximizing_player and current_pit == self.player_id:
                continue
            new_board[current_pit] += 1
            stones -= 1

        # Check for extra turn
        extra_turn = False
        if maximizing_player and current_pit == self.player_id:
            extra_turn = True
        elif not maximizing_player and current_pit == self.opponent_id:
            extra_turn = True

        # Capture
        if maximizing_player and 7 <= current_pit <= 12 and new_board[current_pit] == 1:
            opposite_pit = 12 - current_pit
            captured = new_board[opposite_pit]
            if captured > 0:
                new_board[self.player_id] += captured + 1
                new_board[opposite_pit] = 0
                new_board[current_pit] = 0
        elif not maximizing_player and 0 <= current_pit <= 5 and new_board[current_pit] == 1:
            opposite_pit = 12 - current_pit
            captured = new_board[opposite_pit]
            if captured > 0:
                new_board[self.opponent_id] += captured + 1
                new_board[opposite_pit] = 0
                new_board[current_pit] = 0

        # Check for game over
        if self.is_game_over(new_board):
            self.collect_remaining(new_board)

        return new_board, extra_turn

    def collect_remaining(self, board):
        player_remaining = sum(board[0:6])
        ai_remaining = sum(board[7:13])
        board[6] += player_remaining
        board[13] += ai_remaining
        for i in range(0, 6):
            board[i] = 0
        for i in range(7, 13):
            board[i] = 0
