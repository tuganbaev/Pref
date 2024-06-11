from .preferans_round import PreferansRound
from game.card import Card, Suit, Rank
from .consts import GAME_MAP
import random

class PreferansGame:
    def __init__(self, bots):
        self.bots = bots
        self.round_results = []
        self.declarer = None
        self.deck = [Card(suit, rank) for suit in Suit for rank in Rank]
        self.hands = {bot: [] for bot in self.bots}
        self.deal_cards()

    def reset(self):
        self.deck = [Card(suit, rank) for suit in Suit for rank in Rank]
        self.hands = {bot: [] for bot in self.bots}
        self.declarer = None
        self.deal_cards()

    def deal_cards(self):
        random.shuffle(self.deck)
        for i in range(10):
            for bot in self.bots:
                self.hands[bot].append(self.deck.pop())
        for bot in self.bots:
            bot.receive_hand(self.hands[bot])    

    def conduct_bidding(self):
        highest_bid_key = None
        highest_bid_value = None  # Store the numeric representation for easier comparison
        highest_bidder = None  # To track which bot made the highest bid
        pass_count = 0  # To track consecutive passes
        bid_rounds = 0  # To ensure the loop can exit safely after all have had multiple chances

        while pass_count < 2 and bid_rounds < len(self.bots) * 2:
            for bot in self.bots:
                if pass_count >= 2:
                    break  # Break if two consecutive passes have occurred
                bid_key = bot.make_bid(hand=bot.hand)
                print(f"{bot.name} bids: {bid_key}")

                if bid_key == "pass":
                    pass_count += 1  # Increment the pass count
                else:
                    pass_count = 0  # Reset pass count on a valid bid
                    current_bid_value = int(bid_key)
                    # Check if this is the first valid bid or if it's higher than the current highest bid
                    if highest_bid_key is None or current_bid_value > highest_bid_value:
                        highest_bid_key = bid_key
                        highest_bid_value = current_bid_value
                        highest_bidder = bot  # Update the highest bidder

            bid_rounds += 1  # Increment the count of bid rounds

        if highest_bid_key:
            contract_number, suit = GAME_MAP[highest_bid_key]
            self.declarer = highest_bidder  # Set the declarer to the highest bidder
            self.trump_suit = suit
            print(f"{self.declarer.name} wins the bid with {contract_number} {suit.name if suit else 'No Trump'}")
        else:
            print("All players passed. Default to a predetermined scenario.")
            self.trump_suit = Suit.SPADES  # Default scenario
            self.declarer = self.bots[0]  # Default declarer as a fallback

        return highest_bid_key  # Return for further processing or logging


    def start_game(self, number_of_rounds=10):
        starting_index = 0
        
        for i in range(number_of_rounds):
            self.reset()
            self.conduct_bidding()
            initial_player = self.bots[starting_index]
            round_game = PreferansRound(self.bots, self.trump_suit, initial_player)
            round_game.play_tricks(hands=self.hands)
            self.round_results.append(round_game.tricks_won)
            
            # Move to the next player, wrap around using modulo
            starting_index = (starting_index + 1) % len(self.bots)
        
        self.summarize_results()

    def summarize_results(self):
        total_wins = {bot: 0 for bot in self.bots}
        for result in self.round_results:
            for bot, wins in result.items():
                total_wins[bot] += wins
        for bot, wins in total_wins.items():
            print(f"{bot.name} won {wins} tricks in total.")
