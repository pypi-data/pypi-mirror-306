import numpy as np

class SimpleLinearRegression:
    def __init__(self):
        self.slope = None
        self.intercept = None

    def fit(self, X, y):
        n = len(X)
        self.slope = (n * np.sum(X * y) - np.sum(X) * np.sum(y)) / (n * np.sum(X ** 2) - np.sum(X) ** 2)
        self.intercept = (np.sum(y) - self.slope * np.sum(X)) / n

    def predict(self, X):
        return self.intercept + self.slope * X
