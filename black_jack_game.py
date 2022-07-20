#!/usr/bin/env python
# coding: utf-8

# In[1]:

import random
import Base 
suits=Base.suits
ranks=Base.ranks
values=Base.values
playing=True


# In[2]:
class Card:
    def __init__(self,suit,rank):
        self.suit=suit
        self.rank=rank
        
    def __str__(self):
        return self.rank + ' of ' + self.suit + '\n' + str(Card.print(self))

    def print(self):
        print('_______')
        print(f'| {self.rank:<2}    |')         #{self.rank:<2}  ":<2" is string padding used for making a 2 character string with left allignment
        print('|       |')
        print(f'|   {self.suit}   |')
        print('|       |')
        print(f'|    {self.rank:>2} |')        #{self.rank:<2}  ":>2" is string padding used for making a 2 character string with right allignment
        print('└───────┘') 


# In[3]:

class Deck:                                                                    # creating deck of cards in different ways and shuffle the deck using 
                                                                               # inbuilt shuffle function of random library
    def __init__(self):
        self.deck = []                                                         # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))                              # build Card objects and add them to the list deck 
                
                                     
    def __str__(self):
        deck_comp = ''                                                         # start with an empty string
        for card in self.deck:
            deck_comp += '\n '+ card.__str__()                                 # add each Card object's print string
        return 'The deck has:' + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        single_card = self.deck.pop()
        return single_card
# In[4]:
class Hand:
    def __init__(self):
        self.cards=[]                                                        #start with an empty list
        self.value=0                                                         #start with zero values
        self.aces=0                                                          #add an attribute to keep track of aces
    def add_card(self,card):
        self.cards.append(card)
        self.value+=values[card.rank]
        if card.rank=='Ace':
            self.aces+=1                                                     #add to self.aces
    def adjust_for_ace(self):
        while self.value>21 and self.aces>0:
            self.value-=10
            self.aces-=1


# In[5]:
class Chips:
    def __init__(self):
        self.total=100                                                      #default value
        self.bet=0
    def win_bet(self):
        self.total+=self.bet
    def lose_bet(self):
        self.total-=self.bet
def take_bet(chips):
    while True:
        try:
            print('Max chips limit: 100')
            chips.bet=int(input('How many chips would you like to bet? '))
        except ValueError:
            print('Sorry! the bet must be an integer.')
        else:
            if chips.bet>chips.total:
                print(f'Sorry! Your bet can exceed {chips.total}.')
            else:
                break
                             
def hit(deck,hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()
def hit_or_stand(deck,hand):
    global playing                                                        #control the while loop below
    while True:
        x=input('Would you like to hit or stand? h or s: ')
        if x[0].lower()=='h':
            hit(deck,hand)
        elif x[0].lower()=='s':
            print('Player stands. Dealer is playing')
            playing=False
        else:
            print('Sorry plz try again.')
            print('Pease enter h or s only')
            continue
        break

def show_some(player,dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('',dealer.cards[1])  
    print("\nPlayer's Hand:", *player.cards,sep='\n ')
    
def show_all(player,dealer):
    print("\nDealer's Hand:", *dealer.cards,sep='\n ')
    print("Dealer's Hand =",dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =",player.value)
def player_busts(player,dealer,chips):
    print("Player busts!")
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print("Player wins!")
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print("Dealer busts!")
    chips.win_bet()
    
def dealer_wins(player,dealer,chips):
    print("Dealer wins!")
    chips.lose_bet()
    
def push(player,dealer):
    print("Dealer and Player tie! It's a push.")


# In[6]:
while True:
                                                                      # Print an opening statement
        print('Welcome to BlackJack! Get as close to 21 as you can without going over!')
        print('Dealer hits until she reaches 17. Aces count as 1 or 11.')
                                                                      # asking for the name of user
        username = input("Please give a username: ")

                                                                     # Create & shuffle the deck, deal two cards to each player
        deck = Deck()
        deck.shuffle()

        player_hand = Hand()
        player_hand.add_card(deck.deal())
        player_hand.add_card(deck.deal())

        dealer_hand = Hand()
        dealer_hand.add_card(deck.deal())
        dealer_hand.add_card(deck.deal())

                                                                    # Set up the Player's chips
        player_chips = Chips()                                      # remember the default value is 100    

                                                                    # Prompt the Player for their bet
        take_bet(player_chips)
                                                                    # Show cards (but keep one dealer card hidden)
        show_some(player_hand,dealer_hand)

        while playing:                                              # recall this variable from our hit_or_stand function

                                                                    # Prompt for Player to Hit or Stand
            hit_or_stand(deck,player_hand) 

                                                                    # Show cards (but keep one dealer card hidden)
            show_some(player_hand,dealer_hand)  

                                                                    # If player's hand exceeds 21, run player_busts() and break out of loop
            if player_hand.value > 21:
                player_busts(player_hand,dealer_hand,player_chips)
                break        


                                                                    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17 
        if player_hand.value <= 21:

            while dealer_hand.value < 17:
                hit(deck,dealer_hand)    

                                                                    # Show all cards
            show_all(player_hand,dealer_hand)

                                                                    # Run different winning scenarios
            if dealer_hand.value > 21:
                dealer_busts(player_hand,dealer_hand,player_chips)

            elif dealer_hand.value > player_hand.value:
                dealer_wins(player_hand,dealer_hand,player_chips)

            elif dealer_hand.value < player_hand.value:
                player_wins(player_hand,dealer_hand,player_chips)
            else:
                push(player_hand,dealer_hand)        

                                                                   # Inform Player of their chips total 
        print("\nPlayer's winnings stand at",player_chips.total)

                                                                   #Data file
        file=open('Data.txt','a+')
        from datetime import datetime
                                                                   # datetime object containing current date and time
        now = datetime.now()
                                                                   # dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        list_data=[dt_string,' ','Username = '+username,' Player chips after game: ',str(player_chips.total),'\n']
        file.writelines(list_data)
        file.close()

                                                                   # Ask to play again
        new_game = input("Would you like to play another hand? Enter 'y' or 'n' ")

        if new_game[0].lower()=='y':
            playing=True
            continue
        else:
            print('Thanks for playing')
            break

view_access=input('Do you want to access the data file (y/n):')
if view_access=='y':
    passwd=input('Plz provide admin Passwd:')
    password=open('Passwd.txt','r')
    p=password.readlines()
    file=open('Data.txt','r')
    if p[0]==passwd:
        print(file.read())
    else:
        print('Invalid password')
else:
    print('Thankyou')
