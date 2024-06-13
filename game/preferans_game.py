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
        self.prikup = []
        self.results = {
            bot: {
                'pulya': 0,
                'gora': 0,
                'visty': {opponent: 0 for opponent in self.bots if opponent != bot}
            } for bot in self.bots
        }
        self.player_status = {bot: None for bot in self.bots}

        # Start the game by dealing cards
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
        # The remaining cards are placed in the prikup. I know in real game it's illegal to place it in last round
        self.prikup = self.deck     

    def give_prikup_and_update_hand(self, bot, prikup):
        # Pass hand + prikup to the function
        combined_hand = self.hands[bot] + prikup

        # The bot chooses which 2 cards to discard
        cards_to_discard = bot.choose_cards_to_discard(self.hands[bot], prikup)
        
        # Ensure the discarded cards are valid (they must be in the combined hand)
        if not all(card in combined_hand for card in cards_to_discard):
            raise ValueError("Invalid cards to discard")

        # Remove the discarded cards from the combined hand
        updated_hand = [card for card in combined_hand if card not in cards_to_discard]
        
        # Update the bot's hand and the game's hand
        self.hands[bot] = updated_hand
        bot.receive_hand(updated_hand)
        
        # Store discarded cards in prikup (for future use or rules)
        self.prikup = cards_to_discard

    def conduct_bidding(self, initial_player):
        highest_bid_key = None
        highest_bid_value = -100  # Store the numeric representation for easier comparison
        highest_bidder = None  # To track which bot made the highest bid
        pass_count = 0  # To track passes
        start_index = self.bots.index(initial_player)
        ordered_bots = self.bots[start_index:] + self.bots[:start_index]

    
        while pass_count < 2:
            for bot in ordered_bots:
                if pass_count >= 2:
                    break  # Break if two consecutive passes have occurred
                bid_key = bot.make_bid(hand=bot.hand)
                if bid_key <= highest_bid_value:
                    bid_key = "pass"  # Disallow lower bids
                if bid_key == "pass":
                    pass_count += 1
                else:
                    current_bid_value = int(bid_key)
                    # Check if this is the first valid bid or if it's higher than the current highest bid
                    if highest_bid_key is None or current_bid_value > highest_bid_value:
                        highest_bid_key = bid_key
                        highest_bid_value = current_bid_value
                        highest_bidder = bot  # Update the highest bidder

        if highest_bid_key:
            contract_number, suit = GAME_MAP[highest_bid_key]
            self.declarer = highest_bidder
            self.player_status[highest_bidder] = 'declarer'
            self.trump_suit = suit
        else:
            self.declarer = None
            highest_bid_value = 30 # Raspasy

        return highest_bid_key  # Return for further processing or logging

    # def handle_visting(self, contract_id, player, ordered_bots):
    #     #Accepted ansers "pass", "vist", "pol-vista"
    #     #find next bot after player
    #     player_index = ordered_bots.index(player)
    #     new_order_bots = ordered_bots[player_index+1:] + ordered_bots[:player_index]
    #     first_want_to_vist = ordered_bots[0].become_vistuz(ordered_bots[0].hand, contract_id, self.player_status)
    #     self.player_status[ordered_bots[0]] = first_want_to_vist
    #     second_want_to_vist = ordered_bots[1].become_vistuz(ordered_bots[1].hand, contract_id, self.player_status)
    #     if second_want_to_vist == 'pass' and second_want_to_vist == 'pol-vista':
    #         #if first pass, but second pol-vista, then first should decide play or not
    #         first_want_to_vist = ordered_bots[0].become_vistuz(ordered_bots[0].hand, contract_id, self.player_status)
    #     if first_want_to_vist == 'pass' and (second_want_to_vist == "pass" or second_want_to_vist == 'pol-vista'):
    #         self.all_pass()
        


    def start_game(self, number_of_rounds=10):
        starting_index = 0
        
        for i in range(number_of_rounds):
            self.reset()
            initial_player = self.bots[starting_index]
            contract_id = self.conduct_bidding(initial_player)
            self.give_prikup_and_update_hand(initial_player, self.prikup)
            round_game = PreferansRound(self.bots, self.trump_suit, initial_player, contract_id)
            round_game.play_tricks(hands=self.hands)
            self.round_results.append(round_game.tricks_won)
            
            self.calculate_points(contract_id, round_game.tricks_won, self.declarer)
            starting_index = (starting_index + 1) % len(self.bots)
        
        self.summarize_results()

    
    def stalingrad_game(self, number_of_rounds=10):
        starting_index = 0

        for i in range(number_of_rounds):
            self.reset()

            #Играем сталинград, водит первый
            initial_player = self.bots[starting_index]
            self.declarer = initial_player
            contract_id = self.default_contract()
            self.trump_suit = GAME_MAP[contract_id][1]
            
            round_game = PreferansRound(self.bots, self.trump_suit, initial_player, contract_id)
            round_game.play_tricks(hands=self.hands)
            self.round_results.append(round_game.tricks_won)
            self.calculate_points(contract_id, round_game.tricks_won, self.declarer)
            starting_index = (starting_index + 1) % len(self.bots)
        
        self.summarize_results()


    def default_contract(self):
        return 1

    def summarize_results(self):
        for bot in self.bots:
            pulya = self.results[bot]['pulya']
            gora = self.results[bot]['gora']
            vists = self.results[bot]['visty']
            vists_str = {opponent.name: vists[opponent] for opponent in vists}
            print(f"{bot.name} scored {pulya} pulya, {gora} gora, {vists_str} vists")

    def calculate_points(self, contract_id, round_results, player):
        if contract_id == 30:
            for bot in self.bots:
                self.results[bot]['gora'] += round_results[bot]
        elif contract_id == 16:
            tricks_taken = round_results[player]
            if tricks_taken == 0:
                self.results[player]['pulya'] += 10
            else:
                self.results[player]['gora'] += tricks_taken * 10
        else:
            contract_number, suit = GAME_MAP[int(contract_id)]
            contract_value = (contract_number - 5) * 2

            if round_results[player] >= contract_number:
                self.results[player]['pulya'] += contract_value
            else:
                self.results[player]['gora'] += contract_value

            for defender in self.bots:
                if defender != player:
                    self.results[defender]['visty'][player] += round_results[defender] * contract_value
                    missed_tricks = contract_number - round_results[player]
                    if missed_tricks > 0:
                        self.results[defender]['visty'][player] += missed_tricks * contract_value

