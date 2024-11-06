# circlus_py

`circlus_py` is a Python wrapper for the [**circlus**](https://cran.r-project.org/package=circlus) R package, providing access to circular mixture models implemented in R. The `circlus` package offers flexible mixture modeling for circular data, supporting custom-defined distributions, which is valuable for analyzing angular or periodic data.

This Python package allows you to utilize `circlus` models and sampling functions directly from Python, streamlining workflows for those familiar with Python while leveraging the statistical power of R.

## Features

The `circlus_py` package includes the following model functions:

- **FLXMCpkbd**: A mixture model using the Poisson Kernel-Based Distribution (PKBD).
- **FLXMCspcauchy**: A mixture model using the spherical Cauchy distribution.

Additionally, it includes sampling functions:

- **rspcauchy**: Generates samples from the spherical Cauchy distribution.
- **rpkbd**: Generates samples from the Poisson Kernel-Based Distribution.

## Requirements

### 1. R Installation

To use `circlus_py`, you need to have **R installed** on your system, as this package relies on `rpy2` to interface with R. You can download and install R from [CRAN](https://cran.r-project.org/).

- **Linux**: Install R using your package manager (e.g., `sudo apt install r-base` on Ubuntu).
- **macOS**: Install R via [Homebrew](https://brew.sh) with `brew install r`.
- **Windows**: Download and install R from [CRAN](https://cran.r-project.org/).

### 2. R Packages

In addition to R, you will need the `circlus` and `flexmix` R packages installed. To install these packages, open R and run:

```R
install.packages("flexmix")
install.packages("circlus")
```

### 3. Python Dependencies

The `circlus_py` package requires the following Python packages:
- **rpy2**: For interfacing Python with R.
- **numpy**: For handling data in Python.

You can install these dependencies by running:

```bash
pip install -r requirements.txt
```


This will install the `circlus_py` wrapper package, enabling you to use the `circlus` R package models and sampling functions from Python.

## Usage

### Model Functions

The four main model functions (`FLXMCpkbd`, `FLXMCspcauchy`, `FLXMRpkbd`, and `FLXMRspcauchy`) can be used to fit circular mixture and regression models. Each function requires the following parameters:

- **`Y`**: 2D array where each row is a normalized vector.
- **`K`**: An integer specifying the number of clusters (default is `K=2`).


### Sampling Functions

The `circlus_py` package also includes functions to generate samples from two circular distributions:

- **rspcauchy**: Generates samples from the spherical Cauchy distribution.
  - **Parameters**: `n` (number of samples), `rho` (concentration parameter), and `mu` (mean direction, a vector).
  
- **rpkbd**: Generates samples from the Poisson Kernel-Based Distribution (PKBD).
  - **Parameters**: `n` (number of samples), `rho` (concentration parameter), `mu` (mean direction), and `method` (sampling method, default `"ACG"`).

### Example:

```python
import numpy as np
from circlus import FLXMCpkbd, FLXMCspcauchy, rspcauchy, rpkbd

# Parameters for generating samples
n_samples = 100
rho = 0.5
mu_pkbd = [0, 1]
mu_cauchy = [1, 0]

# Generate samples from the PKBD distribution
pkbd_samples = np.array(rpkbd(n=n_samples, rho=rho, mu=mu_pkbd))
print("Generated PKBD samples:\n", pkbd_samples)

# Generate samples from the spherical Cauchy distribution
cauchy_samples = np.array(rspcauchy(n=n_samples, rho=rho, mu=mu_cauchy))
print("Generated Spherical Cauchy samples:\n", cauchy_samples)

# Cluster the PKBD samples using FLXMCpkbd
result_pkbd = FLXMCpkbd(Y=pkbd_samples, K=2)
posterior = result_pkbd.do_slot("posterior")
posterior_scaled = posterior.rx2("scaled")
posterior_np = np.array(posterior_scaled)
print("Posterior Probabilities (Cluster Allocations):\n", posterior_np)

result_spcauchy = FLXMCspcauchy(Y=cauchy_samples, K=2)
posterior = result_spcauchy.do_slot("posterior")
posterior_scaled = posterior.rx2("scaled")
posterior_np = np.array(posterior_scaled)
print("Posterior Probabilities (Cluster Allocations):\n", posterior_np)
```

## About the `circlus` R Package

The [**circlus**](https://cran.r-project.org/package=circlus) package provides flexible mixture models for circular data. It includes methods for clustering and density estimation on circular data, which are particularly useful in fields such as biology, meteorology, and geology, where angular or periodic measurements are common. The package integrates smoothly with `flexmix`, an R framework for finite mixture modeling.

The `circlus` package includes models based on Poisson Kernel-Based Distributions (PKBD) and spherical Cauchy distributions, as well as random number generators for these distributions.

For more details, see the [CRAN page for circlus](https://cran.r-project.org/package=circlus).

## Troubleshooting

If you encounter any issues, here are some common problems and solutions:

1. **R is Not Installed**: Ensure that R is installed on your system and accessible in your system’s PATH.
2. **Missing R Packages**: If you see errors related to missing R packages, install `flexmix` and `circlus` in R:
   ```R
   install.packages("flexmix")
   install.packages("circlus")
   ```

3. **Version Conflicts**: Ensure that you have compatible versions of `rpy2`, `pandas`, and `R`.

## License

This Python wrapper, `circlus_py`, is distributed under the GPL-3 License.

---

This README provides a comprehensive overview, installation instructions, usage examples, and troubleshooting tips for `circlus_py`, making it easy for users to understand the package’s functionality and requirements.
