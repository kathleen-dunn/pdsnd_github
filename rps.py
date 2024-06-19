#!/usr/bin/env python3

"""This program plays a game of Rock, Paper, Scissors between two Players,
and reports both Player's scores each round."""
from enum import Enum
import random

moves = ['rock', 'paper', 'scissors']

"""The Player class is the parent class for all of the Players
in this game"""


class Move(Enum):
    ROCK = 'rock'
    PAPER = 'paper'
    SCISSORS = 'scissors'

    @classmethod
    def moves(cls):
        """ Returns a list of all available moves. """
        return [e.value for e in cls]


class Player:

    total = 0

    def move(self):
        return 'rock'

    def learn(self, my_move, their_move):
        pass

    def __init__(self):
        self.my_move = None
        self.their_move = None

    def learn(self, my_move, their_move):
        self.my_move = my_move
        self.their_move = their_move


"""The Human class for human interaction"""

class HumanPlayer(Player):
    def __init__(self):
        super().__init__()

    def move(self):
        while True:
            move = input("rock, paper, scissors?").lower()
            if move in moves:
                return move
            print(f"The move {move} is invalid.  Try again!")


"""The RandomPlayer class will make use of the random function"""

class RandomPlayer(Player):
    def __init__(self):
        super().__init__()

    def move(self):
        """ Selects a random move from the defined Move enumer """
        return random.choice(Move.moves())


class ReflectPlayer(Player):
    def __init__(self):
        super().__init__()

    def learn(self, my_move, their_move):
        self.my_move = my_move
        self.their_move = their_move

    def move(self):
        if self.their_move is None:
            return random.choice(moves)
        else:
            return self.their_move[-1]


class CyclePlayer(Player):
    def __init__(self):
        super().__init__()

    def move(self):
        if self.my_move is None:
            return random.choice(moves)
        else:
            index = moves.index(self.my_move) + 1
            if index == len(moves):
                index = 0
            return moves[index]


def beats(one, two):
    return ((one == 'rock' and two == 'scissors') or
            (one == 'scissors' and two == 'paper') or
            (one == 'paper' and two == 'rock'))


class Game:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.total_rounds = 0

    def play_round(self):
        move1 = self.p1.move()
        move2 = self.p2.move()
        print(f"Player 1: {move1}  Player 2: {move2}")
        if beats(move1, move2):
            print("Player 1 wins")
            self.p1.total += 1

        elif beats(move2, move1):
            print("Player 2 wins")
            self.p2.total += 1

        else:
            print("You have a tie")
        self.p1.learn(move1, move2)
        self.p2.learn(move2, move1)
        self.total_rounds += 1
        print(f'The score is: {self.p1.total} | {self.p2.total}')

    def play_game(self):
        print("Game start!")
        for round in range(3):
            print(f"Round {round}:")
            self.play_round()
            print("Game over!")

    def play_again(self):
        choice = ''
        while choice not in ['y', 'n']:
            choice = input("Would you like to play again? (y/n)")
            if choice == 'n':
                print("Thanks for playing! See you next time.")
                return 'game_over'
            elif choice == 'y':
                print("Restarting the game...")
                return self.play_game()

    def print_final_scores(self):
        print("Final scores:")
        print(f"Player 1: {self.p1.total}")
        print(f"Player 2: {self.p2.total}")
        print(f"Total rounds played: {self.total_rounds}")


if __name__ == '__main__':
    players = {
        '1': Player,
        '2': RandomPlayer,
        '3': ReflectPlayer,
        '4': CyclePlayer,
        '5': HumanPlayer
    }
    print("Player list:")
    for number, player in players.items():
        print(f"{number}. {player.__name__}")
    while (p1 := input("Choose player 1: ")) not in players.keys():
        print("Invalid choice, please select player 1 from the list.")
    while (p2 := input("Choose player 2: ")) not in players.keys():
        print("Invalid choice, please select player 2 from the list.")

    game = Game(players[p1](), players[p2]())
    game.play_game()
    game.play_again()
    game.print_final_scores()
