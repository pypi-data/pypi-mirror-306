# models.py
import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects import Formula
import numpy as np

# Import the required R packages
circlus = importr("circlus")
flexmix = importr("flexmix")

def FLXMCpkbd(Y, K=2):
    """Fits a mixture model using the Poisson Kernel-Based Distribution (PKBD).
    
    Parameters:
    - Y: 2D array where each row is a normalized vector (data on the sphere), stored as a matrix in R.
    - K: Number of clusters.
    
    Returns:
    - Result of the flexmix model fit.
    """
    Y = np.array(Y)
    ro.globalenv['y'] = ro.r.matrix(Y, nrow=Y.shape[0], ncol=Y.shape[1])

    # Define the formula for intercept-only model
    formula_r = Formula("y ~ 1")
    
    return flexmix.flexmix(formula_r, k=K, model=circlus.FLXMCpkbd())

def FLXMCspcauchy(Y, K=2):
    """Fits a mixture model using the spherical Cauchy distribution.
    
    Parameters:
    - Y: 2D array where each row is a normalized vector (data on the sphere), stored as a matrix in R.
    - K: Number of clusters.
    
    Returns:
    - Result of the flexmix model fit.
    """
    Y = np.array(Y)
    ro.globalenv['y'] = ro.r.matrix(Y, nrow=Y.shape[0], ncol=Y.shape[1])

    formula_r = Formula("y ~ 1")
    
    return flexmix.flexmix(formula_r, k=K, model=circlus.FLXMCspcauchy())

