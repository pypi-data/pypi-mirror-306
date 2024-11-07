# rank_transformation.py
def ranks(data, var, grand=True, **kwargs):
    """
    Rank-transformation of single-case data files.

    Parameters:
    data (DataFrame): A single-case data frame.
    var (str or list): The names of the variables to be ranked.
    grand (bool): If True, ranks will be calculated across all cases; if False, ranks will be calculated within each case.

    Returns:
    DataFrame: An scdf object where the values of the variable(s) are replaced with ranks.
    """
    if isinstance(var, str):
        var = [var]  # Ensure var is a list

    ranked_data = data.copy()  # Create a copy to avoid modifying the original data

    for v in var:
        if grand:
            # Rank across all cases
            ranked_data[v] = ranked_data[v].rank(**kwargs)
        else:
            # Rank within each case
            ranked_data[v] = ranked_data.groupby(data['phase'])[v].rank(**kwargs)

    return ranked_data