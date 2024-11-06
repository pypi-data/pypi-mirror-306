from setuptools import setup, find_packages

setup(
    name="circlus_py",
    version="0.1.0",
    description="Python wrapper for the circlus R package",
    author="Lukas Sablica",
    packages=find_packages(),
    install_requires=[
        "rpy2",  # Required to interface with R
        "numpy",  
    ],
    python_requires='>=3.6',
)
