# data_processing.py

import pandas as pd
import numpy as np

def fill_missing(data, dvar, mvar, na_rm=True):
    """
    Replaces missing measurements in a single-case data DataFrame.

    Parameters:
    - data: A DataFrame representing single-case data.
    - dvar: Name of the dependent variable (column).
    - mvar: Name of the measurement time variable (column).
    - na_rm: If set to True, NA values will be interpolated (default is True).

    Returns:
    - A DataFrame with missing data points filled.
    """
    # Ensure the data is sorted by measurement time
    data = data.sort_values(by=mvar)

    # Interpolating missing values if na_rm is True
    if na_rm:
        data[dvar] = data[dvar].interpolate(method='linear')

    return data
