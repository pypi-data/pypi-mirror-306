import pandas as pd
import numpy as np
from .nap import nap

def ird(data, dvar='values', pvar='phase', decreasing=False, phases=('A', 'B')):
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

        # Calculate NAP using the nap function
        nap_result = nap(case_data, dvar=dvar, pvar=pvar, decreasing=decreasing, phases=phases)
        nap_value = nap_result['NAP'].iloc[0]  # Extract NAP value

        n_a = len(phase_A_data)
        n_b = len(phase_B_data)

        # Calculate IRD
        if n_a > 0 and n_b > 0:
            ir_rate = nap_result['NAP'].iloc[0]  # NAP is already a percentage
            print(f"nap result is: {nap_result['NAP'].iloc[0]}")
            ird_value = 1 - ((n_a**2 / (2 * n_a * n_b)) * (2 - ir_rate))
        else:
            ird_value = np.nan

        results.append({
            'Case': case,
            'IRD': ird_value/100
        })

    results_df = pd.DataFrame(results)
    return results_df