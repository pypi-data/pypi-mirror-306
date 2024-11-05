# Monte-Carlo routines
import numpy as np

def ede(x, model):
    """
    The essential dynamics energy of coordinates x in pca model model
    """
    scores = model.transform([x.flatten()])[0]
    E = 0.0
    for j, s in enumerate(scores):
        E += (s * s / model.explained_variance_[j]) * 0.5
    return E

def mmc_series(n_samples, interval, n_dims=None, start=None):
    """
    Returns a Metropolis Monte-Carlo sequence.

    Args:
        n_namples: int, number of samples to return
        interval: int, number of MC steps between samples
        n_dims: int, dimensionality of the sequence,
        start: list-like, length n_dims, starting values for the sequence.
               if not given, is set to a vector of zeros.

    Returns:
        [n_samples, n_dims] numpy array of samples.
    """
    if start is None and n_dims is None:
        n_dims = 1
        start = np.zeros(n_dims)
    elif start is None:
        start = np.zeros(n_dims)
    elif n_dims is None:
        n_dims = len(start)
    else:
        if len(start) != n_dims:
            raise ValueError('Error - start vector must be of length {}'.format(n_dims))
    posn = np.array(start)
    samples = np.zeros((n_samples, n_dims))
    eold = (posn * posn).sum() * 0.5
    for i in range(n_samples * interval):
        dp = np.random.random(n_dims) * 2.0 - 1.0
        dp = dp / np.linalg.norm(dp)
        posn = posn + dp
        enew = (posn * posn).sum() * 0.5
        de = enew - eold
        if np.exp(-de) > np.random.random():
            eold = enew
        else:
            posn = posn - dp
        if i % interval == 0:
            j = i // interval
            samples[j] = posn
    return samples
