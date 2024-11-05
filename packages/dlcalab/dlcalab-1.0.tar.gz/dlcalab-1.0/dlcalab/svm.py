import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_circles
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split

# Generate a non-linearly separable dataset
X, y = make_circles(n_samples=100, noise=0.1, factor=0.4, random_state=42)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Set up a grid for visualization
xx, yy = np.meshgrid(np.linspace(-1.5, 1.5, 100), np.linspace(-1.5, 1.5, 100))

# Function to plot decision boundaries
def plot_decision_boundaries(svm_model, X, y, title):
    plt.scatter(X[:, 0], X[:, 1], c=y, s=30, cmap=plt.cm.Paired)
    Z = svm_model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    plt.contourf(xx, yy, Z, alpha=0.3, cmap=plt.cm.Paired)
    plt.title(title)
    plt.xlim(-1.5, 1.5)
    plt.ylim(-1.5, 1.5)

# Train and plot SVM with linear kernel
svm_linear = SVC(kernel='linear')
svm_linear.fit(X_train, y_train)

plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plot_decision_boundaries(svm_linear, X, y, "SVM with Linear Kernel")

# Train and plot SVM with polynomial kernel
svm_poly = SVC(kernel='poly', degree=3)
svm_poly.fit(X_train, y_train)

plt.subplot(1, 3, 2)
plot_decision_boundaries(svm_poly, X, y, "SVM with Polynomial Kernel")

# Train and plot SVM with RBF kernel
svm_rbf = SVC(kernel='rbf')
svm_rbf.fit(X_train, y_train)

plt.subplot(1, 3, 3)
plot_decision_boundaries(svm_rbf, X, y, "SVM with RBF Kernel")

plt.tight_layout()
plt.show()
