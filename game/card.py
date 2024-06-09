from enum import Enum

class Suit(Enum):
    SPADES = 1  # Пика
    CLUBS = 2   # Трефа
    DIAMONDS = 3 # Бубна
    HEARTS = 4  # Черви

class Rank(Enum):
    SEVEN = '7'
    EIGHT = '8'
    NINE = '9'
    TEN = '10'
    JACK = 'J'
    QUEEN = 'Q'
    KING = 'K'
    ACE = 'A'

class Card:
    suit_icons = {
        Suit.SPADES: '♠',
        Suit.CLUBS: '♣',
        Suit.DIAMONDS: '♦',
        Suit.HEARTS: '♥'
    }

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __repr__(self):
        return f"{self.rank.value}{Card.suit_icons[self.suit]}"

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.suit == other.suit and self.rank == other.rank
        return False

    def __hash__(self):
        return hash((self.suit, self.rank))