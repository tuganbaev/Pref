from bots.simple_bot import SimpleBot
from bots.user_bot import UserBot
from bots.greedy_bot import GreedyBot
from game.preferans_game import PreferansGame
from game.card import Suit, Rank, Card

# Упрощенная версия игры, всегда играют 6 пик, первая рука всегда играет
def start_stalingrad_game():
    bots = [GreedyBot("GreedyBot1"), SimpleBot("Bot2"), SimpleBot("Bot3")]
    game = PreferansGame(bots)
    game.stalingrad_game()

# Обычная версия игры.
def start_regular_game():
    bots = [GreedyBot("GreedyBot1"), SimpleBot("Bot2"), SimpleBot("Bot3")]
    game = PreferansGame(bots)
    game.start_game()

# Игра с пользователем. Кажется, в ней можно вводить свои ходы
def start_game_with_user():
    player = UserBot("Player")
    bots = [player, GreedyBot("GreedyBot1"), SimpleBot("Bot2")]
    game = PreferansGame(bots)
    game.start_game()

if __name__ == "__main__":
    start_regular_game()
