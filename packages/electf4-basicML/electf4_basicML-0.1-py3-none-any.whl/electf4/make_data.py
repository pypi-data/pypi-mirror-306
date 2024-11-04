import numpy as np
import matplotlib.pyplot as plt
import numbers

from .validators import check_random_state


def make_circles(n_samples = 100, 
                 *, 
                 noise = None, 
                 random_state = None, 
                 factor = 0.8):
    if isinstance(n_samples, numbers.Integral):
        n_samples_out = n_samples // 2
        n_samples_in = n_samples - n_samples_out

    generator = check_random_state(random_state)
    linspace_out = np.linspace(0, 2 * np.pi, n_samples_out, endpoint = False)
    linspace_in = np.linspace(0, 2 * np.pi, n_samples_in, endpoint = False)
    outer_circ_x = np.cos(linspace_out)
    outer_circ_y = np.sin(linspace_out)
    inner_circ_x = np.cos(linspace_in) * factor
    inner_circ_y = np.sin(linspace_in) * factor

    X = np.vstack(
        [np.append(outer_circ_x, inner_circ_x), np.append(outer_circ_y, inner_circ_y)]
    ).T
    y = np.hstack(
        [np.zeros(n_samples_out, dtype=np.intp), np.ones(n_samples_in, dtype = np.intp)]
    )

    if noise is not None:
        X += generator.normal(scale=noise, size=X.shape)

    return X, y