import numpy as np
import random

class Blackjack:
    def __init__(self):
        self.reset()

    def _generate_deck(self):
        deck = []
        for _ in range(4):
            deck.extend(list(range(2, 11)) + [10, 10, 10])
        random.shuffle(deck)
        return deck

    def _deal_card(self):
        return self.deck.pop()

    def _deal_initial_cards(self):
        self.player_hand = [self._deal_card(), self._deal_card()]
        self.dealer_hand = [self._deal_card(), self._deal_card()]

    def _calculate_score(self, hand):
        score = sum(hand)
        num_aces = hand.count(11)
        while score > 21 and num_aces:
            score -= 10
            num_aces -= 1
        return score

    def _is_bust(self, hand):
        return self._calculate_score(hand) > 21

    def reset(self):
        self.deck = self._generate_deck()
        self._deal_initial_cards()
        self.usable_ace = False
        return (self.calculate_sum(self.player_hand), self.dealer_hand[0], self.usable_ace)

    def step(self, action):
        if action == 0:  # Hit
            self.player_hand.append(self._deal_card())
            done = self._is_bust(self.player_hand)
            if done:
                reward = -1
            else:
                reward = 0
        elif action == 1:  # Stand
            done = True
            while self._calculate_score(self.dealer_hand) < 17:
                self.dealer_hand.append(self._deal_card())
            player_score = self._calculate_score(self.player_hand)
            dealer_score = self._calculate_score(self.dealer_hand)
            if self._is_bust(self.dealer_hand) or player_score > dealer_score:
                reward = 1
            elif player_score < dealer_score:
                reward = -1
            else:
                reward = 0
        return (self.calculate_sum(self.player_hand), self.dealer_hand[0], self.usable_ace), reward, done

    def calculate_sum(self, hand):
        score = sum(hand)
        if score <= 11 and 11 in hand:
            self.usable_ace = True
            score += 10
        return score
    

    def _get_winner(self):
        player_score = self.calculate_sum(self.player_hand)
        dealer_score = self.calculate_sum(self.dealer_hand)

        if self._is_bust(self.player_hand):  # Si el jugador se pasa
            return -1
        elif self._is_bust(self.dealer_hand):  # Si el crupier se pasa
            return 1
        elif player_score > dealer_score:  # Si el jugador tiene una puntuación más alta que el crupier
            return 1
        elif player_score < dealer_score:  # Si el crupier tiene una puntuación más alta que el jugador
            return -1
        else:  # En caso de empate
            return 0
