# Save as regression.py
import numpy as np

class SimpleLinearRegression:
    def __init__(self):
        self.slope = None
        self.intercept = None

    def fit(self, x, y):
        n = len(x)
        x_mean = np.mean(x)
        y_mean = np.mean(y)

        self.slope = np.sum((x - x_mean) * (y - y_mean)) / np.sum((x - x_mean) ** 2)
        self.intercept = y_mean - self.slope * x_mean

    def predict(self, x):
        return self.intercept + self.slope * x

    def __str__(self):
        return f"Simple Linear Regression Model: y = {self.slope}x + {self.intercept}"
