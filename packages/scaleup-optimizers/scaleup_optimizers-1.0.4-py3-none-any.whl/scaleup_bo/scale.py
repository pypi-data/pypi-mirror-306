import numpy as np
from skopt.space import Real, Integer, Categorical

class Scale:
    def __init__(self, search_space):
        self.search_space = search_space

    def normalize(self, X):
        """
        Normalize parameters to scale [0,1]

        Parameters
        ----------
        X : numpy.ndarray
            The input array containing parameter values to be normalized. Each row corresponds
            to a parameter configuration, and each column corresponds to a parameter.

        Returns
        -------
        X_norm : numpy.ndarray
            The normalized array where the parameter values are scaled between [0, 1].

        """
        X_norm = []
        for i, dim in enumerate(self.search_space):
            if isinstance(dim, (Real, Integer)):
                if np.any(X[:, i].astype(float) < dim.low) or np.any(X[:, i].astype(float) > dim.high):
                    raise ValueError(f"Value out of bounds for parameter {i}: {X[:, i]}. Must be in range [{dim.low}, {dim.high}]")
                if isinstance(dim, Real) and dim.prior == 'log-uniform':
                    X_norm.append((np.log10(X[:, i].astype(float)) - np.log10(dim.low)) / (np.log10(dim.high) - np.log10(dim.low)))
                else:
                    X_norm.append((X[:, i].astype(float) - dim.low) / (dim.high - dim.low))
            elif isinstance(dim, Categorical):
                cat_indices = []
                for x in X[:, i]:
                    if x not in dim.categories:
                        raise ValueError(f"Invalid categorical value '{x}' found in parameter {i}: {X[:, i]}")
                    cat_indices.append(dim.categories.index(x) / (len(dim.categories) - 1))
                X_norm.append(cat_indices)
        return np.array(X_norm).T

    def denormalize(self, X_norm):
        """
        Denormalize parameters back to the original scale


        Parameters
        ----------
        X_norm : numpy.ndarray
            The input array containing normalized parameter values. Each row corresponds to
            a normalized parameter configuration, and each column corresponds to a parameter.
            
        Returns
        -------
        X : numpy.ndarray
            The denormalized array where the parameter values are rescaled to their original bounds.

        """
        X = []
        for i, dim in enumerate(self.search_space):
            if isinstance(dim, Real):
                if dim.prior == 'log-uniform':
                    X_denorm = 10.0 ** (X_norm[:, i] * (np.log10(dim.high) - np.log10(dim.low)) + np.log10(dim.low))
                else:
                    X_denorm = (X_norm[:, i] * (dim.high - dim.low) + dim.low)
                X.append(np.round(np.clip(X_denorm, dim.low, dim.high), decimals=10))

            elif isinstance(dim, Integer):
                X_denorm = np.round(X_norm[:, i] * (dim.high - dim.low) + dim.low).astype(int)
                X.append(np.clip(X_denorm, dim.low, dim.high))

            elif isinstance(dim, Categorical):
                X.append([dim.categories[(int(np.round(x * (len(dim.categories) - 1))))] for x in X_norm[:, i]])

        return np.array(X, dtype=object).T
