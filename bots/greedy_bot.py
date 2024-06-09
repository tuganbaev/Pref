from .base_bot import BaseBot
from game.card import Card, Suit, Rank

class GreedyBot(BaseBot):
    def make_bid(self):
        # Placeholder method for bidding, should be overridden
        return "6-1"  # Default placeholder

    def play_card(self, trick, legal_cards, hand = None):
        # Define a ranking system based on Preferans rules
        rank_values = {
            Rank.SEVEN: 0,
            Rank.EIGHT: 1,
            Rank.NINE: 2,
            Rank.TEN: 3,
            Rank.JACK: 4,
            Rank.QUEEN: 5,
            Rank.KING: 6,
            Rank.ACE: 7
        }

        legal_cards.sort(key=lambda card: -rank_values[card.rank])
        return legal_cards[0]