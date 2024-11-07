import pandas as pd
import numpy as np
from scipy.stats import binom_test
from sklearn.linear_model import LinearRegression

def calculate_trend(single_case_data, dvar, mvar, method="OLS"):
    # Access the internal DataFrame
    data = single_case_data.df
    
    if method == "OLS":
        # Ordinary Least Squares
        model = LinearRegression()
        model.fit(data[[mvar]], data[dvar])
        return model

    elif method == "bisplit":
        # Bisplit Method
        mid = len(data) // 2
        first_half = data.iloc[:mid]
        second_half = data.iloc[mid:]
        x_medians = [first_half[mvar].median(), second_half[mvar].median()]
        y_medians = [first_half[dvar].median(), second_half[dvar].median()]
        
        bisplit_df = pd.DataFrame({mvar: x_medians, dvar: y_medians})
        model = LinearRegression()
        model.fit(bisplit_df[[mvar]], bisplit_df[dvar])
        return model

    elif method == "trisplit":
        # Trisplit Method
        third = len(data) // 3
        first_part = data.iloc[:third]
        last_part = data.iloc[-third:]
        
        x_medians = [first_part[mvar].median(), last_part[mvar].median()]
        y_medians = [first_part[dvar].median(), last_part[dvar].median()]
        
        trisplit_df = pd.DataFrame({mvar: x_medians, dvar: y_medians})
        model = LinearRegression()
        model.fit(trisplit_df[[mvar]], trisplit_df[dvar])
        return model

    else:
        raise ValueError("Invalid trend method specified. Choose 'OLS', 'bisplit', or 'trisplit'.")

def cdc(single_case_data, dvar="values", pvar="phase", mvar="mt", method="OLS", 
        conservative=0.25, decreasing=False):
    """
    CDC function for change detection using bisplit, trisplit, or OLS methods.
    
    Parameters:
    - single_case_data: SingleCaseData object containing single-case data.
    - dvar: Dependent variable column name.
    - pvar: Phase variable column name.
    - mvar: Measurement time variable column name.
    - method: Trend estimation method, one of 'OLS', 'bisplit', 'trisplit'.
    - conservative: Conservative threshold for change detection.
    - decreasing: Direction of change to detect (increasing or decreasing).
    
    Returns:
    - dict with CDC results, p-values, and systematic change status.
    """
    # Access the internal DataFrame
    data = single_case_data.df
    
    # Split data into phases A and B
    phase_A = data[data[pvar] == "A"]
    phase_B = data[data[pvar] == "B"]
    
    # Validate data length in each phase for trend estimation
    if len(phase_A) < 5 or len(phase_B) < 5:
        raise ValueError("Each phase must contain at least 5 data points for selected method.")

    # Fit trend model on phase A data
    trend_model = calculate_trend(single_case_data, dvar, mvar, method)
    
    # Predict values in phase B based on phase A trend
    phase_B_pred = trend_model.predict(phase_B[[mvar]])
    
    # CDC criteria: apply conservative threshold based on phase A data
    sd_A = phase_A[dvar].std()
    mean_A = phase_A[dvar].mean()
    cdc_exc = 0  # Counter for phase B values exceeding the threshold

    if not decreasing:
        # Look for systematic increase
        for i, actual in enumerate(phase_B[dvar]):
            pred = phase_B_pred[i]
            if actual > pred + (conservative * sd_A) and actual > mean_A + (conservative * sd_A):
                cdc_exc += 1
    else:
        # Look for systematic decrease
        for i, actual in enumerate(phase_B[dvar]):
            pred = phase_B_pred[i]
            if actual < pred - (conservative * sd_A) and actual < mean_A - (conservative * sd_A):
                cdc_exc += 1
    
    # Perform binomial test on the exceedances in phase B
    p_value = binom_test(cdc_exc, len(phase_B), alternative="greater")
    systematic_change = "systematic change" if p_value < 0.05 else "no change"
    
    # Summarize results in a structured, readable format
    results_text = f"""
    Change Detection Criteria (CDC) Analysis
    ----------------------------------------
    Method: {method}
    Conservative Threshold: {conservative}
    Direction of Change: {"Decreasing" if decreasing else "Increasing"}
    
    Phase B Exceedances: {cdc_exc} out of {len(phase_B)}
    CDC P-Value: {p_value:.4f}
    Result: {systematic_change}
    """
    
    return results_text



# import pandas as pd
# import numpy as np
# from scipy.stats import binom_test
# from sklearn.linear_model import LinearRegression

# def calculate_trend(data, dvar, mvar, method="OLS"):
#     if method == "OLS":
#         # Ordinary Least Squares
#         model = LinearRegression()
#         model.fit(data[[mvar]], data[dvar])
#         return model

#     elif method == "bisplit":
#         # Bisplit Method
#         mid = len(data) // 2
#         first_half = data.iloc[:mid]
#         second_half = data.iloc[mid:]
#         x_medians = [first_half[mvar].median(), second_half[mvar].median()]
#         y_medians = [first_half[dvar].median(), second_half[dvar].median()]
        
#         bisplit_df = pd.DataFrame({mvar: x_medians, dvar: y_medians})
#         model = LinearRegression()
#         model.fit(bisplit_df[[mvar]], bisplit_df[dvar])
#         return model

#     elif method == "trisplit":
#         # Trisplit Method
#         third = len(data) // 3
#         first_part = data.iloc[:third]
#         last_part = data.iloc[-third:]
        
#         x_medians = [first_part[mvar].median(), last_part[mvar].median()]
#         y_medians = [first_part[dvar].median(), last_part[dvar].median()]
        
#         trisplit_df = pd.DataFrame({mvar: x_medians, dvar: y_medians})
#         model = LinearRegression()
#         model.fit(trisplit_df[[mvar]], trisplit_df[dvar])
#         return model

#     else:
#         raise ValueError("Invalid trend method specified. Choose 'OLS', 'bisplit', or 'trisplit'.")

# def cdc(data, dvar="values", pvar="phase", mvar="mt", method="OLS", 
#         conservative=0.25, decreasing=False):
#     """
#     CDC function for change detection using bisplit, trisplit, or OLS methods.
    
#     Parameters:
#     - data: DataFrame containing single-case data.
#     - dvar: Dependent variable column name.
#     - pvar: Phase variable column name.
#     - mvar: Measurement time variable column name.
#     - method: Trend estimation method, one of 'OLS', 'bisplit', 'trisplit'.
#     - conservative: Conservative threshold for change detection.
#     - decreasing: Direction of change to detect (increasing or decreasing).
    
#     Returns:
#     - dict with CDC results, p-values, and systematic change status.
#     """
#     # Split data into phases A and B
#     phase_A = data[data[pvar] == "A"]
#     phase_B = data[data[pvar] == "B"]
    
#     # Validate data length in each phase for trend estimation
#     if len(phase_A) < 5 or len(phase_B) < 5:
#         raise ValueError("Each phase must contain at least 5 data points for selected method.")

#     # Fit trend model on phase A data
#     trend_model = calculate_trend(phase_A, dvar, mvar, method)
    
#     # Predict values in phase B based on phase A trend
#     phase_B_pred = trend_model.predict(phase_B[[mvar]])
    
#     # CDC criteria: apply conservative threshold based on phase A data
#     sd_A = phase_A[dvar].std()
#     mean_A = phase_A[dvar].mean()
#     cdc_exc = 0  # Counter for phase B values exceeding the threshold

#     if not decreasing:
#         # Look for systematic increase
#         for i, actual in enumerate(phase_B[dvar]):
#             pred = phase_B_pred[i]
#             if actual > pred + (conservative * sd_A) and actual > mean_A + (conservative * sd_A):
#                 cdc_exc += 1
#     else:
#         # Look for systematic decrease
#         for i, actual in enumerate(phase_B[dvar]):
#             pred = phase_B_pred[i]
#             if actual < pred - (conservative * sd_A) and actual < mean_A - (conservative * sd_A):
#                 cdc_exc += 1
    
#     # Perform binomial test on the exceedances in phase B
#     p_value = binom_test(cdc_exc, len(phase_B), alternative="greater")
#     systematic_change = "systematic change" if p_value < 0.05 else "no change"
    
#     # Summarize results
#     results = {
#         "cdc": systematic_change,
#         "cdc_exceedances": cdc_exc,
#         "cdc_p_value": p_value,
#         "phase_B_count": len(phase_B),
#         "method": method,
#         "conservative_threshold": conservative,
#         "decreasing": decreasing
#     }
    
#     return results
