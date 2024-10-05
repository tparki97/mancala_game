# game.py

import sys
from ai import AI

class MancalaGame:
    def __init__(self):
        # Initialize board
        # Indices 0-5: Player 1 pits
        # Index 6: Player 1 store
        # Indices 7-12: AI pits
        # Index 13: AI store
        self.board = [4] * 14
        self.board[6] = 0
        self.board[13] = 0
        self.current_player = None  # 1 for Player, 2 for AI
        self.ai = AI(player_id=13)

    def display_board(self):
        ai_pits = ' '.join([f"{i}({self.board[i]})" for i in range(12, 6, -1)])
        player_pits = ' '.join([f"{i}({self.board[i]})" for i in range(0, 6)])
        
        print("\nCurrent Board:")
        print(" " * 30 + "AI Pits")
        print(" " * 15 + ai_pits)
        print(f"AI Store (13): {self.board[13]}".ljust(30) + f"Player Store (6): {self.board[6]}")
        print(" " * 15 + player_pits)
        print(" " * 30 + "Player Pits\n")

    def choose_player_order(self):
        while True:
            choice = input("Do you want to play first or second? (1/2): ")
            if choice == '1':
                self.current_player = 1
                break
            elif choice == '2':
                self.current_player = 2
                break
            else:
                print("Invalid input. Please enter 1 or 2.")

    def play(self):
        self.choose_player_order()
        self.display_board()

        while not self.is_game_over():
            if self.current_player == 1:
                move = self.get_player_move()
                extra_turn = self.make_move(move, 1)
                self.display_board()
                if not extra_turn:
                    self.current_player = 2
            else:
                print("AI is making a move...")
                move = self.ai.get_best_move(self.board)
                print(f"AI selects pit {move}")
                extra_turn = self.make_move(move, 2)
                self.display_board()
                if not extra_turn:
                    self.current_player = 1

        self.end_game()

    def get_player_move(self):
        while True:
            try:
                move = int(input("Select a pit to sow (0-5): "))
                if move < 0 or move > 5:
                    print("Invalid pit number. Choose between 0 and 5.")
                elif self.board[move] == 0:
                    print("Selected pit is empty. Choose a different pit.")
                else:
                    return move
            except ValueError:
                print("Invalid input. Please enter a number between 0 and 5.")

    def make_move(self, pit, player):
        board = self.board
        stones = board[pit]
        board[pit] = 0
        current_pit = pit

        while stones > 0:
            current_pit = (current_pit + 1) % 14
            # Skip opponent's store
            if player == 1 and current_pit == 13:
                continue
            if player == 2 and current_pit == 6:
                continue
            board[current_pit] += 1
            stones -= 1

        # Check for extra turn
        extra_turn = False
        if player == 1 and current_pit == 6:
            extra_turn = True
        elif player == 2 and current_pit == 13:
            extra_turn = True

        # Capture
        if player == 1 and 0 <= current_pit <= 5 and board[current_pit] == 1:
            opposite_pit = 12 - current_pit
            captured = board[opposite_pit]
            if captured > 0:
                board[6] += captured + 1
                board[opposite_pit] = 0
                board[current_pit] = 0
        elif player == 2 and 7 <= current_pit <= 12 and board[current_pit] == 1:
            opposite_pit = 12 - current_pit
            captured = board[opposite_pit]
            if captured > 0:
                board[13] += captured + 1
                board[opposite_pit] = 0
                board[current_pit] = 0

        # Check for game over
        if self.is_game_over():
            self.collect_remaining()

        return extra_turn

    def is_game_over(self):
        side1 = sum(self.board[0:6])
        side2 = sum(self.board[7:13])
        return side1 == 0 or side2 == 0

    def collect_remaining(self):
        player_remaining = sum(self.board[0:6])
        ai_remaining = sum(self.board[7:13])
        self.board[6] += player_remaining
        self.board[13] += ai_remaining
        for i in range(0, 6):
            self.board[i] = 0
        for i in range(7, 13):
            self.board[i] = 0

    def end_game(self):
        print("Game Over!")
        print(f"Player Store (6): {self.board[6]}")
        print(f"AI Store (13): {self.board[13]}")
        if self.board[6] > self.board[13]:
            print("You win!")
        elif self.board[6] < self.board[13]:
            print("AI wins!")
        else:
            print("It's a tie!")

if __name__ == "__main__":
    game = MancalaGame()
    game.play()
