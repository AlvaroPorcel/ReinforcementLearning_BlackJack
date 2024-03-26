from blackjack import Blackjack
from agent import QLearningAgent


def print_game_state(player_sum, dealer_card, usable_ace, action):
    print(f"Player sum: {player_sum}, Dealer card: {dealer_card}, Usable ace: {usable_ace}")
    if action == 0:
        print("Agent chose to hit.")
    else:
        print("Agent chose to stand.")

if __name__ == "__main__":
    env = Blackjack()
    agent = QLearningAgent(n_actions=2)  # Dos acciones: pedir carta o quedarse

    num_episodes = 10000
    for episode in range(num_episodes):
        state = env.reset()
        done = False
        while not done:
            action = agent.choose_action(*state)
            next_state, reward, done = env.step(action)
            agent.update_q_table(state, action, reward, next_state)
            state = next_state

    num_test_episodes = 10
    total_wins = 0
    for _ in range(num_test_episodes):
        state = env.reset()
        done = False
        print("Starting a new game:")
        while not done:
            player_sum, dealer_card, usable_ace = state
            action = agent.choose_action(player_sum, dealer_card, usable_ace)
            print_game_state(player_sum, dealer_card, usable_ace, action)
            state, reward, done = env.step(action)
            if done:
                print("Game over.")
            # Mostrar la mano completa del crupier
                print(f"Dealer's hand: {env.dealer_hand}")
                if reward == 1:
                    print("Player wins!")
                    total_wins += 1
                elif reward == -1:
                    print("Dealer wins.")
                else:
                    print("It's a draw.")

win_rate = total_wins / num_test_episodes
print(f"Win rate after testing: {win_rate}")
