import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True  

class Card():
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + " of " + self.suit
    
class Deck():
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank)) 
    
    def __str__(self):
        deck_comp = ""
        for card in self.deck:
            deck_comp += '\n' + card.__str__()
        return "The deck has:" + deck_comp
    
    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card
    
class Hand():
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]                                 
        if card.rank == "Ace":              
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

class Chips():
    def __init__(self):
        self.total = 100
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


def take_bet(chips):
    while True:
        try:              
            chips.bet = int(input("How many chips would you like to bet? "))
        except ValueError:
            print("Sorry, a bet must be a number!")
        else:
            if chips.bet > chips.total: 
                print("Sorry, your bet can't exceed", chips.total)
            else:
                break        
                            

def hit(deck,hand): 
    hand.add_card(deck.deal()) 
    hand.adjust_for_ace()

def hit_or_stand(deck, hand):
    global playing      
    while True:
        answer = input("Would you like to Hit or Stand? Enter 'h' or 's' ")
        if answer[0].lower() == 'h':
            hit(deck,hand)
        elif answer[0].lower() == 's':
            print("Player stands, dealer plays!")
            playing = False
        else:              
            print("Sorry, please try again.")   
            continue                  
        break                  

def show_some(player, dealer):
    print("\nDealer's hand:")
    print("<card hidden>")
    print(dealer.cards[1]) 
    print("\nPlayer's hand:", *player.cards, sep = '\n')
    print(f"Player's hand so far: {player.value}")

def show_all(player,dealer):
    print("\nDealer's hand:", *dealer.cards, sep = '\n')
    print(f"Dealer's hand = {dealer.value}")
    print("\nPlayer's hand:", *player.cards, sep = '\n')
    print(f"Player's hand = {player.value}")

def player_busts(chips):
    print("Player busts!")
    chips.lose_bet()

def player_wins(chips):
    print("Player wins!")
    chips.win_bet()    

def dealer_busts(chips):
    print("Dealer busts!")
    chips.win_bet()

def dealer_wins(chips):
    print("Dealer wins!")
    chips.lose_bet()

def push():
    print("Dealer and player tie! It's a push.")


while True:
    print('Welcome to BlackJack! Get as close to 21 as you can without going over!\n\
    Dealer hits until she reaches 17. Aces count as 1 or 11.')

    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    player_chips = Chips()

    take_bet(player_chips)
    show_some(player_hand, dealer_hand)


    while playing: 
        hit_or_stand(deck, player_hand) 
        show_some(player_hand, dealer_hand)
        if player_hand.value > 21: 
            player_busts(player_chips) 
            break 
    
    if player_hand.value <= 21: 
        while dealer_hand.value < 17:
            hit(deck, dealer_hand) 
        show_all(player_hand, dealer_hand) 
        if dealer_hand.value > 21:  
            dealer_busts(player_chips) 
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_chips)
        else:
            push()

    print("\nPlayer's winnings stand at ", player_chips.total)
    new_game = input("Would you like to play another hand? Enter 'Y' or 'N' ")
    if new_game[0].lower() == 'y':
        playing = True      
        continue        
    else:
        print("Thank you for playing!")
        break
    