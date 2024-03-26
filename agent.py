import numpy as np
class QLearningAgent:
    def __init__(self, n_actions):
        self.n_actions = n_actions
        self.q_table = np.zeros((32, 11, 2, n_actions))  # State space: player sum, dealer's card, usable ace, action
        self.epsilon = 0.1  # Exploration rate
        self.alpha = 0.5    # Learning rate
        self.gamma = 1.0    # Discount factor

    def choose_action(self, player_sum, dealer_card, usable_ace):
        if np.random.uniform(0, 1) < self.epsilon:
            return np.random.randint(self.n_actions)  # Exploration
        else:
            return np.argmax(self.q_table[player_sum, dealer_card, int(usable_ace)])

    def update_q_table(self, state, action, reward, next_state):
        player_sum, dealer_card, usable_ace = state
        next_player_sum, _, _ = next_state
        td_target = reward + self.gamma * np.max(self.q_table[next_player_sum])  # Temporal difference target
        td_error = td_target - self.q_table[player_sum, dealer_card, int(usable_ace), action]
        self.q_table[player_sum, dealer_card, int(usable_ace), action] += self.alpha * td_error



