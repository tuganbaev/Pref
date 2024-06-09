from .base_bot import BaseBot

class UserBot(BaseBot):
    def sort_hand(self):
        #Default sorting is to sort by suit and rank. Suit order is Spades, Clubs, Diamonds, Hearts. Rank order is Ace, King, Queen, Jack, 10, 9, 8, 7.
        super().sort_hand()

    def make_bid(self):
        # Allow user to input a bid
        bid = input(f"{self.name}, enter your bid: ")
        return bid

    def play_card(self, trick, legal_cards):
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
