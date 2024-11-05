import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler

# Load the Iris dataset
iris = load_iris()
X = iris.data  # Features
y = iris.target  # Actual labels

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# K-Means implementation
class SimpleKMeans:
    def __init__(self, k=3):
        self.k = k

    def fit(self, X):
        # Randomly initialize centroids
        np.random.seed(42)
        random_indices = np.random.choice(X.shape[0], self.k, replace=False)
        self.centroids = X[random_indices]

        for _ in range(100):  # Max iterations
            # Assign clusters
            distances = np.linalg.norm(X[:, np.newaxis] - self.centroids, axis=2)
            self.labels = np.argmin(distances, axis=1)

            # Update centroids
            new_centroids = np.array([X[self.labels == i].mean(axis=0) for i in range(self.k)])
            if np.all(new_centroids == self.centroids):
                break
            self.centroids = new_centroids

    def predict(self, X):
        distances = np.linalg.norm(X[:, np.newaxis] - self.centroids, axis=2)
        return np.argmin(distances, axis=1)

# Perform K-Means clustering with k=3
kmeans = SimpleKMeans(k=3)
kmeans.fit(X_scaled)
predicted_labels = kmeans.labels

# Plot the results
plt.figure(figsize=(12, 5))

# Plotting predicted labels
plt.subplot(1, 2, 1)
plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=predicted_labels, cmap='viridis', marker='o', edgecolor='k')
plt.title('K-Means Clustering (Predicted Labels)')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')

# Plotting actual labels
plt.subplot(1, 2, 2)
plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=y, cmap='viridis', marker='o', edgecolor='k')
plt.title('Iris Dataset (Actual Labels)')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')

plt.tight_layout()
plt.show()

# Elbow Method to determine optimal number of clusters
inertia = []
k_range = range(1, 11)

for k in k_range:
    kmeans = SimpleKMeans(k=k)
    kmeans.fit(X_scaled)
    inertia.append(np.sum((X_scaled - kmeans.centroids[kmeans.labels]) ** 2))

# Plot inertia for different values of k
plt.figure(figsize=(8, 5))
plt.plot(k_range, inertia, marker='o')
plt.title('Elbow Method for Optimal k')
plt.xlabel('Number of clusters (k)')
plt.ylabel('Inertia')
plt.xticks(k_range)
plt.grid()
plt.show()
