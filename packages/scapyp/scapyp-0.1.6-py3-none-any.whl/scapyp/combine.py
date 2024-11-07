import pandas as pd
def combine(*scdfs, dvar=None, pvar=None, mvar=None, info=None, author=None):
    """
    Combine single-case data frames.

    Parameters:
    *scdfs: A variable number of single-case data frames to combine.
    dvar (str): Name of the dependent variable.
    pvar (str): Name of the phase variable.
    mvar (str): Name of the measurement-time variable.
    info (str): Additional information on the SCDF file.
    author (str): Author of the data.

    Returns:
    DataFrame: A combined single-case data frame (scdf).
    """
    # Combine all scdfs into one
    combined_data = pd.concat(scdfs, ignore_index=True)

    # Set new variable names if provided
    if dvar:
        combined_data.rename(columns={'values': dvar}, inplace=True)
    if pvar:
        combined_data.rename(columns={'phase': pvar}, inplace=True)
    if mvar:
        combined_data.rename(columns={'mt': mvar}, inplace=True)

    # Add additional info and author if provided
    combined_data.attrs['info'] = info
    combined_data.attrs['author'] = author

    return combined_data