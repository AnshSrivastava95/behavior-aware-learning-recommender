class RewardFunction:
    def __init__(self, weight_score=0.4, weight_improvement=0.6):
        self.weight_score = weight_score
        self.weight_improvement = weight_improvement

    def calculate_reward(self, current_score, previous_score=None):
        current_score = max(0.0, min(1.0, current_score))
        improvement = 0.0
        if previous_score is not None:
            improvement = (current_score - previous_score)
            improvement = max(-1.0, min(1.0, improvement))
            improvement = (improvement + 1.0) / 2.0
            
        if previous_score is not None:
            reward = (self.weight_score * current_score) + (self.weight_improvement * improvement)
        else:
            reward = current_score
            
        return reward

    def map_to_bandit(self, reward):
        return reward
