from bots.simple_bot import SimpleBot
from bots.user_bot import UserBot
from game.preferans_game import PreferansGame, Suit

if __name__ == "__main__":
    player_1 = UserBot("Player1")
    bots = [player_1, SimpleBot("Bot2"), SimpleBot("Bot3")]
    trump_suit = Suit.HEARTS  # Example trump suit
    game = PreferansGame(bots, trump_suit)
    game.play_game()
