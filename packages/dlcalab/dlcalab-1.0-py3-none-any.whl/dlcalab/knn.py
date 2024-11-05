import numpy as np
import pandas as pd
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

# Load the MNIST digits dataset
digits = load_digits()
X = digits.data  # Feature matrix (images flattened into 64 features)
y = digits.target  # Labels

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# KNN from scratch
def knn_predict(X_train, y_train, X_test_instance, k):
    # Compute distances between X_test_instance and all training samples
    distances = np.sqrt(np.sum((X_train - X_test_instance) ** 2, axis=1))
    # Get the k nearest samples
    k_indices = distances.argsort()[:k]
    k_nearest_labels = y_train[k_indices]
    # Return the most common label among the k nearest neighbors
    unique, counts = np.unique(k_nearest_labels, return_counts=True)
    return unique[np.argmax(counts)]

# Evaluate KNN for different values of k
k_values = [1, 3, 5, 7, 9]
accuracies = []

for k in k_values:
    y_pred = [knn_predict(X_train, y_train, x_test, k) for x_test in X_test]
    accuracy = accuracy_score(y_test, y_pred)
    accuracies.append(accuracy)
    print(f"Accuracy for k={k}: {accuracy * 100:.2f}%")

# Plotting k vs accuracy
plt.plot(k_values, accuracies, marker='o')
plt.xlabel("k (Number of Neighbors)")
plt.ylabel("Accuracy")
plt.title("Effect of k on KNN Classification Accuracy")
plt.show()
