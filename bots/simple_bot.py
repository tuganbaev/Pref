from .base_bot import BaseBot

class SimpleBot(BaseBot):
    def make_bid(self):
        # Always pass
        return 0

    def play_card(self, trick, legal_cards):
        # Play the first legal card
        return super().play_card(trick, legal_cards)