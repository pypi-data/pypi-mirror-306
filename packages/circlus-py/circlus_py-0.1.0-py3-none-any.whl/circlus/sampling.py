# sampling.py
import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import FloatVector
import numpy as np
from rpy2.robjects import numpy2ri
numpy2ri.activate()

# Import circlus package
circlus = importr("circlus")

def rspcauchy(n, rho, mu):
    """Generates samples from the spherical Cauchy distribution.
    
    Parameters:
    - n: Number of samples.
    - rho: Concentration parameter.
    - mu: Mean direction, a vector (e.g., [0, 0]).
    
    Returns:
    - A NumPy array of samples with `n` rows.
    """
    # Ensure `mu` is passed as an R-compatible vector
    mu_r = FloatVector(mu)
    samples = circlus.rspcauchy(n, rho=rho, mu=mu_r)
    return np.array(samples).reshape((n, -1))

def rpkbd(n, rho, mu, method="ACG"):
    """Generates samples from the Poisson Kernel-Based Distribution (PKBD).
    
    Parameters:
    - n: Number of samples.
    - rho: Concentration parameter.
    - mu: Mean direction, a vector (e.g., [0, 0]).
    - method: Sampling method, default is "ACG".
    
    Returns:
    - A NumPy array of samples with `n` rows.
    """
    # Ensure `mu` is passed as an R-compatible vector
    mu_r = FloatVector(mu)
    samples = circlus.rpkbd(n, rho=rho, mu=mu_r, method=method)
    return np.array(samples).reshape((n, -1))
