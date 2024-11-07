import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

def mad(x, center=None, constant=1.4826, na_rm=False, low=False, high=False):
    """Calculate the Median Absolute Deviation (MAD)."""
    if na_rm:
        x = x[~np.isnan(x)]
    if center is None:
        center = np.median(x)
    n = len(x)
    deviations = np.abs(x - center)
    if (low or high) and n % 2 == 0:
        if low and high:
            raise ValueError("'low' and 'high' cannot be both True")
        n2 = n // 2 + int(high)
        return constant * np.partition(deviations, n2)[n2]
    return constant * np.median(deviations)


def trend(time_data, values_data):
    """
    Calculate the trend (slope) of the values data over time using linear regression.

    Parameters:
    - time_data: Series or list of time measurements
    - values_data: Series or list of observed values corresponding to the time measurements

    Returns:
    - The slope of the trend line, representing the rate of change over time.
    """
    if len(time_data) < 2:
        return np.nan  # Trend calculation requires at least two points

    # Reshape time data for linear regression
    time_data = np.array(time_data).reshape(-1, 1)
    values_data = np.array(values_data)

    model = LinearRegression().fit(time_data, values_data)
    return model.coef_[0]  # Return the slope of the fitted line

