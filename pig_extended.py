import random
import time
import argparse

class Player:
    def __init__(self):
        self.score = 0

    def take_turn(self):
        pass

class HumanPlayer(Player):
    def take_turn(self):
        while True:
            choice = input("Roll or Hold? (r/h): ").lower()
            if choice == 'r':
                roll = random.randint(1, 6)
                print(f"You rolled a {roll}")
                if roll == 1:
                    print("Turn over. You scored 0 points this turn.")
                    return 0
                self.score += roll
            elif choice == 'h':
                return self.score
            else:
                print("Invalid choice. Enter 'r' to roll or 'h' to hold.")

class ComputerPlayer(Player):
    def take_turn(self):
        x = self.score
        hold_limit = min(25, 100 - x)
        while self.score < hold_limit:
            roll = random.randint(1, 6)
            print(f"Computer rolled a {roll}")
            self.score += roll
            if roll == 1:
                print("Computer's turn is over. It scored 0 points this turn.")
                return 0
        return self.score

class PlayerFactory:
    def create_player(self, player_type):
        if player_type == "human":
            return HumanPlayer()
        elif player_type == "computer":
            return ComputerPlayer()
        else:
            raise ValueError("Invalid player type")

class Game:
    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.current_player = 0
        self.scores = [0, 0]
        self.start_time = time.time()
        self.timed = False

    def switch_player(self):
        self.current_player = 1 - self.current_player

    def play(self):
        while all(score < 100 for score in self.scores):
            player = self.players[self.current_player]
            print(f"Player {self.current_player + 1}'s turn.")
            print(f"Current score: Player 1 - {self.scores[0]}, Player 2 - {self.scores[1]}")
            turn_score = player.take_turn()
            if turn_score == 0:
                self.scores[self.current_player] = 0
                print(f"Player {self.current_player + 1} lost all points this turn.")
            else:
                self.scores[self.current_player] += turn_score
                print(f"Player {self.current_player + 1} scored {turn_score} points this turn.")
                if self.scores[self.current_player] >= 100:
                    print(f"Player {self.current_player + 1} wins!")
                    break
            self.switch_player()
            if self.timed and (time.time() - self.start_time) >= 60:
                self.determine_winner()
                break

    def determine_winner(self):
        if self.scores[0] > self.scores[1]:
            print("Player 1 wins!")
        elif self.scores[1] > self.scores[0]:
            print("Player 2 wins!")
        else:
            print("It's a tie!")

class TimedGameProxy:
    def __init__(self, game):
        self.game = game
        self.start_time = time.time()
        self.time_limit = 60  # 1 minute

    def play(self):
        while True:
            if time.time() - self.start_time >= self.time_limit:
                self.game.determine_winner()
                break
            else:
                self.game.play()

if __name__ == '__main__':
    player1_type = input("Enter player 1 type (human/computer): ")
    player2_type = input("Enter player 2 type (human/computer): ")

    player_factory = PlayerFactory()
    player1 = player_factory.create_player(player1_type)
    player2 = player_factory.create_player(player2_type)

    game = Game(player1, player2)

    if input("Do you want to play the timed version? (y/n): ").strip().lower() == 'y':
        game.timed = True
        timed_game = TimedGameProxy(game)
        timed_game.play()
    else:
        game.play()

