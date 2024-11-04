import numpy as np
from .make_data import make_circles as mc
import pandas as pd
import matplotlib.pyplot as plt

def tdd_make_circles():
    n_samples = 1000
    X, y = mc(n_samples = n_samples, 
                        noise = 0.1, 
                        random_state = 42, 
                        factor = 0.3)

    circles = pd.DataFrame({"X0":X[:, 0], "X1":X[:, 1], "label":y})

    plt.scatter(X[:, 0], 
                X[:, 1], 
                c = y, 
                cmap = plt.cm.RdYlBu)
    plt.show()





