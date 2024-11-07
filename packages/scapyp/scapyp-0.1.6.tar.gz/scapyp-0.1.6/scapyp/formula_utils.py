# formula_utils.py
def create_fixed_formula(dvar, mvar, slope, level, trend, var_phase, var_inter):
    """Constructs the fixed effects formula for the model."""
    inter = ""
    phase = ""
    mt = ""
    if slope:
        inter = " + ".join(var_inter)
        inter = "+ " + inter
    if level:
        phase = " + ".join(var_phase)
        phase = "+ " + phase
    if trend:
        mt = f"+ {mvar} "
    return f"{dvar} ~ 1 {mt}{phase}{inter}"

def create_random_formula(mvar, slope, level, trend, var_phase, var_inter):
    """Constructs the random effects formula for the model with grouping by case."""
    inter = ""
    phase = ""
    mt = ""
    
    if slope:
        inter = " + ".join(var_inter)
        inter = "+ " + inter
    if level:
        phase = " + ".join(var_phase)
        phase = "+ " + phase
    if trend:
        mt = f"+ {mvar} "
    
    # Include |case at the end for grouping by case, similar to the R version
    return f"1 {mt}{phase}{inter} | case"
