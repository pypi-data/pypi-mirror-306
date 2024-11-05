import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv('housing.csv')
X = data['square_feet'].values  # Feature: square footage
Y = data['price'].values        # Target: price

# Normalize the data (feature scaling)
X = (X - np.mean(X)) / np.std(X)

# Hyperparameters
learning_rate = 0.01
iterations = 1000

# Initial weights
m = 0
c = 0

# Number of data points
n = len(X)

# Gradient Descent
for i in range(iterations):
    Y_pred = m * X + c  # Predicted values
    # Calculate gradients
    D_m = (-2/n) * sum(X * (Y - Y_pred))  # Derivative with respect to m
    D_c = (-2/n) * sum(Y - Y_pred)        # Derivative with respect to c
    # Update weights
    m = m - learning_rate * D_m
    c = c - learning_rate * D_c

# Predicted values
Y_pred = m * X + c

# Mean Squared Error
mse = np.mean((Y - Y_pred) ** 2)
print(f"Mean Squared Error: {mse}")

# Plotting the results
plt.scatter(X, Y, color='blue', label="Data points")
plt.plot(X, Y_pred, color='red', label="Regression line")
plt.xlabel("Square Footage (normalized)")
plt.ylabel("House Price")
plt.legend()
plt.show()
