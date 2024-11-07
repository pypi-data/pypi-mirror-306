# variable_management.py
def set_vars(data, dvar, mvar, pvar):
    """
    Set analysis variables in a single-case data frame (scdf).

    Parameters:
    data (DataFrame): A single-case data frame.
    dvar (str): Name of the dependent variable.
    mvar (str): Name of the measurement-time variable.
    pvar (str): Name of the phase variable.

    Returns:
    DataFrame: Updated data frame with the specified variable names.
    """
    data = data.copy()
    data.columns = [dvar if col == 'values' else col for col in data.columns]
    data.columns = [mvar if col == 'mt' else col for col in data.columns]
    data.columns = [pvar if col == 'phase' else col for col in data.columns]
    return data

def set_dvar(data, dvar):
    """
    Set the dependent variable in a single-case data frame.

    Parameters:
    data (DataFrame): A single-case data frame.
    dvar (str): Name of the dependent variable.

    Returns:
    DataFrame: Updated data frame with the specified dependent variable name.
    """
    return set_vars(data, dvar, data.columns[2], data.columns[1])

def set_mvar(data, mvar):
    """
    Set the measurement-time variable in a single-case data frame.

    Parameters:
    data (DataFrame): A single-case data frame.
    mvar (str): Name of the measurement-time variable.

    Returns:
    DataFrame: Updated data frame with the specified measurement-time variable name.
    """
    return set_vars(data, data.columns[0], mvar, data.columns[1])

def set_pvar(data, pvar):
    """
    Set the phase variable in a single-case data frame.

    Parameters:
    data (DataFrame): A single-case data frame.
    pvar (str): Name of the phase variable.

    Returns:
    DataFrame: Updated data frame with the specified phase variable name.
    """
    return set_vars(data, data.columns[0], data.columns[2], pvar)