import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt

# Load the Iris dataset and preprocess it for binary classification (Setosa vs. Versicolor)
iris = load_iris()
X = iris.data[:, :2]  # Use only the first two features (sepal length and width) for visualization
y = iris.target

# Select only two classes (0 = setosa, 1 = versicolor)
X = X[y < 2]
y = y[y < 2]

# Normalize the features
X = (X - np.mean(X, axis=0)) / np.std(X, axis=0)

# Add intercept term
X = np.c_[np.ones(X.shape[0]), X]  # Adding a column of ones for bias

# Initialize weights
weights = np.zeros(X.shape[1])

# Sigmoid function
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

# Prediction function
def predict(X, weights):
    return sigmoid(np.dot(X, weights))

# Loss function (binary cross-entropy)
def compute_loss(y, y_pred):
    return -np.mean(y * np.log(y_pred) + (1 - y) * np.log(1 - y_pred))

# Gradient descent
learning_rate = 0.01
iterations = 1000
losses = []

for i in range(iterations):
    # Predictions
    y_pred = predict(X, weights)
    # Calculate gradient
    gradient = np.dot(X.T, (y_pred - y)) / y.size
    # Update weights
    weights -= learning_rate * gradient
    # Compute and store loss
    loss = compute_loss(y, y_pred)
    losses.append(loss)

# Plot the loss curve
plt.plot(range(iterations), losses)
plt.xlabel("Iterations")
plt.ylabel("Binary Cross-Entropy Loss")
plt.title("Loss Curve")
plt.show()

# Classification function based on a threshold
def classify(X, weights, threshold=0.5):
    return (predict(X, weights) >= threshold).astype(int)

# Make predictions
y_pred_class = classify(X, weights)

# Evaluation metrics
accuracy = accuracy_score(y, y_pred_class)
precision = precision_score(y, y_pred_class)
recall = recall_score(y, y_pred_class)
f1 = f1_score(y, y_pred_class)

print(f"Accuracy: {accuracy * 100:.2f}%")
print(f"Precision: {precision * 100:.2f}%")
print(f"Recall: {recall * 100:.2f}%")
print(f"F1 Score: {f1 * 100:.2f}%")

# Visualization of decision boundaries
x_min, x_max = X[:, 1].min() - 1, X[:, 1].max() + 1
y_min, y_max = X[:, 2].min() - 1, X[:, 2].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1),
                     np.arange(y_min, y_max, 0.1))

# Predict over the grid
grid = np.c_[np.ones(xx.ravel().shape), xx.ravel(), yy.ravel()]
Z = classify(grid, weights)
Z = Z.reshape(xx.shape)

plt.contourf(xx, yy, Z, alpha=0.3, cmap=plt.cm.Paired)
plt.scatter(X[:, 1], X[:, 2], c=y, edgecolors='k', cmap=plt.cm.Paired)
plt.xlabel("Sepal Length (normalized)")
plt.ylabel("Sepal Width (normalized)")
plt.title("Decision Boundary")
plt.show()
