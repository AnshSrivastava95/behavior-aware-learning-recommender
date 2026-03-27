import numpy as np

class EpsilonGreedyBandit:
    def __init__(self, actions, epsilon=0.1):
        self.actions = actions
        self.epsilon = epsilon
        self.n_actions = len(actions)
        self.counts = np.zeros(self.n_actions)
        self.values = np.zeros(self.n_actions)

    def select_action(self, student_cluster=None):
        if np.random.rand() < self.epsilon:
            action_index = np.random.choice(self.n_actions)
        else:
            max_value = np.max(self.values)
            best_actions = np.where(self.values == max_value)[0]
            action_index = np.random.choice(best_actions)
            
        return self.actions[action_index]

    def update(self, action, reward):
        action_index = self.actions.index(action)
        self.counts[action_index] += 1
        n = self.counts[action_index]
        self.values[action_index] += (1 / n) * (reward - self.values[action_index])

    def get_summary(self):
        return {
            self.actions[i]: {"value": self.values[i], "count": self.counts[i]}
            for i in range(self.n_actions)
        }
