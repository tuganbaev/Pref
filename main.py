from bots.simple_bot import SimpleBot
from bots.user_bot import UserBot
from bots.greedy_bot import GreedyBot
from game.preferans_game import PreferansGame
from game.card import Suit, Rank, Card

def start_burgalar_game():
    player_1 = UserBot("Player1")
    bots = [GreedyBot("GreedyBot1"), SimpleBot("Bot2"), SimpleBot("Bot3")]
    game = PreferansGame(bots)
    game.start_game()


if __name__ == "__main__":
    start_burgalar_game()
