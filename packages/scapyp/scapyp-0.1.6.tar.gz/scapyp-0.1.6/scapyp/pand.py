import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency, fisher_exact
import itertools

def pand(data, dvar='values', pvar='phase', decreasing=False, phases=('A', 'B'), method='sort', complex_phases=(['A1', 'A2'], ['B1', 'B2'])):
    # Check if the data is a SingleCaseData instance and use its DataFrame
    if hasattr(data, 'df'):
        data = data.df
    
    unique_phases = data[pvar].unique()
    is_simple = all(phase in unique_phases for phase in phases)

    # Check for the 'case' column
    if 'case' in data.columns:
        cases = data['case'].unique()
    else:
        cases = ['Single Case']  # Treat as single case if 'case' column is missing

    results = []

    for case in cases:
        case_data = data[data['case'] == case] if 'case' in data.columns else data

        if is_simple:
            phase_a_data = case_data[case_data[pvar] == phases[0]][dvar]
            phase_b_data = case_data[case_data[pvar] == phases[1]][dvar]
            phase_a_label, phase_b_label = phases
        else:
            phase_a_data = case_data[case_data[pvar].isin(complex_phases[0])][dvar]
            phase_b_data = case_data[case_data[pvar].isin(complex_phases[1])][dvar]
            phase_a_label = "-".join(complex_phases[0])
            phase_b_label = "-".join(complex_phases[1])

        n_a = len(phase_a_data)
        n_b = len(phase_b_data)
        n_total = n_a + n_b

        if method == 'sort':
            all_data = case_data[[dvar, pvar]].copy()
            if decreasing:
                all_data[dvar] = -all_data[dvar]
            sorted_data = all_data.sort_values(by=[dvar, pvar], ascending=True)
            phase_order = sorted_data[pvar].values
            phase_original = case_data[pvar].values

            mat_counts = pd.crosstab(phase_original, phase_order)
            mat_counts = mat_counts.reindex(index=unique_phases, columns=unique_phases, fill_value=0)
            mat_proportions = mat_counts / n_total * 100

            pand_value = (mat_proportions.values[0, 0] + mat_proportions.values[1, 1])
            overlaps = mat_counts.values[0, 1] + mat_counts.values[1, 0]
            perc_overlap = (overlaps / n_total) * 100

            chi_test = chi2_contingency(mat_counts, correction=False)
            phi = np.sqrt(chi_test[0] / n_total)

            fisher_result = None
            if mat_counts.shape == (2, 2):
                fisher_result = fisher_exact(mat_counts.values)

            # Print the results in the desired format
            print("Percentage of all non-overlapping data\n")
            print(f"Method: {method}\n")
            print(f"PAND = {pand_value:.1f}%")
            print(f"Φ = {phi:.3f} ; Φ² = {phi**2:.3f}\n")
            print(f"{n_total} measurements ({n_a} Phase {phase_a_label}, {n_b} Phase {phase_b_label}) in {len(cases)} cases")
            print(f"Overlapping data: n = {overlaps} ; percentage = {perc_overlap:.1f}\n")
            print("2 x 2 Matrix of percentages")
            print(mat_proportions.round(1).to_string(header=True, index=True))
            print("\n2 x 2 Matrix of counts")
            print(mat_counts.to_string(header=True, index=True))
            print("\nChi-Squared test:")
            print(f"X² = {chi_test[0]:.3f}, df = {chi_test[1]}, p = {chi_test[1]:.3f}\n")
            if fisher_result:
                print("Fisher exact test:")
                print(f"Odds ratio = {fisher_result[0]:.3f}, p = {fisher_result[1]:.3f}\n")

        elif method == 'minimum':
            def pand_minimum(values_a, values_b):
                if decreasing:
                    values_a = -1 * values_a
                    values_b = -1 * values_b
                n_a = len(values_a)
                n_b = len(values_b)
                x = [-float('inf')] + sorted(values_a)
                y = sorted(values_b) + [float('inf')]
                overlaps = max(i + j for i, j in itertools.product(range(n_a + 1), range(n_b + 1)) if x[i] < y[-j - 1])
                return overlaps

            overlaps = pand_minimum(phase_a_data, phase_b_data)
            nonoverlaps = n_total - overlaps
            pand_value = (nonoverlaps / n_total) * 100
            perc_overlap = 100 - pand_value

            # Print the results for the minimum method
            print("Percentage of all non-overlapping data\n")
            print(f"Method: {method}\n")
            print(f"PAND = {pand_value:.1f}%")
            print(f"{n_total} measurements ({n_a} Phase {phase_a_label}, {n_b} Phase {phase_b_label}) in {len(cases)} cases")
            print(f"Overlapping data: n = {overlaps} ; percentage = {perc_overlap:.1f}\n")
