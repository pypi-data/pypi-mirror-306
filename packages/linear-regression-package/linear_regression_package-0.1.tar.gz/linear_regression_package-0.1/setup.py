
from setuptools import setup, find_packages

setup(
    name='linear_regression_package',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'matplotlib',
        'scikit-learn'
    ],
    description='A simple linear regression model package with gradient descent',
    author='Boukrara_Melissa',
    author_email='m.boukrara@esi-sba.dz'
)
