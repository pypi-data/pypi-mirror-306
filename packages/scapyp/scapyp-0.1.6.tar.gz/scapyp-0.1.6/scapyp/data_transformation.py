# data_transformations.py

import pandas as pd
import numpy as np
from statsmodels.nonparametric.smoothers_lowess import lowess

def moving_median(x, lag=1):
    """Calculate the moving median."""
    return x.rolling(window=lag*2 + 1, min_periods=1, center=True).median()

def moving_mean(x, lag=1):
    """Calculate the moving mean."""
    return x.rolling(window=lag*2 + 1, min_periods=1, center=True).mean()

def local_regression(x, mt=None, f=0.2):
    """Perform local regression on the data."""
    if mt is None:
        mt = np.arange(len(x))
    return lowess(x, mt, frac=f)[:, 1]

def transform_single_case(single_case, **kwargs):
    """Transform a SingleCaseData instance by applying functions."""
    for name, func in kwargs.items():
        single_case.df[name] = func(single_case.df)
