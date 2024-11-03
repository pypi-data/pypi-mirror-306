import numpy as np

class SimpleLinearRegression:
    def __init__(self):
        self.coefficient = None
        self.intercept = None

    def fit(self, X, y):
        n = len(X)
        X_mean = np.mean(X)
        y_mean = np.mean(y)

        self.coefficient = np.sum((X - X_mean) * (y - y_mean)) / np.sum((X - X_mean) ** 2)
        self.intercept = y_mean - self.coefficient * X_mean

    def predict(self, X):
        return self.intercept + self.coefficient * X
