import pandas as pd
import numpy as np
from statsmodels.formula.api import ols
from .singlecasedf import SingleCaseData  # Adjust this import based on your package structure

def trend(data, dvar='values', pvar='phase', mvar='mt', first_mt=0, model=None):
    """
    Provides trend analysis for single-case or multi-case data, calculating linear and quadratic trends across phases.
    
    Parameters:
    - data (DataFrame or SingleCaseData): Data containing cases, values, phases, etc.
    - dvar (str): Column name for dependent variable (default: 'values').
    - pvar (str): Column name for phases (default: 'phase').
    - mvar (str): Column name for measurement time (default: 'mt').
    - first_mt (int): Starting point for measurement time for each phase (default: 0).
    - model (dict): Custom regression models in the form {name: formula} (optional).

    Returns:
    - DataFrame: Trend analysis results for each phase and overall, including intercept, slope (B), and Beta for each case.
    """

    # Check if the data is a SingleCaseData instance and extract .df
    if isinstance(data, SingleCaseData):
        if 'case' not in data.df.columns:
            data.df['case'] = data.name if data.name else 'Unnamed Case'
        data = data.df  # Use the DataFrame within SingleCaseData

    # Ensure 'case' column exists, even for standard DataFrames
    if 'case' not in data.columns:
        data['case'] = 'Unnamed Case'

    # Define default formulas
    formulas = {
        'Linear': f"{dvar} ~ {mvar}",
        'Quadratic': f"{dvar} ~ I({mvar} ** 2)"
    }

    # Add custom models if provided
    if model:
        formulas.update(model)

    results = []

    # Loop through each unique case
    for case in data['case'].unique():
        case_data = data[data['case'] == case]
        
        for name, formula in formulas.items():
            # Overall trend across all phases
            all_data = case_data.copy()
            all_data[mvar] -= all_data[mvar].min() - first_mt  # Reset mt for all phases
            model_all = ols(formula, data=all_data).fit()
            results.append({
                'Case': case,
                'Phase': 'ALL',
                'Model': name,
                'Intercept': model_all.params.iloc[0],
                'B': model_all.params.iloc[1] if len(model_all.params) > 1 else np.nan,
                'Beta': model_all.params.iloc[1] / model_all.bse.iloc[1] if len(model_all.params) > 1 else np.nan
            })
            
            # Trends for each phase
            for phase in case_data[pvar].unique():
                phase_data = case_data[case_data[pvar] == phase].copy()
                phase_data[mvar] -= phase_data[mvar].min() - first_mt  # Reset mt per phase
                model_phase = ols(formula, data=phase_data).fit()
                results.append({
                    'Case': case,
                    'Phase': phase,
                    'Model': name,
                    'Intercept': model_phase.params.iloc[0],
                    'B': model_phase.params.iloc[1] if len(model_phase.params) > 1 else np.nan,
                    'Beta': model_phase.params.iloc[1] / model_phase.bse.iloc[1] if len(model_phase.params) > 1 else np.nan
                })

    # Convert results to DataFrame
    results_df = pd.DataFrame(results)
    return results_df
