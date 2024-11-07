import pandas as pd
import numpy as np
from statsmodels.regression.mixed_linear_model import MixedLM
from scipy.stats import chi2
from .formula_utils import create_fixed_formula, create_random_formula

# Dummy variable creation
def add_dummies(data, dvar, pvar, mvar):
    if hasattr(data, 'df'):
        data = data.df
    
    # Define `phaseB` precisely at phase transition
    data['phaseB'] = np.where(data[pvar] == 'B', 1, 0)
    data['interB'] = data['phaseB'] * data[mvar]

    # Print to verify transition alignment
    # print("\nDummy Variables:\n", data[['phaseB', 'interB']].head())
    return data, ['phaseB'], ['interB']

# Define formulas
def define_formulas(dvar, mvar, var_phase, var_inter, random_slopes):
    fixed_formula = create_fixed_formula(dvar, mvar, slope=True, level=True, trend=True, 
                                         var_phase=var_phase, var_inter=var_inter)

    random_formula = "1" if not random_slopes else create_random_formula(mvar, False, False, False, var_phase, var_inter)
    
    print("\nFixed Formula:", fixed_formula)
    print("Random Formula:", random_formula)
    return fixed_formula, random_formula

# Fit model with enhanced error handling
def fit_hierarchical_model(data, fixed_formula, random_formula, method="ML"):
    md = MixedLM.from_formula(fixed_formula, data, groups=data['case'], re_formula=random_formula)
    try:
        # Removing start_params to allow statsmodels to set defaults
        model_fit = md.fit(reml=(method == "REML"), method="powell")
        print("\nModel Fit Summary:\n", model_fit.summary())
    except Exception as e:
        print("Error in fitting model:", e)
        return None
    return model_fit

# ICC calculation
def calculate_icc(model_fit, data, dvar, method="ML"):
    null_md = MixedLM.from_formula(f"{dvar} ~ 1", data, groups=data['case'])
    null_fit = null_md.fit(reml=(method == "REML"), method="powell")
    
    random_effect_variance = model_fit.cov_re.iloc[0, 0] if not model_fit.cov_re.empty else 0
    residual_variance = model_fit.scale
    total_variance = random_effect_variance + residual_variance
    icc_value = random_effect_variance / total_variance if total_variance > 0 else 0
    
    print("\nRandom Effect Variance:", random_effect_variance)
    print("Residual Variance:", residual_variance)
    print("Total Variance:", total_variance)
    print("ICC Value:", icc_value)

    icc_summary = f"ICC = {icc_value:.3f}; L = {null_fit.llf:.1f}; p = {1 - chi2.cdf(2 * null_fit.llf, df=1):.3f}"
    
    return icc_value, icc_summary

# Main function
def hplm(data, dvar='values', pvar='phase', mvar='mt', model="W", contrast="first", 
         contrast_level=None, contrast_slope=None, method="ML", random_slopes=False):
    
    # Step 1: Prepare Dummy Variables
    data, var_phase, var_inter = add_dummies(data, dvar, pvar, mvar)

    # Step 2: Define Formulas
    fixed_formula, random_formula = define_formulas(dvar, mvar, var_phase, var_inter, random_slopes)

    # Step 3: Fit Model without `start_params`
    model_fit = fit_hierarchical_model(data, fixed_formula, random_formula, method=method)
    if model_fit is None:
        print("Model fitting failed.")
        return

    # Step 4: Calculate ICC
    icc_value, icc_summary = calculate_icc(model_fit, data, dvar, method=method)

    # Step 5: Prepare Fixed Effects Output
    fixed_effects = pd.DataFrame({
        "B": model_fit.params.round(3),
        "SE": model_fit.bse.round(3),
        "t": model_fit.tvalues.round(3),
        "p": model_fit.pvalues.round(3)
    })
    fixed_effects.index.name = "Effect"

    # Display Output
    print("\nHierarchical Piecewise Linear Regression\n")
    print(f"Estimation method: {method}")
    print(f"Contrast model: {model} / level: {contrast_level}, slope: {contrast_slope}")
    print(f"{data['case'].nunique()} Cases\n")
    print(icc_summary)
    print("\nFixed effects (values ~ 1 + mt + phaseB + interB):\n", fixed_effects.to_string())

