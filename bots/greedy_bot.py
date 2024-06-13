from .base_bot import BaseBot
from game.card import Card, Suit, Rank
from collections import Counter
from game.consts import GAME_MAP


class GreedyBot(BaseBot):
    def make_bid(self, hand):
        # Calculate the strength of the hand to decide on making a bid
        suit_strength = Counter(card.suit for card in hand)
        most_common_suit, count = suit_strength.most_common(1)[0]
        if count >= 3:  # Simple condition to decide on making a bid
            for key, (trick, suit) in GAME_MAP.items():
                if trick == 6 and suit == most_common_suit:
                    return key  # Return the key that matches the bid
        return "pass"

    def choose_contract(self, hand):
        # Assume it chooses the most common suit and aims for a low contract
        suit_strength = Counter(card.suit for card in hand)
        most_common_suit, _ = suit_strength.most_common(1)[0]
        return (6, most_common_suit)  # Choose to play 6 tricks with the most common suit

    def play_card(self, trick, legal_cards, contract_id, trump_suit, previous_tricks):
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
    
    def choose_cards_to_discard(self, hand, prikiup):
        combined_hand = hand + prikiup
        self.hand = combined_hand[2:]
        return combined_hand[:2] # Discard the first two cards
    
