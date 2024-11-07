import pandas as pd
import numpy as np
from scipy.stats import wilcoxon, mannwhitneyu

def nap(data, dvar='values', pvar='phase', decreasing=False, phases=('A', 'B')):
    """
    Computes the Nonoverlap of All Pairs (NAP) for each case across specified phases.

    Parameters:
    - data (DataFrame or SingleCaseData): Single-case or multiple-case data frame containing cases, values, phases, etc.
    - dvar (str): Column name for dependent variable (default: 'values').
    - pvar (str): Column name for phases (default: 'phase').
    - decreasing (bool): Whether a decrease in values is expected (default: False).
    - phases (tuple): Phases to compare (default: ('A', 'B')).

    Returns:
    - DataFrame: A DataFrame containing NAP metrics for each case.
    """
    # Check if the data is a SingleCaseData instance and use its DataFrame
    if hasattr(data, 'df'):
        data = data.df
    
    is_multi_case = 'case' in data.columns
    cases = data['case'].unique() if is_multi_case else ['Single Case']
    results = []

    for case in cases:
        case_data = data if not is_multi_case else data[data['case'] == case]
        phase_A_data = case_data[case_data[pvar] == phases[0]][dvar].dropna()
        phase_B_data = case_data[case_data[pvar] == phases[1]][dvar].dropna()

        if phase_A_data.empty or phase_B_data.empty:
            continue

        # Total possible pairs
        pairs = len(phase_A_data) * len(phase_B_data)

        # Compute non-overlap pairs
        if not decreasing:
            positives = sum(b > a for a in phase_A_data for b in phase_B_data)
            ties = sum(b == a for a in phase_A_data for b in phase_B_data)
        else:
            positives = sum(b < a for a in phase_A_data for b in phase_B_data)
            ties = sum(b == a for a in phase_A_data for b in phase_B_data)

        non_overlaps = positives + (0.5 * ties)
        nap_value = (non_overlaps / pairs) * 100
        nap_rescaled = (2 * nap_value) - 100

        # Perform the statistical test
        if len(phase_A_data) == len(phase_B_data):
            # If lengths are equal, use Wilcoxon test
            try:
                w, p_value = wilcoxon(phase_A_data, phase_B_data, alternative='less' if not decreasing else 'greater')
            except ValueError:
                w, p_value = np.nan, np.nan
        else:
            # Use Mann-Whitney U test for unequal lengths
            u_stat, p_value = mannwhitneyu(phase_A_data, phase_B_data, alternative='less' if not decreasing else 'greater')
            w = u_stat  # Assign U statistic as w for consistency

        # Effect size calculations
        d = 3.464 * (1 - np.sqrt((1 - nap_value / 100) / 0.5))
        r_squared = d**2 / (d**2 + 4)

        # Collect results
        results.append({
            'Case': case,
            'NAP': nap_value,
            'NAP Rescaled': nap_rescaled,
            'Pairs': pairs,
            'Non-overlaps': non_overlaps,
            'Positives': positives,
            'Ties': ties,
            'w': w if not np.isnan(w) else 0,  # Replace NaN with 0 for display
            'p': p_value,  # Display the actual p-value
            'd': round(d, 2),
            'R²': round(r_squared, 2)
        })

    results_df = pd.DataFrame(results)
    return results_df
