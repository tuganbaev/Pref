from .base_bot import BaseBot

class SimpleBot(BaseBot):
    def make_bid(self):
        # Placeholder method for bidding, should be overridden
        return "6-1"  # Default placeholder

    def play_card(self, trick, legal_cards, hand = None):
        # Play the first legal card
        return super().play_card(trick, legal_cards)