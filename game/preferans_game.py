import random
from .card import Card, Suit, Rank

class PreferansGame:
    def __init__(self, bots, trump_suit):
        self.bots = bots
        self.deck = [Card(suit, rank) for suit in Suit for rank in Rank]
        self.hands = {bot: [] for bot in bots}
        self.trick = []
        self.trump_suit = trump_suit
        # Start with a random player for the first round
        random.shuffle(self.bots)

    def deal_cards(self):
        random.shuffle(self.deck)
        for i in range(10):
            for bot in self.bots:
                self.hands[bot].append(self.deck.pop())
        for bot in self.bots:
            bot.receive_hand(self.hands[bot])

    def card_value(self, card):
        rank_order = {
            Rank.SEVEN: 0, Rank.EIGHT: 1, Rank.NINE: 2, Rank.TEN: 3,
            Rank.JACK: 4, Rank.QUEEN: 5, Rank.KING: 6, Rank.ACE: 7
        }
        return rank_order[card.rank]

    def get_legal_cards(self, hand, trick):
        if not trick:
            return hand  # If there is no trick yet, all cards are legal

        leading_suit = trick[0][1].suit
        same_suit_cards = [card for card in hand if card.suit == leading_suit]
        if same_suit_cards:
            return same_suit_cards

        trump_cards = [card for card in hand if card.suit == self.trump_suit]
        if trump_cards:
            return trump_cards

        return hand

    def determine_trick_winner(self, trick):
        leading_suit = trick[0][1].suit
        winning_card = trick[0][1]
        winner = trick[0][0]

        for bot, card in trick:
            if card.suit == self.trump_suit:
                if (winning_card.suit != self.trump_suit or 
                    self.card_value(card) > self.card_value(winning_card)):
                    winning_card = card
                    winner = bot
            elif card.suit == leading_suit and winning_card.suit == leading_suit:
                if self.card_value(card) > self.card_value(winning_card):
                    winning_card = card
                    winner = bot

        return winner

    def play_game(self):
        print(f"Trump suit: {Card.suit_icons[self.trump_suit]}")
        self.deal_cards()

        for round in range(10):
            self.trick = []
            current_player_index = 0  # Start from the first player in the list

            # Rotate bots so that the winner of the last trick starts first
            if round > 0:
                winner_index = self.bots.index(winner)
                self.bots = self.bots[winner_index:] + self.bots[:winner_index]

            for bot in self.bots:
                legal_cards = self.get_legal_cards(self.hands[bot], self.trick)
                card = bot.play_card(self.trick, legal_cards)

                if card not in legal_cards:
                    raise ValueError(f"{bot.name} tried to play an illegal card: {card}")

                self.trick.append((bot, card))
                self.hands[bot].remove(card)

            winner = self.determine_trick_winner(self.trick)
            trick_str = ", ".join([f"{bot.name} played {card}" for bot, card in self.trick])
            print(f"{winner.name} wins the trick: {trick_str}")


