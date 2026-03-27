import numpy as np
import pandas as pd
from bandit.integration_api import LearningStyleBanditManager

def simulate_student_cluster_learning(manager, n_students=50, iterations=20):
    cluster_preferences = {
        0: {"best_strategy": "hybrid", "best_modality": "visual"},
        1: {"best_strategy": "focused", "best_modality": "quiz"},
        2: {"best_strategy": "focused", "best_modality": "practice"}
    }
    students = [
        {"id": f"student_{i}", "cluster": np.random.choice([0, 1, 2])}
        for i in range(n_students)
    ]
    print(f"Starting simulation with {n_students} students across 3 clusters...")
    for i in range(iterations):
        for student in students:
            profile = manager.get_student_profile(student['id'], student['cluster'])
            pref = cluster_preferences[student['cluster']]
            score = 0.5 
            if profile['strategy'] == pref['best_strategy']:
                score += 0.2
            if profile['prefered_modality'] == pref['best_modality']:
                score += 0.2
            score += np.random.normal(0, 0.05)
            score = max(0.0, min(1.0, score))
            manager.update_performance(student['id'], student['cluster'], profile, score)
    print("\n--- Simulation Complete ---")
    for cid in [0, 1, 2]:
        print(f"\nInsights for Cluster {cid}:")
        insights = manager.get_cluster_insights(cid)
        best_strat = max(insights['strategies'], key=lambda k: insights['strategies'][k]['value'])
        print(f"  Best Strategy: {best_strat} (Value: {insights['strategies'][best_strat]['value']:.3f})")
        best_mod = max(insights['modalities'], key=lambda k: insights['modalities'][k]['value'])
        print(f"  Best Modality: {best_mod} (Value: {insights['modalities'][best_mod]['value']:.3f})")

if __name__ == "__main__":
    manager = LearningStyleBanditManager(epsilon=0.2, n_clusters=3)
    simulate_student_cluster_learning(manager)
