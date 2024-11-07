import pandas as pd
import numpy as np
from scipy.stats import norm
from .singlecasedf import SingleCaseData

def overlap(data, dvar='values', pvar='phase', mvar='mt', decreasing=False, phases=('A', 'B')):
    """
    Computes overlap indices comparing two phases for each case in single or multiple-case data.

    Parameters:
    - data (SingleCaseData or DataFrame): Single-case data in `SingleCaseData` format or as a DataFrame.
    - dvar (str): Column name for dependent variable (default: 'values').
    - pvar (str): Column name for phases (default: 'phase').
    - mvar (str): Column name for measurement time (default: 'mt').
    - decreasing (bool): Whether a decrease in values is expected (default: False).
    - phases (tuple): Phases to compare, typically (phase1, phase2).

    Returns:
    - DataFrame: Overlap indices for each case.
    """
    # Check if the input is a SingleCaseData instance
    if isinstance(data, SingleCaseData):
        # Extract DataFrame and add case name if missing
        df = data.df.copy()
        if 'case' not in df.columns:
            df['case'] = data.name if data.name else 'Unnamed Case'
    else:
        # Assume data is already a DataFrame
        df = data

    # Proceed with overlap calculation
    case_names = df['case'].unique()
    results = []

    # Loop through each case
    for case in case_names:
        case_data = df[df['case'] == case]

        # Define phases for comparison
        phase_1_data = case_data[case_data[pvar] == phases[0]][dvar].dropna()
        phase_2_data = case_data[case_data[pvar] == phases[1]][dvar].dropna()

        # Check if data is available in both phases
        if phase_1_data.empty or phase_2_data.empty:
            continue  # Skip this case if one of the phases has no data

        # Basic overlap calculations
        pnd = np.mean(phase_2_data > phase_1_data.max()) * 100 if not decreasing else np.mean(phase_2_data < phase_1_data.min()) * 100
        pem = np.mean(phase_2_data >= np.median(phase_1_data)) * 100 if not decreasing else np.mean(phase_2_data <= np.median(phase_1_data)) * 100
        pet = np.mean(phase_2_data > phase_1_data.quantile(0.75)) * 100 if not decreasing else np.mean(phase_2_data < phase_1_data.quantile(0.25)) * 100
        nap = (norm.cdf((phase_2_data.mean() - phase_1_data.mean()) / np.sqrt((phase_1_data.var() + phase_2_data.var()) / 2)) * 2 - 1) * 100
        nap_rescaled = nap / 2  # Rescaling NAP
        pand = np.mean(phase_2_data >= np.percentile(phase_1_data, 95)) * 100

        # Other indices (diff mean, trend, etc.)
        diff_mean = phase_2_data.mean() - phase_1_data.mean()
        diff_trend = np.polyfit(range(len(phase_2_data)), phase_2_data, 1)[0] - np.polyfit(range(len(phase_1_data)), phase_1_data, 1)[0]
        smd = (phase_2_data.mean() - phase_1_data.mean()) / phase_1_data.std()
        hedges_g = smd * (1 - (3 / (4 * (len(phase_1_data) + len(phase_2_data)) - 9)))

        # Compile results
        results.append({
            'Case': case,
            'Design': f"{phases[0]}-{phases[1]}",
            'PND': pnd,
            'PEM': pem,
            'PET': pet,
            'NAP': nap,
            'NAP rescaled': nap_rescaled,
            'PAND': pand,
            'Diff_mean': diff_mean,
            'Diff_trend': diff_trend,
            'SMD': smd,
            'Hedges_g': hedges_g
        })

    # Convert to DataFrame for easy viewing
    results_df = pd.DataFrame(results)
    return results_df
