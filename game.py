# game.py

import sys
from ai import AI

class MancalaGame:
    def __init__(self):
        # Initialize pits: indices 0-5 for Player, 7-12 for AI
        self.pits = [4] * 14
        self.pits[6] = 0  # Player Store
        self.pits[13] = 0  # AI Store
        self.current_player = None
        self.ai = AI()

    def display_board(self):
        print("\nCurrent Board:")
        print("AI Pits:")
        print("  ", end="")
        for pit in range(12, 6, -1):
            print(f"{pit:2} ", end="")
        print("\nAI Store:", f"{self.pits[13]:2}")
        print("P1 Pits:", end=" ")
        for pit in range(0, 6):
            print(f"{pit:2} ", end="")
        print("\nPlayer Store:", f"{self.pits[6]:2}\n")

    def is_game_over(self):
        # Check if all pits on one side are empty
        if sum(self.pits[0:6]) == 0 or sum(self.pits[7:13]) == 0:
            return True
        return False

    def collect_remaining(self):
        # Collect remaining seeds to the respective stores
        if sum(self.pits[0:6]) > 0:
            self.pits[6] += sum(self.pits[0:6])
            for i in range(0, 6):
                self.pits[i] = 0
        if sum(self.pits[7:13]) > 0:
            self.pits[13] += sum(self.pits[7:13])
            for i in range(7, 13):
                self.pits[i] = 0

    def determine_winner(self):
        if self.pits[6] > self.pits[13]:
            print("You win!")
        elif self.pits[6] < self.pits[13]:
            print("AI wins!")
        else:
            print("It's a tie!")

    def make_move(self, pit, player):
        seeds = self.pits[pit]
        self.pits[pit] = 0
        current_pit = pit

        while seeds > 0:
            current_pit = (current_pit + 1) % 14
            # Skip opponent's store
            if player == 'player' and current_pit == 13:
                continue
            if player == 'ai' and current_pit == 6:
                continue
            self.pits[current_pit] += 1
            seeds -= 1

        # Check for extra turn
        if player == 'player' and current_pit == 6:
            return 'player'
        if player == 'ai' and current_pit == 13:
            return 'ai'

        # Check for capture
        if player == 'player' and 0 <= current_pit <=5 and self.pits[current_pit] ==1:
            opposite_pit = 12 - current_pit
            if self.pits[opposite_pit] >0:
                self.pits[6] += self.pits[opposite_pit] +1
                self.pits[current_pit] = 0
                self.pits[opposite_pit] =0
        if player == 'ai' and 7 <= current_pit <=12 and self.pits[current_pit] ==1:
            opposite_pit = 12 - current_pit
            if self.pits[opposite_pit] >0:
                self.pits[13] += self.pits[opposite_pit] +1
                self.pits[current_pit] =0
                self.pits[opposite_pit] =0

        return 'player' if player == 'ai' else 'ai'

    def get_valid_moves(self, player):
        if player == 'player':
            return [i for i in range(0,6) if self.pits[i] >0]
        else:
            return [i for i in range(7,13) if self.pits[i] >0]

    def play_game(self):
        # Choose turn order
        while True:
            choice = input("Do you want to go first or second? (1/2): ")
            if choice == '1':
                self.current_player = 'player'
                break
            elif choice == '2':
                self.current_player = 'ai'
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")

        while not self.is_game_over():
            self.display_board()
            if self.current_player == 'player':
                valid_moves = self.get_valid_moves('player')
                if not valid_moves:
                    break
                while True:
                    try:
                        move = int(input(f"Your move (choose pit {valid_moves}): "))
                        if move in valid_moves:
                            break
                        else:
                            print("Invalid pit. Choose a valid pit.")
                    except ValueError:
                        print("Please enter a number.")
                self.current_player = self.make_move(move, 'player')
            else:
                print("AI is thinking...")
                move = self.ai.get_best_move(self.pits)
                print(f"AI chooses pit {move}")
                self.current_player = self.make_move(move, 'ai')

        self.collect_remaining()
        self.display_board()
        self.determine_winner()

if __name__ == "__main__":
    game = MancalaGame()
    game.play_game()
