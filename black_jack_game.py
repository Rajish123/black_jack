"""
Black Jack:
- contains computer dealer and human player
- human player places a bet
- player starts with 2 cards face up and dealer starts with 1 card face up and 1 card face down
- player goes first in the gameplay
- player goal is to get closer to a total value of 21 than the dealer does
- Possible actions to take:
1. Hit: Receive another card
2. Stay: Stop receiving card
- Total value is the sum of total face up cards
- Once the player turn has ended its comp turn..If the player is still under 21 then the dealer hits until it beats the player or it gets bust.
- ways to end game:
1. If the player keeps hitting and goes over 21 then it gets bust and looses.The game is over and comp collects the bet
2. Computer beats player i.e, computer keeps hitting and sum is greator than human player
3. If computer keeps hitting and gets bust, then player wins

Face card(Jack, Queen, King) -> 10 points
Aces -> 11 points
"""

import random

suits = ('heart', 'spade', 'diamond', 'club')
ranks = ('two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'jack', 'queen', 'king', 'ace')
values = {'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'jack': 10, 'queen': 10, 'king': 10, 'ace': 11}

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self): 
        return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self):
        self.all_cards = []
        for suit in suits:
            for rank in ranks:
                # create a card object
                created_card = Card(suit, rank)
                self.all_cards.append(created_card)

    def shuffle(self):
        random.shuffle(self.all_cards)

    def deal_one(self):
        return self.all_cards.pop()

    def __str__(self):
        deck_comp = " "
        for card in self.all_cards:
            deck_comp += '\n' + card.__str__()
        return f"The deck has:\n {deck_comp}"
        

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        # attribute to keep track of aces
        self.aces = 0

    def add_card(self,card ):
        self.cards.append(card)
        self.value += self.cards[-1].value
        # self.value += values[card.rank]

        if card.rank == 'ace':
            self.aces += 1

    def adjust_for_aces(self):
        # if total value > 21 and you get an ace then change the value of ace to 1
        if self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1
    
    def __str__(self):
        return f"Total point = {self.value} \n Number of Aces = {self.aces} \n"

class Chips:
    def __init__(self, total = 100):
        self.total = total
        self.bet = 0
        self.win = 0
        self.lose = 0

    def win_bet(self):
        self.total += self.bet
        self.win += 1

    def lose_bet(self):
        self.total -= self.bet
        self.lose += 1

    def __str__(self):
        return f"Total chip = {self.total}\n Win streak = {self.win}\n Lose_streak = {self.lose}"


def take_bet(player, chips):
    while True:
        try:
            chips.bet = int(input("Bet your chips: "))
        except:
            print("Please provide an integer! ")
        else:
            if chips.total < chips.bet:
                print(f"You dont have enough chips! You have {chips.total} ")
                continue
            else:
                break


def hit(deck, hand):
    single_card = deck.deal_one()
    hand.add_card(single_card)
    hand.adjust_for_aces()


def hit_or_stand(deck,hand):
    global playing
    while True:
        choice = input("Hit or Stand?(h/s): ")
        if choice[0].lower() == "h":
            hit(deck, hand)
        elif choice[0].lower() == "s":
            print("Player Stands! Dealer Turn.")
            playing = False
        else:
            print("Input is not understood.Please enter h or s.")
            continue
        break


def show_some(player, dealer):
    print("Dealer's Hand ")
    print("one card hidden\n")
    print(dealer.cards[-1])
    print("-" * 20)
    print("Player's Hand\n")
    for card in player.cards:
        print(card)
    print("-" * 20)


def show_all(player, dealer):
    print("Dealer's Hand ")
    for card in dealer.cards:
        print(card)
    print("\n\n")
    print("Player's Hand ")
    for card in player.cards:
        print(card)
    print("\n\n")
    
        
def player_busts(player, dealer, chips):
    print("Player Busts! ")
    chips.lose_bet()

def player_wins(player, dealer, chips):
    print("Player wins! ")
    chips.win_bet()

def dealer_busts(player, dealer, chips):
    print("Dealer Busts! Player wins.")
    chips._bet()

def dealer_wins(player, dealer, chips):
    print("Dealer Wns! ")
    chips.lose_bet()

def draw(player, dealer):
    print("Its a Tie! ")


if __name__ == "__main__":
    while True:

    # print an opening statement
        print("welcome to black jack".title())

        # create and shuffle a deck, deal two cards to each player
        deck = Deck()
        deck.shuffle()
        player1 = input("Enter your name:  ")
        dealer = input("Enter name for dealer: ")
        player1 = Hand()
        dealer = Hand()
        for x in range(2):
            player1.add_card(deck.deal_one())
            dealer.add_card(deck.deal_one())

        # set up player chips
        try:
            total_chips = int(input("Enter total amount of chips:  "))
        except:
            print("Invalid amount.Try again")
        else:
            chips = Chips(total_chips)

        # prompt player for their bet
        bet = take_bet(player1, chips) 

        # show cards(but keep one dealer card hidden)
        show_some(player1, dealer)

        playing = True
        while playing:
        # prompt for player to hit or stand
            hit_or_stand(deck, player1)
        # show cards but keep one dealer card hidden
            show_some(player1, dealer)

        # if player's hand exceed 21, run player_busts and end of loop 
            if player1.value > 21:
                player_busts(player1, dealer, chips)
                dealer_wins(player1, dealer, chips)
                break

        # if player hasnt busted , play dealer hand until dealer reaches 17
        if player1.value <= 21:
            while dealer.value < player1.value:
                hit(deck, dealer)

    # show all cards
            show_all(player1, dealer)

    # run different winning scenarios
            if dealer.value > 21:
                dealer_busts(player1, dealer, chips)
            elif dealer.value > player1.value:
                dealer_wins(player1, dealer, chips)
            elif dealer.value < player1.value:
                player_wins(player1, dealer, chips)
            else:
                draw(player1, dealer)

    # inform player of their chips total
        print(f"total point: {player1.value} total chips : {chips.total} ")

    # ask to play again
        play_again = input("Continue playing?(Y/N): ")
        if play_again.lower() == "y":
            playing = True
            continue
        else:
            print("Thank you for playing!")
            break










# dec = Deck()
# dec.shuffle()
# print(dec)
# print("__________________")
# card_add = dec.all_cards[0]
# print(card_add)
# print("________________")
# new = dec.deal_one()
# print(new)
# print("_____________")
# print(card_add.value)
# han = Hand()
# han.add_card(card_add)
# print(han)
# print("__________")
# han.add_card(new)
# print(han)

        