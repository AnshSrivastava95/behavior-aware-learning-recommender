import json
import os
import numpy as np
from bandit.epsilon_greedy import EpsilonGreedyBandit
from bandit.reward_function import RewardFunction

class LearningStyleBanditManager:
    def __init__(self, epsilon=0.1, n_clusters=3, storage_file='bandit_data.json'):
        self.strategies = ['focused', 'hybrid']
        self.modalities = ['visual', 'reading', 'quiz', 'practice', 'revision', 'challenge']
        self.reward_fn = RewardFunction()
        self.storage_file = storage_file
        self.strategy_bandits = {
            cluster_id: EpsilonGreedyBandit(self.strategies, epsilon)
            for cluster_id in range(n_clusters)
        }
        self.modality_bandits = {
            cluster_id: EpsilonGreedyBandit(self.modalities, epsilon)
            for cluster_id in range(n_clusters)
        }
        self.student_performance_history = {} 
        self.load_data()

    def save_data(self):
        data = {
            "strategy_bandits": {
                str(cid): {
                    "counts": b.counts.tolist(),
                    "values": b.values.tolist()
                } for cid, b in self.strategy_bandits.items()
            },
            "modality_bandits": {
                str(cid): {
                    "counts": b.counts.tolist(),
                    "values": b.values.tolist()
                } for cid, b in self.modality_bandits.items()
            }
        }
        with open(self.storage_file, 'w') as f:
            json.dump(data, f)

    def load_data(self):
        if not os.path.exists(self.storage_file):
            return
        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
            for cid_str, b_data in data.get("strategy_bandits", {}).items():
                cid = int(cid_str)
                if cid in self.strategy_bandits:
                    self.strategy_bandits[cid].counts = np.array(b_data["counts"])
                    self.strategy_bandits[cid].values = np.array(b_data["values"])
            for cid_str, b_data in data.get("modality_bandits", {}).items():
                cid = int(cid_str)
                if cid in self.modality_bandits:
                    self.modality_bandits[cid].counts = np.array(b_data["counts"])
                    self.modality_bandits[cid].values = np.array(b_data["values"])
        except Exception as e:
            print(f"Error loading bandit data: {e}")

    def get_student_profile(self, student_id, cluster_id):
        cluster_id = cluster_id if cluster_id in self.strategy_bandits else 0
        strategy = self.strategy_bandits[cluster_id].select_action()
        preferred_modality = self.modality_bandits[cluster_id].select_action()
        return {
            "strategy": strategy,
            "prefered_modality": preferred_modality,
            "prefered_difficulty": 0.65
        }

    def update_performance(self, student_id, cluster_id, profile_used, score):
        cluster_id = cluster_id if cluster_id in self.strategy_bandits else 0
        previous_score = self.student_performance_history.get(student_id)
        reward = self.reward_fn.calculate_reward(score, previous_score)
        self.strategy_bandits[cluster_id].update(profile_used['strategy'], reward)
        self.modality_bandits[cluster_id].update(profile_used['prefered_modality'], reward)
        self.student_performance_history[student_id] = score
        self.save_data()
        return reward

    def get_cluster_insights(self, cluster_id):
        if cluster_id not in self.strategy_bandits:
            return None
        return {
            "strategies": self.strategy_bandits[cluster_id].get_summary(),
            "modalities": self.modality_bandits[cluster_id].get_summary()
        }
