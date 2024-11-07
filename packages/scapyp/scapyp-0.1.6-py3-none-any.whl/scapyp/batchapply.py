# batch_apply.py
def batch_apply(scdf, fn, simplify=False):
    """
    Apply a function to each element in a single-case data frame (scdf).

    Parameters:
    scdf (list): A list of inputs to apply the function to.
    fn (callable): The function to apply to each element. Should take one argument.
    simplify (bool): If True, will simplify the output to a DataFrame if the function returns a vector.

    Returns:
    list or DataFrame: A list of the output of each function call, or a DataFrame if simplified.
    """
    out = []
    
    for case in scdf:
        result = fn(case)
        out.append(result)
    
    if simplify:
        # Assuming the function returns a vector, we convert the list of results to a DataFrame
        import pandas as pd
        df_out = pd.DataFrame(out)
        df_out['case'] = [case['case'] for case in scdf]  # Assuming 'case' is a column in each case
        return df_out
    return out