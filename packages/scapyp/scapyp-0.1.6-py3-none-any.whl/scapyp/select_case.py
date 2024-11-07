def select_case(scdf, *cases):
    """
    Selects specified cases from a single-case data frame (scdf).

    Parameters:
    - scdf (DataFrame): The DataFrame containing single-case data.
    - *cases (str): Case names to select.

    Returns:
    - DataFrame: A filtered DataFrame containing only the specified cases.
    """
    # Check if any cases are provided
    if not cases:
        raise ValueError("Please specify at least one case to select.")
    
    # Filter the DataFrame based on the specified cases
    selected_df = scdf[scdf['case'].isin(cases)]
    
    return selected_df