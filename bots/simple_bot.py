from .base_bot import BaseBot
from collections import Counter
from game.card import Suit

class SimpleBot(BaseBot):
    def make_bid(self, hand):
        # Placeholder method for bidding, should be overridden
        return 1

    def play_card(self,
                trick, # Карты на столе
                legal_cards, # Карты, которые можно сыграть
                contract_id, # ID игры. Можно смотреть в consts
                trump_suit, # Козырь
                previous_tricks #Прошлые взятки
                ):
        # Play the first legal card
        return super().play_card(trick, legal_cards, contract_id, trump_suit, previous_tricks)
    
    def choose_contract(self, hand):
        return 1 # Choose to play 6 tricks with the most common suit
    
    def choose_cards_to_discard(self, hand, prikiup):
        combined_hand = hand + prikiup
        self.hand = combined_hand[2:]
        return combined_hand[:2] # Discard the first two cards