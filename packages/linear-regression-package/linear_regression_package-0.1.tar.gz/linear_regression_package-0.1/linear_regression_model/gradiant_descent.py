import numpy as np
from .linear_model import LinearRegressionModel


def gradient(X, y, model):
    m = len(y)
    return (1 / m) * X.T.dot(model.model(X) - y)

def gradient_descent(X, y, model, learning_rate, n_iter):
    cost_history = np.zeros(n_iter)
    for i in range(n_iter):
        model.theta -= learning_rate * gradient(X, y, model)
        cost_history[i] = model.cost_function(X, y)
    
    return model.theta, cost_history
 