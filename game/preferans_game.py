import random
from .card import Card, Suit, Rank
from .trick import Trick

class PreferansGame:
    def __init__(self, bots):
        self.bots = bots
        self.deck = [Card(suit, rank) for suit in Suit for rank in Rank]
        self.hands = {bot: [] for bot in bots}
        self.trump_suit = None
        self.tricks_won = {bot: 0 for bot in bots} 
        # Start with a random player for the first round
        random.shuffle(self.bots)

    # Функция, которая раздает карты
    def deal_cards(self):
        random.shuffle(self.deck)
        for i in range(10):
            for bot in self.bots:
                self.hands[bot].append(self.deck.pop())
        for bot in self.bots:
            bot.receive_hand(self.hands[bot])

    # Функция, которая возвращает список карт, которые игрок может сыграть
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

    #Endpoint to create a new stalingrad
    def start_game(self):
        # First player's bid sets the trump and contract
        bid = self.bots[0].make_bid()
        if bid == "6-1":
            self.trump_suit = Suit.SPADES
            self.contract = 6
        self.play_game()

    # Раздача
    def play_game(self):
        print(f"Trump suit: {Card.suit_icons[self.trump_suit]}")
        self.deal_cards()

        current_winner = None  

        for round in range(10):
            if current_winner:
                winner_index = self.bots.index(current_winner)
                self.bots = self.bots[winner_index:] + self.bots[:winner_index]

            trick = Trick(self.trump_suit)
            for bot in self.bots:
                legal_cards = self.get_legal_cards(self.hands[bot], trick)
                card = bot.play_card(str(trick), legal_cards, hand = self.hands[bot])

                if card not in legal_cards:
                    raise ValueError(f"{bot.name} tried to play an illegal card: {card}")

                trick.add_card(bot, card)
                self.hands[bot].remove(card)

            current_winner = trick.determine_winner()  
            self.tricks_won[current_winner] += 1
            print(f"{current_winner.name} wins the trick: {trick}")

        for bot, tricks_won in self.tricks_won.items():
            print(f"{bot.name} won {tricks_won} tricks.")


