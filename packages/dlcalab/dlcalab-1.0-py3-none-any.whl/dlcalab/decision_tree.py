import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

# Load the Iris dataset
iris = load_iris()
X, y = iris.data, iris.target

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the Decision Tree classifier
clf = DecisionTreeClassifier(random_state=42)
clf.fit(X_train, y_train)

# Predict and evaluate the model
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")

# Visualize the Decision Tree structure
plt.figure(figsize=(12, 8))
plot_tree(clf, feature_names=iris.feature_names, class_names=iris.target_names, filled=True, rounded=True)
plt.title("Decision Tree Structure")
plt.show()

# Analyze feature importance
feature_importances = clf.feature_importances_
for feature, importance in zip(iris.feature_names, feature_importances):
    print(f"Feature: {feature}, Importance: {importance:.2f}")

# Plot feature importance
plt.figure(figsize=(8, 6))
plt.barh(iris.feature_names, feature_importances, color="skyblue")
plt.xlabel("Feature Importance")
plt.title("Feature Importance in Decision Tree Classifier")
plt.show()
