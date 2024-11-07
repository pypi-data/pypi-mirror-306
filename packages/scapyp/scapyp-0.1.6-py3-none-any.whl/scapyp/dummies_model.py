import pandas as pd
import numpy as np

def plm_dummy(df, model, dvar, pvar, mvar, contrast_level, contrast_slope):
    """
    Helper function to create phase and interaction dummies for a given case based on model parameters.
    """
    # Define phase dummy variable (level shift)
    df['phaseB'] = np.where(df[pvar] == 'B', 1, 0)
    
    # Define interaction dummy (slope change by phase)
    df['interB'] = df['phaseB'] * df[mvar]
    
    return df

def add_model_dummies(data, model, dvar='values', pvar='phase', mvar='mt', contrast_level="first", contrast_slope="first"):
    """
    Adds model-specific dummy variables and interaction terms based on the specified model and contrast.
    """
    data = data.df if hasattr(data, 'df') else data  # Ensure data is in DataFrame form if using SingleCaseData
    
    # Initialize lists to hold dummy variable names for phases and interactions
    var_phase = []
    var_inter = []
    
    # Apply dummy creation for each case in the data
    case_list = data['case'].unique()
    dummy_df = pd.DataFrame()  # To store transformed cases

    for case in case_list:
        case_df = data[data['case'] == case].copy()  # Isolate each case's data
        
        # Generate dummies for this case
        case_df = plm_dummy(case_df, model, dvar, pvar, mvar, contrast_level, contrast_slope)
        
        # Bind data for this case into the output DataFrame
        dummy_df = pd.concat([dummy_df, case_df], ignore_index=True)
    
    # Set up phase and interaction variable names
    var_phase = ['phaseB']  # Simple example for two-phase model
    var_inter = ['interB']
    
    return dummy_df, var_phase, var_inter
