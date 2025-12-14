"""
数学建模项目源代码包
"""

from .data_handler import DataHandler
from .model import MathematicalModel, OptimizationModel, SimulationModel
from .utils import (
    plot_results,
    plot_multiple_lines,
    calculate_statistics,
    normalize_data,
    save_log,
    print_separator
)

__version__ = '1.0.0'
__all__ = [
    'DataHandler',
    'MathematicalModel',
    'OptimizationModel',
    'SimulationModel',
    'plot_results',
    'plot_multiple_lines',
    'calculate_statistics',
    'normalize_data',
    'save_log',
    'print_separator'
]
