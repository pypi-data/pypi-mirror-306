import random
import time

# Global variable to keep track of the number of shots taken
shots_taken = 0

# draws a random card from the available deck pool
def draw_card(deck, deckSize):
    random_num = random.randint(1, deckSize)
    counter = 0
    for i in range (0, 13):
        if (counter + deck[i] >= random_num):
            return i + 1
        else:
            counter += deck[i]

# display all cards held
def print_cards(who, hand):
    print(who + " cards:", end=" ")
    for i in range (0, len(hand)):
         match hand[i]:
            case 11:
                print("|J|", end=" ")
            case 12:
                print("|Q|", end=" ")
            case 13:
                print("|K|", end=" ")
            case 1:
                print("|A|", end=" ")
            case _:
                print("|" + str(hand[i]) + "|", end=" ")
    print()    

# sums all cards in the specified hand
def sum_cards(hand):
    sums = [0]
    for i in range(0, len(hand)):
        match hand[i]:
            case 11 | 12 | 13:
                for j in range(0, len(sums)):
                    sums[j] += 10
            case 1:
                sums_length = len(sums)
                for j in range(0, sums_length):
                    sums.append(sums[j] + 1)
                    sums[j] += 11
            case _:
                for j in range(0, len(sums)):
                    sums[j] += hand[i]
    # if any sum > 21, remove it
    # if any sum = 21, BLACKJACK!
    valid_sums = [element for element in sums if element <= 21]
    if 21 in valid_sums:
        return [21]

    return valid_sums

def start_game(bet_amount):
    deck = [4,4,4,4,4,4,4,4,4,4,4,4,4]
    deckSize = 52
    print("You are betting $" + str(bet_amount))

    # draws 2 cards for the player
    player_cards = []
    for i in range (0, 2):
        drawn_card = draw_card(deck, deckSize)
        deck[drawn_card - 1] -= 1
        deckSize -= 1
        player_cards.append(drawn_card)

    # draws 2 cards for the dealer
    dealer_cards = []
    for i in range (0, 2):
        drawn_card = draw_card(deck, deckSize)
        deck[drawn_card - 1] -= 1
        deckSize -= 1
        dealer_cards.append(drawn_card)

    # check if anyone has blackjack
    player_sum = sum_cards(player_cards)
    dealer_sum = sum_cards(dealer_cards)
    if (player_sum[0] == 21 and dealer_sum == 21):
        print_cards("Dealer", dealer_cards)
        print_cards("Player", player_cards)
        print("It's a tie! You will recieve your bet back")
        return 0
    elif (dealer_sum[0] == 21):
        print_cards("Dealer", dealer_cards)
        print_cards("Player", player_cards)
        print("Unlucky :(, you lost $" + str(bet_amount) + "!")
        return bet_amount * -1
    elif (player_sum[0] == 21):
        print_cards("Dealer", dealer_cards)
        print_cards("Player", player_cards)
        print("NICE, you just won $" + str(bet_amount) + "!")
        return bet_amount
        
    while (True):
        hidden_card = dealer_cards[0]
        dealer_cards[0] = '?'
        print_cards("Dealer", dealer_cards)
        print_cards("Player", player_cards)
        dealer_cards[0] = hidden_card
        print()

        player_sum = sum_cards(player_cards)
        greatest_player_sum = 0
        for i in range (0, len(player_sum)):
            if (player_sum[i] > greatest_player_sum):
                greatest_player_sum = player_sum[i]
        
        decision = "hit"
        global shots_taken
        if (shots_taken >= 5 and greatest_player_sum < 17):
            print("You're too drunk, yolo bolo let's HIT!")
            time.sleep(1.2)
        else:
            decision = input("Please type \"stand\" or \"hit\"\n")

        if (decision == "stand"):
            print(get_commentary('stand'))
            print("You chose to STAND")
            print()
            time.sleep(1.2)
            player_sum = sum_cards(player_cards)
            greatest_player_sum = 0
            for i in range (0, len(player_sum)):
                if (player_sum[i] > greatest_player_sum):
                    greatest_player_sum = player_sum[i]
            
            dealer_sum = sum_cards(dealer_cards)
            greatest_dealer_sum = 0
            for i in range (0, len(dealer_sum)):
                if (dealer_sum[i] > greatest_dealer_sum):
                    greatest_dealer_sum = dealer_sum[i]

            print_cards("Dealer", dealer_cards)
            print_cards("Player", player_cards)
            print()

            while (dealer_sum != [] and greatest_dealer_sum < 17):
                time.sleep(1.2)
                drawn_card = draw_card(deck, deckSize)
                deck[drawn_card - 1] -= 1
                deckSize -= 1
                dealer_cards.append(drawn_card)
                dealer_sum = sum_cards(dealer_cards)
                print_cards("Dealer", dealer_cards)
                print_cards("Player", player_cards)
                print()
                for i in range (0, len(dealer_sum)):
                    if (dealer_sum[i] > greatest_dealer_sum):
                        greatest_dealer_sum = dealer_sum[i]
                print("Current greatest dealer sum =", greatest_dealer_sum)

            if (dealer_sum == []):
                print("Dealer busted!, you win $" + str(bet_amount) + "!")
                return bet_amount
            elif (greatest_dealer_sum == greatest_player_sum):
                print("It's a tie! You will recieve your bet back")
                return 0
            elif (greatest_dealer_sum > greatest_player_sum):
                print("Unlucky :(, you lost $" + str(bet_amount) + "!")
                return bet_amount * -1
            else:
                print("NICE, you just won $" + str(bet_amount) + "!")
                return bet_amount

        elif(decision == "hit"):
            print(get_commentary('hit'))
            print("You chose to HIT")
            print()
            time.sleep(1.2)
            drawn_card = draw_card(deck, deckSize)
            deck[drawn_card - 1] -= 1
            deckSize -= 1
            player_cards.append(drawn_card)
            player_sum = sum_cards(player_cards)
            if (len(player_sum) == 0):
                print_cards("Dealer", dealer_cards)
                print_cards("Player", player_cards)
                print(get_commentary('bust'))
                print("You busted! RIP $" + str(bet_amount) + "!")
                return bet_amount * -1
            if (player_sum == [21]):
                print_cards("Dealer", dealer_cards)
                print_cards("Player", player_cards)
                print("NICE, you just won $" + str(bet_amount) + "!")
                return bet_amount
        else:
            print("You did not type the input correctly!")

    return

def get_commentary(action):
    hit_normal = [
        "Taking a chance, I see!",
        "Not satisfied yet?",
        "Feeling lucky?", 
        "Brace yourself for another card!",
    ]
    stand_normal = [
        "Playing it safe, I like it.",
        "Happy with what you have?", 
        "A wise choice, perhaps?", 
        "Let's see what the dealer has...",
    ]
    hit_drunk = [
        "This is DEFINITELY a good idea!",
        "There's no way this can backfire!",
        "You NEED another card! And maybe another drink!",
    ]
    stand_drunk = [
        "But what if you got another card anyway...?",
        "Aww, but what if your total could be higher?",
        "You're SO confident that you'll win with this hand!"
    ]
    bust = [
        "Ouch! That's a bust!", 
        "Over 21, better luck next time.", 
        "You flew too close to the sun.",
        "Unlucky! The dealer takes it!"
    ]
    if action.lower() == 'hit':
        if shots_taken < 4:
            return random.choice(hit_normal)
        else:
            return random.choice(hit_drunk)
    elif action.lower() == 'stand':
        if shots_taken < 4:
            return random.choice(stand_normal)
        else:
            return random.choice(stand_drunk)
    elif action.lower() == 'bust':
        return random.choice(bust)
    else:
        return "I can only commentate on 'hit', 'stand', or 'bust' actions."
    
def get_advice(advice_type):
    good_advice = [
        "Remember to take a break!",
        "Stopping after losing is the smarter option",
        "Drink water and stay hydrated!",
        "If you’re not having fun, it’s time to step away",
    ]
    
    bad_advice = [
        "99 percent of all gamblers quit before they make it big",
        "You haven't really lost your money until you walk away",
        "No one remembers the person who lost 100 times but everyone remembers the person who won once",
        "It takes just 1 win to earn everything back",
        "If you lose you can just walk away and come back later. If you win once you're set for life",
    ]
    if advice_type.lower() == 'good':
        return random.choice(good_advice)
    elif advice_type.lower() == 'bad':
        return random.choice(bad_advice)
    else:
        return "I can only give 'good' or 'bad' advice!"

def take_shots_reset():
    global shots_taken
    shots_taken = 0
    return "You are sober again!"

def take_shots(number_of_shots):

    # Validates the input
     if type(number_of_shots) != int:
        return "Please enter a valid number of shots!"
     elif number_of_shots < 0:
        return "You can't take negative shots!"
     else:
        # Increments the global variable shots_taken by the number of shots taken
        # Print a message based on the total number of shots taken
        global shots_taken
        shots_taken += number_of_shots
        if shots_taken <= 1:
            return "You feel great!"
        elif shots_taken <= 3:
            return "You feel tipsy!"
        elif shots_taken <= 5:
            return "You feel drunk!"
        elif shots_taken <= 7:
            return "Get me some car keys and let's go for a drive!"
        elif shots_taken <= 9:
            return "I am invincible!"
        elif shots_taken >= 10:
            take_shots_reset()
            return "You are wasted! Go home!"
        return