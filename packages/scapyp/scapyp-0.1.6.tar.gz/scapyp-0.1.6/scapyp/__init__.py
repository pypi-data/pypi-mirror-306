# __init__.py in the scapyp package

from .autocorr import autocorr
from .batchapply import batch_apply
from .case_selection import select_cases
from .cdc import calculate_trend, cdc
# from .check_args import (
#     is_true, has_length, not_condition, one_of, within, at_least, at_most, by_class,
#     is_logical, check
# )
from .combine import combine
from .corrected_tau import kendall_full, corrected_tau
from .data_processing import fill_missing
from .data_transformation import moving_median, moving_mean, local_regression, transform_single_case
from .describe import describe
from .dummies_model import plm_dummy, add_model_dummies
from .formula_utils import create_fixed_formula, create_random_formula
from .hplm import add_dummies, define_formulas, fit_hierarchical_model, calculate_icc, hplm
from .ird import ird
from .nap import nap
from .outlier_handling import outlier
from .overlap import overlap
from .pand import pand
from .prepare_data import opt, revise_names, _check_scdf, check_scdf, prepare_scdf
from .rank_transformation import ranks
from .readdata import readdata
from .select_case import select_case
from .singlecasedf import SingleCaseData
from .stat_utils import mad, trend
from .trend import trend
from .variable_management import set_vars, set_dvar, set_mvar, set_pvar

# You can specify what should be exposed when importing * from scapyp
__all__ = [
    'autocorr', 'batch_apply', 'select_cases', 'calculate_trend', 'cdc', 'is_true', 'has_length', 
    'not_condition', 'one_of', 'within', 'at_least', 'at_most', 'by_class', 'is_logical', 'check',
    'combine', 'kendall_full', 'corrected_tau', 'fill_missing', 'moving_median', 'moving_mean', 
    'local_regression', 'transform_single_case', 'describe', 'plm_dummy', 'add_model_dummies',
    'create_fixed_formula', 'create_random_formula', 'add_dummies', 'define_formulas', 
    'fit_hierarchical_model', 'calculate_icc', 'hplm', 'ird', 'nap', 'outlier', 'overlap', 'pand', 
    'pand_minimum', 'opt', 'revise_names', '_check_scdf', 'check_scdf', 'prepare_scdf', 'ranks', 
    'readdata', 'select_case', 'SingleCaseDF', 'mad', 'trend', 'set_vars', 'set_dvar', 'set_mvar', 
    'set_pvar'
]
