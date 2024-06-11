from .base_bot import BaseBot
from collections import Counter
from game.card import Suit

class SimpleBot(BaseBot):
    def make_bid(self, hand):
        # Placeholder method for bidding, should be overridden
        return 1

    def play_card(self, trick, legal_cards, hand = None):
        # Play the first legal card
        return super().play_card(trick, legal_cards)
    
    def choose_contract(self, hand):
        return 1 # Choose to play 6 tricks with the most common suit