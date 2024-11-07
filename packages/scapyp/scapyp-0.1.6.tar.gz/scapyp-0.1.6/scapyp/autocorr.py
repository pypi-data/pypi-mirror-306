# autocorrelation.py
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import acf

def autocorr(data, dvar, pvar, mvar, lag_max=3, **kwargs):
    """
    Calculate autocorrelations within each phase and across all phases.

    Parameters:
    data (DataFrame): A single-case data frame.
    dvar (str): Name of the dependent variable.
    pvar (str): Name of the phase variable.
    mvar (str): Name of the measurement-time variable.
    lag_max (int): The maximum lag to compute autocorrelations.

    Returns:
    DataFrame: A DataFrame containing separate autocorrelations for each phase and for all phases.
    """
    case_names = data['case'].unique()  # Assuming 'case' is a column in the DataFrame
    var_lag = [f"Lag {i}" for i in range(1, lag_max + 1)]
    ac_results = []

    for case in case_names:
        case_data = data[data['case'] == case]
        phases = case_data[pvar].unique()
        df = pd.DataFrame(index=phases.tolist() + ['all'], columns=var_lag)

        for phase in phases:
            y = case_data[case_data[pvar] == phase][dvar].dropna().values
            if len(y) < 2:  # If not enough data points, skip
                continue
            acf_values = acf(y, nlags=lag_max, **kwargs)[1:lag_max + 1]  # Skip the 0 lag
            df.loc[phase, var_lag[:len(acf_values)]] = acf_values

        # Calculate autocorrelation for all phases
        all_y = case_data[dvar].dropna().values
        if len(all_y) >= 2:
            all_acf_values = acf(all_y, nlags=lag_max, **kwargs)[1:lag_max + 1]
            df.loc['all', var_lag[:len(all_acf_values)]] = all_acf_values

        ac_results.append(df)

    # Concatenate results into a single DataFrame
    result_df = pd.concat(ac_results, keys=case_names)
    return result_df