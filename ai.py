# ai.py

import math
import copy

class AI:
    def __init__(self, depth=6):
        self.depth = depth

    def get_best_move(self, pits):
        best_score = -math.inf
        best_move = None
        for move in self.get_valid_moves(pits):
            new_pits = copy.deepcopy(pits)
            new_pits = self.make_move(new_pits, move, 'ai')
            score = self.minimax(new_pits, self.depth -1, -math.inf, math.inf, False)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def minimax(self, pits, depth, alpha, beta, is_maximizing):
        if depth ==0 or self.is_game_over(pits):
            return self.evaluate(pits)
        if is_maximizing:
            max_eval = -math.inf
            for move in self.get_valid_moves(pits, 'ai'):
                new_pits = copy.deepcopy(pits)
                new_pits = self.make_move(new_pits, move, 'ai')
                eval = self.minimax(new_pits, depth -1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for move in self.get_valid_moves(pits, 'player'):
                new_pits = copy.deepcopy(pits)
                new_pits = self.make_move(new_pits, move, 'player')
                eval = self.minimax(new_pits, depth -1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def evaluate(self, pits):
        return pits[13] - pits[6]

    def is_game_over(self, pits):
        return sum(pits[0:6]) ==0 or sum(pits[7:13]) ==0

    def get_valid_moves(self, pits, player='ai'):
        if player == 'player':
            return [i for i in range(0,6) if pits[i] >0]
        else:
            return [i for i in range(7,13) if pits[i] >0]

    def make_move(self, pits, pit, player):
        seeds = pits[pit]
        pits[pit] =0
        current_pit = pit

        while seeds >0:
            current_pit = (current_pit +1) %14
            if player == 'player' and current_pit ==13:
                continue
            if player == 'ai' and current_pit ==6:
                continue
            pits[current_pit] +=1
            seeds -=1

        # Capture
        if player == 'player' and 0 <= current_pit <=5 and pits[current_pit] ==1:
            opposite_pit = 12 - current_pit
            if pits[opposite_pit] >0:
                pits[6] += pits[opposite_pit] +1
                pits[current_pit] =0
                pits[opposite_pit] =0
        if player == 'ai' and 7 <= current_pit <=12 and pits[current_pit] ==1:
            opposite_pit = 12 - current_pit
            if pits[opposite_pit] >0:
                pits[13] += pits[opposite_pit] +1
                pits[current_pit] =0
                pits[opposite_pit] =0

        return pits
