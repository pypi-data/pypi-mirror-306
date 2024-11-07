import pandas as pd
from .stat_utils import mad, trend
from .singlecasedf import SingleCaseData

def describe(data):
    """
    Computes descriptive statistics for each case and phase in the provided data.
    
    Parameters:
    - data: SingleCaseData instance or DataFrame containing the data.

    Returns:
    - A pandas DataFrame containing all descriptive statistics
    """
    if isinstance(data, SingleCaseData):
        df = data.df
    else:
        df = data

    # Check if 'case' column exists; if not, treat the data as a single case
    if 'case' in df.columns:
        cases = df['case'].unique()
    else:
        cases = ['Single Case']  # Treat as single case if 'case' column is missing

    # Create a list to store all statistics
    all_stats = []
    
    for case in cases:
        case_data = df[df['case'] == case] if 'case' in df.columns else df
        phases = case_data['phase'].unique()
        
        for phase in phases:
            phase_data = case_data[case_data['phase'] == phase]['values']
            time_data = case_data[case_data['phase'] == phase]['mt']
            
            stats = {
                'case': case,
                'phase': phase,
                'n': len(phase_data),
                'mis': phase_data.isna().sum(),
                'm': round(phase_data.mean(), 2),
                'md': round(phase_data.median(), 2),
                'sd': round(phase_data.std(), 2),
                'mad': round(mad(phase_data), 2),
                'min': round(phase_data.min(), 2),
                'max': round(phase_data.max(), 2),
                'trend': round(trend(time_data, phase_data), 2)
            }
            all_stats.append(stats)
    
    # Create DataFrame from all statistics
    results_df = pd.DataFrame(all_stats)
    
    # Set MultiIndex for better organization
    results_df = results_df.set_index(['case', 'phase'])
    
    return results_df

























# # import pandas as pd
# # from singlecasedf import SingleCaseData
# # from stat_utils import mad, trend  # Import corrected stat_utils functions

# # def describe(single_case_data):
# #     """
# #     Computes descriptive statistics for single-case data.

# #     Parameters:
# #     - single_case_data: SingleCaseData instance containing the data.

# #     Returns:
# #     - A DataFrame containing descriptive statistics for each phase.
# #     """
# #     # Extract data and variable names from SingleCaseData
# #     dvar = single_case_data.dvar
# #     pvar = single_case_data.pvar
# #     mvar = single_case_data.mvar
# #     df = single_case_data.df

# #     # Initialize descriptions dictionary with metrics as rows
# #     descriptions = {
# #         "Metric": ["n", "mis", "m", "md", "sd", "mad", "min", "max", "trend"]
# #     }

# #     # Calculate statistics for each phase separately
# #     for phase in df[pvar].unique():
# #         phase_data = df[df[pvar] == phase][dvar]
# #         time_data = df[df[pvar] == phase][mvar]

# #         descriptions[f"Phase {phase}"] = [
# #             len(phase_data),
# #             phase_data.isna().sum(),
# #             phase_data.mean(),
# #             phase_data.median(),
# #             phase_data.std(),
# #             mad(phase_data),  # MAD calculated using `mad` from stat_utils
# #             phase_data.min(),
# #             phase_data.max(),
# #             trend(time_data, phase_data)  # Trend calculated using updated `trend`
# #         ]

# #     # Convert descriptions to a DataFrame for readable output
# #     desc_df = pd.DataFrame(descriptions).set_index("Metric")
# #     return desc_df

# import pandas as pd
# from stat_utils import mad, trend  # Assuming these functions are available and configured
# from singlecasedf import SingleCaseData

# def describe(data):
#     """
#     Computes descriptive statistics for each case and phase in the provided data.
    
#     Parameters:
#     - data: SingleCaseData instance or DataFrame containing the data.

#     Returns:
#     - A formatted summary of descriptive statistics for each case.
#     """
#     # Convert to DataFrame if input is SingleCaseData instance
#     if isinstance(data, SingleCaseData):
#         df = data.df
#     else:
#         df = data

#     # Get unique case names
#     cases = df['case'].unique()
    
#     # Initialize the output
#     summary = "# A single-case data frame with multiple cases\n\n"
#     summary += f"{'Case':<10} {'Measurements':<15} {'Design'}\n"
#     summary += "-" * 40 + "\n"

#     # Process each case
#     for case in cases:
#         case_data = df[df['case'] == case]

#         # Get phase design for the case
#         phases = case_data['phase'].unique()
#         phase_design = "-".join(phases)

#         # Add case overview to summary
#         summary += f"{case:<10} {len(case_data):<15} {phase_design}\n"

#         # Calculate descriptive statistics for each phase
#         stats = {
#             "Metric": ["n", "mis", "m", "md", "sd", "mad", "min", "max", "trend"]
#         }
        
#         for phase in phases:
#             phase_data = case_data[case_data['phase'] == phase]['values']
#             time_data = case_data[case_data['phase'] == phase]['mt']
            
#             stats[f"Phase {phase}"] = [
#                 len(phase_data),
#                 phase_data.isna().sum(),
#                 phase_data.mean(),
#                 phase_data.median(),
#                 phase_data.std(),
#                 mad(phase_data),
#                 phase_data.min(),
#                 phase_data.max(),
#                 trend(time_data, phase_data)
#             ]
        
#         # Convert stats to DataFrame for readability
#         stats_df = pd.DataFrame(stats).set_index("Metric")
#         summary += f"\nDetailed Descriptive Statistics for Case: {case}\n"
#         summary += f"{stats_df}\n\n"

#     return summary
