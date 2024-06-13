from .base_bot import BaseBot
from game.card import Suit
from game.consts import GAME_MAP

class UserBot(BaseBot):
    def sort_hand(self):
        #Default sorting is to sort by suit and rank. Suit order is Spades, Clubs, Diamonds, Hearts. Rank order is Ace, King, Queen, Jack, 10, 9, 8, 7.
        super().sort_hand()

    def make_bid(self, hand):
        print("Your hand:", hand)
        print("Available bids:")
        for key, value in GAME_MAP.items():
            if key == 30:
                continue
            if isinstance(value, tuple):
                num_tricks, suit = value
                suit_name = suit.name if suit else "No Trump"
                print(f"{key}: {num_tricks} tricks with {suit_name}")
            else:
                print(f"{key}: {value}")
        
        bid_key = int(input("Enter the number corresponding to your bid: "))
        return bid_key

    def choose_contract(self, hand):
        print("Your hand:", hand)
        trump = input("Choose trump suit (Spades, Hearts, Diamonds, Clubs): ")
        num_tricks = int(input("How many tricks do you call (6-10)?: "))

        return num_tricks, Suit[trump.upper()]

    def play_card(self, trick, legal_cards, contract_id, trump_suit, previous_tricks):
        print(f"\nTrick: {trick}")
        self.print_hand()
        legal_cards_str = ", ".join(map(str, legal_cards))
        print(f"Legal cards: {legal_cards_str}")

        while True:
            card_str = input(f"{self.name}, enter the card you want to play (e.g., '7-1' for 7♠): ")
            card = self.str_to_card(card_str)
            print(f"{self.name} plays: {card}")
            
            if card in legal_cards:
                return card
            else:
                print("Illegal move, try again.")
