import numpy as np
def outlier(data, dvar, pvar, mvar, method="SD", criteria=3.5):
    """
    Identifies and drops outliers within a single-case data frame (scdf).
    """
    if method == "SD":
        mean = data[dvar].mean()
        std_dev = data[dvar].std()
        lower_bound = mean - (criteria * std_dev)
        upper_bound = mean + (criteria * std_dev)
        outliers = data[(data[dvar] < lower_bound) | (data[dvar] > upper_bound)]
        
    elif method == "MAD":
        mad = np.median(np.abs(data[dvar] - np.median(data[dvar])))
        lower_bound = np.median(data[dvar]) - (criteria * mad)
        upper_bound = np.median(data[dvar]) + (criteria * mad)
        outliers = data[(data[dvar] < lower_bound) | (data[dvar] > upper_bound)]
        
    elif method == "CI":
        confidence_interval = 1.96  # Assuming a 95% confidence interval
        mean = data[dvar].mean()
        std_dev = data[dvar].std()  # Ensure std_dev is defined for CI
        std_error = std_dev / np.sqrt(len(data))
        lower_bound = mean - (confidence_interval * std_error)
        upper_bound = mean + (confidence_interval * std_error)
        outliers = data[(data[dvar] < lower_bound) | (data[dvar] > upper_bound)]
        
    elif method == "Cook":
        import statsmodels.api as sm
        model = sm.OLS(data[dvar], sm.add_constant(data[mvar])).fit()
        influence = model.get_influence()
        cook_d = influence.cooks_distance[0]
        threshold = 4 / len(data) if criteria == "4/n" else criteria
        outliers = data[cook_d > threshold]

    else:
        raise ValueError("Method not recognized. Choose from 'MAD', 'Cook', 'SD', 'CI'.")
    
    # Create a report of the outliers and drop them from the original data
    dropped_n = len(outliers)
    dropped_mt = outliers[mvar].tolist()
    
    cleaned_data = data.drop(outliers.index)

    return cleaned_data, dropped_n, dropped_mt
