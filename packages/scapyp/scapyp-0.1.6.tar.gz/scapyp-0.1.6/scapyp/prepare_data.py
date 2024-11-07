import pandas as pd
from .singlecasedf import SingleCaseData

def opt(setting):
    """
    Placeholder for a configuration function.
    Returns a boolean value for specific configuration settings.
    """
    if setting == "rigorous_class_check":
        return True  # Default to True;
    return False

def revise_names(column_names, length):
    """
    Placeholder function to standardize or modify column names if necessary.
    Here, we simply return the column names unchanged.
    """
    # Modify this function based on the intended logic for revising column names
    return column_names

def _check_scdf(data):
    warnings = []
    errors = []
    # Add validation logic here, if any.
    if not warnings and not errors:
        return True
    return {'warnings': warnings, 'errors': errors}

def check_scdf(data, show_message=False):
    results = _check_scdf(data)
    
    if results is True:
        if show_message:
            print("No errors or warnings.")
        return True

    if 'warnings' in results and results['warnings']:
        for warning_msg in results['warnings']:
            print(f"Warning: {warning_msg}")
    
    if 'errors' in results and results['errors']:
        error_messages = "\n".join(results['errors'])
        raise ValueError(f"Errors detected:\n{error_messages}")

def prepare_scdf(data, na_rm=False):
    # Perform rigorous check if enabled
    if opt("rigorous_class_check"):
        check_scdf(data)
    
    # Retrieve phase, measurement time, and dependent variable names
    pvar = phase(data)
    mvar = mt(data)
    dvar = dv(data)
    
    # Adjust DataFrame column names
    data.columns = revise_names(data.columns, len(data))
    
    # Process each case in the data
    for case_idx, case_data in enumerate(data):
        if isinstance(case_data, pd.DataFrame):
            data[case_idx] = pd.DataFrame(case_data)
            print("Found DataFrame within scdf and changed it to data.frame.")
        
        # Remove rows with NaNs in `dvar` if na_rm is True
        if na_rm:
            data[case_idx] = data[case_idx].dropna(subset=[dvar])
        
        # Ensure `pvar` is categorical and drop unused categories
        if not pd.api.types.is_categorical_dtype(data[case_idx][pvar]):
            data[case_idx][pvar] = data[case_idx][pvar].astype('category')
        data[case_idx][pvar] = data[case_idx][pvar].cat.remove_unused_categories()

    return data
