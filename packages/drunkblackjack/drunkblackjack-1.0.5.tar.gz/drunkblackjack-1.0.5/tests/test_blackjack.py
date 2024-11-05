import pytest
from src.drunkblackjack import module
import random


class Tests:

    random.seed(0)

    # first 4 cards should be a 7, K, 7, A
    def test_first_four_draws(self):
        deck = [4,4,4,4,4,4,4,4,4,4,4,4,4]
        deckSize = 52
        cards_drawn = []
        for i in range (0,4):
            drawn_card = module.draw_card(deck, deckSize)
            deck[drawn_card-1] -= 1
            deckSize -= 1
            cards_drawn.append(drawn_card)
        assert cards_drawn == [7, 13, 7, 1]

    # player starts with 5, 9, if you hit, you will draw a 9 and bust, losing 1000
    def test_blackjack_player_bust(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: "hit")
        result = module.start_game(1000)
        assert result == -1000
        
    # player has 10, 4, dealer has 9, 3
    # if player stands, dealers draws a 3, is forced to hit, then draws a 2
    # which beats your 14
    def test_blackjack_dealer_bust(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: "stand")
        result = module.start_game(1000)
        assert result == -1000
    
    # player has 10, 5, dealer has 9, K
    # if player hits, he will receive a 6, blackjack
    def test_blackjack_player_blackjack(self, monkeypatch):
        inputs = iter(["hit", "stand"])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        result = module.start_game(1000)
        assert result == 1000

    # if shots_taken less than 5, play responsibly!
    # player has 2, Q
    # dealer has 2, Q
    # player stands, dealer draws 9 hitting a blackjack, rip
    def test_blackjack_not_drunk(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: "stand")
        result = module.start_game(1000)
        assert result == -1000

    # you have taken at least 5 shot
    # player has 9, 2 dealer has 6, 8
    # starting to play like a bot, if sum < 17, forced to hit
    # player will draw a J blackjack!
    def test_blackjack_drunk(self, monkeypatch):
        module.take_shots(5)
        monkeypatch.setattr('builtins.input', lambda _: "stand")
        result = module.start_game(1000)
        assert result == 1000

    # should return an array with both as ace 1 and 11
    def test_sum_cards_with_1_ace(self):
        sums = module.sum_cards([1, 9])
        assert sums == [20, 10] or sums == [10, 20]

    # if blackjack, return [21]
    def test_sum_blackjack(self):
        sums = module.sum_cards([13, 1])
        assert sums == [21]

    # an array of 1 sum if no aces
    def test_sum_no_aces(self):
        sums = module.sum_cards([10, 13])
        assert sums == [20]

    # Test if the function returns one of the good advices
    def test_get_good_advice(self):
        advice = module.get_advice('good')
        assert advice in [
            "Remember to take a break!",
            "Stopping after losing is the smarter option",
            "Drink water and stay hydrated!",
            "If you’re not having fun, it’s time to step away"
        ]

    # Test if the function returns one of the bad advices
    def test_get_bad_advice(self):
        advice = module.get_advice('bad')
        assert advice in [
            "99 percent of all gamblers quit before they make it big",
            "You haven't really lost your money until you walk away",
            "No one remembers the person who lost 100 times but everyone remembers the person who won once",
            "It takes just 1 win to earn everything back",
            "If you lose you can just walk away and come back later. If you win once you're set for life"
        ]

    # Test if the function returns an error message for invalid advice type
    def test_get_advice_invalid_input(self):
        advice = module.get_advice('neutral')
        assert advice == "I can only give 'good' or 'bad' advice!"

    # Test if the function is case insensitive for 'good' and 'bad'
    def test_get_advice_case_insensitivity(self):
        good_advice_lower = module.get_advice('good')
        good_advice_upper = module.get_advice('GOOD')
        bad_advice_lower = module.get_advice('bad')
        bad_advice_upper = module.get_advice('BAD')
        assert good_advice_lower in [
            "Remember to take a break!",
            "Stopping after losing is the smarter option",
            "Drink water and stay hydrated!",
            "If you’re not having fun, it’s time to step away"
        ]
        assert good_advice_upper in [
            "Remember to take a break!",
            "Stopping after losing is the smarter option",
            "Drink water and stay hydrated!",
            "If you’re not having fun, it’s time to step away"
        ]
        assert bad_advice_lower in [
            "99 percent of all gamblers quit before they make it big",
            "You haven't really lost your money until you walk away",
            "No one remembers the person who lost 100 times but everyone remembers the person who won once",
            "It takes just 1 win to earn everything back",
            "If you lose you can just walk away and come back later. If you win once you're set for life"
        ]
        assert bad_advice_upper in [
            "99 percent of all gamblers quit before they make it big",
            "You haven't really lost your money until you walk away",
            "No one remembers the person who lost 100 times but everyone remembers the person who won once",
            "It takes just 1 win to earn everything back",
            "If you lose you can just walk away and come back later. If you win once you're set for life"
        ]

    # Test for the function take_shots_reset
    def test_take_shots_reset(self):
        assert module.take_shots_reset() == "You are sober again!"

    # Test for the function take_shots with invalid inputs
    def test_take_shots_negative(self):
        assert module.take_shots(-1) == "You can't take negative shots!"
    def test_take_shots_invalid(self):
        assert module.take_shots("a") == "Please enter a valid number of shots!"

    # Test for the function take_shots with valid inputs
    def test_take_shots_0(self):
        assert module.take_shots(0) == "You feel great!"
    def test_take_shots_1(self):
        module.take_shots_reset()
        assert module.take_shots(1) == "You feel great!"
    def test_take_shots_2(self): 
        module.take_shots_reset()
        assert module.take_shots(2) == "You feel tipsy!"
    def test_take_shots_3(self):
        module.take_shots_reset()
        assert module.take_shots(3) == "You feel tipsy!"
    def test_take_shots_4(self):
        module.take_shots_reset()
        assert module.take_shots(4) == "You feel drunk!"
    def test_take_shots_5(self):
        module.take_shots_reset()
        assert module.take_shots(5) == "You feel drunk!"
    def test_take_shots_6(self):
        module.take_shots_reset()
        assert module.take_shots(6) == "Get me some car keys and let's go for a drive!"
    def test_take_shots_7(self):
        module.take_shots_reset()
        assert module.take_shots(7) == "Get me some car keys and let's go for a drive!"
    def test_take_shots_8(self):
        module.take_shots_reset()
        assert module.take_shots(8) == "I am invincible!"
    def test_take_shots_9(self):
        module.take_shots_reset()
        assert module.take_shots(9) == "I am invincible!"
    def test_take_shots_10(self):
        module.take_shots_reset()
        assert module.take_shots(10) == "You are wasted! Go home!"
    def test_take_shots_100(self):
        module.take_shots_reset()
        assert module.take_shots(100) == "You are wasted! Go home!"
    
    # Test for the function take_shots with a binge
    def test_take_shots_binge(self):
        module.take_shots_reset()
        assert module.take_shots(1) == "You feel great!"
        assert module.take_shots(2) == "You feel tipsy!"
        assert module.take_shots(1) == "You feel drunk!"
        assert module.take_shots(2) == "Get me some car keys and let's go for a drive!"
        assert module.take_shots(3) == "I am invincible!"
        assert module.take_shots(6) == "You are wasted! Go home!"

    def test_get_commentary_invalid(self):
        assert module.get_commentary('invalid') == "I can only commentate on 'hit', 'stand', or 'bust' actions."

    def test_get_commentary_hit_normal(self):
        module.take_shots_reset()
        commentary = module.get_commentary('hit')
        assert commentary in [
            "Taking a chance, I see!",
            "Not satisfied yet?",
            "Feeling lucky?", 
            "Brace yourself for another card!",
        ]
    
    def test_get_commentary_hit_drunk(self):
        module.take_shots_reset()
        module.take_shots(5)
        commentary = module.get_commentary('hit')
        assert commentary in [
            "This is DEFINITELY a good idea!",
            "There's no way this can backfire!",
            "You NEED another card! And maybe another drink!",
        ]

    def test_get_commentary_stand_normal(self):
        module.take_shots_reset()
        commentary = module.get_commentary('stand')
        assert commentary in [
            "Playing it safe, I like it.",
            "Happy with what you have?", 
            "A wise choice, perhaps?", 
            "Let's see what the dealer has...",
        ]

    def test_get_commentary_stand_drunk(self):
        module.take_shots_reset()
        module.take_shots(5)
        commentary = module.get_commentary('stand')
        assert commentary in [
           "But what if you got another card anyway...?",
            "Aww, but what if your total could be higher?",
            "You're SO confident that you'll win with this hand!"
        ]

    def test_get_commentary_bust(self):
        commentary = module.get_commentary('bust')
        assert commentary in [
            "Ouch! That's a bust!", 
            "Over 21, better luck next time.", 
            "You flew too close to the sun.",
            "Unlucky! The dealer takes it!"
        ]
