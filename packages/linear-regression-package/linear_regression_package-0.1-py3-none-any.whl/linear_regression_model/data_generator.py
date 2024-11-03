import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_regression

def generate_data(n_samples=100, n_features=1, noise=10):
    x, y = make_regression(n_samples=n_samples, n_features=n_features, noise=noise)
    y = y.reshape(n_samples, 1)
    return x, y

def add_bias_column(x):
    return np.hstack((x, np.ones((x.shape))))

def plot_data(x, y, model=None, X=None):
    plt.scatter(x, y, label="Data")
    if model and X is not None:
        plt.plot(x, model.model(X), color="red", label="Regression Line")
    plt.legend()
    plt.show()
    