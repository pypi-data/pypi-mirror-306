import numpy as np


class LinearRegressionModel:
     
    def __init__(self):
        self.theta = None

    def initialize_theta(self, n_features):
        self.theta = np.random.randn(n_features , 1)
        return self.theta
    
    def model(self, X):
        return X.dot(self.theta)
    
    def cost_function(self, X, y):
        m = len(y)
        return 1 / (2 * m) * np.sum((self.model(X) - y) ** 2)






