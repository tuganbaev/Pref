from game.card import Card, Rank, Suit

class BaseBot:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def receive_hand(self, hand):
        self.hand = hand
        self.sort_hand()

    def sort_hand(self):
        # Sorting rules: Suits ordered by their numerical value and ranks in descending order
        suit_order = {
            Suit.SPADES: 1,
            Suit.CLUBS: 2,
            Suit.DIAMONDS: 3,
            Suit.HEARTS: 4
        }
        
        rank_order = {
            Rank.ACE: 14,  # Highest rank
            Rank.KING: 13,
            Rank.QUEEN: 12,
            Rank.JACK: 11,
            Rank.TEN: 10,
            Rank.NINE: 9,
            Rank.EIGHT: 8,
            Rank.SEVEN: 7  # Lowest rank
        }
        
        self.hand.sort(key=lambda card: (suit_order[card.suit], -rank_order[card.rank]))


    def print_hand(self):
        hand_str = ", ".join(map(str, self.hand))
        print(f"{self.name}'s hand: {hand_str}")

    def make_bid(self):
        # Default implementation, to be overridden if needed
        return 0

    def play_card(self, trick, legal_cards):
        # Default implementation, to be overridden
        # For example, just play the first legal card
        if legal_cards:
            return legal_cards[0]
        raise ValueError("No legal cards to play.")

    # Methods for card conversion and validation
    def str_to_card(self, card_str):
        rank_str, suit_str = card_str.split('-')
        rank = self.str_to_rank(rank_str.strip())
        suit = self.str_to_suit(suit_str.strip())
        return Card(suit, rank)

    def str_to_rank(self, rank_str):
        rank_mapping = {
            '7': Rank.SEVEN, '8': Rank.EIGHT, '9': Rank.NINE, '10': Rank.TEN,
            '11': Rank.JACK, '12': Rank.QUEEN, '13': Rank.KING, '14': Rank.ACE,
            'j': Rank.JACK, 'q': Rank.QUEEN, 'k': Rank.KING, 'a': Rank.ACE,
            'J': Rank.JACK, 'Q': Rank.QUEEN, 'K': Rank.KING, 'A': Rank.ACE
        }
        return rank_mapping[rank_str]

    def str_to_suit(self, suit_str):
        suit_mapping = {
            '1': Suit.SPADES, '2': Suit.CLUBS, '3': Suit.DIAMONDS, '4': Suit.HEARTS
        }
        return suit_mapping[suit_str]
