import random
from .card import Card, Suit, Rank
from .trick import Trick

class PreferansRound:
    def __init__(self, bots, trump_suit, initial_player):
        self.bots = bots
        self.trump_suit = trump_suit
        self.initial_player = initial_player
        self.tricks_won = {bot: 0 for bot in self.bots}
        self.hands = {}

    # Раздача
    def play_tricks(self, hands):
        self.hands = hands
        current_winner = self.initial_player  # Start with the initial player or the winner of the previous trick
        for _ in range(10):  # Assume 10 tricks per round
            trick = Trick(self.trump_suit)
            if current_winner:
                start_index = self.bots.index(current_winner)
                ordered_bots = self.bots[start_index:] + self.bots[:start_index]
            else:
                ordered_bots = self.bots[:]

            for bot in ordered_bots:
                legal_cards = self.get_legal_cards(self.hands[bot], trick)
                card = bot.play_card(str(trick), legal_cards)
                if card not in legal_cards:
                    raise ValueError(f"{bot.name} tried to play an illegal card: {card}")
                trick.add_card(bot, card)
                self.hands[bot].remove(card)

            current_winner = trick.determine_winner()
            self.tricks_won[current_winner] += 1

    def get_legal_cards(self, hand, trick):
        if not trick.cards:
            return hand
        leading_suit = trick.cards[0][1].suit
        same_suit_cards = [card for card in hand if card.suit == leading_suit]
        if same_suit_cards:
            return same_suit_cards
        trump_cards = [card for card in hand if card.suit == self.trump_suit]
        if trump_cards:
            return trump_cards
        return hand
    
    def count_score(self):
        pass