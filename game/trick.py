from game.card import Rank

class Trick:
    def __init__(self, trump_suit):
        self.cards = []  # Stores tuples of (bot, card)
        self.trump_suit = trump_suit

    def add_card(self, bot, card):
        self.cards.append((bot, card))

    def determine_winner(self):
        if not self.cards:
            return None

        leading_suit = self.cards[0][1].suit
        winning_card = self.cards[0][1]
        winner = self.cards[0][0]

        for bot, card in self.cards:
            if card.suit == self.trump_suit and (winning_card.suit != self.trump_suit or self.card_value(card) > self.card_value(winning_card)):
                winning_card = card
                winner = bot
            elif card.suit == leading_suit and winning_card.suit == leading_suit and self.card_value(card) > self.card_value(winning_card):
                winning_card = card
                winner = bot
        return winner

    def card_value(self, card):
        rank_order = {
            Rank.SEVEN: 0, Rank.EIGHT: 1, Rank.NINE: 2, Rank.TEN: 3,
            Rank.JACK: 4, Rank.QUEEN: 5, Rank.KING: 6, Rank.ACE: 7
        }
        return rank_order[card.rank]    

    def __str__(self):
        return ", ".join([f"{bot.name} played {card}" for bot, card in self.cards])

