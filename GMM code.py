import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
os.environ["OMP_NUM_THREADS"] = "1"
from sklearn.preprocessing import StandardScaler
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score
np.random.seed(42)

n_students = 100

data = {
    "video_time": np.random.randint(10, 120, n_students),
    "text_time": np.random.randint(5, 100, n_students),
    "quiz_attempts": np.random.randint(1, 15, n_students),
    "avg_score_video": np.random.randint(40, 100, n_students),
    "avg_score_quiz": np.random.randint(40, 100, n_students),
    "completion_rate": np.random.uniform(0.4, 1.0, n_students),
    "retry_count": np.random.randint(0, 5, n_students)
}

df = pd.DataFrame(data)
df["student_id"] = range(1, n_students + 1)

print(df.head())
features = [
    "video_time",
    "text_time",
    "quiz_attempts",
    "avg_score_video",
    "avg_score_quiz",
    "completion_rate",
    "retry_count"
]

X = df[features]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
gmm = GaussianMixture(n_components=3, random_state=42)
gmm.fit(X_scaled)

labels = gmm.predict(X_scaled)
df["cluster"] = labels
cluster_summary = df.groupby("cluster")[features].mean()
print("\nCluster Summary:")
print(cluster_summary)
probabilities = gmm.predict_proba(X_scaled)

prob_df = pd.DataFrame(probabilities, columns=["Cluster_0", "Cluster_1", "Cluster_2"])

df = pd.concat([df, prob_df], axis=1)

print("\nWith Probabilities:")
print(df.head())
score = silhouette_score(X_scaled, labels)
print("\nSilhouette Score:", score)
output = df[["student_id", "Cluster_0", "Cluster_1", "Cluster_2"]]

print("\nFinal Output:")
print(output)
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
centers = pca.transform(gmm.means_)

plt.figure()

for cluster in range(3):
    plt.scatter(
        X_pca[df["cluster"] == cluster, 0],
        X_pca[df["cluster"] == cluster, 1],
        label=f"Cluster {cluster}"
    )

plt.scatter(
    centers[:, 0],
    centers[:, 1],
    marker='X',
    s=50,
    label="Centers"
)

plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.title("Clusters with Centers")
plt.legend()

plt.show()