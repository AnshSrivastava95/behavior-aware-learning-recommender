from bandit.integration_api import LearningStyleBanditManager

bandit_manager = LearningStyleBanditManager(epsilon=0.1, n_clusters=3)

def get_student_cluster(student_id):
    return 0 

student_id = "user_123"
cluster_id = get_student_cluster(student_id)

student_profile = bandit_manager.get_student_profile(student_id, cluster_id)
print(f"Generated Profile for {student_id}: {student_profile}")

test_score = 0.85 
reward = bandit_manager.update_performance(student_id, cluster_id, student_profile, test_score)

print(f"Bandit updated! Reward calculated: {reward:.3f}")

print("\nCurrent Insights for Cluster 0:")
print(bandit_manager.get_cluster_insights(0))
