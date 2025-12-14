"""
配置文件 - Configuration file
用于存储项目配置参数
"""

import os

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# 数据目录
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
INPUT_DIR = os.path.join(DATA_DIR, 'input')
OUTPUT_DIR = os.path.join(DATA_DIR, 'output')

# Excel文件配置
EXCEL_ENGINE = 'openpyxl'  # 用于读写xlsx文件

# 默认文件路径
DEFAULT_INPUT_FILE = os.path.join(INPUT_DIR, 'input_data.xlsx')
DEFAULT_OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'results.xlsx')

# 数值计算参数（可根据具体问题调整）
PRECISION = 1e-6  # 计算精度
MAX_ITERATIONS = 1000  # 最大迭代次数

# 可视化配置
PLOT_STYLE = 'seaborn'
FIGURE_SIZE = (10, 6)
DPI = 300  # 图像分辨率
