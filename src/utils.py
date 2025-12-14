"""
工具函数模块 - Utility Functions Module
提供各种辅助功能
"""

import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime
from config import PLOT_STYLE, FIGURE_SIZE, DPI, OUTPUT_DIR


def setup_plot_style():
    """设置绘图样式"""
    try:
        plt.style.use(PLOT_STYLE)
    except (OSError, ValueError) as e:
        # 如果样式不可用，使用默认样式（可选：取消下一行注释来显示警告）
        # print(f"Warning: Plot style '{PLOT_STYLE}' not available, using default style")
        pass


def plot_results(x, y, xlabel='X', ylabel='Y', title='Results', save_path=None):
    """
    绘制结果图
    
    参数:
        x: array-like, x轴数据
        y: array-like, y轴数据
        xlabel: str, x轴标签
        ylabel: str, y轴标签
        title: str, 图表标题
        save_path: str, 保存路径（可选）
    """
    setup_plot_style()
    
    plt.figure(figsize=FIGURE_SIZE)
    plt.plot(x, y, linewidth=2)
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.title(title, fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=DPI)
        print(f"图表已保存至: {save_path}")
    
    plt.show()


def plot_multiple_lines(data_dict, xlabel='X', ylabel='Y', title='Results', save_path=None):
    """
    绘制多条曲线
    
    参数:
        data_dict: dict, 键为曲线名称，值为(x, y)元组
        xlabel: str, x轴标签
        ylabel: str, y轴标签
        title: str, 图表标题
        save_path: str, 保存路径（可选）
    """
    setup_plot_style()
    
    plt.figure(figsize=FIGURE_SIZE)
    
    for label, (x, y) in data_dict.items():
        plt.plot(x, y, label=label, linewidth=2)
    
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.title(title, fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=DPI)
        print(f"图表已保存至: {save_path}")
    
    plt.show()


def calculate_statistics(data):
    """
    计算数据的统计信息
    
    参数:
        data: array-like, 输入数据
        
    返回:
        dict, 统计信息
    """
    data_array = np.array(data)
    
    stats = {
        'mean': np.mean(data_array),
        'median': np.median(data_array),
        'std': np.std(data_array),
        'min': np.min(data_array),
        'max': np.max(data_array),
        'range': np.ptp(data_array)
    }
    
    return stats


def normalize_data(data, method='minmax'):
    """
    数据归一化
    
    参数:
        data: array-like, 输入数据
        method: str, 归一化方法 ('minmax' 或 'zscore')
        
    返回:
        numpy.ndarray, 归一化后的数据
    """
    data_array = np.array(data)
    
    if method == 'minmax':
        # Min-Max归一化到[0, 1]
        min_val = np.min(data_array)
        max_val = np.max(data_array)
        if max_val - min_val == 0:
            return np.zeros_like(data_array)
        return (data_array - min_val) / (max_val - min_val)
    
    elif method == 'zscore':
        # Z-score标准化
        mean = np.mean(data_array)
        std = np.std(data_array)
        if std == 0:
            return np.zeros_like(data_array)
        return (data_array - mean) / std
    
    else:
        raise ValueError(f"未知的归一化方法: {method}")


def save_log(message, log_file='log.txt'):
    """
    保存日志信息
    
    参数:
        message: str, 日志消息
        log_file: str, 日志文件名
    """
    log_path = os.path.join(OUTPUT_DIR, log_file)
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    
    with open(log_path, 'a', encoding='utf-8') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"[{timestamp}] {message}\n")


def print_separator(char='=', length=50):
    """
    打印分隔线
    
    参数:
        char: str, 分隔符字符
        length: int, 分隔线长度
    """
    print(char * length)
