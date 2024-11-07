# case_selection.py
def select_cases(scdf, *args):
    """
    Select a subset of cases from a single-case data frame (scdf).

    Parameters:
    scdf (DataFrame): A single-case data frame.
    *args: Selection criteria (either numeric indices or case names).

    Returns:
    DataFrame: A subset of the original scdf based on the selection criteria.
    """
    # Convert args to a list for easier processing
    selection_criteria = list(args)

    # Select cases based on the criteria
    if all(isinstance(x, int) for x in selection_criteria):
        # Numeric indices
        selected_cases = scdf.iloc[selection_criteria]
    else:
        # Assuming args contain case names
        selected_cases = scdf[scdf['case'].isin(selection_criteria)]

    return selected_cases