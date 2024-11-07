import pandas as pd
from scipy.stats import kendalltau
from sklearn.linear_model import TheilSenRegressor
import numpy as np
from .singlecasedf import SingleCaseData

def kendall_full(x, y, tau_method="b", continuity_correction=True):
    if tau_method not in ["a", "b"]:
        raise ValueError("Unknown method specified. Use 'a' or 'b'.")
    
    tau, p_value = kendalltau(x, y, method="auto")
    if continuity_correction:
        n = len(x)
        p_value *= (1 - 1 / (2 * n))
    return {"tau": tau, "p": p_value}

def corrected_tau(single_case_data, phases=('A', 'B'), alpha=0.05, continuity=False, repeated=False, tau_method='b'):
    dvar = single_case_data.dvar
    pvar = single_case_data.pvar
    mvar = single_case_data.mvar

    phaseA_data = single_case_data.df[single_case_data.df[pvar] == phases[0]]
    phaseB_data = single_case_data.df[single_case_data.df[pvar] == phases[1]]
    combined_data = pd.concat([phaseA_data, phaseB_data])

    if phaseA_data[dvar].var() == 0:
        print("Warning: Phase A has identical values; autocorrelation set to NA.")
        auto_tau = {"tau": np.nan, "p": np.nan}
    else:
        auto_tau = kendall_full(phaseA_data[dvar], phaseA_data[mvar], tau_method=tau_method, continuity_correction=continuity)

    reg = TheilSenRegressor()
    reg.fit(phaseA_data[[mvar]], phaseA_data[dvar])
    combined_data['fit'] = reg.predict(combined_data[[mvar]])
    combined_data['residual'] = combined_data[dvar] - combined_data['fit']
    phase_binary = (combined_data[pvar] == phases[1]).astype(int)

    base_corr_tau = kendall_full(combined_data['residual'], phase_binary, tau_method=tau_method, continuity_correction=continuity)
    uncorrected_tau = kendall_full(combined_data[dvar], phase_binary, tau_method=tau_method, continuity_correction=continuity)
    corr_applied = False if np.isnan(auto_tau["p"]) or auto_tau["p"] > alpha else True
    final_tau = base_corr_tau if corr_applied else uncorrected_tau

    # Structured print output
    print("Baseline Corrected Tau")
    print("------------------------")
    print(f"Method: {'Theil-Sen regression' if not repeated else 'Siegel repeated median regression'}")
    print("Kendall's tau-b applied.")
    print(f"Continuity correction {'applied' if continuity else 'not applied'}.\n")
    
    print("Case1 :")
    print(f"{'Model':<25} {'Tau':<10} {'p-value':<10}")
    print(f"{'Baseline autocorrelation':<25} {auto_tau['tau'] if auto_tau['tau'] is not None else 'NA':<10.2f} {auto_tau['p'] if auto_tau['p'] is not None else 'NA':<10.2f}")
    print(f"{'Uncorrected tau':<25} {uncorrected_tau['tau']:<10.2f} {uncorrected_tau['p']:<10.2f}")
    print(f"{'Baseline corrected tau':<25} {base_corr_tau['tau']:<10.2f} {base_corr_tau['p']:<10.2f}")
    print("\nBaseline correction " + ("should be applied." if corr_applied else "should not be applied."))

    print("\nFinal Corrected Tau Results Summary")
    print("-----------------------------------")
    print(f"{'Tau Calculation':<25} {'Tau':<10} {'p-value':<10}")
    print(f"{'Final Tau (Selected)':<25} {final_tau['tau']:<10.2f} {final_tau['p']:<10.2f}")
    print(f"{'Autocorrelation Tau':<25} {auto_tau['tau'] if auto_tau['tau'] is not None else 'NA':<10.2f} {auto_tau['p'] if auto_tau['p'] is not None else 'NA':<10.2f}")
    print(f"{'Uncorrected Tau':<25} {uncorrected_tau['tau']:<10.2f} {uncorrected_tau['p']:<10.2f}")
    print(f"{'Baseline Corrected Tau':<25} {base_corr_tau['tau']:<10.2f} {base_corr_tau['p']:<10.2f}")
